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

## Output style & token economy

Apply `.spectdd/templates/output-style.md` at the level set in `.spectdd/config.json`
(`terse` default | `normal` | `ultra` = max compression). Non-negotiables: file-first
(never echo into chat a document just written to a file), compact footer (one line in
terse/ultra), telegraphic replies; artifacts and phase footers stay complete and exact.

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
Done: <=3 one-line bullets | Next (plan): <=2
Continue? (yes = approve specify & start plan)
```

`approval_mode` in `.spectdd/config.json`: "terminal" (default) = the developer runs
the approve command themselves; remind them and wait for the gate. "chat" = ONLY an
explicit yes (yes/si/ok) to this question lets you run
`spectdd approve specify --feature <slug> --via chat` and start /spectdd:plan;
anything else: stop and address the feedback. Never self-approve without that explicit yes.
