# Changelog

## 0.9.1
- `spectdd check` now validates the **full upstream chain**, not just the
  immediately preceding phase: approving `tasks` while `plan` is pending no
  longer opens the `implement` gate.
- `spectdd approve` warns when earlier gates are still pending (the human can
  still approve out of order, but never silently).
- `spectdd setup` refuses to run without a TTY instead of silently writing a
  default constitution; use `--interactive` to force it (e.g. in scripts/tests).
- New `spectdd --version` flag.
- Console messages are ASCII-safe (no more mojibake on Windows consoles).

## 0.9.0
- **Brownfield onboarding**: new `/spectdd:onboard` command — analyzes an existing
  codebase (manifests fully, source sampled) and generates constitution +
  architecture.md + gap report, marking uncertainties `[ASSUMED]`.
- `spectdd init` auto-detects the stack (package.json, pyproject.toml, go.mod,
  pom.xml, build.gradle) and pre-fills the wizard.

## 0.8.0
- **Phase handoff**: every phase ends with Done (≤3 bullets) + Next (≤2) + "Continue?".
- **Chat approval mode** (`--approval chat`): an explicit "yes" to the handoff
  authorizes the agent to run the approve for you, audited as `via: chat`.

## 0.7.0
- **spectdd-architect skill**: language question first, then language-specific
  architecture interview with ★ recommendations. Progressive disclosure: only the
  chosen language's question bank enters the context window.

## 0.6.0
- **Output minimization**: file-first rule (no echoing documents into chat),
  one-line compact footers, failure traces trimmed to the failing assertion.
  ~65-70% less LLM output vs verbose baseline in simulations.

## 0.5.0
- `ultra` compression level; token-economy rules in every phase prompt.

## 0.4.0
- Interactive setup wizard on first `init`; `spectdd setup` to re-run it.

## 0.3.0
- `spectdd revoke` with downstream cascade; `.spectdd/memory/` created by init;
  typo warning on approving unknown features; status shows output style.

## 0.2.0
- Native terse output style; built-in code audit and security audit in review;
  `SECURITY-NOTE` markers during implement.

## 0.1.0
- Initial release: gated SDD+TDD workflow (constitution → specify → plan → tasks →
  implement → review) with human-only approvals enforced by CLI exit codes.
  Installers for Claude Code, Cursor and GitHub Copilot.
