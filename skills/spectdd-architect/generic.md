# Architecture questions — any language

Q1 Project type? 1) API/service 2) CLI 3) Library 4) Web app 5) Batch/worker
Q2 Architecture style? 1) layered ★ simple, testable 2) hexagonal — many external integrations 3) single module — small scope
Q3 Persistence? 1) relational DB ★ default until proven otherwise 2) document DB 3) files/none
Q4 Public interface contract? 1) OpenAPI/schema-first ★ testable, documented 2) code-first
Q5 Test levels? 1) unit + integration ★ minimum per constitution 2) + e2e — user flows critical
Q6 Config/secrets? 1) env vars, validated at boot ★ 12-factor 2) config files
Q7 Observability? 1) structured logs ★ minimum viable 2) + metrics/traces — production service
Q8 CI? 1) tests+lint on every PR ★ non-negotiable 2) + release pipeline
