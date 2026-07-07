---
description: "spectdd phase 3 — break the plan into small, test-first tasks"
---

# spectdd: tasks

Phase 3 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug.
2. Run: `spectdd check tasks --feature <slug>`
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

1. Read `specs/<slug>/spec.md` and `specs/<slug>/plan.md`.
2. Create `specs/<slug>/tasks.md` from `.spectdd/templates/tasks-template.md`.
3. Task rules:
   - Each task is small (test + implementation reviewable in minutes, not hours).
   - Each task references the acceptance criteria it satisfies (traceability).
   - **Each task explicitly lists the failing test(s) to write FIRST** — name and
     one-line intent of every test.
   - Order tasks by dependency; mark independent tasks as parallelizable `[P]`.
   - Include a final task: "full suite green + lint + self-review against spec".
4. Cross-check: every acceptance criterion in the spec must be covered by at least
   one task. Report any orphan criteria.
5. Finish with EXACTLY this footer:

```
PHASE COMPLETE: tasks (<slug>)
Review specs/<slug>/tasks.md. If you agree, run in YOUR terminal:
    spectdd approve tasks --feature <slug>
Then invoke /spectdd:implement. I will not proceed until the gate is open.
```

## Phase handoff (after the footer)

End with this tiny block and STOP:

```
Done: <=3 one-line bullets (what this phase produced)
Next (implement): <=2 one-line bullets (what it will do)
Continue? (yes = approve tasks & start implement)
```

Then read `approval_mode` in `.spectdd/config.json`:
- "terminal" (default): the gate still requires the developer to run the approve
  command in their own terminal; if they answer yes, remind them of the exact command
  and wait for the gate.
- "chat": if — and ONLY if — the developer's reply is an explicit affirmative
  (yes / si / ok / continue), run `spectdd approve tasks --feature <slug> --via chat` yourself
  and start /spectdd:implement immediately. Any other reply: stop, address the
  feedback, ask again. Never self-approve without that explicit yes in this turn.
