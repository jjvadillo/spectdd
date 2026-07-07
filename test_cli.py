# Architecture questions — Java

Q1 Project type? 1) REST API/microservice 2) Batch 3) Library 4) Desktop
Q2 Java version? 1) 21 LTS ★ virtual threads, records 2) 17 LTS — org constraint
Q3 Build? 1) Gradle (Kotlin DSL) ★ fast, flexible 2) Maven — convention, ubiquitous
Q4 Framework? 1) Spring Boot ★ ecosystem, hiring 2) Quarkus — fast start/native 3) none — library
Q5 Architecture style? 1) hexagonal (ports/adapters) ★ testable domain 2) layered — small services 3) modular monolith
Q6 (if data) Persistence? 1) Spring Data JPA ★ productivity 2) jOOQ — SQL control 3) JDBC template
Q7 Database? 1) PostgreSQL ★ 2) MySQL 3) Oracle — org constraint
Q8 Tests? 1) JUnit 5 + Mockito + Testcontainers ★ real DB in integration 2) JUnit + H2
Q9 Quality? 1) Checkstyle + SpotBugs + JaCoCo ★ style+bugs+coverage 2) SonarQube — if server exists
Q10 API docs? 1) springdoc-openapi ★ free from code 2) manual
