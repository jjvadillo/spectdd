# Contributing to spectdd

Thanks for stopping by! This project eats its own dog food, so contributions follow
the spectdd philosophy: **spec first, test first, human review always.**

## How to contribute

1. **Open an issue before a PR.** Describe the problem as a mini-spec: what happens,
   what you expected, acceptance criteria if it's a feature. Small specs welcome.
2. **TDD is mandatory.** Every code change needs a failing test written first.
   PRs without tests for new behavior will be asked to add them.
3. Run the suite before pushing: `pip install -e ".[dev]" && pytest` (all green).
4. Keep artifacts proportional: small fix → small PR. No drive-by refactors.

## Good first issues

Look for the `good first issue` label. Typical starters:
- Add a language question bank to the architect skill (e.g. `rust.md`, `csharp.md`).
- Improve stack detection in `_detect_project()` (more manifests, better defaults).
- Translate command prompts or README sections.

## Project layout

- `src/spectdd/cli.py` — the whole CLI (gates, wizard, detection).
- `src/spectdd/assets/commands/` — the 7 phase prompts installed into assistants.
- `src/spectdd/assets/skills/` — architect interview + language question banks.
- `src/spectdd/assets/templates/` — document templates copied to `.spectdd/`.
- `tests/test_cli.py` — 58 tests, written before the code they verify.

## Code style

Python 3.10+, stdlib only (no runtime dependencies — keep it that way), type hints
in public functions.

MIT licensed: by contributing you agree your work is released under the same license.
