---
date: 2026-02-24T08:00:00
series: "Giving an AI Agent a Brain"
categories:
  - AI Infrastructure
  - IronClaw
tags:
  - ironclaw
  - mcp
  - synthesis
  - ec2
  - aws
  - python
  - java
  - ai-agents
authors:
  - totto
  - claude
  - synthesis
---

# Giving an AI Agent a Brain: Connecting IronClaw to Synthesis via MCP

IronClaw is the internal AI agent I run for eXOReaction. It sits on an EC2 instance, connected to Slack via a Python Socket Mode bridge, and answers questions from the team. The underlying model is kimi-k2.5 via OpenRouter. It is fast and capable, and it has no idea who we are.

<!-- more -->

Every conversation starts from zero. Ask it about our skill library, our methodology, a specific client engagement, and it either hallucinates or tells you it doesn't have that context. This is fine for a generic assistant. It is less fine when you want the agent to actually *know your company* — to be able to search 100+ YAML skill definitions, read memory files, and surface relevant documentation without you pasting everything into the prompt each time.

The fix is to give it a connected knowledge base. We already have one: [Synthesis](/blog/2026/02/25/ai-agents-without-knowledge-infrastructure-are-interns-with-amnesia/), a knowledge infrastructure tool that indexes files at 200–300 files/second and exposes search, graph, and relationship queries over MCP. Synthesis runs locally, keeps everything on-prem, and produces sub-second search across thousands of files.

The plan: sync the relevant files to the EC2 instance, run Synthesis against them, bridge its stdio MCP interface to HTTP, and register it as an MCP server in IronClaw. Four steps. It took most of a day, and almost all the time was spent on surprises I didn't anticipate.

This is Part 1. It covers the setup, the gotchas, and getting to "28 tools registered." [Part 2 covers whether it actually works in practice.](/blog/2026/02/24/ironclaw-synthesis-part2/)

---

## The architecture

Before diving in, here is what the final setup looks like:

```
Slack → #ironclaw channel
         ↓  @IronClaw question
    [Python Socket Mode bridge] (systemd service on ironclaw0)
         ↓  HTTP POST to localhost
    [IronClaw gateway] (Docker, port 3000)
         ↓  MCP tool call
    [synthesis-mcp-bridge] (Python 3.11, port 8765, StreamableHTTP)
         ↓  stdio JSON-RPC 2.0
    [synthesis-mcp-server] (Java subprocess, Lucene index)
         ↓  search / relate / graph / ask
    [~/ironclaw-workspace/] (155 files: skills, memory, docs)
```

IronClaw speaks MCP to its registered servers over HTTP. Synthesis speaks MCP over stdio — it launches as a subprocess and communicates via line-by-line JSON-RPC. These two things are not directly compatible, which is why there is a Python bridge in the middle.

---

## Step 1: Getting the knowledge base onto the server

The first step was creating the workspace. I settled on three directories:

```
~/ironclaw-workspace/
  skills/     # 100+ YAML skill definitions
  memory/     # Markdown memory files (MEMORY.md, topic files)
  docs/       # CLAUDE.md, PROOF-POINTS.md, key references
```

Rsync from local to EC2 is straightforward:

```bash
rsync -avz --delete \
  ~/.claude/skills/ \
  ironclaw0:~/ironclaw-workspace/skills/

rsync -avz --delete \
  ~/.claude/projects/memory/ \
  ironclaw0:~/ironclaw-workspace/memory/

rsync -avz \
  ~/Documents/CLAUDE.md \
  ~/Documents/eXOReaction/PROOF-POINTS.md \
  ironclaw0:~/ironclaw-workspace/docs/
```

155 files total. This is IronClaw's long-term memory — the things it should know without being told each conversation.

---

## Step 2: Installing Synthesis on EC2 — Java version surprise

Synthesis is a Java application. The JAR is about 168 MB (it bundles Lucene). Copy it over, run `init`, done — or so I thought.

The documentation said Java 17. EC2 Amazon Linux 2023 ships with Java 17 by default. I ran:

```bash
synthesis init -d ~/ironclaw-workspace
```

And got:

```
Error: LinkageError occurred while loading main class io.xorcery.synthesis.mcp.MCP
	java.lang.UnsupportedClassVersionError:
	io/xorcery/synthesis/mcp/MCP has been compiled by a more recent
	version of the Java Runtime (class file version 65.0), this
	version of the Java Runtime only recognizes class file versions
	up to 61.0
```

Class file version 65.0 is Java 21. Version 61.0 is Java 17. The JAR had been compiled with 21 despite the docs saying 17. Fix:

```bash
sudo dnf install -y java-21-amazon-corretto
sudo alternatives --set java \
  /usr/lib/jvm/java-21-amazon-corretto.x86_64/bin/java
```

After that, `synthesis init` ran and indexed 155 files. A quick `synthesis search "skill library"` returned results in under a second.

There was one more Synthesis gotcha: it requires a client UUID and an approval status file. On a fresh machine, these don't exist, and Synthesis refuses to run. The fix is to copy them from your local machine:

```bash
scp ~/.synthesis/approval-status ironclaw0:~/.synthesis/approval-status
scp ~/.synthesis/client-uuid     ironclaw0:~/.synthesis/client-uuid
```

Not documented prominently, but straightforward once you know what's missing.

---

## Step 3: The bridge — where the interesting problems live

This is the part that took the most time.

`synthesis-mcp-server` communicates over **stdio**: you spawn it as a subprocess, write JSON-RPC requests to its stdin, read responses from its stdout, one line per message. This is the standard MCP stdio transport.

IronClaw's `mcp add` command accepts an HTTP URL. It cannot spawn subprocesses. So I needed a Python server that would:

1. Accept MCP requests over HTTP from IronClaw
2. Forward them to the Java process over stdio
3. Return the responses

The Python `mcp` SDK requires Python 3.11+. AL2023 ships Python 3.9 as the system default.

```bash
sudo dnf install -y python3.11 python3.11-pip
python3.11 -m pip install mcp uvicorn starlette
```

### First attempt: SSE transport

The `mcp` library has a `SseServerTransport` class for HTTP-based MCP. I wired it up, pointed it at a proxy that forwarded to the Java subprocess, and ran it. IronClaw tried to connect. The bridge crashed immediately:

```
TypeError: 'NoneType' object is not callable
```

Deep in the MCP SDK's SSE handler. After reading the source, I realised the SSE transport is a legacy pattern — it expects GET requests on `/sse` to open a streaming connection, then POST on `/messages`. IronClaw, running a newer MCP version, uses the **Streamable HTTP** protocol (introduced in MCP 1.26+). Different protocol, different endpoints, different framing.

### Second attempt: raw ASGI

I rewrote the handler as a raw ASGI application, manually parsing the incoming request and forwarding it to the Java process. Got further this time — the connection was established — but then:

```
405 Method Not Allowed
```

IronClaw was POSTing to `/mcp`. My handler was only accepting GET. Flipped it. Then IronClaw hung waiting for a proper Streamable HTTP session response.

### Third attempt: StreamableHTTPSessionManager

The `mcp` SDK has `StreamableHTTPSessionManager` for exactly this use case. The key setting is `stateless=True` — IronClaw doesn't maintain session state across tool calls in the way a persistent client would. The bridge structure:

```python
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

WORKSPACE = "/home/ec2-user/ironclaw-workspace"
MCP_JAR = "/home/ec2-user/.synthesis/lib/synthesis-mcp-server.jar"

server = Server("synthesis")

@server.list_tools()
async def list_tools():
    resp = await synthesis_call("tools/list", {})
    # ... convert and return

@server.call_tool()
async def call_tool(name, arguments):
    resp = await synthesis_call("tools/call", {"name": name, "arguments": arguments})
    # ... extract and return

session_manager = StreamableHTTPSessionManager(
    app=server, stateless=True
)

async def handle_mcp(scope, receive, send):
    await session_manager.handle_request(scope, receive, send)

app = Starlette(routes=[Mount("/mcp", app=handle_mcp)])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8765)
```

This got IronClaw to connect. Then I hit the most subtle bug of the day.

---

## The `notifications/initialized` trap

When an MCP client connects, it sends an `initialize` request. The server responds. Then the client sends a `notifications/initialized` notification — a one-way message, no response expected.

`synthesis-mcp-server` doesn't implement `notifications/initialized`. When it receives one, it sends back an error:

```json
{"jsonrpc":"2.0","id":null,"error":{"code":-32601,"message":"Unknown method: notifications/initialized"}}
```

That error sits in the Java process's stdout buffer. The next thing my bridge sends is a `tools/list` request. The next thing it reads back is... that error message, not the tools list. The bridge returned 0 tools to IronClaw.

This is maddening to diagnose because everything *looks* fine. The connection succeeds, the handshake completes, the registration appears. It just registers with no tools. Only when I added explicit logging of every line read from the Java process did I see the error response sitting there, consumed by the wrong read call.

The fix: after sending `notifications/initialized`, explicitly read and discard the error line before doing anything else.

```python
# Send initialization handshake
await send_and_recv({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {...}})

# Send the notification (required by MCP spec)
proc.stdin.write((json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n").encode())
await proc.stdin.drain()

# synthesis-mcp-server sends an error for this — consume it before the next call
_discard = await proc.stdout.readline()

# NOW the subprocess is ready for real requests
```

After that fix: 8 Synthesis tools registered — `search`, `relate`, `graph`, `stats`, `ask`, `enrich`, `explain`, `summary`.

The bridge runs as a systemd service:

```ini
[Unit]
Description=Synthesis MCP Bridge
After=network.target

[Service]
User=ec2-user
ExecStart=/usr/bin/python3.11 /home/ec2-user/synthesis-mcp-bridge.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Step 4: Registration and the `.env` wipe

With the bridge running, registration is one command:

```bash
~/ironclaw.sh mcp add synthesis http://127.0.0.1:8765/mcp
```

IronClaw confirmed the registration. I restarted the container and hit a login screen. IronClaw had forgotten its LLM configuration entirely.

The `mcp add` command rewrites `~/.ironclaw/.env` with a fresh set of database settings — and only database settings. The LLM backend, API key, model name, secrets key: all wiped. On restart, IronClaw sees no LLM config and falls back to prompting for a login.

The fix: restore the full `.env` immediately after any `mcp add` call. I now keep the complete env content in a separate file and copy it back every time.

After the restore: IronClaw starts, connects to Synthesis, and reports **28 tools registered** — 8 from Synthesis, 20 built-in.

---

## Where this leaves us

The plumbing works. IronClaw is connected to a Lucene index of 155 files: skill definitions, memory markdown, key documentation. It can call `search`, `relate`, `ask`, and the rest. When you ask it something in Slack, it has the option to reach into the knowledge base rather than relying purely on the model's weights.

Whether it actually does that reliably is what [Part 2](/blog/2026/02/24/ironclaw-synthesis-part2/) covers. The short preview: it is more interesting than I expected, and not entirely in the ways I hoped.

---

*Synthesis is the knowledge infrastructure tool described in this series.*
