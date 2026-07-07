---
name: spectdd-workflow
description: Gated SDD+TDD workflow rules for projects using spectdd (a .spectdd/ directory exists in the repo). Use when starting feature work, writing specs/plans/tasks, implementing code, or whenever a spectdd gate, phase or approval is mentioned.
---

This project uses spectdd. Never bypass it:

1. New feature or change request -> `/spectdd:specify`, then plan -> tasks -> implement -> review, strictly in order.
2. Before starting any phase run `spectdd check <phase> --feature <slug>`; if GATE CLOSED, show the developer the approve command and STOP.
3. `spectdd approve` is developer-only. Sole exception: `approval_mode` is "chat" in `.spectdd/config.json` AND the developer just answered the handoff question with an explicit yes — then run it with `--via chat`.
4. Never edit `.spectdd/state.json` or `.spectdd/config.json` directly.
5. Existing codebase without a constitution -> `/spectdd:onboard` first. Brand-new project -> `spectdd-architect` skill, then `/spectdd:constitution`.
6. Token economy: apply `.spectdd/templates/output-style.md` (file-first, compact footers).
