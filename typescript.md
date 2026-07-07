---
description: "spectdd phase 5 — final review: spec compliance + built-in code audit + built-in security audit"
---

# spectdd: review

Phase 5 (final) of the spectdd workflow. Input from developer: $ARGUMENTS

## Gate check (mandatory, do this FIRST)

1. Identify the feature slug.
2. Run: `spectdd check review --feature <slug>`
3. If GATE CLOSED: show the output and STOP. Never run `spectdd approve` yourself.

## Output style

Read `.spectdd/config.json`. If `output_style` is `terse` (default) or `ultra`, apply
`.spectdd/templates/output-style.md`: telegraphic chat replies, zero filler.
The audit reports below stay complete and exact.
Token economy (all levels, `ultra` = max compression): never repeat content that lives in another artifact — reference it (e.g. "covers AC-2.1"); keep artifacts proportional to the problem; trim tool output shown in chat to the relevant lines.

Act as an independent, skeptical reviewer. Three audits, in order. These audits are
built into spectdd — do not rely on any external plugin or command.

## Audit 1 — Spec compliance

For every acceptance criterion in `specs/<slug>/spec.md`, verify there is a passing
test that genuinely exercises it (not a tautology). Produce a traceability table:
criterion -> test -> status.

## Audit 2 — Code audit

Review the full diff of the feature for:
- Correctness: logic errors, off-by-one, race conditions, unhandled edge cases.
- Error handling: swallowed exceptions, missing failure paths, unclear messages.
- Performance: N+1 queries, unnecessary loops/allocations, unbounded growth.
- Design: duplication, dead code, needless complexity, constitution violations
  (style, typing, layout, naming).
- Test quality: FIRST principles, behavior-not-implementation, meaningful failures.

## Audit 3 — Security audit

Check the diff line by line for, at minimum:
- **Input validation** missing on any external input (user, file, network, env).
- **Injection**: SQL/NoSQL (non-parameterized queries), OS command, XSS, template,
  path traversal, unsafe deserialization, SSRF.
- **Authentication / authorization**: endpoints or operations reachable without the
  proper checks; privilege escalation; insecure session handling.
- **Secrets**: credentials, tokens or keys in code, config, logs or test fixtures.
- **Sensitive data exposure**: PII in logs, verbose error messages leaking internals.
- **Dependencies**: new packages added — are they necessary, maintained, and allowed
  by the constitution?
- Resolve every `SECURITY-NOTE` comment left during the implement phase.

Rate each finding: **critical | high | medium | low**. Findings rated critical or
high BLOCK the merge: report them and propose fixes (do not apply them; fixes go
through a new TDD micro-cycle with developer-approved tests).

## Honest gap report

List anything NOT implemented, deviations from spec/plan, and known limitations.
An empty gap report is suspicious — look harder.

## Footer

Finish with EXACTLY:

```
PHASE COMPLETE: review (<slug>)
Audits: spec compliance [PASS|FAIL], code audit [n findings], security audit [n findings, worst: <severity>].
Merge is blocked while critical/high security findings remain open.
Suggested next step: open a Pull Request including specs/<slug>/ for reviewers.
```
