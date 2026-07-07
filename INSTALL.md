# 📖 Installation & setup guide / Guía de instalación y puesta en marcha

🇬🇧 [English](#-english) · 🇪🇸 [Español](#-español)

---

## 🇬🇧 English

### Step 0 — Install the CLI (once per machine)

```bash
pipx install git+https://github.com/jjvadillo/spectdd.git
```

Installs the `spectdd` command globally, isolated from your projects (recommended).
Alternative: `pip install git+https://github.com/jjvadillo/spectdd.git` inside a
virtualenv. Verify with `spectdd --help`.

---

### 🅰️ Case A — NEW project (starting from zero)

**1. Create the folder and initialize spectdd**

```bash
mkdir my-app && cd my-app
git init                          # recommended: approvals are signed with git user.name
spectdd init --assistant claude   # or cursor | copilot | all
```

`init` installs into the repo: the 7 slash commands (`.claude/commands/spectdd/`,
`.cursor/commands/` or `.github/prompts/` depending on the assistant), the
`spectdd-architect` skill, document templates and `.spectdd/` (state + config).
Being an empty folder, the **interactive wizard** starts and asks: project name,
language, frameworks, test framework, lint, typing, dependency policy, output style
(`terse` recommended) and approval mode (`terminal` = strict, `chat` = your "yes" in
chat approves). With your answers it generates `.spectdd/memory/constitution.md`
already filled.

Useful flags: `--style ultra` (max token compression) · `--approval chat` ·
`--no-input` (skip wizard, e.g. CI) · `--interactive` (force wizard).

**2. Open your assistant and define the architecture**

```
spectdd-architect        ← skill: invoke it by name in the chat
```

Asks your language first, then architecture questions one at a time (framework, DB,
testing, layout...), each with a ★ recommendation. Writes
`.spectdd/memory/architecture.md`. Only the question bank for YOUR language enters
the context (token saving).

**3. Review and approve the constitution**

```
/spectdd:constitution    ← in the assistant: refines the wizard-generated file
```
```bash
spectdd approve constitution   # in YOUR terminal (skip if approval_mode=chat and you said yes)
```

**4. Build your first feature (the gated loop)**

```
/spectdd:specify users can register and log in     → review specs/001-*/spec.md
```
```bash
spectdd approve specify --feature 001-users-login
```
```
/spectdd:plan        → review plan.md      →  spectdd approve plan --feature 001-...
/spectdd:tasks       → review tasks.md     →  spectdd approve tasks --feature 001-...
/spectdd:implement   → TDD loop: approve each RED test in chat; code goes GREEN
                     →  spectdd approve implement --feature 001-...
/spectdd:review      → audits (spec compliance + code + security); fix criticals, merge
```

In `approval_mode: chat` you skip every `spectdd approve` above: answering **yes** to
the end-of-phase "Continue?" records it for you (audited as `via: chat`).

---

### 🅱️ Case B — EXISTING project

**1. Initialize spectdd inside your repo**

```bash
cd my-existing-project
spectdd init --assistant claude   # or cursor | copilot | all
```

Same installation as Case A, with two differences: `init` **detects your stack**
(package.json, pyproject.toml, go.mod, pom.xml, build.gradle) and pre-fills the
wizard defaults with what it found — press Enter to accept — and it prints a
reminder to run the onboarding analysis. Nothing in your existing code is touched:
spectdd only adds `.spectdd/` and the assistant command files.

**2. Let the agent analyze your codebase**

```
/spectdd:onboard         ← in the assistant
```

Reads your manifests and configs completely, samples representative source files
(never the whole tree), and generates: `constitution.md` filled with your REAL
conventions (uncertain items marked `[ASSUMED]` — correct them), `architecture.md`
reverse-engineered from the code, and a **gap report** (missing tests, no lint, no
CI...). Each gap can become a feature later via `/spectdd:specify`.

**3. Approve the constitution and work normally**

```bash
spectdd approve constitution
```

From here it's identical to Case A step 4: `specify → plan → tasks → implement →
review` for every new feature or bugfix, with gates between phases. You do NOT run
the architect skill (onboard already produced `architecture.md`).

---

### Everyday commands (both cases)

| Command | When you use it |
|---|---|
| `spectdd status` | See which phases/features are approved, by whom and via which channel |
| `spectdd approve <phase> --feature <slug>` | Open the next gate after reviewing an artifact |
| `spectdd revoke <phase> --feature <slug>` | You edited an approved doc → closes that gate and all downstream ones |
| `spectdd setup` | Re-run the wizard (asks before overwriting the constitution) |
| `spectdd check <phase> --feature <slug>` | (Agent's command) exit 0 = gate open, 1 = closed — you rarely type it |

**Tip:** commit `.spectdd/` (including `state.json`) — approvals become part of your
repo's history and code review.

---

## 🇪🇸 Español

### Paso 0 — Instalar el CLI (una vez por máquina)

```bash
pipx install git+https://github.com/jjvadillo/spectdd.git
```

Instala el comando `spectdd` global y aislado (recomendado). Alternativa:
`pip install ...` dentro de un virtualenv. Comprueba con `spectdd --help`.

---

### 🅰️ Caso A — Proyecto NUEVO (desde cero)

**1. Crea la carpeta e inicializa spectdd**

```bash
mkdir mi-app && cd mi-app
git init                          # recomendado: las aprobaciones se firman con git user.name
spectdd init --assistant claude   # o cursor | copilot | all
```

`init` instala en el repo los 7 comandos slash, la skill `spectdd-architect`, las
plantillas y `.spectdd/` (estado + config). Al ser carpeta vacía arranca el **wizard
interactivo**: nombre, lenguaje, frameworks, framework de tests, lint, tipado,
política de dependencias, estilo de salida (`terse` recomendado) y modo de
aprobación (`terminal` = estricto, `chat` = tu "sí" en el chat aprueba). Con tus
respuestas genera `.spectdd/memory/constitution.md` ya rellena.

Flags útiles: `--style ultra` (máxima compresión de tokens) · `--approval chat` ·
`--no-input` (sin wizard, p. ej. CI) · `--interactive` (forzar wizard).

**2. Abre tu asistente y define la arquitectura**

```
spectdd-architect        ← skill: invócala por su nombre en el chat
```

Pregunta primero tu lenguaje y después arquitectura, de una en una (framework, BD,
testing, estructura...), cada una con recomendación ★. Escribe
`.spectdd/memory/architecture.md`. Solo el banco de preguntas de TU lenguaje entra
en contexto (ahorro de tokens).

**3. Revisa y aprueba la constitución**

```
/spectdd:constitution    ← en el asistente: refina el fichero del wizard
```
```bash
spectdd approve constitution   # en TU terminal (sáltalo si approval_mode=chat y dijiste sí)
```

**4. Construye tu primera feature (el bucle con puertas)**

```
/spectdd:specify los usuarios pueden registrarse e iniciar sesión   → revisa spec.md
```
```bash
spectdd approve specify --feature 001-usuarios-login
```
```
/spectdd:plan        → revisa plan.md    →  spectdd approve plan --feature 001-...
/spectdd:tasks       → revisa tasks.md   →  spectdd approve tasks --feature 001-...
/spectdd:implement   → bucle TDD: apruebas cada test en ROJO en el chat
                     →  spectdd approve implement --feature 001-...
/spectdd:review      → auditorías (spec + código + seguridad); corrige críticos y mergea
```

Con `approval_mode: chat` te saltas todos los `spectdd approve`: responder **sí** al
"¿Continuar?" de fin de fase lo registra por ti (auditado como `via: chat`).

---

### 🅱️ Caso B — Proyecto EXISTENTE

**1. Inicializa spectdd dentro de tu repo**

```bash
cd mi-proyecto-existente
spectdd init --assistant claude   # o cursor | copilot | all
```

Igual que el caso A con dos diferencias: `init` **detecta tu stack** (package.json,
pyproject.toml, go.mod, pom.xml, build.gradle) y pre-rellena el wizard con lo
encontrado — Enter para aceptar — y te recuerda ejecutar el análisis de onboarding.
No toca nada de tu código: solo añade `.spectdd/` y los ficheros de comandos.

**2. Deja que el agente analice tu código**

```
/spectdd:onboard         ← en el asistente
```

Lee manifiestos y configs completos, muestrea ficheros fuente representativos (nunca
el árbol entero) y genera: `constitution.md` con tus convenciones REALES (lo dudoso
marcado `[ASSUMED]` — corrígelo), `architecture.md` extraída del código, y un
**informe de huecos** (tests que faltan, sin lint, sin CI...). Cada hueco puede
convertirse en feature con `/spectdd:specify`.

**3. Aprueba la constitución y trabaja normal**

```bash
spectdd approve constitution
```

Desde aquí es idéntico al paso 4 del caso A para cada feature o bugfix. No ejecutes
la skill architect: onboard ya generó `architecture.md`.

---

### Comandos del día a día (ambos casos)

| Comando | Cuándo lo usas |
|---|---|
| `spectdd status` | Ver qué fases/features están aprobadas, por quién y por qué canal |
| `spectdd approve <fase> --feature <slug>` | Abrir la siguiente puerta tras revisar un artefacto |
| `spectdd revoke <fase> --feature <slug>` | Editaste un doc aprobado → cierra esa puerta y todas las posteriores |
| `spectdd setup` | Relanzar el wizard (pide confirmación antes de sobrescribir) |
| `spectdd check <fase> --feature <slug>` | (Comando del agente) exit 0 = puerta abierta, 1 = cerrada |

**Consejo:** commitea `.spectdd/` (incluido `state.json`) — las aprobaciones quedan
en el historial del repo y en el code review.

