---
description: "spectdd onboarding — adopt an EXISTING project: analyze the codebase and generate the spectdd memory files from what is already there"
---

# spectdd: onboard (existing project)

Entry point for brownfield projects. Run AFTER `spectdd init` (which installs the
commands and typical files) and INSTEAD of writing the constitution from scratch.
Input from developer: $ARGUMENTS

## Output style

Read `.spectdd/config.json`. If `output_style` is `terse` (default) or `ultra`, apply
`.spectdd/templates/output-style.md`. File-first: analysis results go to files, never
echoed in chat. Token economy: read manifests and configs fully, but only SAMPLE
representative source files (entry points, one module per layer, one test file) —
do not read the whole tree.

## Step 1 — Detect the stack (read, don't guess)

Inventory from the actual repo: language(s) and versions (manifests: pyproject.toml,
package.json, go.mod, pom.xml, build.gradle...), frameworks and key dependencies,
test framework + where tests live + how to run them, lint/format/typing configs,
project layout (top-level map, one line per dir), CI workflows, existing docs
(README, ADRs, AGENTS.md).

## Step 2 — Generate the spectdd memory files

1. `.spectdd/memory/constitution.md`: fill the template with the DETECTED stack and
   the project's existing conventions. Mark anything uncertain with `[ASSUMED]` so
   the developer can correct it. Keep the mandatory TDD policy and audit DoD.
2. `.spectdd/memory/architecture.md`: reverse-engineered decisions table
   (decision | current choice | evidence file) covering layout, frameworks, data
   storage, testing, lint/CI. Same format the architect skill produces.
3. If the developer's $ARGUMENTS mention pain points or goals, add a short
   "Direction" section to architecture.md.

## Step 3 — Gap report

List (one line each): missing tests or broken suite, no lint/typing, no CI,
undocumented conventions, dead config. Suggest — do not apply — fixes; each gap can
become a future feature via /spectdd:specify.

## Footer

```
PHASE COMPLETE: onboard
Review .spectdd/memory/constitution.md (fix any [ASSUMED]) and architecture.md.
If you agree, run in YOUR terminal:  spectdd approve constitution
Then /spectdd:specify your first feature. I will not proceed until the gate is open.
```

## Phase handoff (after the footer)

Same handoff protocol as every phase: Done (<=3 bullets) + Next (constitution
approval) + "Continue?". In `approval_mode: chat`, an explicit yes lets you run
`spectdd approve constitution --via chat` and go straight to /spectdd:specify.
