---
description: "spectdd phase 4 — TDD implementation loop (red-green-refactor per task, developer approves every red test)"
---

# spectdd: implement

Phase 4 of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug.
2. Run: `spectdd check implement --feature <slug>`
3. If GATE CLOSED: show the output and STOP. Never run `spectdd approve` yourself.

## Output style

Read `.spectdd/config.json`. If `output_style` is `terse` (default) or `ultra`, apply
`.spectdd/templates/output-style.md`: telegraphic chat replies, zero filler.
Code, tests, diffs, real test output and phase footers stay complete and exact.
Token economy (all levels, `ultra` = max compression): never repeat content that lives in another artifact — reference it (e.g. "covers AC-2.1"); keep artifacts proportional to the problem; trim tool output shown in chat to the relevant lines.
File-first: NEVER print in chat a document you just wrote to a file — give the path
plus an outline of at most 5 lines (10 in `normal` style); the developer reads the file.
Compact footer: in `terse`/`ultra`, replace the phase footer with ONE line with the
same data: `DONE <phase>(<slug>) | review <path> | approve: spectdd approve <phase>
--feature <slug> | next: /spectdd:<next>`

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
Done: <=3 one-line bullets (what this phase produced)
Next (review): <=2 one-line bullets (what it will do)
Continue? (yes = approve implement & start review)
```

Then read `approval_mode` in `.spectdd/config.json`:
- "terminal" (default): the gate still requires the developer to run the approve
  command in their own terminal; if they answer yes, remind them of the exact command
  and wait for the gate.
- "chat": if — and ONLY if — the developer's reply is an explicit affirmative
  (yes / si / ok / continue), run `spectdd approve implement --feature <slug> --via chat` yourself
  and start /spectdd:review immediately. Any other reply: stop, address the
  feedback, ask again. Never self-approve without that explicit yes in this turn.
