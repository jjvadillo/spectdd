---
description: "spectdd phase 1 — write the functional specification (WHAT and WHY, no tech details)"
---

# spectdd: specify

Phase 1 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Determine the feature slug: next sequential number + short kebab-case name
   (e.g. `001-user-favorites`). If the developer already named one, reuse it.
2. Run: `spectdd check specify --feature <slug>`
3. If it prints GATE CLOSED, show the output to the developer and STOP. Do not
   negotiate, do not proceed, and NEVER run `spectdd approve` yourself.

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

1. Create `specs/<slug>/spec.md` from `.spectdd/templates/spec-template.md`.
2. Content rules:
   - User stories: "As a [role], I want [capability], so that [outcome]".
   - Acceptance criteria in Given/When/Then form — these will become the TDD tests
     later, so make each one concrete, observable and testable.
   - Edge cases, out-of-scope section, and open questions.
   - STRICTLY FUNCTIONAL: no frameworks, no database schemas, no class names.
3. Ask the developer up to 5 numbered clarification questions for anything ambiguous
   BEFORE writing the final version. Mark unresolved items as `[NEEDS CLARIFICATION]`.
4. Do not invent requirements the user did not ask for (no gold plating).
5. Finish with EXACTLY this footer:

```
PHASE COMPLETE: specify (<slug>)
Review specs/<slug>/spec.md. If you agree, run in YOUR terminal:
    spectdd approve specify --feature <slug>
Then invoke /spectdd:plan. I will not proceed until the gate is open.
```

## Phase handoff (after the footer)

End with this tiny block and STOP:

```
Done: <=3 one-line bullets (what this phase produced)
Next (plan): <=2 one-line bullets (what it will do)
Continue? (yes = approve specify & start plan)
```

Then read `approval_mode` in `.spectdd/config.json`:
- "terminal" (default): the gate still requires the developer to run the approve
  command in their own terminal; if they answer yes, remind them of the exact command
  and wait for the gate.
- "chat": if — and ONLY if — the developer's reply is an explicit affirmative
  (yes / si / ok / continue), run `spectdd approve specify --feature <slug> --via chat` yourself
  and start /spectdd:plan immediately. Any other reply: stop, address the
  feedback, ask again. Never self-approve without that explicit yes in this turn.
