<div align="center">

# 🔒 spectdd

### Spec-Driven + Test-Driven Development for AI coding assistants<br/>— with *real* human approval gates —

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)
[![Version](https://img.shields.io/badge/version-0.9.0-brightgreen.svg)](CHANGELOG.md)
[![Tests](https://img.shields.io/badge/tests-58%20passed-success.svg)](tests/test_cli.py)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](CONTRIBUTING.md)

**Your AI writes the code. You keep the steering wheel. Your wallet keeps its tokens.**

🇬🇧 [English](#-english) · 🇪🇸 [Español](#-español)

</div>

---

## 🇬🇧 English

### 😱 The problem

| Without spectdd | With spectdd |
|---|---|
| 🎲 **Vibe coding** — code no failing test ever justified | 🔴🟢♻️ **Enforced TDD** — you approve every red test before a line of implementation |
| 🚦 Agent races ahead without your sign-off | 🔒 **Real gates** — a CLI exit code blocks every phase until *you* approve |
| 🕳️ No code review — bugs & N+1s slip through | 🔍 **Built-in code audit** in the review phase |
| 🔓 No security review — injections & leaked secrets ship | 🛡️ **Built-in security audit** — critical/high findings block the merge |
| 💸 Token burn — verbose chat, duplicated markdown | ⚡ **Token efficiency by design** — up to ~70% less output |

Tools like Spec Kit or Kiro structure the phases, but their "wait for human review"
is just a sentence in a prompt. In spectdd **the gate is an exit code**: the agent
must run `spectdd check <phase>` and it fails until you approve. No external
plugins. Works the same on **Claude Code, Cursor and GitHub Copilot**.

### 🗺️ The workflow

```
 🧭 onboard (existing code)  or  🏗️ architect (new project)
        └──> 📜 constitution → 📋 specify → 📐 plan → ✅ tasks → 🔴🟢♻️ implement → 🔍 review
                    ▲              ▲           ▲          ▲             ▲
                you approve    you approve  you approve  you approve   you approve
```

Every approval is signed (name + timestamp + channel) in `.spectdd/state.json` —
commit it and approvals become part of code review.

### 📦 Install

```bash
pipx install git+https://github.com/jjvadillo/spectdd.git   # recommended
pip  install git+https://github.com/jjvadillo/spectdd.git   # alternative
```

### 🚀 Quick start

> 📖 Full step-by-step guide (new project vs existing project, every command
> explained): **[INSTALL.md](INSTALL.md)**

```bash
cd your-project
spectdd init --assistant claude    # or cursor | copilot | all
```

First run launches an **interactive wizard** (project name, language, frameworks,
tests, lint, typing, dependencies, output style, approval mode) and generates a
pre-filled constitution. On an existing codebase, `init` **auto-detects your stack**
(`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`...) and pre-fills the answers.

Then, inside your assistant:

| Step | Command | You get |
|---|---|---|
| 🧭 | `/spectdd:onboard` *(existing projects)* | Constitution + `architecture.md` from your real code, gap report |
| 🏗️ | `spectdd-architect` skill *(new projects)* | Architecture interview, one question at a time, ★ recommendations |
| 📜 | `/spectdd:constitution` | Non-negotiable principles |
| 📋 | `/spectdd:specify <idea>` | User stories + testable acceptance criteria |
| 📐 | `/spectdd:plan` | Technical plan bound by the constitution |
| ✅ | `/spectdd:tasks` | Small, ordered, test-first tasks |
| 🔴🟢♻️ | `/spectdd:implement` | TDD loop — you approve each red test |
| 🔍 | `/spectdd:review` | Spec compliance + code audit + security audit |

### 🤝 Phase handoff — two approval modes

At the end of each phase the agent prints a tiny block:

```
Done: what this phase produced (≤3 bullets)
Next (plan): what it will do (≤2 bullets)
Continue? (yes = approve specify & start plan)
```

| Mode | Your "yes" in chat | Best for |
|---|---|---|
| `terminal` *(default)* | Not enough — you still run `spectdd approve ...` yourself | Maximum control, teams, CI |
| `chat` | Authorizes the agent to run the approve **for you** (audited as `via: chat`) | Solo flow, speed |

Pick it with `spectdd init --approval chat`, in the wizard, or in `.spectdd/config.json`.

### 🧰 CLI reference

| Command | What it does |
|---|---|
| `spectdd init --assistant claude\|cursor\|copilot\|all [--style terse\|normal\|ultra] [--approval terminal\|chat] [--interactive\|--no-input]` | Install commands, architect skill, templates + setup wizard (auto-detects your stack) |
| `spectdd setup` | Re-run the wizard (asks before overwriting the constitution) |
| `spectdd approve <phase> [--feature SLUG] [--by NAME] [--via terminal\|chat]` | Record a human approval (opens the next gate) |
| `spectdd check <phase> [--feature SLUG]` | Used by the agent — exit 1 = gate closed |
| `spectdd revoke <phase> [--feature SLUG]` | Withdraw an approval **and every downstream one** |
| `spectdd status` | Approval state of every phase & feature, style, audit trail |

### ⚡ Token efficiency by design

- 🗜️ **3 chat compression levels**: `normal` · `terse` (default) · `ultra` (fragments, abbreviations, one line per idea).
- 📄 **File-first rule**: documents written to disk are never echoed in chat — path + ≤5-line outline. The single biggest saver.
- 🔗 **Artifact economy**: spec/plan/tasks never repeat each other, they cross-reference by ID ("covers AC-2.1"). No boilerplate, no gold plating.
- ✂️ **Compact footers & trimmed traces**: one-line phase footers; only the failing assertion in chat.
- 🏗️ **Lazy architect skill**: ~6-line trigger; of the 5 language question banks only the one you pick ever enters the context window.
- 🔒 **Never compressed**: code, tests, diffs, commands and audit reports stay byte-exact.

> In simulated full runs these rules cut LLM output by **~65-70%** vs a verbose
> baseline. Real savings depend on your model and feature size.

### 🥊 Why this and not something else?

| | Raw AI assistant | Spec Kit / Kiro | **spectdd** |
|---|---|---|---|
| Spec & plan before code | ❌ | ✅ | ✅ |
| Human gate between phases | ❌ | 📝 prompt only | 🔒 **enforced by exit code** |
| TDD (test approved before impl.) | ❌ | ❌ | ✅ |
| Code + security audits built-in | ❌ | ❌ | ✅ |
| Token-optimized output | ❌ | ❌ | ✅ (~65-70% less) |
| Adopts existing codebases | — | weak | ✅ `/spectdd:onboard` |

### 🧪 Development

Dogfooding: the CLI itself was built test-first (58 tests).

```bash
pip install -e ".[dev]" && pytest
```

MIT license. Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[CHANGELOG](CHANGELOG.md). Open an issue with a spec before a PR. 😉

---

## 🇪🇸 Español

### 😱 El problema

| Sin spectdd | Con spectdd |
|---|---|
| 🎲 **Vibe coding** — código que ningún test en rojo justificó | 🔴🟢♻️ **TDD obligatorio** — apruebas cada test en rojo antes de una línea de implementación |
| 🚦 El agente avanza sin tu visto bueno | 🔒 **Puertas reales** — un exit code bloquea cada fase hasta que *tú* apruebas |
| 🕳️ Sin code review — bugs y N+1 se cuelan | 🔍 **Auditoría de código integrada** en la fase review |
| 🔓 Sin revisión de seguridad — inyecciones y secretos filtrados | 🛡️ **Auditoría de seguridad integrada** — los hallazgos critical/high bloquean el merge |
| 💸 Derroche de tokens — chat verboso, markdown duplicado | ⚡ **Eficiencia de tokens por diseño** — hasta ~70% menos salida |

Herramientas como Spec Kit o Kiro estructuran las fases, pero su "espera al humano"
es solo una frase en un prompt. En spectdd **la puerta es un exit code**: el agente
debe ejecutar `spectdd check <fase>` y falla hasta que tú apruebas. Sin plugins
externos. Funciona igual en **Claude Code, Cursor y GitHub Copilot**.

### 📦 Instalación y arranque

> 📖 Guía completa paso a paso (proyecto nuevo vs existente, todos los comandos
> explicados): **[INSTALL.md](INSTALL.md)**

```bash
pipx install git+https://github.com/jjvadillo/spectdd.git
cd tu-proyecto
spectdd init --assistant claude    # o cursor | copilot | all
```

La primera ejecución lanza el **wizard interactivo** (nombre, lenguaje, frameworks,
tests, lint, tipado, dependencias, estilo de salida y modo de aprobación) y genera
una constitución ya rellena. En un proyecto existente, `init` **detecta tu stack**
automáticamente y pre-rellena las respuestas.

Después, en tu asistente: `/spectdd:onboard` si el proyecto ya existe (constitución +
arquitectura + informe de huecos desde tu código real) o la skill `spectdd-architect`
si empiezas de cero (entrevista con recomendaciones ★) → `/spectdd:constitution` →
`/spectdd:specify` → `/spectdd:plan` → `/spectdd:tasks` → `/spectdd:implement`
(bucle TDD: apruebas cada test en rojo) → `/spectdd:review` (auditorías).

### 🤝 Handoff entre fases — dos modos de aprobación

Al final de cada fase: **Hecho** (≤3 puntos) + **Siguiente** (≤2 puntos) + **¿Continuar?**

| Modo | Tu "sí" en el chat | Ideal para |
|---|---|---|
| `terminal` *(por defecto)* | No basta — ejecutas tú `spectdd approve ...` | Máximo control, equipos |
| `chat` | Autoriza al agente a ejecutar el approve **por ti** (auditado como `via: chat`) | Trabajo en solitario, agilidad |

### 🧰 Comandos

| Comando | Para qué |
|---|---|
| `spectdd init --assistant ... [--style ...] [--approval ...]` | Instalar todo + wizard (detecta tu stack) |
| `spectdd setup` | Relanzar el wizard |
| `spectdd approve <fase> [--feature SLUG] [--via chat]` | Registrar tu aprobación (abre la puerta) |
| `spectdd check <fase> [--feature SLUG]` | Lo usa el agente — exit 1 = puerta cerrada |
| `spectdd revoke <fase> [--feature SLUG]` | Retirar una aprobación **y todas las posteriores** |
| `spectdd status` | Estado de fases, features, estilo y auditoría |

### ⚡ Eficiencia de tokens

Tres niveles de compresión del chat (`normal`/`terse`/`ultra`), regla **file-first**
(los documentos no se vuelcan al chat), economía de artefactos (referencias por ID,
sin repetición), footers de una línea, trazas recortadas a la aserción que falla y
skill de arquitectura con carga perezosa (solo entra en contexto el banco de
preguntas del lenguaje elegido). Código, tests, diffs y auditorías **nunca** se
comprimen. En simulaciones: **~65-70% menos salida** que una línea base verbosa.

### 🧭 Filosofía

1. **Tú eres dueño de la especificación y de los tests; la IA es dueña de la implementación.**
2. Ninguna fase empieza sin aprobación humana explícita y registrada.
3. El código solo existe cuando hay un test en rojo que lo justifica.
4. Ahorrar tokens nunca significa perder precisión.

### 📄 Licencia

MIT. Construido con TDD estricto: 58 tests escritos antes que el código.
Contribuciones: [CONTRIBUTING.md](CONTRIBUTING.md) · Historial: [CHANGELOG.md](CHANGELOG.md)
