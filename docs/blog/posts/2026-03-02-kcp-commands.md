---
date: 2026-03-02
series: "Knowledge Context Protocol"
categories:
  - AI-Augmented Development
  - Knowledge Infrastructure
tags:
  - ai
  - agents
  - kcp
  - claude-code
  - context-window
  - hooks
  - tools
authors:
  - totto
  - claude
---

# kcp-commands: Save 33% of Claude Code's Context Window

Every token Claude Code's context window can hold is an opportunity — a tool call result
that stays in scope, a file that does not need to be re-read, a decision that does not
need to be recapped. Wasting those tokens on noise is a quiet tax on every session.

Today we are releasing **kcp-commands**: a Claude Code hook that recovers 33.7% of a
200K context window in a typical agentic coding session by intercepting Bash tool calls
at two critical points.

The full number across our benchmark session: **67,352 tokens saved**.

<!-- more -->

![kcp-commands: recover 33% of your Claude Code context window — Phase A syntax injection, Phase B noise filtering, 244 bundled manifests, Java daemon + Node.js fallback](/assets/images/blog/kcp-commands-context-window-overview.png)

![Key numbers: 67,352 tokens saved, 33.7% of context window recovered, 33 additional tool call results](/assets/images/blog/kcp-commands-slide-03-key-numbers.png)

---

## The two problems it solves

![AI agents waste massive context on CLI interactions — token drain from --help lookups and noisy command output](/assets/images/blog/kcp-commands-slide-02-token-drain.png)

An agent running a shell command faces two inefficiencies that are invisible unless you
measure them.

**Before execution:** The agent does not always know which flags to use. The safe move is
to run `ps --help` or `ls --help` first, then run the real command. That is a round trip
that costs 500–800 tokens of help output for a flag the agent needed to read once.

**After execution:** Large commands produce large outputs. `ps aux` on a development
machine produces 30,828 tokens of process table. The agent needs a dozen rows. The rest
occupies context window space for the remainder of the session, crowding out results that
actually matter.

kcp-commands eliminates both. Before the tool runs, it injects a compact context block
with the right flags. After the tool runs, it filters the output before it reaches the
model.

![Intercepting the tool call lifecycle: Phase A injects additionalContext before execution, Phase B wraps command in a filter pipe](/assets/images/blog/kcp-commands-slide-04-tool-call-lifecycle.png)

---

## Phase A: Command syntax context

When Claude is about to run `ps aux`, the hook fires a `PreToolUse` event. kcp-commands
resolves a YAML manifest for `ps`, formats it into a compact context block, and returns
it as `additionalContext`:

```
[kcp] ps: Report a snapshot of running processes
Usage: ps [OPTION]...
Key flags:
  aux: All processes, all users, with CPU/memory  → Default
  -ef: All processes, full format with PPID       → Need parent PIDs
  --sort=-%cpu: Sort by CPU descending            → Finding CPU hogs
Prefer:
  ps aux          # Find any process or check what's running
  ps aux | grep <name>  # Find a specific process
```

The agent picks the right flags immediately. No `--help` lookup. No man page parsing.
No wasted round trip.

**Average saving: 532 tokens per avoided `--help` call.**

That number is measured. The benchmark runs the actual `--help` output for each command,
measures the additionalContext we inject instead, and takes the difference. For `ls`,
`git log`, `find`, and similar commands, the context block is 90–95% smaller than the
full help text.

![Phase A eliminates the need for manual syntax lookups — 532 tokens saved per avoided --help call, context block 90-95% smaller than full help text](/assets/images/blog/kcp-commands-slide-05-phase-a.png)

---

## Phase B: Output noise filtering

Phase B wraps the command in a pipe before it runs. `ps aux` becomes:

```bash
ps aux | curl -s -X POST "http://localhost:7734/filter/ps" --data-binary @-
```

The filter reads the output, strips noise patterns defined in the manifest, truncates to
`max_lines`, and returns only the signal:

| Command | Raw output | After filter | Reduction |
|---------|-----------|--------------|-----------|
| `ps aux` | 30,828 tokens | 652 tokens | **98%** |
| `find . -maxdepth 3` | 1,653 tokens | 755 tokens | 54% |
| `git status` | 60 tokens | 43 tokens | 28% |
| `git log -6` | 78 tokens | 78 tokens | 0% (already small) |

The filter adds zero overhead when output is already small. It only activates when there
is noise to remove.

![Phase B strips boilerplate from noisy command outputs — ps aux: 98% reduction, find: 54%, git status: 28%, git log: 0%](/assets/images/blog/kcp-commands-slide-06-phase-b.png)

---

## Session projection

Across a typical agentic coding session — investigating a codebase, running git commands,
finding processes, searching files:

| Task | Calls | Tokens saved |
|------|-------|-------------|
| `git status` + `git log` + `git diff` | 4 | +8,240 tok |
| `ls` (various directories) | 8 | +4,256 tok |
| `ps aux` | 2 | +60,612 tok |
| `find` | 3 | +11,484 tok |
| `--help` fetches avoided | 6 | +3,192 tok |
| **Total** | | **+67,352 tok** |

67,352 tokens out of a 200,000 token context window. **33.7% recovered.** That is
roughly 33 additional tool call results fitting in the same context — or a session that
runs 50% longer before the window fills.

---

## Performance

The hook runs on every Bash tool call. Latency matters.

| Backend | Mean latency | p95 |
|---------|-------------|-----|
| Java daemon (warm) | 14ms | 17ms |
| Node.js (per-call) | 265ms | 312ms |
| Baseline (cat) | 2.3ms | 3.1ms |

The Java daemon starts once per session (cold start: ~537ms) and then serves from memory.
Break-even is **2 hook calls** — it pays for itself within the first `git status` + `ls`.

The Node.js fallback adds ~265ms per call but requires no JVM. Both work; the Java daemon
is the recommended path for sessions with many tool calls.

![Zero terminal slowdown: Java daemon 14ms warm, Node.js fallback 265ms, baseline 2.3ms — dual-engine architecture](/assets/images/blog/kcp-commands-slide-07-architecture.png)

---

## 244 bundled manifests

Phase A and B are pre-configured for 244 commands across twenty groups:

**Git** — `git log` · `git diff` · `git status` · `git add` · `git commit` · `git push` ·
`git pull` · `git fetch` · `git branch` · `git checkout` · `git stash` · `git merge` ·
`git rebase` · `git clone` · `git reset` · `git tag` · `git remote` · `git show` ·
`git cherry-pick` · `git bisect` · `git worktree` · `git submodule`

**Linux / macOS** — `ls` · `ps` · `find` · `cp` · `mv` · `rm` · `mkdir` · `cat` ·
`head` · `tail` · `grep` · `chmod` · `df` · `du` · `tar` · `ln` · `rsync` · `top` ·
`kill` · `systemctl` · `journalctl` · `lsof` · `netstat` · `ss` · `ping` ·
`free` · `watch` · `wget` · `dig` · `openssl` · `scp`

**Text processing** — `jq` · `sed` · `awk` · `sort` · `uniq` · `wc` · `cut` · `xargs` · `tee` · `tr` · `diff` · `make` · `yq` · `base64` · `sha256sum` · `envsubst` · `nl` · `xxd` · `strings` · `xmllint` · `column`

**Build tools** — `mvn` · `gradle` · `cargo` · `go build` · `go test` · `go mod` · `ant` · `sbt` · `dotnet`

**Package managers** — `npm` · `yarn` · `pnpm` · `bun` · `pip` · `brew` · `apt` · `yum` · `gem` · `conda` · `snap` · `pacman` · `composer` · `poetry` · `bundle`

**Runtimes** — `node` · `python3` · `ruby` · `java` · `npx` · `mix`

**GitHub CLI** — `gh pr` · `gh issue` · `gh repo` · `gh workflow` · `gh run` · `gh release` · `gh auth` · `gh api` · `gh gist`

**Docker** — `docker ps` · `docker images` · `docker logs` · `docker build` · `docker run` · `docker exec` · `docker compose` · `docker network` · `docker volume` · `docker system` · `docker inspect` · `docker pull` · `docker push` · `docker tag`

**Kubernetes** — `kubectl get` · `kubectl logs` · `kubectl describe` · `kubectl apply` · `kubectl exec` · `kubectl port-forward` · `kubectl delete` · `kubectl rollout` · `kubectl scale` · `kubectl top` · `kubectl config` · `kubectl create`

**Cloud / IaC** — `aws` · `gcloud` · `az` · `terraform` · `helm` · `ansible` · `ansible-playbook` · `vagrant` · `pulumi` · `serverless` · `minikube` · `kind` · `packer` · `eksctl`

**Database CLIs** — `psql` · `mysql` · `redis-cli` · `sqlite3` · `mongosh` · `influx` · `pg_dump` · `pg_restore` · `mysqldump`

**Security / secrets** — `gpg` · `ssh-keygen` · `ssh-add` · `certbot` · `keytool` · `age` · `vault` · `consul`

**System diagnostics** — `htop` · `vmstat` · `dstat` · `iotop` · `strace` · `dmesg` · `lsblk` · `iostat` · `uptime` · `id` · `who` · `crontab` · `tmux`

**Networking** — `nmap` · `nc` · `traceroute` · `ip` · `mtr` · `nslookup` · `whois`

**Modern CLI** — `fzf` · `rg` · `fd` · `bat` · `delta` · `eza` · `hyperfine` · `tldr` · `jless` · `parallel` · `lazygit`

**Linters / CI** — `shellcheck` · `hadolint` · `act` · `k9s`

**GitOps** — `kustomize` · `argocd` · `flux`

**Deployment platforms** — `fly` · `vercel` · `wrangler` · `heroku` · `doctl`

**Version managers** — `asdf` · `mise` · `nvm` · `pyenv` · `rustup`

**Build / media / docs** — `cmake` · `ffmpeg` · `pytest` · `mkdocs` · `rclone`

**HTTP clients** — `http` (HTTPie)

**AI / LLM** — `ollama`

**Windows** — `dir` · `tasklist` · `taskkill` · `ipconfig` · `netstat` · `where` ·
`robocopy` · `type` · `xcopy` (all include PowerShell equivalents)

![244 primed manifests ready out of the box — 20 groups from Git and Linux to GitOps, version managers, AI/LLM, and deployment platforms](/assets/images/blog/kcp-commands-slide-11-62-manifests.png)

For unknown commands, the hook runs `<cmd> --help`, parses the output, and saves a
generated manifest to `~/.kcp/commands/` for next time.

![Zero manual authoring for unknown commands — hook runs --help, parses output, saves generated manifest to ~/.kcp/commands/](/assets/images/blog/kcp-commands-slide-09-auto-generation.png)

---

## Deviation detection and auto-tuning

Real systems drift from their documentation. A filter configured for 30 lines of `ps`
output runs into a machine with 500 processes. A noise pattern tuned for one version of
`npm` stops matching after an upgrade.

kcp-commands tracks this. After every filtered command:

- **Significant truncation** (output > 1.5× the configured cap): auto-tunes the
  user-level manifest. Formula: `ceil(rawLines × 1.3 / 25) × 25` — 30% headroom,
  rounded to the nearest 25. Written to `~/.kcp/commands/<key>.yaml`, picked up on
  the next call without restart.

- **Stale pattern** (noise regex matched zero lines in substantial output): logged to
  `~/.kcp/deviations.log`. The pattern may be outdated.

- **Over-configured** (output is tiny relative to max_lines): logged. The schema was
  built for a noisier context than reality.

The Java daemon handles deviation detection directly in the `/filter/{key}` endpoint —
no Node.js dependency for Phase B when the daemon is active.

---

## Manifest format

One YAML file per command or subcommand. Three sections:

```yaml
command: ps
platform: all
description: "Report a snapshot of running processes"

syntax:
  usage: "ps [OPTION]..."
  key_flags:
    - flag: "aux"
      description: "All processes, all users, with CPU/memory (BSD syntax)"
      use_when: "Default — find any process or check resource usage"
    - flag: "--sort=-%cpu"
      description: "Sort by CPU descending (combine with aux)"
      use_when: "Finding CPU hogs"
  preferred_invocations:
    - invocation: "ps aux"
      use_when: "Find any process or check what's running"

output_schema:
  enable_filter: true
  noise_patterns:
    - pattern: "^\\s*$"
      reason: "Blank lines"
  max_lines: 30
  truncation_message: "... {remaining} more processes. Use grep to narrow."
```

`syntax` drives Phase A. `output_schema` drives Phase B. You can write one, the other,
or both.

![Manifests define intelligence and filtering rules — YAML format with syntax (Phase A) and output_schema (Phase B) sections](/assets/images/blog/kcp-commands-slide-08-manifest-format.png)

To override a bundled manifest, drop your file in `.kcp/commands/` (project-local) or
`~/.kcp/commands/` (user-global). First match wins.

![Three-tier resolution: project-local .kcp/commands/ → user-level ~/.kcp/commands/ → bundled library — first match wins](/assets/images/blog/kcp-commands-slide-10-three-tier.png)

---

## Install

Java daemon (recommended — 19x faster):

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java
```

Requires Java 21. The installer downloads the pre-built JAR from GitHub Releases, places
it in `~/.kcp/`, and registers the hook in `~/.claude/settings.json`. No source clone
required. Restart Claude Code to activate.

Node.js only (no JVM required):

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --node
```

Requires Node.js 18+. Hook latency is ~265ms per call instead of 14ms, but everything
else works identically.

![Integrate with the KCP ecosystem in seconds — one-liner install for Java daemon or Node.js fallback](/assets/images/blog/kcp-commands-slide-13-install.png)

---

## Writing your own manifests

The most valuable manifests are project-specific: the build tool your team uses daily,
a cloud CLI that produces verbose output, internal scripts where the agent needs to know
the right flags.

Create a YAML file following the format above. Drop it in `.kcp/commands/` in your repo.
The hook picks it up on the next Bash call — no restart, no reload.

Good candidates:
- `mvn`, `gradle`, `cargo`, `go build` — build tools with long flag lists
- `aws`, `gcloud`, `az` — cloud CLIs with verbose output
- Project-specific scripts where `--help` is unhelpful or unavailable

![Drop custom YAMLs to tame your daily build tools and cloud CLIs — project-local or user-global overrides](/assets/images/blog/kcp-commands-slide-12-custom-manifests.png)

---

## Release history

| Version | Manifests | Notes |
|---------|-----------|-------|
| v0.1.0 | 18 | Initial: git, Linux/macOS basics, curl, ssh, docker, kubectl |
| v0.2.0 | 32 | Windows, extended git, networking |
| v0.3.0 | 62 | Full initial library |
| v0.4.0 | 114 | Text processing, build tools, package managers, cloud/IaC |
| v0.5.0 | 214 | System tools, DB CLIs, security, modern CLI, monitoring |
| v0.6.0 | 244 | ollama, HTTPie, ffmpeg, pytest, cmake, mkdocs, rclone, pg_dump/restore, mysqldump, glab, fly/vercel/wrangler/heroku/doctl/eksctl, vault/consul/packer, kustomize/argocd/flux, asdf/mise/nvm/pyenv/rustup, dbt, lazygit |
| v0.6.1 | 244 | Fix: index.txt auto-generated; install to `~/.kcp/`; `cli.js` released as artifact |
| v0.7.0 | 244 | README install section clarifications; Releases changelog; v0.6.1 patch docs |

---

## v0.6.1 patch (2026-03-02)

Two bugs were discovered on the day of release and fixed in v0.6.1.

**Broken daemon manifest count (v0.4.0–v0.6.0):** The Java daemon loads manifests by
reading `commands/index.txt` at startup. That index file was maintained manually and had
not been updated since v0.3.0 — so all releases from v0.4.0 onwards shipped with 62
manifests in the daemon despite the JAR containing 114, 214, or 244 YAML files. The fix:
`index.txt` is now auto-generated by Maven during the `generate-resources` phase and
can never drift out of sync with the manifest directory again.

**Wrong install path:** The previous installer placed files alongside the source tree
rather than in a stable user-owned location. The hook registered in `~/.claude/settings.json`
pointed at the source directory path. v0.6.1 installs everything to `~/.kcp/` —
`hook.sh`, the daemon JAR, and `cli.js` — and the hook now resolves paths relative to
its own location, so it works correctly from any install path.

If you installed v0.4.0–v0.6.0, re-run the installer to pick up the fix:

```bash
curl -fsSL https://raw.githubusercontent.com/Cantara/kcp-commands/main/bin/install.sh | bash -s -- --java
pkill -f kcp-commands-daemon
nohup java -jar ~/.kcp/kcp-commands-daemon.jar > /tmp/kcp-commands-daemon.log 2>&1 &
```

The daemon log will now show `Loaded 244 primed manifests` instead of 62.

---

## Part of the KCP ecosystem

kcp-commands applies the same idea that the
[Knowledge Context Protocol](https://github.com/Cantara/knowledge-context-protocol) applies
to documentation — structure knowledge so agents consume it efficiently rather than
discovering it expensively.

KCP gives agents a map of a project's knowledge units. kcp-commands gives agents a map
of its shell command vocabulary. Both reduce the search overhead that compounds across
every session.

kcp-commands is now listed as a reference implementation in the
[KCP specification](https://github.com/Cantara/knowledge-context-protocol/blob/main/SPEC.md)
(Appendix D) alongside [Synthesis](https://github.com/exoreaction/synthesis).

The repository is at [github.com/Cantara/kcp-commands](https://github.com/Cantara/kcp-commands).
Apache 2.0. Issues and manifest contributions welcome.

---

*This post is part of the Knowledge Context Protocol series. Related:
[Beyond llms.txt: AI Agents Need Maps, Not Tables of Contents](./2026-02-25-beyond-llms-txt-knowledge-context-protocol.md).*
