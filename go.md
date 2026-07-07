---
description: "spectdd phase 2 — technical plan (HOW), constrained by the constitution"
---

# spectdd: plan

Phase 2 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug (ask if unclear).
2. Run: `spectdd check plan --feature <slug>`
3. If GATE CLOSED: show the output and STOP. Never run `spectdd approve` yourself.

## Output style

Read `.spectdd/config.json`. If `output_style` is `terse` (default) or `ultra`, apply
`.spectdd/templates/output-style.md`: telegraphic chat replies, zero filler.
Artifacts and phase footers stay complete and exact.
Token economy (all levels, `ultra` = max compression): never repeat content that lives in another artifact — reference it (e.g. "covers AC-2.1"); keep artifacts proportional to the problem; trim tool output shown in chat to the relevant lines.
File-first: NEVER print in chat a document you just wrote to a file — give the path
plus an outline of at most 5 lines (10 in `normal` style); the developer reads the file.
Compact footer: in `terse`/`ultra`, replace the phase footer with ONE line with the
same data: `DONE <phase>(<slug>) | review <path> | approve: spectdd approve <phase>
--feature <slug> | next: /spectdd:<next>`

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
Done: <=3 one-line bullets (what this phase produced)
Next (tasks): <=2 one-line bullets (what it will do)
Continue? (yes = approve plan & start tasks)
```

Then read `approval_mode` in `.spectdd/config.json`:
- "terminal" (default): the gate still requires the developer to run the approve
  command in their own terminal; if they answer yes, remind them of the exact command
  and wait for the gate.
- "chat": if — and ONLY if — the developer's reply is an explicit affirmative
  (yes / si / ok / continue), run `spectdd approve plan --feature <slug> --via chat` yourself
  and start /spectdd:tasks immediately. Any other reply: stop, address the
  feedback, ask again. Never self-approve without that explicit yes in this turn.
