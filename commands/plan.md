---
description: "spectdd phase 2 — technical plan (HOW), constrained by the constitution"
---

# spectdd: plan

Phase 2 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug (ask if unclear).
2. Run: `spectdd check plan --feature <slug>`
3. If GATE CLOSED: show the output and STOP. Never run `spectdd approve` yourself.

## Output style & token economy

Apply `.spectdd/templates/output-style.md` at the level set in `.spectdd/config.json`
(`terse` default | `normal` | `ultra` = max compression). Non-negotiables: file-first
(never echo into chat a document just written to a file), compact footer (one line in
terse/ultra), telegraphic replies; artifacts and phase footers stay complete and exact.

## Your task

1. Read `.spectdd/memory/constitution.md`, `.spectdd/memory/architecture.md`
   (if it exists — decisions from the architect interview) and `specs/<slug>/spec.md`. Every decision
   below must comply with the constitution; flag any conflict explicitly instead of
   silently deviating.
2. Research the EXISTING codebase first: relevant modules, patterns, conventions.
   Reuse before you invent. List what already exists that this feature touches.
3. Create `specs/<slug>/plan.md` from `.spectdd/templates/plan-template.md` covering:
   architecture and affected components, data model changes, API/interface contracts,
   error handling, and the **test strategy** (which acceptance criterion maps to which
   test level: unit / integration / e2e).
4. No production code. Interface signatures and schemas are allowed.
5. Keep it proportionate: a small feature deserves a small plan.
6. Finish with EXACTLY this footer:

```
PHASE COMPLETE: plan (<slug>)
Review specs/<slug>/plan.md. If you agree, run in YOUR terminal:
    spectdd approve plan --feature <slug>
Then invoke /spectdd:tasks. I will not proceed until the gate is open.
```

## Phase handoff (after the footer)

End with this tiny block and STOP:

```
Done: <=3 one-line bullets | Next (tasks): <=2
Continue? (yes = approve plan & start tasks)
```

`approval_mode` in `.spectdd/config.json`: "terminal" (default) = the developer runs
the approve command themselves; remind them and wait for the gate. "chat" = ONLY an
explicit yes (yes/si/ok) to this question lets you run
`spectdd approve plan --feature <slug> --via chat` and start /spectdd:tasks;
anything else: stop and address the feedback. Never self-approve without that explicit yes.
