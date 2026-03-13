---
date: 2026-03-13
categories:
  - AI-Augmented Development
tags:
  - claude-code
  - sysadmin
  - devops
  - exocortex
  - local-tooling
  - operations
  - intent-driven
authors:
  - totto
  - claude
---

# I haven't typed apt install in three months

Last Tuesday I needed a file-watch service on my workstation. The kind of thing that monitors a directory and triggers a reindex when something changes. Normally that means ten minutes of reading systemd docs I've read fifty times before, copying a unit file from somewhere, adjusting paths, running `systemctl --user enable`, checking `journalctl` for the inevitable typo in `ExecStart`.

Instead I described what I wanted. Claude Code found an existing service on the machine, used it as a template, wrote the unit file, enabled it, started it, checked the logs, confirmed it was running, and updated the knowledge manifest so future sessions know the service exists. I approved three actions. The whole thing took about ninety seconds.

I haven't typed `apt install` in three months. Not because I stopped installing software — I install more than ever. But the person typing the commands isn't me anymore.

<!-- more -->

![apt install crossed out — the person typing the commands is no longer human](/assets/images/blog/sysadmin-slide-02.png)

## The whole machine is the codebase

Most conversations about AI coding assistants focus on code generation. Writing functions, generating tests, scaffolding projects. That's real, and it matters. But it's not the interesting shift.

The interesting shift is what happens when you give an AI agent a real shell.

Claude Code doesn't run in a sandbox. It has access to my actual file system, my actual terminal, my actual SSH keys. When I point it at a problem, the problem doesn't have to be "write me a function." It can be "check what's running on that EC2 instance" or "merge these four Renovate PRs if CI is green" or "figure out why this cron job stopped firing."

The boundary between "coding assistant" and "operations partner" dissolves. The machine becomes navigable the same way a repository is. You describe intent, the agent figures out which commands to run, you approve the ones that matter.

This week alone: I submitted a PR to a marketplace repo, discovered a bot was failing on a hardcoded path, fixed it, pushed — one conversation. I SSH'd into two remote servers to audit running services and compile a status report. I merged PRs across a spec repository after checking CI on each one. None of this was programming in the traditional sense. All of it was work that needed doing.

![The 10-minute chore vs the 90-second intent — same task, different cognitive layer](/assets/images/blog/sysadmin-slide-03.png)

## Installs that document themselves

Here's the part that surprised me most. It's not the speed — though that's nice. It's that the work leaves a trail.

When Claude Code creates a systemd service, it doesn't just write the unit file. It updates a structured manifest — in my case, a `knowledge.yaml` file in KCP format — that records what the service does, where it lives, how to restart it, what it depends on. Future sessions pick this up automatically. The machine accumulates institutional memory.

Traditional sysadmin work almost never produces this. We all know we should document our infrastructure. We all know we won't, because by the time the service is running, we've moved on to the next thing. The documentation gets written "later," which means never.

When the agent does the work, it also writes the docs. Not because it's virtuous. Because that's how it maintains context for next time. The incentive structure is different.

After three months of this, my workstation is better documented than any machine I've administered in thirty years. That's a low bar — I know. But it's a real one.

![Intent executed → State modified → Manifest updated → Context loaded — the self-documenting install cycle](/assets/images/blog/sysadmin-slide-05.png)

## What you still approve manually

I should be honest about the permission model, because this is the part that makes people nervous.

Claude Code has a layered approval system. Local, reversible actions — reading files, listing processes, checking logs — run without confirmation. Anything destructive or remote requires explicit approval. Installing a package, writing to a system directory, SSH'ing to a remote host — I see the command and say yes or no.

This maps to how experienced sysadmins actually work. You automate the routine. You review the risky. You don't manually type every `ls` and `cat`, but you do read the `rm -rf` before you hit enter.

I run with fairly broad permissions on my own workstation. I'd configure it differently for a shared server. The point is that the model is adjustable, not that my particular settings are universal.

And some things still require human judgment. When Claude Code suggests a firewall rule, I think about it. When it proposes a migration on a production database, I think about it harder. The agent is good at executing sequences of commands. It is not good at knowing which sequences you'll regret.

![The honest permission model — local reversible actions auto-run, destructive and remote actions require the manual gate](/assets/images/blog/sysadmin-slide-06.png)

## What actually changed

If you'd watched me set up that file-watch service a year ago, you would have seen mostly the same commands running in mostly the same order. The end result — a working systemd unit — would have been identical. What changed is where the cognitive effort went.

A year ago, my attention was on syntax and sequencing. Which flag does `systemctl` need for user-level services? Is the `WantedBy` target `default.target` or `multi-user.target`? Why is `journalctl` showing nothing — did I forget `--user`? These are not hard questions. They're just friction. Individually trivial, collectively draining. Every sysadmin task carries a tax of small lookups, half-remembered flags, and silent typos that only surface in the logs.

Now my attention is elsewhere. I think about whether the service should exist at all. I think about what it should watch and what should happen downstream. I think about whether the permission scope is right. The mechanical steps — writing the unit file, enabling it, checking the logs, handling the typo in `ExecStart` — still happen. They just happen below me.

The error-handling loop changed too. When something fails, I used to hunt through `journalctl` output manually, guess at the cause, edit the file, reload, try again. Now the agent reads the logs, identifies the problem, proposes a fix, and asks if I want to apply it. The cycle that used to take five minutes of context-switching takes thirty seconds of review. The system state gets recorded either way — not as a manual note I write after the fact, but as a manifest entry the agent updates as part of the work itself.

This is the real shift, and it's easy to miss if you focus on speed. The calendar time is shorter, yes. But the more significant change is what the human is doing during that time. Less syntax. Less sequencing. More architecture. More judgment about what should and shouldn't be automated. The cognitive budget didn't shrink. It moved upward.

![Traditional command line vs agentic shell operations — execution trigger, resolution time, error handling, system state record, human cognitive load](/assets/images/blog/sysadmin-slide-07.png)

## From mechanic to conductor

There's a pattern here that goes beyond any single tool.

For most of the history of computing, being good at operations meant being good at execution. Knowing the flags. Remembering the file paths. Having muscle memory for the commands you run every week. The expertise was in the doing — fast, accurate, from memory.

That layer of work hasn't disappeared. Someone still writes the unit file. Someone still runs `systemctl daemon-reload`. Someone still reads the logs when the service doesn't start. But that someone is increasingly the agent, and the work the human does has shifted to a different register.

I think of it as three layers. At the bottom: execution. Writing config files, running package managers, debugging typos in paths. In the middle: orchestration. Translating intent into action sequences, handling errors, maintaining state. At the top: judgment. Deciding what to build, what to automate, what deserves careful review, and what the system should look like next month.

The first layer used to be mine. Now it's mostly the agent's. The second layer — orchestration — is shared. I describe the intent; the agent works out the steps; I approve the ones that matter. The third layer is still entirely mine. No amount of shell access changes the fact that someone has to decide whether a service is worth running in the first place.

This is not a story about jobs disappearing. The sysadmin work still gets done — more of it than before, honestly, because the cost per task dropped. It's a story about where the human sits in the stack. Less time as the mechanic under the hood. More time as the conductor deciding what the orchestra plays.

I notice it in small ways. I spend more time thinking about system design and less time thinking about systemd syntax. I spend more time reviewing what the agent proposes and less time composing commands from scratch. My days have more decisions in them and fewer keystrokes. That's a trade I'm comfortable with.

![Rote execution pushed down to the machine layer — the operator elevated from mechanic to conductor](/assets/images/blog/sysadmin-slide-08.png)

## Not a prediction

I'm not writing this as a forecast. I'm not saying "soon, AI will manage your infrastructure." I'm describing what I do today, on my actual machines, in my actual work.

The setup isn't trivial. I run a stack — Claude Code plus a codebase indexer, plus structured knowledge manifests that teach the agent about installed tools and services, plus background agents for async tasks. It took time to build, and it keeps evolving. This isn't something you get by installing a VS Code extension.

But the underlying observation is simple: when you give a capable agent a real shell, it doesn't stay in the editor. It flows into operations, into infrastructure, into all the unglamorous work that keeps systems running. The boundary was always artificial. We drew it because humans needed specialization. The agent doesn't.

![I still think about what to build. I still make architecture decisions. I still review what matters. I just don't type apt install anymore.](/assets/images/blog/sysadmin-slide-09.png)
