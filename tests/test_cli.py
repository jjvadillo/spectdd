"""Tests for the spectdd CLI — written first, TDD style."""
import json
import os
import subprocess
import sys

import pytest

from spectdd import cli


@pytest.fixture()
def repo(tmp_path, monkeypatch):
    """An empty project directory acting as the user's repo."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


# ---------------------------------------------------------------- init

def test_init_claude_creates_slash_commands(repo):
    rc = cli.main(["init", "--assistant", "claude"])
    assert rc == 0
    cmds = repo / ".claude" / "commands" / "spectdd"
    assert (cmds / "specify.md").is_file()
    assert (cmds / "implement.md").is_file()
    assert len(list(cmds.glob("*.md"))) == 7  # six phases + onboard


def test_init_copilot_uses_prompt_extension(repo):
    cli.main(["init", "--assistant", "copilot"])
    prompts = repo / ".github" / "prompts"
    assert (prompts / "spectdd-specify.prompt.md").is_file()


def test_init_all_installs_every_assistant(repo):
    cli.main(["init", "--assistant", "all"])
    assert (repo / ".claude" / "commands" / "spectdd" / "plan.md").is_file()
    assert (repo / ".cursor" / "commands" / "spectdd-plan.md").is_file()
    assert (repo / ".github" / "prompts" / "spectdd-plan.prompt.md").is_file()


def test_init_creates_state_and_templates(repo):
    cli.main(["init", "--assistant", "claude"])
    assert (repo / ".spectdd" / "state.json").is_file()
    assert (repo / ".spectdd" / "templates" / "spec-template.md").is_file()
    state = json.loads((repo / ".spectdd" / "state.json").read_text())
    assert state == {"constitution": None, "features": {}}


def test_init_is_idempotent_and_keeps_state(repo):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    cli.main(["init", "--assistant", "claude"])  # re-run must not wipe approvals
    state = json.loads((repo / ".spectdd" / "state.json").read_text())
    assert state["constitution"]["approved_by"] == "dev"


# ------------------------------------------------------------- approve

def test_approve_constitution_records_signature(repo):
    cli.main(["init", "--assistant", "claude"])
    rc = cli.main(["approve", "constitution", "--by", "javier"])
    assert rc == 0
    state = json.loads((repo / ".spectdd" / "state.json").read_text())
    assert state["constitution"]["approved_by"] == "javier"
    assert "at" in state["constitution"]


def test_approve_feature_phase(repo):
    cli.main(["init", "--assistant", "claude"])
    rc = cli.main(["approve", "specify", "--feature", "001-favs", "--by", "javier"])
    assert rc == 0
    state = json.loads((repo / ".spectdd" / "state.json").read_text())
    assert state["features"]["001-favs"]["specify"]["approved_by"] == "javier"


def test_approve_rejects_unknown_phase(repo):
    cli.main(["init", "--assistant", "claude"])
    with pytest.raises(SystemExit):
        cli.main(["approve", "nonsense"])


def test_feature_phase_requires_feature_flag(repo):
    cli.main(["init", "--assistant", "claude"])
    rc = cli.main(["approve", "plan"])  # missing --feature
    assert rc == 2


# --------------------------------------------------------------- check

def test_check_fails_when_gate_not_approved(repo):
    cli.main(["init", "--assistant", "claude"])
    rc = cli.main(["check", "specify", "--feature", "001-favs"])
    assert rc == 1


def test_check_passes_when_previous_gates_approved(repo):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    assert cli.main(["check", "specify", "--feature", "001-favs"]) == 0
    assert cli.main(["check", "plan", "--feature", "001-favs"]) == 1
    cli.main(["approve", "specify", "--feature", "001-favs", "--by", "dev"])
    assert cli.main(["check", "plan", "--feature", "001-favs"]) == 0


def test_full_gate_chain_for_implement(repo):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    for phase in ("specify", "plan", "tasks"):
        cli.main(["approve", phase, "--feature", "001-x", "--by", "dev"])
    assert cli.main(["check", "implement", "--feature", "001-x"]) == 0
    assert cli.main(["check", "review", "--feature", "001-x"]) == 1


# -------------------------------------------------------------- status

def test_status_lists_features_and_gates(repo, capsys):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    cli.main(["approve", "specify", "--feature", "001-favs", "--by", "dev"])
    cli.main(["status"])
    out = capsys.readouterr().out
    assert "constitution" in out and "001-favs" in out
    assert "specify" in out


def test_check_without_init_explains_problem(repo, capsys):
    rc = cli.main(["check", "specify", "--feature", "x"])
    assert rc == 1
    assert "spectdd init" in capsys.readouterr().out


# -------------------------------------------------- integrations (v0.2)

def _asset(phase):
    from importlib import resources
    return (resources.files("spectdd") / "assets" / "commands" / f"{phase}.md").read_text(encoding="utf-8")


def test_every_command_defines_terse_output_style():
    # Native token-saving style (no external skill needed)
    for phase in ("constitution", "specify", "plan", "tasks", "implement", "review"):
        text = _asset(phase).lower()
        assert "output style" in text, f"{phase}.md lacks output style section"
        assert "terse" in text


def test_review_phase_has_native_code_and_security_audits():
    text = _asset("review").lower()
    assert "code audit" in text
    assert "security audit" in text
    for marker in ("injection", "secrets", "authorization", "input validation"):
        assert marker in text, f"security audit missing: {marker}"
    assert "critical" in text and "high" in text  # severity ratings


def test_implement_requires_secure_coding_per_task():
    text = _asset("implement").lower()
    assert "security" in text and "validate" in text


def test_constitution_template_dod_includes_audits_and_style():
    from importlib import resources
    tpl = (resources.files("spectdd") / "assets" / "templates" /
           "constitution-template.md").read_text(encoding="utf-8").lower()
    assert "code audit" in tpl and "security audit" in tpl
    assert "output style" in tpl


def test_init_writes_config_with_terse_default(repo):
    cli.main(["init", "--assistant", "claude"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text())
    assert cfg["output_style"] == "terse"


def test_init_style_flag_overrides(repo):
    cli.main(["init", "--assistant", "claude", "--style", "normal"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text())
    assert cfg["output_style"] == "normal"


def test_init_installs_output_style_reference(repo):
    cli.main(["init", "--assistant", "claude"])
    assert (repo / ".spectdd" / "templates" / "output-style.md").is_file()


# ------------------------------------------------------------ smoke CLI

def test_entrypoint_runs_as_module(repo):
    r = subprocess.run(
        [sys.executable, "-m", "spectdd", "--help"],
        capture_output=True, text=True, env={**os.environ},
    )
    assert r.returncode == 0
    assert "spectdd" in r.stdout.lower()


# -------------------------------------------------- e2e fixes (v0.3)

def test_init_creates_memory_dir(repo):
    cli.main(["init", "--assistant", "claude"])
    assert (repo / ".spectdd" / "memory").is_dir()


def test_status_shows_output_style(repo, capsys):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["status"])
    assert "terse" in capsys.readouterr().out


def test_approve_warns_when_feature_folder_missing(repo, capsys):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    rc = cli.main(["approve", "specify", "--feature", "999-typo", "--by", "dev"])
    assert rc == 0  # warning, not error
    assert "warning" in capsys.readouterr().out.lower()


def test_revoke_clears_phase_and_downstream(repo):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    for phase in ("specify", "plan", "tasks"):
        cli.main(["approve", phase, "--feature", "001-x", "--by", "dev"])
    rc = cli.main(["revoke", "plan", "--feature", "001-x"])
    assert rc == 0
    state = json.loads((repo / ".spectdd" / "state.json").read_text())
    gates = state["features"]["001-x"]
    assert "specify" in gates          # upstream intact
    assert "plan" not in gates         # revoked
    assert "tasks" not in gates        # downstream cascaded
    assert cli.main(["check", "tasks", "--feature", "001-x"]) == 1


def test_revoke_constitution(repo):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    assert cli.main(["revoke", "constitution"]) == 0
    assert cli.main(["check", "specify", "--feature", "001-x"]) == 1


# ---------------------------------------------- interactive setup (v0.4)

def _feed(monkeypatch, answers):
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def test_init_interactive_creates_filled_constitution(repo, monkeypatch):
    _feed(monkeypatch, ["MiApp", "Python 3.12", "FastAPI", "pytest",
                        "ruff + black", "estricto", "solo con aprobación", "terse", ""])
    rc = cli.main(["init", "--assistant", "claude", "--interactive"])
    assert rc == 0
    c = (repo / ".spectdd" / "memory" / "constitution.md").read_text(encoding="utf-8")
    for value in ("MiApp", "FastAPI", "pytest", "ruff + black"):
        assert value in c
    # los datos quedan también en config.json
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["project"]["name"] == "MiApp"


def test_init_wizard_empty_answers_use_defaults(repo, monkeypatch):
    _feed(monkeypatch, [""] * 9)
    cli.main(["init", "--assistant", "claude", "--interactive"])
    c = (repo / ".spectdd" / "memory" / "constitution.md").read_text(encoding="utf-8")
    assert "pytest" in c                      # default test framework
    assert repo.name in c                     # default project name = cwd


def test_init_wizard_can_set_normal_style(repo, monkeypatch):
    _feed(monkeypatch, ["", "", "", "", "", "", "", "normal", ""])
    cli.main(["init", "--assistant", "claude", "--interactive"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["output_style"] == "normal"


def test_init_non_tty_does_not_prompt(repo, monkeypatch):
    def boom(prompt=""):
        raise AssertionError("wizard must not prompt in non-interactive mode")
    monkeypatch.setattr("builtins.input", boom)
    rc = cli.main(["init", "--assistant", "claude"])  # stdin is not a tty in tests
    assert rc == 0
    assert not (repo / ".spectdd" / "memory" / "constitution.md").exists()


def test_setup_command_runs_wizard_later(repo, monkeypatch):
    cli.main(["init", "--assistant", "claude"])
    _feed(monkeypatch, ["OtraApp", "", "", "", "", "", "", "", ""])
    rc = cli.main(["setup", "--interactive"])
    assert rc == 0
    c = (repo / ".spectdd" / "memory" / "constitution.md").read_text(encoding="utf-8")
    assert "OtraApp" in c


def test_setup_asks_before_overwriting(repo, monkeypatch):
    cli.main(["init", "--assistant", "claude"])
    _feed(monkeypatch, ["App1", "", "", "", "", "", "", "", ""])
    cli.main(["setup", "--interactive"])
    _feed(monkeypatch, ["n"])                 # rechazar sobrescritura
    rc = cli.main(["setup", "--interactive"])
    assert rc == 0
    c = (repo / ".spectdd" / "memory" / "constitution.md").read_text(encoding="utf-8")
    assert "App1" in c                        # sigue intacta


# ---------------------------------------------- token efficiency (v0.5)

def test_ultra_style_supported(repo):
    cli.main(["init", "--assistant", "claude", "--style", "ultra"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["output_style"] == "ultra"


def test_wizard_accepts_ultra(repo, monkeypatch):
    _feed(monkeypatch, ["", "", "", "", "", "", "", "ultra", ""])
    cli.main(["init", "--assistant", "claude", "--interactive"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["output_style"] == "ultra"


def test_every_command_includes_token_economy_rules():
    for phase in ("constitution", "specify", "plan", "tasks", "implement", "review"):
        text = _asset(phase).lower()
        assert "token economy" in text, f"{phase}.md lacks token economy rules"
        assert "ultra" in text


def test_output_style_reference_documents_all_levels():
    from importlib import resources
    tpl = (resources.files("spectdd") / "assets" / "templates" /
           "output-style.md").read_text(encoding="utf-8").lower()
    assert "ultra" in tpl
    assert "artifact economy" in tpl or "token" in tpl


# ------------------------------------------- output minimization (v0.6)

def test_commands_apply_file_first_rule():
    # nunca volcar al chat un documento recién escrito a fichero
    for phase in ("constitution", "specify", "plan", "tasks"):
        assert "file-first" in _asset(phase).lower(), f"{phase}.md lacks file-first rule"


def test_commands_define_compact_footer():
    for phase in ("constitution", "specify", "plan", "tasks", "implement"):
        text = _asset(phase).lower()
        assert "compact footer" in text, f"{phase}.md lacks compact footer rule"


def test_implement_trims_failure_traces():
    text = _asset("implement").lower()
    assert "failing assertion" in text


def test_output_style_documents_file_first():
    from importlib import resources
    tpl = (resources.files("spectdd") / "assets" / "templates" /
           "output-style.md").read_text(encoding="utf-8").lower()
    assert "file-first" in tpl and "compact footer" in tpl


# ------------------------------------------- architect skill (v0.7)

def test_init_installs_architect_skill_library(repo):
    cli.main(["init", "--assistant", "claude"])
    lib = repo / ".spectdd" / "skills" / "architect"
    assert (lib / "architect.md").is_file()
    for lang in ("python", "typescript", "java", "go", "generic"):
        assert (lib / f"{lang}.md").is_file(), f"missing {lang}.md"


def test_claude_gets_thin_architect_skill_entry(repo):
    cli.main(["init", "--assistant", "claude"])
    skill = repo / ".claude" / "skills" / "spectdd-architect" / "SKILL.md"
    assert skill.is_file()
    text = skill.read_text(encoding="utf-8")
    assert "architect/architect.md" in text
    assert len(text) < 800  # disparador fino: casi cero tokens hasta invocarla


def test_cursor_and_copilot_get_architect_trigger(repo):
    cli.main(["init", "--assistant", "all"])
    assert (repo / ".cursor" / "commands" / "spectdd-architect.md").is_file()
    assert (repo / ".github" / "prompts" / "spectdd-architect.prompt.md").is_file()


def test_architect_core_uses_lazy_loading_and_single_questions():
    from importlib import resources
    core = (resources.files("spectdd") / "assets" / "skills" /
            "architect.md").read_text(encoding="utf-8").lower()
    assert "only" in core          # carga SOLO el fichero del lenguaje elegido
    assert "one question" in core  # una pregunta cada vez


def test_language_files_carry_marked_recommendations():
    from importlib import resources
    for lang in ("python", "typescript", "java", "go"):
        text = (resources.files("spectdd") / "assets" / "skills" /
                f"{lang}.md").read_text(encoding="utf-8")
        assert "★" in text, f"{lang}.md has no marked recommendations"


# --------------------------------------------- phase handoff (v0.8)

def test_default_approval_mode_is_terminal(repo):
    cli.main(["init", "--assistant", "claude"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["approval_mode"] == "terminal"


def test_init_chat_approval_flag(repo):
    cli.main(["init", "--assistant", "claude", "--approval", "chat"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["approval_mode"] == "chat"


def test_wizard_asks_approval_mode(repo, monkeypatch):
    _feed(monkeypatch, ["", "", "", "", "", "", "", "", "chat"])
    cli.main(["init", "--assistant", "claude", "--interactive"])
    cfg = json.loads((repo / ".spectdd" / "config.json").read_text(encoding="utf-8"))
    assert cfg["approval_mode"] == "chat"


def test_approve_records_via_channel(repo):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev", "--via", "chat"])
    state = json.loads((repo / ".spectdd" / "state.json").read_text(encoding="utf-8"))
    assert state["constitution"]["via"] == "chat"


def test_gate_phases_include_handoff_block():
    for phase in ("constitution", "specify", "plan", "tasks", "implement"):
        text = _asset(phase).lower()
        assert "handoff" in text, f"{phase}.md lacks phase handoff"
        assert "approval_mode" in text
        assert "explicit" in text  # el sí debe ser explícito


def test_constitution_hard_rules_have_chat_exception():
    text = _asset("constitution").lower()
    assert "sole exception" in text and '"chat"' in text


# ------------------------------------------- brownfield onboarding (v0.9)

def test_init_installs_onboard_command_everywhere(repo):
    cli.main(["init", "--assistant", "all"])
    assert (repo / ".claude" / "commands" / "spectdd" / "onboard.md").is_file()
    assert (repo / ".cursor" / "commands" / "spectdd-onboard.md").is_file()
    assert (repo / ".github" / "prompts" / "spectdd-onboard.prompt.md").is_file()


def test_onboard_command_analyzes_existing_project():
    text = _asset("onboard").lower()
    for marker in ("existing", "detect", "architecture.md", "constitution",
                   "file-first", "gap"):
        assert marker in text, f"onboard.md missing: {marker}"


def test_onboard_is_not_a_gated_phase(repo):
    # onboard no forma parte de la cadena de puertas
    cli.main(["init", "--assistant", "claude"])
    with pytest.raises(SystemExit):
        cli.main(["check", "onboard"])


def test_wizard_detects_node_project(repo, monkeypatch):
    (repo / "package.json").write_text('{"name": "x", "devDependencies": {"vitest": "^1"}}')
    _feed(monkeypatch, [""] * 9)   # aceptar todos los valores detectados
    cli.main(["init", "--assistant", "claude", "--interactive"])
    c = (repo / ".spectdd" / "memory" / "constitution.md").read_text(encoding="utf-8")
    assert "Node" in c or "TypeScript" in c
    assert "vitest" in c.lower()


def test_wizard_detects_go_project(repo, monkeypatch):
    (repo / "go.mod").write_text("module example.com/x\n\ngo 1.22\n")
    _feed(monkeypatch, [""] * 9)
    cli.main(["init", "--assistant", "claude", "--interactive"])
    c = (repo / ".spectdd" / "memory" / "constitution.md").read_text(encoding="utf-8")
    assert "Go" in c


def test_init_reports_detected_project(repo, capsys):
    (repo / "pyproject.toml").write_text("[project]\nname='x'\n")
    cli.main(["init", "--assistant", "claude"])
    assert "detected" in capsys.readouterr().out.lower()


# ------------------------------------------------ evaluation fixes (v0.9.1)

def test_check_validates_full_upstream_chain(repo, capsys):
    # aprobar tasks saltándose specify y plan no debe abrir implement
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    cli.main(["approve", "tasks", "--feature", "001-x", "--by", "dev"])
    rc = cli.main(["check", "implement", "--feature", "001-x"])
    assert rc == 1
    out = capsys.readouterr().out
    assert "specify" in out and "plan" in out


def test_approve_warns_when_skipping_phases(repo, capsys):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    rc = cli.main(["approve", "tasks", "--feature", "001-x", "--by", "dev"])
    assert rc == 0                             # sigue siendo decisión del humano
    out = capsys.readouterr().out.lower()
    assert "warning" in out and "specify" in out and "plan" in out


def test_approve_in_order_does_not_warn_about_skipping(repo, capsys):
    cli.main(["init", "--assistant", "claude"])
    cli.main(["approve", "constitution", "--by", "dev"])
    (repo / "specs" / "001-x").mkdir(parents=True)
    cli.main(["approve", "specify", "--feature", "001-x", "--by", "dev"])
    assert "pending" not in capsys.readouterr().out.lower()


def test_setup_refuses_without_tty(repo, monkeypatch):
    cli.main(["init", "--assistant", "claude"])

    def boom(prompt=""):
        raise AssertionError("setup must not prompt without a TTY")
    monkeypatch.setattr("builtins.input", boom)
    rc = cli.main(["setup"])                   # stdin no es TTY en los tests
    assert rc == 1
    assert not (repo / ".spectdd" / "memory" / "constitution.md").exists()


def test_setup_aborts_on_eof_even_if_isatty_lies(repo, monkeypatch):
    # en Windows, stdin redirigido desde NUL devuelve isatty() == True;
    # el EOF a mitad del wizard debe abortar sin escribir nada
    import types
    cli.main(["init", "--assistant", "claude"])
    monkeypatch.setattr("sys.stdin", types.SimpleNamespace(isatty=lambda: True))

    def eof(prompt=""):
        raise EOFError
    monkeypatch.setattr("builtins.input", eof)
    rc = cli.main(["setup"])
    assert rc == 1
    assert not (repo / ".spectdd" / "memory" / "constitution.md").exists()


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "spectdd" in out
    from spectdd import __version__
    assert __version__ in out


def test_console_messages_are_ascii(repo, capsys):
    (repo / "pyproject.toml").write_text("[project]\nname='x'\n")
    cli.main(["init", "--assistant", "claude"])
    out = capsys.readouterr().out
    assert all(ord(ch) < 128 for ch in out), "console output must be ASCII-safe"
