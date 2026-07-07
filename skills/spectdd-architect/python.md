# Architecture questions — Python

Q1 Project type? 1) REST API 2) CLI 3) Library 4) Web app (server-rendered) 5) Worker/ETL
Q2 (API/Web) Framework? 1) FastAPI ★ async, typed, OpenAPI free 2) Django — batteries/admin 3) Flask — minimal
Q3 Packaging/env? 1) uv ★ fast, lockfile, one tool 2) poetry 3) pip + venv
Q4 Layout? 1) src/ layout ★ avoids import traps, packaging-ready 2) flat
Q5 (if data) Database? 1) PostgreSQL ★ safe default, JSONB 2) SQLite — single node/simple 3) MongoDB — document-shaped data
Q6 (if SQL) Access? 1) SQLAlchemy 2.0 ★ standard, typed 2) Django ORM (with Django) 3) raw + psycopg
Q7 Async? 1) yes — I/O bound, many connections ★ if API 2) no — simpler, CPU bound
Q8 Tests? 1) pytest + coverage ★ de facto standard 2) unittest
Q9 Lint/format/types? 1) ruff + mypy ★ one fast linter+formatter, static types 2) flake8+black+isort
Q10 Config/secrets? 1) pydantic-settings + .env ★ validated config 2) os.environ direct
Q11 Architecture style? 1) layered (api/service/repo) ★ simple, testable 2) hexagonal — many integrations 3) flat module — small tools
