# Architecture questions — TypeScript/JavaScript

Q1 Project type? 1) REST/GraphQL API 2) Frontend SPA 3) Full-stack 4) CLI 5) Library
Q2 Runtime? 1) Node LTS ★ ecosystem, stability 2) Bun — speed, all-in-one 3) Deno
Q3 TypeScript strict mode? 1) yes ★ catches bugs at compile time 2) no (plain JS)
Q4 (API) Framework? 1) Fastify ★ fast, schema-validated 2) NestJS — big teams, structure 3) Express — familiar 4) Hono — edge
Q5 (Frontend/Full-stack) 1) Next.js ★ SSR+RSC default 2) React+Vite — SPA 3) SvelteKit
Q6 Package manager? 1) pnpm ★ fast, strict deps 2) npm 3) yarn
Q7 (if data) DB + access? 1) PostgreSQL + Drizzle ★ typed SQL, light 2) PostgreSQL + Prisma — DX, migrations 3) SQLite
Q8 Validation? 1) zod ★ runtime + inferred types 2) class-validator (NestJS)
Q9 Tests? 1) Vitest ★ fast, ESM native 2) Jest 3) node:test
Q10 Lint/format? 1) Biome ★ one fast tool 2) ESLint + Prettier — plugin ecosystem
Q11 Monorepo? 1) no ★ start simple 2) yes — pnpm workspaces/turborepo
