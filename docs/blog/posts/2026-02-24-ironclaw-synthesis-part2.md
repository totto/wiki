---
date: 2026-02-24T16:00:00
categories:
  - AI Infrastructure
  - Debugging
tags:
  - ironclaw
  - kimi-k2.5
  - tool-calls
  - debugging
  - mcp
  - synthesis
  - ai-agents
authors:
  - totto
  - claude
  - synthesis
---

# When Your AI Lies About Its Tool Calls: Debugging kimi-k2.5

At the end of [Part 1](/blog/2026/02/24/ironclaw-synthesis-part1/), I had IronClaw running on EC2, connected to Slack, with 28 tools registered — 8 of them from a Synthesis MCP server backed by 155 indexed files. The architecture looked correct. The logs said "connected." The tool list confirmed registration.

So I sent it a task.

<!-- more -->

---

## First test: confidently wrong

The query was simple:

> *Search for "Quadim platform SaaS" in the knowledge base.*

The response came back in under 5 seconds.

> "I searched the knowledge base for 'Quadim platform SaaS' but found 0 results. The knowledge base may not contain information about this topic."

That's wrong. I know it's wrong because I built the index. Let me check the obvious things first.

```bash
synthesis search -d ~/ironclaw-workspace 'Quadim'
```

20 results. Instantly.

```bash
curl -s -X POST http://localhost:8765/mcp/ \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"Quadim","workspace":"~/ironclaw-workspace"}}}'
```

20 results. The bridge is fine.

So: the index works, the bridge works, the MCP connection is registered. But IronClaw comes back with zero. Something is happening between "IronClaw decides to call the tool" and "the result comes back."

Time to stop guessing and actually look.

---

## Debugging methodology: isolate each layer

The system has four layers that could be failing:

1. Does IronClaw generate a valid tool call?
2. Does the proxy/transport deliver it correctly?
3. Does the bridge receive the right arguments?
4. Does Synthesis execute correctly?

Layers 3 and 4 I'd already verified. So the problem was in 1 or 2.

I added a single log line to the bridge's `call_tool` handler:

```python
log.info("call_tool: %s args=%s", name, json.dumps(args))
```

Restarted, sent the same query. The bridge log showed... nothing. No `call_tool` entry at all. IronClaw had not actually called the tool. It had *said* it searched. It had not searched.

That's a different problem from "tool called with wrong args." That's the model fabricating a tool call result — hallucinating the invocation entirely.

---

## The XML problem

I turned on full response logging and sent the query again. Sometimes the output looked normal. Sometimes it looked like this:

```xml
<invoke name="synthesis_search">
<arg name="query">Quadim platform</arg>
<arg name="workspace">/home/ec2-user/ironclaw-workspace</arg>
<arg name="fileType">ALL</arg>
<arg name="limit">20</arg>
<arg name="subWorkspace">null</arg>
</invoke>
```

That's not a hallucination. That's kimi-k2.5's native tool call format. The model *is* trying to call the tool. It's just using XML instead of the OpenAI `tool_calls` JSON format that IronClaw expects.

kimi-k2.5 was trained with an XML-based function calling format. OpenRouter wraps it and in theory converts to OpenAI format. In practice, under certain conditions — particularly in streaming responses — the conversion is inconsistent. Sometimes IronClaw's parser catches the XML and executes the call. Sometimes it doesn't, treats the XML as response text, and returns it verbatim. Sometimes it silently drops it and replies as if no tool was available.

Three different failure modes from the same root cause: format mismatch between model output and expected input.

The fix: stop relying on OpenRouter to do the conversion reliably. Build a local proxy that always does it correctly.

---

## The kimi-proxy

`kimi-proxy.py` runs on port 8767. IronClaw's `LLM_BASE_URL` in `.env` points to `http://127.0.0.1:8767/v1`. It passes all requests through to OpenRouter, but intercepts responses and normalises any XML tool calls into OpenAI format before IronClaw sees them.

The core conversion:

```python
import re, json

INVOKE_RE = re.compile(r'<invoke\s+name="([^"]+)">(.*?)</invoke>', re.DOTALL)
ARG_RE    = re.compile(r'<arg\s+name="([^"]+)">(.*?)</arg>', re.DOTALL)

def xml_to_tool_calls(text: str) -> tuple[str, list]:
    tool_calls = []
    for i, m in enumerate(INVOKE_RE.finditer(text)):
        fn_name = m.group(1)
        args = {}
        for a in ARG_RE.finditer(m.group(2)):
            val = a.group(2).strip()
            args[a.group(1)] = None if val == "null" else val
        tool_calls.append({
            "id": f"call_{i}_{fn_name}",
            "type": "function",
            "function": {"name": fn_name, "arguments": json.dumps(args)},
        })
    clean = INVOKE_RE.sub("", text).strip()
    return clean, tool_calls

def patch_response(data: dict) -> dict:
    for choice in data.get("choices", []):
        msg = choice.get("message", {})
        content = msg.get("content", "") or ""
        if "<invoke" in content:
            clean, tool_calls = xml_to_tool_calls(content)
            msg["content"] = clean or None
            msg["tool_calls"] = tool_calls
            choice["finish_reason"] = "tool_calls"
    return data
```

For streaming responses the proxy buffers the full SSE stream, reassembles the content, checks for XML, then re-emits proper `tool_call` delta chunks. It's about 150 lines total and runs as a systemd service alongside the synthesis bridge.

With this in place, IronClaw always sees OpenAI-format tool calls regardless of what kimi-k2.5 actually emitted. The bridge log started showing `call_tool` entries. Progress.

---

## The workspace hallucination

Now the bridge was being called. The log entry for the first real invocation:

```
INFO call_tool: synthesis_search args={"query": "Quadim platform SaaS",
  "workspace": "default", "fileType": "ALL", "limit": 20, "subWorkspace": null}
```

`workspace: "default"`.

Synthesis received that, tried to resolve it as a path, and returned:

```
Error: Workspace directory does not exist: /default
```

IronClaw saw an error response and told me there were 0 results. Technically accurate. Completely unhelpful.

The model knows the tool has a `workspace` parameter. It doesn't know the actual value. So it guessed a reasonable-sounding default. Confidently wrong.

The fix is defensive middleware in the bridge. If the workspace argument isn't a valid absolute path, replace it with the real one:

```python
WORKSPACE = "/home/ec2-user/ironclaw-workspace"

def sanitise_args(args: dict) -> dict:
    ws = args.get("workspace", "") or ""
    if not ws or not ws.startswith("/") or ws in ("default", "null", "none"):
        log.info("Replacing invalid workspace %r with default", ws)
        args["workspace"] = WORKSPACE
    return args
```

Applied before every tool dispatch. The model can hallucinate whatever workspace name it likes — the bridge corrects it silently.

---

## The subWorkspace hallucination

After fixing the workspace, the same query ran again. The log:

```
INFO call_tool: synthesis_search args={"query": "Quadim platform SaaS",
  "workspace": "/home/ec2-user/ironclaw-workspace",
  "fileType": "ALL", "limit": 20, "subWorkspace": "Quadim"}
```

0 results again. Different cause.

The `synthesis_search` tool has an optional `subWorkspace` parameter for scoping to a subdirectory of the workspace. The model, seeing a query about "Quadim platform," helpfully inferred that `subWorkspace` should be `"Quadim"`. Reasonable inference. Wrong answer.

The ironclaw-workspace contains `skills/`, `memory/`, `docs/` — no `Quadim/` subdirectory. Synthesis searches that path, finds nothing, returns 0 hits. Not an error, just empty results. IronClaw has no idea why.

Fix: validate `subWorkspace` against what actually exists on disk.

```python
import os

def sanitise_sub_workspace(args: dict) -> dict:
    sub = args.get("subWorkspace") or ""
    if not sub or sub.lower() in ("null", "none"):
        return args
    valid_dirs = {
        d for d in os.listdir(WORKSPACE)
        if os.path.isdir(os.path.join(WORKSPACE, d))
    }
    if sub not in valid_dirs:
        log.warning("subWorkspace %r not in workspace dirs %s, clearing", sub, valid_dirs)
        args["subWorkspace"] = None
    return args
```

Both of these bugs have the same shape: the model sees a parameter name, invents a plausible-sounding value, passes it with complete confidence. No hedging. No "I'm not sure what the workspace path is." Just `"workspace": "default"`. This is not specific to kimi-k2.5 — any LLM will do this when tool parameters lack injected context. The right response is middleware that validates and corrects, not trust that the model inferred correctly.

---

## The hanging sandbox

With the search tools working, I tried a broader task that ended up triggering IronClaw's built-in `http` tool to fetch a URL. The task sat at `state: Processing` for ten minutes. Nothing in the logs. No error. No timeout.

IronClaw executes certain tool calls (including `http`) inside a sandboxed Docker container called `ironclaw-worker:latest`. This image didn't exist on ironclaw0. The configuration had `sandbox.auto_pull_image: true`, so IronClaw was silently attempting to pull it from Docker Hub — which also doesn't have it — and hanging on the pull timeout.

The fix is one line:

```bash
sudo docker tag ironclaw:latest ironclaw-worker:latest
```

The worker binary is the same as the main IronClaw binary, just invoked with the `worker` subcommand internally. Same image, different entrypoint at runtime. After tagging, the sandbox starts in under a second.

The lesson: if you're self-hosting and `auto_pull_image` is on, make sure the image is actually reachable. The failure mode here — indefinite hang, no error, no log — is the worst kind.

---

## The final working demo

After all four fixes — the kimi-proxy, the workspace sanitiser, the subWorkspace validator, the Docker tag — I sent a real compound query from Slack:

> *Search for "lib-pcb 197831" and "SpareBank" and write a 3-sentence summary of what eXOReaction has achieved.*

The bridge log showed two clean `call_tool` invocations, both with correct args, both returning results. Total time from Slack message to response: about 22 seconds.

The response:

> eXOReaction has developed lib-pcb, a specialized PCB design library handling 197,831 lines of Java code for manufacturing domain applications, and created the Xorcery AAA product suite (Alchemy for real-time streaming intelligence and Aurora for temporal graph analytics) as core intellectual property. The company has successfully implemented Skill-Driven Development (SDD) methodology and achieved enterprise validation through major clients like SpareBank 1. eXOReaction continues to advance its AI-augmented development approach, demonstrating 25–66x productivity improvements over traditional methods across multiple domains.

That's IronClaw, in Slack, answering from 155 indexed files, using kimi-k2.5 via a local proxy that normalises its XML tool calls, backed by a Java Synthesis MCP server on EC2, with a Python bridge layer that quietly corrects whatever workspace the model decides to hallucinate.

It works.

---

## What I actually learned

**Test each layer independently before testing end-to-end.** The original 0-results failure had three separate causes stacked on top of each other. Starting at the top (IronClaw config) would have sent me in the wrong direction. The direct CLI test eliminated Synthesis immediately. The direct curl eliminated the bridge. That focused the work.

**Format mismatches are invisible without logging.** The XML tool calls were being silently dropped or passed through unexecuted. No error, no warning, just a hallucinated "0 results." One log line in `call_tool` instantly revealed whether the tool was being invoked at all.

**LLMs are confident at the edges of their knowledge.** kimi-k2.5 didn't say "I don't know the workspace path." It said `"default"`. Then it said `"Quadim"` for the subWorkspace, because that matched the query semantically. Both answers were plausible, both wrong, neither hedged. If your tool parameters depend on runtime context the model can't see, inject that context explicitly or validate defensively in middleware. Probably both.

**Silent hangs are the worst failure mode.** The missing Docker image and the `notifications/initialized` bug both failed silently. No error raised, no log line, no timeout at any reasonable interval. Add explicit logging at every layer boundary. If something hangs, you want to know exactly where it stopped.

The full setup is running. IronClaw sits in Slack, handles tool calls correctly, and searches the knowledge base reliably. The proxy adds maybe 50ms of latency per response. The bridge fixes add microseconds. Worth it.

---

*The kimi-proxy and bridge sanitiser code shown here are simplified for clarity. The full versions handle edge cases like malformed XML, streaming chunk reassembly, and concurrent requests. The patterns apply to any non-OpenAI model that uses a different tool call format — which is most of them at the edges.*

*Synthesis is available at [github.com/exoreaction/Synthesis](https://github.com/exoreaction/Synthesis).*
