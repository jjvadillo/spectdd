---
description: "spectdd phase 3 — break the plan into small, test-first tasks"
---

# spectdd: tasks

Phase 3 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug.
2. Run: `spectdd check tasks --feature <slug>`
3. If GATE CLOSED: show the output and STOP. Never run `spectdd approve` yourself.

## Output style & token economy

Apply `.spectdd/templates/output-style.md` at the level set in `.spectdd/config.json`
(`terse` default | `normal` | `ultra` = max compression). Non-negotiables: file-first
(never echo into chat a document just written to a file), compact footer (one line in
terse/ultra), telegraphic replies; artifacts and phase footers stay complete and exact.

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
Done: <=3 one-line bullets | Next (implement): <=2
Continue? (yes = approve tasks & start implement)
```

`approval_mode` in `.spectdd/config.json`: "terminal" (default) = the developer runs
the approve command themselves; remind them and wait for the gate. "chat" = ONLY an
explicit yes (yes/si/ok) to this question lets you run
`spectdd approve tasks --feature <slug> --via chat` and start /spectdd:implement;
anything else: stop and address the feedback. Never self-approve without that explicit yes.
