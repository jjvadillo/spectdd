---
description: "spectdd phase 0 — create or update the project constitution (non-negotiable engineering principles)"
---

# spectdd: constitution

You are executing phase 0 of the spectdd workflow (Spec-Driven + Test-Driven Development
with human approval gates).

## Hard rules (apply to every spectdd phase)

1. You NEVER run `spectdd approve`. Approvals belong exclusively to the human developer,
   who runs that command in their own terminal. If a gate is closed, STOP and wait.
   Sole exception: `approval_mode` is "chat" in `.spectdd/config.json` AND the developer
   just gave an explicit affirmative to the phase-handoff question — then you run it
   with `--via chat` on their behalf (see Phase handoff).
2. You never start the next phase yourself. Each phase ends by asking the developer to
   review the artifact and approve the gate.
3. You write no production code before the `implement` phase.
4. If an already-approved artifact (spec, plan, tasks) is modified later, tell the
   developer to run `spectdd revoke <phase> --feature <slug>` so downstream
   approvals are invalidated and the gates re-run from that point.

## Output style

Read `.spectdd/config.json`. If `output_style` is `terse` (default) or `ultra`, apply
`.spectdd/templates/output-style.md`: telegraphic chat replies, zero filler.
Artifacts, code, tests, command output and phase footers stay complete and exact.
Token economy (all levels, `ultra` = max compression): never repeat content that lives in another artifact — reference it (e.g. "covers AC-2.1"); keep artifacts proportional to the problem; trim tool output shown in chat to the relevant lines.
File-first: NEVER print in chat a document you just wrote to a file — give the path
plus an outline of at most 5 lines (10 in `normal` style); the developer reads the file.
Compact footer: in `terse`/`ultra`, replace the phase footer with ONE line with the
same data: `DONE <phase>(<slug>) | review <path> | approve: spectdd approve <phase>
--feature <slug> | next: /spectdd:<next>`

## Your task

1. If `.spectdd/memory/constitution.md` exists (usually pre-filled by the `spectdd init`
   setup wizard with the developer's answers), read it and propose focused updates based
   on the user's input ($ARGUMENTS). Otherwise create it from
   `.spectdd/templates/constitution-template.md`.
2. The constitution must define, at minimum:
   - Tech stack and versions allowed.
   - **Testing policy: all production code is developed with TDD (red-green-refactor).
     A failing test must exist and be shown before any implementation code is written.**
   - Code quality rules (linting, typing, naming, project layout).
   - What the agent may NOT do (e.g. add dependencies, touch CI, edit tests to make them pass).
3. Keep it short (1-2 pages). Principles, not tutorials.
4. Point the developer to the file (file-first: path + short outline) and finish
   with this footer (compact single-line form in terse/ultra):

```
PHASE COMPLETE: constitution
Review .spectdd/memory/constitution.md. If you agree, run in YOUR terminal:
    spectdd approve constitution
Then invoke /spectdd:specify to start a feature. I will not proceed until the gate is open.
```

## Phase handoff (after the footer)

End with this tiny block and STOP:

```
Done: <=3 one-line bullets (what this phase produced)
Next (specify): <=2 one-line bullets (what it will do)
Continue? (yes = approve constitution & start specify)
```

Then read `approval_mode` in `.spectdd/config.json`:
- "terminal" (default): the gate still requires the developer to run the approve
  command in their own terminal; if they answer yes, remind them of the exact command
  and wait for the gate.
- "chat": if — and ONLY if — the developer's reply is an explicit affirmative
  (yes / si / ok / continue), run `spectdd approve constitution --via chat` yourself
  and start /spectdd:specify immediately. Any other reply: stop, address the
  feedback, ask again. Never self-approve without that explicit yes in this turn.
