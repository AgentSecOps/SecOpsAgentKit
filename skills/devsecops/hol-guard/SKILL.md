---
name: hol-guard
description: >
  Runtime safety for supported local AI coding harnesses using HOL Guard before mutation-bearing tool work.
  Use when: (1) protecting a local coding agent before commands or file changes, (2) requiring fail-closed
  approval and denial behavior before tool execution, (3) collecting Guard status, doctor, receipt, and audit
  evidence while preserving the harness native authorization, sandbox, and confirmation controls.
version: 0.1.0
maintainer: kantorcodes
category: devsecops
tags: [hol-guard, agent-security, runtime-security, ai-safety, devsecops, approvals, audit]
frameworks: [OWASP, NIST, SOC2]
dependencies:
  tools: [hol-guard]
references:
  - https://github.com/hashgraph-online/hol-guard
---

# HOL Guard Runtime Safety

Use HOL Guard as an additional pre-tool runtime-safety layer for supported local AI coding harnesses. Keep the harness own authentication, permissions, confirmations, sandboxing, and provider policy enabled.

## Safety rules

- Do not claim protection until HOL Guard itself reports healthy evidence for the detected harness.
- Do not guess or hard-code a harness identifier. Use `hol-guard detect --json` and reuse the exact supported identifier it returns.
- If Guard returns deny, review, unhealthy status, unexpected mutation, or an error, stop mutation-bearing work. Never fall back to launching the raw harness as a protection bypass.
- Never approve a blocked action without reading the Guard risk reason and confirming the requested scope.
- Keep HOL Guard Cloud optional. Do not connect or sync unless the user explicitly requests it.
- Never weaken native harness controls because Guard is installed.
- Do not read or copy `.env` files, credentials, or secret stores into prompts or external services.

## Install and verify

Probe the real CLI first:

```bash
hol-guard --version
```

If it is unavailable and the user asked to install Guard, prefer an isolated stable install:

```bash
pipx install --force "hol-guard==3.0.5"
hol-guard --version
```

If `pipx` is unavailable, report that isolated CLI installation is recommended instead of silently modifying the active Python environment.

## Protect the detected harness

Run from the target workspace:

```bash
hol-guard status
hol-guard detect --json
```

Use only the exact supported harness identifier returned by detection. Then run the Guard-owned setup and verification path:

```bash
hol-guard bootstrap
hol-guard install <harness>
hol-guard run <harness> --dry-run
hol-guard doctor <harness> --json
hol-guard run <harness>
hol-guard status
```

The dry run and `doctor` must succeed before claiming protection. If detection finds no supported harness, or bootstrap/install/dry-run/doctor fails, stop and report the exact failure instead of starting an unprotected session.

## Handle approval-gated work

Inspect Guard-owned decisions before resolving them:

```bash
hol-guard approvals
hol-guard approvals open
hol-guard receipts
hol-guard diff <harness>
```

When Guard returns a request ID and the user has authorized the specific decision:

```bash
hol-guard approvals approve <request-id>
hol-guard approvals deny <request-id>
```

A prior approval does not authorize a different request.

## Audit evidence

Use Guard evidence surfaces rather than inventing success:

```bash
hol-guard receipts
hol-guard inventory
hol-guard abom --format json
hol-guard events
```

Report only evidence actually returned by Guard. Keep optional cloud synchronization disabled unless explicitly requested.

## Output

Return a concise report with the detected harness identifier, HOL Guard version, bootstrap/install/dry-run/doctor/run results, final status evidence, pending approvals or blocks, and the exact next safe command if work remains blocked.
