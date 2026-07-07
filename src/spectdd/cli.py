"""spectdd — Spec-Driven + Test-Driven Development workflow with human approval gates.

Commands:
    spectdd init --assistant {claude,cursor,copilot,all,none} [--style terse|normal] [--interactive|--no-input]
    spectdd setup [--interactive]                 (re-run the interactive wizard; needs a TTY)
    spectdd approve <phase> [--feature SLUG] [--by NAME]
    spectdd check   <phase> [--feature SLUG]      (for agents; exit 1 = gate closed)
    spectdd revoke  <phase> [--feature SLUG]      (withdraw approval; cascades downstream)
    spectdd status
    spectdd hook    <event>                       (Claude Code hook handlers; JSON on stdin)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path

from spectdd import __version__

PHASES = ["constitution", "specify", "plan", "tasks", "implement", "review"]
COMMANDS = PHASES + ["onboard"]  # onboard: brownfield entry point, not a gated phase
GLOBAL_PHASES = {"constitution"}
# Gate required *before* each phase may start.
REQUIRES = {
    "constitution": [],
    "specify": ["constitution"],
    "plan": ["specify"],
    "tasks": ["plan"],
    "implement": ["tasks"],
    "review": ["implement"],
}
ASSISTANTS = {
    "claude": (Path(".claude/commands/spectdd"), "{phase}.md"),
    "cursor": (Path(".cursor/commands"), "spectdd-{phase}.md"),
    "copilot": (Path(".github/prompts"), "spectdd-{phase}.prompt.md"),
}
STATE_DIR = Path(".spectdd")
ARCHITECT_TRIGGERS = {
    "claude": Path(".claude/skills/spectdd-architect/SKILL.md"),
    "cursor": Path(".cursor/commands/spectdd-architect.md"),
    "copilot": Path(".github/prompts/spectdd-architect.prompt.md"),
}
ARCHITECT_TRIGGER_MD = """---
name: spectdd-architect
description: Architecture interview at project start — asks the programming language, then language-specific architecture questions with ★ recommendations, and records the decisions for spectdd. Use when starting a project or defining the stack/architecture.
---

Read `.spectdd/skills/architect/architect.md` and follow it exactly.
"""
STATE_FILE = STATE_DIR / "state.json"
CONFIG_FILE = STATE_DIR / "config.json"
STYLES = ["terse", "normal", "ultra"]


# ----------------------------------------------------------------- state

def _load_state() -> dict | None:
    if not STATE_FILE.is_file():
        return None
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def _git_user() -> str:
    try:
        out = subprocess.run(["git", "config", "user.name"],
                             capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return "developer"


def _approval(gates: dict | None, phase: str) -> dict | None:
    return (gates or {}).get(phase)


def _prereqs(phase: str) -> list[str]:
    """Every phase that must be approved before `phase`, in workflow order."""
    chain: list[str] = []

    def walk(p: str) -> None:
        for req in REQUIRES[p]:
            walk(req)
            if req not in chain:
                chain.append(req)

    walk(phase)
    return chain


def _missing_prereqs(state: dict, phase: str, feature: str | None) -> list[str]:
    gates = state["features"].get(feature or "", {})
    return [p for p in _prereqs(phase)
            if not (state.get(p) if p in GLOBAL_PHASES else _approval(gates, p))]


# ------------------------------------------------------------- detection

def _detect_project() -> tuple[str, dict] | None:
    """Cheap stack detection from manifest files. Returns (label, wizard defaults)."""
    cwd = Path(".")
    if (cwd / "package.json").is_file():
        pkg = (cwd / "package.json").read_text(encoding="utf-8", errors="ignore").lower()
        tests = "vitest" if "vitest" in pkg else ("jest" if "jest" in pkg else "vitest")
        lint = "biome" if "biome" in pkg else "eslint + prettier"
        return "node", {"runtime": "Node.js LTS (TypeScript)",
                        "test_framework": tests, "lint": lint}
    if (cwd / "go.mod").is_file():
        return "go", {"runtime": "Go", "test_framework": "go test + testify",
                      "lint": "golangci-lint"}
    if (cwd / "pom.xml").is_file() or (cwd / "build.gradle").is_file() \
            or (cwd / "build.gradle.kts").is_file():
        return "java", {"runtime": "Java 21 LTS", "test_framework": "JUnit 5",
                        "lint": "Checkstyle + SpotBugs"}
    if (cwd / "pyproject.toml").is_file() or (cwd / "requirements.txt").is_file():
        return "python", {"runtime": "Python 3.12", "test_framework": "pytest",
                          "lint": "ruff"}
    return None


# ---------------------------------------------------------------- wizard

CONSTITUTION_PATH = STATE_DIR / "memory" / "constitution.md"

class _WizardAborted(Exception):
    """stdin ran out mid-wizard: abort instead of silently accepting defaults."""


def _ask(question: str, default: str = "", strict: bool = False) -> str:
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"  {question}{suffix}: ").strip()
    except EOFError:
        if strict:
            raise _WizardAborted from None
        answer = ""
    return answer or default


def _run_wizard(strict: bool = False) -> dict:
    print("== spectdd interactive setup ==")
    detected = _detect_project()
    d = detected[1] if detected else {}
    if detected:
        print(f"Existing project detected ({detected[0]}) - defaults pre-filled from it. "
              "For a deep analysis run /spectdd:onboard afterwards.")
    print("Answer (or press Enter to accept the default). This fills your constitution.")
    project = {
        "name": _ask("Project name", Path.cwd().name, strict),
        "runtime": _ask("Language / runtime", d.get("runtime", "Python 3.12"), strict),
        "frameworks": _ask("Frameworks allowed", "standard library only", strict),
        "test_framework": _ask("Test framework", d.get("test_framework", "pytest"), strict),
        "lint": _ask("Lint / format tools", d.get("lint", "ruff"), strict),
        "typing": _ask("Typing policy", "type hints required in public functions", strict),
        "deps": _ask("Dependencies policy",
                     "no new dependencies without explicit developer approval", strict),
    }
    style = _ask("Chat output style (terse/normal/ultra)", "terse", strict).lower()
    project["style"] = style if style in STYLES else "terse"
    approval = _ask("Approval mode (terminal = you run approve; chat = your explicit "
                    "'yes' in chat approves)", "terminal", strict).lower()
    project["approval"] = approval if approval in ("terminal", "chat") else "terminal"
    return project


def _write_constitution(p: dict) -> None:
    CONSTITUTION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONSTITUTION_PATH.write_text(f"""# Project Constitution — {p['name']}

> Non-negotiable principles. Every spec, plan, task and line of code must comply.
> Generated by the spectdd setup wizard; refine it with /spectdd:constitution.
> Changes require developer approval (`spectdd approve constitution`).

## 1. Tech stack

- Language / runtime: {p['runtime']}
- Frameworks allowed: {p['frameworks']}
- Dependencies policy: {p['deps']}

## 2. Testing policy (mandatory)

- All production code is developed with **TDD**: a failing test is written, shown
  and approved by the developer BEFORE any implementation code.
- Test framework: {p['test_framework']}
- The agent must NEVER edit, weaken, skip or delete a test to make it pass.
- Minimum test levels required per feature: unit + (integration|e2e as applicable).

## 3. Code quality

- Formatting / linting: {p['lint']}
- Typing: {p['typing']}

## 4. The agent may NOT

- Run `spectdd approve` (developer-only command).
- Start a phase whose gate is closed.
- Commit or push without explicit instruction.

## 5. Definition of Done

- All acceptance criteria have passing tests.
- Full suite green, lint clean.
- Review phase completed: spec compliance PASS, **code audit** clean, and
  **security audit** with zero critical/high findings.
- Honest gap report produced in the review phase.

## 6. Output style

- Chat output style: {p['style']} (see `.spectdd/templates/output-style.md`).
  Artifacts and code always complete.
""", encoding="utf-8")


def _save_project_config(p: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(
        {"output_style": p["style"],
         "approval_mode": p.get("approval", "terminal"),
         "project": {k: v for k, v in p.items() if k not in ("style", "approval")}},
        indent=2, ensure_ascii=False), encoding="utf-8")


# ------------------------------------------------------------------ init

def cmd_init(args: argparse.Namespace) -> int:
    if args.assistant == "none":
        targets = []  # plugin mode: commands + skills come from the Claude Code plugin
        print("  plugin mode: skipped assistant command files (state/templates only)")
    elif args.assistant == "all":
        targets = list(ASSISTANTS)
    else:
        targets = [args.assistant]
    assets = resources.files("spectdd") / "assets"

    for name in targets:
        dest_dir, pattern = ASSISTANTS[name]
        dest_dir.mkdir(parents=True, exist_ok=True)
        for phase in COMMANDS:
            src = assets / "commands" / f"{phase}.md"
            (dest_dir / pattern.format(phase=phase)).write_text(
                src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  installed {name} commands -> {dest_dir}")

    detected = _detect_project()
    if detected:
        print(f"  existing project detected ({detected[0]}) - run /spectdd:onboard "
              "in your assistant to adopt it")
    (STATE_DIR / "memory").mkdir(parents=True, exist_ok=True)

    # Architect skill: shared library + thin per-assistant trigger (lazy loading)
    skill_lib = STATE_DIR / "skills" / "architect"
    skill_lib.mkdir(parents=True, exist_ok=True)
    for doc in (assets / "skills").iterdir():
        if doc.name == "SKILL.md":  # plugin-format trigger; init writes its own
            continue
        (skill_lib / doc.name).write_text(doc.read_text(encoding="utf-8"), encoding="utf-8")
    for name in targets:
        trigger = ARCHITECT_TRIGGERS[name]
        trigger.parent.mkdir(parents=True, exist_ok=True)
        trigger.write_text(ARCHITECT_TRIGGER_MD, encoding="utf-8")
    print(f"  installed architect skill -> {skill_lib} (+ triggers)")
    tpl_dst = STATE_DIR / "templates"
    tpl_dst.mkdir(parents=True, exist_ok=True)
    for tpl in (assets / "templates").iterdir():
        (tpl_dst / tpl.name).write_text(tpl.read_text(encoding="utf-8"), encoding="utf-8")

    if _load_state() is None:
        _save_state({"constitution": None, "features": {}})
        print(f"  created {STATE_FILE}")

    # Config: output style (token-saving) + approval mode. Merge, never clobber.
    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8")) if CONFIG_FILE.is_file() else {}
    if args.style is not None or "output_style" not in cfg:
        cfg["output_style"] = args.style or cfg.get("output_style", "terse")
    if args.approval is not None or "approval_mode" not in cfg:
        cfg["approval_mode"] = args.approval or cfg.get("approval_mode", "terminal")
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  config -> style={cfg['output_style']}, approval={cfg['approval_mode']}")

    run_wizard = args.interactive or (
        sys.stdin.isatty() and not args.no_input and not CONSTITUTION_PATH.is_file())
    if run_wizard:
        project = _run_wizard()
        _write_constitution(project)
        _save_project_config(project)
        print(f"  created {CONSTITUTION_PATH} with your answers")
        print("spectdd ready. Review the constitution with /spectdd:constitution, "
              "then approve it: spectdd approve constitution")
    else:
        print("spectdd ready. Start with the spectdd-architect skill (architecture interview), then /spectdd:constitution.")
    return 0


# --------------------------------------------------------------- approve

def cmd_approve(args: argparse.Namespace) -> int:
    state = _load_state()
    if state is None:
        print("No .spectdd/state.json found. Run `spectdd init` first.")
        return 1
    phase, feature = args.phase, args.feature
    if phase not in GLOBAL_PHASES and not feature:
        print(f"Phase '{phase}' is per-feature: use --feature <slug>.")
        return 2
    if feature and not (Path("specs") / feature).is_dir():
        print(f"WARNING: specs/{feature}/ does not exist yet. "
              "Check the slug for typos before relying on this approval.")
    skipped = _missing_prereqs(state, phase, feature)
    if skipped:
        print(f"WARNING: approving '{phase}' while earlier gates are still pending: "
              + ", ".join(skipped)
              + ". The workflow expects phases to be approved in order.")
    entry = {"approved_by": args.by or _git_user(),
             "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "via": getattr(args, "via", None) or "terminal"}
    if phase in GLOBAL_PHASES:
        state[phase] = entry
    else:
        state["features"].setdefault(feature, {})[phase] = entry
    _save_state(state)
    scope = feature or "project"
    print(f"APPROVED  {phase} ({scope}) by {entry['approved_by']} at {entry['at']}")
    return 0


# ----------------------------------------------------------------- check

def cmd_check(args: argparse.Namespace) -> int:
    state = _load_state()
    if state is None:
        print("GATE CLOSED: no .spectdd/state.json. Run `spectdd init` first.")
        return 1
    phase, feature = args.phase, args.feature
    if phase not in GLOBAL_PHASES and not feature:
        print(f"Phase '{phase}' is per-feature: use --feature <slug>.")
        return 2
    missing = _missing_prereqs(state, phase, feature)
    if missing:
        print(f"GATE CLOSED for '{phase}': developer approval missing for: "
              + ", ".join(missing))
        print("The DEVELOPER must run in their own terminal:")
        for m in missing:
            flag = "" if m in GLOBAL_PHASES else f" --feature {feature}"
            print(f"    spectdd approve {m}{flag}")
        return 1
    print(f"GATE OPEN: '{phase}' may start.")
    return 0


# ---------------------------------------------------------------- status

def cmd_status(args: argparse.Namespace) -> int:
    state = _load_state()
    if state is None:
        print("No .spectdd/state.json found. Run `spectdd init` first.")
        return 1

    def fmt(entry):
        return f"approved by {entry['approved_by']} ({entry['at']})" if entry else "PENDING"

    style = "terse"
    if CONFIG_FILE.is_file():
        style = json.loads(CONFIG_FILE.read_text(encoding="utf-8")).get("output_style", "terse")
    print("== spectdd status ==")
    print(f"output style : {style}")
    print(f"constitution : {fmt(state.get('constitution'))}")
    if not state["features"]:
        print("(no features yet)")
    for slug, gates in state["features"].items():
        print(f"feature {slug}:")
        for phase in PHASES:
            if phase in GLOBAL_PHASES:
                continue
            print(f"    {phase:<10}: {fmt(gates.get(phase))}")
    return 0


# ----------------------------------------------------------------- setup

def cmd_setup(args: argparse.Namespace) -> int:
    """(Re)run the interactive wizard that fills the constitution."""
    strict = not args.interactive
    if strict and not sys.stdin.isatty():
        print("spectdd setup is interactive and stdin is not a TTY. "
              "Run it from a terminal, or force it with --interactive.")
        return 1
    try:
        if CONSTITUTION_PATH.is_file():
            answer = _ask("Constitution already exists. Overwrite? (y/N)", "n", strict).lower()
            if answer not in ("y", "yes", "s", "si", "sí"):
                print("Keeping the existing constitution.")
                return 0
        project = _run_wizard(strict=strict)
    except _WizardAborted:
        print("stdin closed before the wizard finished - nothing was written. "
              "Run setup from a terminal, or force defaults with --interactive.")
        return 1
    _write_constitution(project)
    _save_project_config(project)
    print(f"Wrote {CONSTITUTION_PATH}. Review it and run: spectdd approve constitution")
    return 0


# ---------------------------------------------------------------- revoke

def cmd_revoke(args: argparse.Namespace) -> int:
    """Withdraw an approval (e.g. after the reviewed artifact changed).

    Revoking a feature phase also clears every downstream phase of that feature,
    forcing the workflow to re-run through the gates from that point on.
    """
    state = _load_state()
    if state is None:
        print("No .spectdd/state.json found. Run `spectdd init` first.")
        return 1
    phase, feature = args.phase, args.feature
    if phase not in GLOBAL_PHASES and not feature:
        print(f"Phase '{phase}' is per-feature: use --feature <slug>.")
        return 2
    if phase in GLOBAL_PHASES:
        state[phase] = None
        _save_state(state)
        print(f"REVOKED  {phase} (project). All phases now gate-closed until "
              "the constitution is re-approved. Feature approvals were kept; "
              "re-review them if the constitution change affects them.")
        return 0
    gates = state["features"].get(feature, {})
    cascade = PHASES[PHASES.index(phase):]
    removed = [p for p in cascade if gates.pop(p, None) is not None]
    _save_state(state)
    print(f"REVOKED  {', '.join(removed) or phase} ({feature}). "
          "Downstream gates are closed again.")
    return 0


# ----------------------------------------------------------------- hooks
#
# Claude Code hook handlers (installed by the spectdd plugin, hooks/hooks.json).
# Each reads the hook JSON payload on stdin. Exit 2 = block the tool call
# (stderr is fed back to the agent); exit 0 = allow. session-start prints a
# compact gate status to stdout (added to the agent's context).

_RE_APPROVE = re.compile(r"\bspectdd\b[^|&;\n]*\bapprove\b")
_RE_MODE_BYPASS = re.compile(r"\bspectdd\b[^|&;\n]*\binit\b[^|&;\n]*--approval[ =]+chat")
_RE_STATE_FILE = re.compile(r"\.spectdd[\\/](state|config)\.json")
_RE_WRITEISH = re.compile(
    r"(>>?|\btee\b|\bsed\b[^|&;\n]*\s-i|\brm\b|\bmv\b|\bcp\b|\bdel\b"
    r"|Set-Content|Out-File|Add-Content|Remove-Item)", re.IGNORECASE)


def _hook_payload() -> dict:
    try:
        data = json.load(sys.stdin)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _hook_bash_guard(payload: dict) -> int:
    cmd = str((payload.get("tool_input") or {}).get("command") or "")
    if _RE_APPROVE.search(cmd):
        cfg_file = Path(payload.get("cwd") or ".") / CONFIG_FILE
        try:
            cfg = json.loads(cfg_file.read_text(encoding="utf-8")) if cfg_file.is_file() else {}
        except Exception:
            cfg = {}
        if cfg.get("approval_mode") == "chat" and "--via chat" in cmd:
            return 0
        print("BLOCKED by spectdd: `spectdd approve` is developer-only. Ask the "
              "developer to run it in their own terminal and wait for the gate.",
              file=sys.stderr)
        return 2
    if _RE_MODE_BYPASS.search(cmd):
        print("BLOCKED by spectdd: switching approval_mode is a developer decision.",
              file=sys.stderr)
        return 2
    if _RE_STATE_FILE.search(cmd) and _RE_WRITEISH.search(cmd):
        print("BLOCKED by spectdd: .spectdd/state.json and config.json are "
              "developer-managed; gates change only through the spectdd CLI.",
              file=sys.stderr)
        return 2
    return 0


def _hook_file_guard(payload: dict) -> int:
    fp = str((payload.get("tool_input") or {}).get("file_path") or "").replace("\\", "/")
    if re.search(r"\.spectdd/(state|config)\.json$", fp):
        print("BLOCKED by spectdd: this file is developer-managed; gates change "
              "only through the spectdd CLI.", file=sys.stderr)
        return 2
    return 0


def _hook_session_start(payload: dict) -> int:
    state_file = Path(payload.get("cwd") or ".") / STATE_FILE
    if not state_file.is_file():
        return 0  # not a spectdd project: stay silent, zero context cost
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        return 0

    def mark(entry) -> str:
        return "OK" if entry else "-"

    parts = [f"constitution={mark(state.get('constitution'))}"]
    for slug, gates in (state.get("features") or {}).items():
        seq = " ".join(f"{ph}={mark(gates.get(ph))}"
                       for ph in PHASES if ph not in GLOBAL_PHASES)
        parts.append(f"{slug}: {seq}")
    print("[spectdd] gates: " + " | ".join(parts))
    print("[spectdd] Gated SDD+TDD project. Before starting a phase run "
          "`spectdd check <phase> --feature <slug>`; `spectdd approve` is developer-only.")
    return 0


def cmd_hook(args: argparse.Namespace) -> int:
    payload = _hook_payload()
    if args.event == "bash-guard":
        return _hook_bash_guard(payload)
    if args.event == "file-guard":
        return _hook_file_guard(payload)
    return _hook_session_start(payload)


# ------------------------------------------------------------------ main

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="spectdd",
        description="spectdd: Spec-Driven + Test-Driven Development with human approval gates.")
    p.add_argument("--version", action="version", version=f"spectdd {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="install slash commands and templates into this repo")
    p_init.add_argument("--assistant", choices=[*ASSISTANTS, "all", "none"], default="all",
                        help="'none' = state and templates only (Claude Code plugin provides commands/skills)")
    p_init.add_argument("--style", choices=STYLES, default=None,
                        help="chat output style: terse (token-saving, default), normal, or ultra (max compression)")
    p_init.add_argument("--approval", choices=["terminal", "chat"], default=None,
                        help="terminal (default): you run approve yourself; chat: your explicit yes in chat approves")
    p_init.add_argument("--interactive", action="store_true",
                        help="force the setup wizard even without a TTY")
    p_init.add_argument("--no-input", action="store_true",
                        help="never prompt (CI mode)")
    p_init.set_defaults(func=cmd_init)

    p_setup = sub.add_parser("setup", help="(re)run the interactive wizard that fills the constitution")
    p_setup.add_argument("--interactive", action="store_true",
                         help="run the wizard even when stdin is not a TTY")
    p_setup.set_defaults(func=cmd_setup)

    p_appr = sub.add_parser("approve", help="record the developer's approval of a phase (humans only)")
    p_appr.add_argument("phase", choices=PHASES)
    p_appr.add_argument("--feature", help="feature slug, e.g. 001-favorites")
    p_appr.add_argument("--by", help="approver name (defaults to git user.name)")
    p_appr.add_argument("--via", choices=["terminal", "chat"], default="terminal",
                        help="how the approval was given (chat = explicit yes to the handoff question)")
    p_appr.set_defaults(func=cmd_approve)

    p_chk = sub.add_parser("check", help="verify that a phase's gates are open (used by agents)")
    p_chk.add_argument("phase", choices=PHASES)
    p_chk.add_argument("--feature")
    p_chk.set_defaults(func=cmd_check)

    p_rev = sub.add_parser("revoke", help="withdraw an approval after changes (cascades downstream)")
    p_rev.add_argument("phase", choices=PHASES)
    p_rev.add_argument("--feature")
    p_rev.set_defaults(func=cmd_revoke)

    p_st = sub.add_parser("status", help="show approval state of all phases")
    p_st.set_defaults(func=cmd_status)

    p_hook = sub.add_parser("hook", help="Claude Code hook handlers (read the hook JSON on stdin)")
    p_hook.add_argument("event", choices=["bash-guard", "file-guard", "session-start"])
    p_hook.set_defaults(func=cmd_hook)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
