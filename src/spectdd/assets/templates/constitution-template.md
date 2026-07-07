# Project Constitution

> Non-negotiable principles. Every spec, plan, task and line of code must comply.
> Changes to this file require developer approval (`spectdd approve constitution`).

## 1. Tech stack

- Language / runtime:
- Frameworks allowed:
- Dependencies policy: (e.g. "no new dependencies without explicit developer approval")

## 2. Testing policy (mandatory)

- All production code is developed with **TDD**: a failing test is written, shown
  and approved by the developer BEFORE any implementation code.
- Test framework:
- The agent must NEVER edit, weaken, skip or delete a test to make it pass.
- Minimum test levels required per feature: unit + (integration|e2e as applicable).

## 3. Code quality

- Formatting / linting:
- Typing:
- Naming conventions:
- Project layout:

## 4. The agent may NOT

- Run `spectdd approve` (developer-only command).
- Start a phase whose gate is closed.
- Commit or push without explicit instruction.
- (add project-specific prohibitions)

## 5. Definition of Done

- All acceptance criteria have passing tests.
- Full suite green, lint clean.
- Review phase completed: spec compliance PASS, **code audit** clean, and
  **security audit** with zero critical/high findings (both audits are built
  into the /spectdd:review command).
- Honest gap report produced in the review phase.

## 6. Output style

- Chat output style: terse (see `.spectdd/templates/output-style.md`) unless
  `.spectdd/config.json` says otherwise. Artifacts and code always complete.
