---
description: "spectdd phase 4 — TDD implementation loop (red-green-refactor per task, developer approves every red test)"
---

# spectdd: implement

Phase 4 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug.
2. Run: `spectdd check implement --feature <slug>`
3. If GATE CLOSED: show the output and STOP. Never run `spectdd approve` yourself.

## Output style & token economy

Apply `.spectdd/templates/output-style.md` at the level set in `.spectdd/config.json`
(`terse` default | `normal` | `ultra` = max compression). Non-negotiables: file-first,
compact footer (one line in terse/ultra), telegraphic replies; code, tests, diffs,
real test output and phase footers stay complete and exact.

## The TDD loop — repeat for EACH task in specs/<slug>/tasks.md, in order

### RED
1. Write ONLY the failing test(s) declared for the task. No production code yet.
2. Run the test suite and show the failure: only the failing assertion line(s) and
   the summary line (real output, never fabricated; no full tracebacks in chat).
3. **STOP. Present the test code to the developer and ask: "Do you approve these
   tests?"** Wait for an explicit yes before continuing. The developer owns the
   specification and the tests; you own the implementation.

### GREEN
4. Write the MINIMUM production code to make the failing test pass, applying
   secure-coding basics: validate and sanitize all external inputs, parameterized
   queries only, no secrets/credentials in code or logs, least-privilege access.
   Flag any security-sensitive surface (auth, file paths, network, deserialization)
   with a `SECURITY-NOTE` comment for the review phase audit.
5. Run the FULL suite. If anything fails, fix the production code — **you must NEVER
   edit, weaken, skip or delete a test to make it pass**. If you believe a test is
   wrong, stop and tell the developer why.

### REFACTOR
6. With the suite green: remove duplication, improve names, honor the constitution's
   quality rules. Run the suite again. Show a compact summary of the task's diff.
7. Mark the task `[X]` in tasks.md and move to the next task.

## Completion

Only when ALL tasks are done and the full suite is green:
1. Run lint/type checks required by the constitution.
2. Produce the final summary: files changed, tests added (count), coverage of each
   acceptance criterion (spec traceability table), and the list of `SECURITY-NOTE`
   markers left for the review phase.
3. Finish with EXACTLY this footer:

```
PHASE COMPLETE: implement (<slug>)
All tasks done, full test suite green. Review the diff. If you agree, run in YOUR terminal:
    spectdd approve implement --feature <slug>
Then invoke /spectdd:review for the final quality pass.
```

## Phase handoff (after the footer)

End with this tiny block and STOP:

```
Done: <=3 one-line bullets | Next (review): <=2
Continue? (yes = approve implement & start review)
```

`approval_mode` in `.spectdd/config.json`: "terminal" (default) = the developer runs
the approve command themselves; remind them and wait for the gate. "chat" = ONLY an
explicit yes (yes/si/ok) to this question lets you run
`spectdd approve implement --feature <slug> --via chat` and start /spectdd:review;
anything else: stop and address the feedback. Never self-approve without that explicit yes.
