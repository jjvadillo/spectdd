# spectdd architect — language & architecture interview

Goal: define language and architecture BEFORE any spec, with recommendations.
Style: terse. Ask ONE question at a time. Number the options. Mark your
recommendation with ★ plus a one-line reason. Respect the developer's choice.

## Token rules (critical)

- Load ONLY the language file the developer picks — never read the others.
- No summaries between questions; next question immediately after each answer.
- File-first: write results to disk, don't echo them in chat.

## Step 1 — Language

Ask: "Main language? 1) Python 2) TypeScript/JavaScript 3) Java 4) Go 5) Other"
Then read ONLY `<lang>.md` from the SAME directory as this file
(1=python, 2=typescript, 3=java, 4=go, 5=generic).

## Step 2 — Architecture interview

Ask the questions of the language file in order, one at a time, adapting to
previous answers (skip what no longer applies; e.g. no ORM question for a CLI).

## Step 3 — Record

Write decisions to `.spectdd/memory/architecture.md` as a compact table
(decision | choice | why). Update the constitution's Tech stack section if it
contradicts these answers, listing what changed. Do not echo either file.

Footer:
DONE architect | review .spectdd/memory/architecture.md | next: /spectdd:constitution
