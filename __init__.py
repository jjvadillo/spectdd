# Architecture questions — Go

Q1 Project type? 1) HTTP API 2) CLI 3) Worker/daemon 4) Library
Q2 Layout? 1) flat, grow later ★ Go idiom: start simple 2) cmd/ + internal/ — several binaries
Q3 (API) Router? 1) net/http + chi ★ stdlib-first, middleware 2) gin — popular, fast 3) echo
Q4 (CLI) 1) cobra ★ subcommands, completions 2) stdlib flag — tiny tools
Q5 (if data) DB access? 1) pgx + sqlc ★ typed SQL generated, no ORM magic 2) GORM — ORM comfort 3) database/sql
Q6 Config? 1) env vars + caarlos0/env ★ 12-factor 2) koanf/viper — files+env
Q7 Errors/logs? 1) stdlib errors + slog ★ structured, no deps 2) zerolog
Q8 Tests? 1) stdlib testing + testify ★ assertions, table tests 2) stdlib only
Q9 Lint? 1) golangci-lint ★ aggregates everything 2) go vet only
Q10 Concurrency needs? 1) low — request/response 2) high — pipelines/workers: design channels+context first ★ decide before coding
