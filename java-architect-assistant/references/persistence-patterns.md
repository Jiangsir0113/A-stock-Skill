# Persistence Patterns

Use this guide to decide where persistence changes belong.

## MyBatis

Common signs:

- `@Mapper`
- `*Mapper.java`
- `*Mapper.xml`
- XML-based SQL under `resources/mapper`

Preferred placement:

- Java mapper interface beside peer mappers
- XML SQL under the existing mapper resource tree
- DO or entity classes beside peer persistence models

When adding queries:

- Match method names between interface and XML
- Reuse existing `resultMap` and common SQL fragments if present
- Keep SQL close to peer statements for the same aggregate

## MyBatis-Plus

Common signs:

- `BaseMapper<T>`
- `ServiceImpl`
- wrappers such as `LambdaQueryWrapper`

Preferred pattern:

- Reuse `BaseMapper`
- Reuse existing `ServiceImpl` inheritance if the project already relies on it
- Prefer lambda wrappers over raw column strings when the project already uses them

Do not introduce XML if the repository handles similar queries fully in code, unless the query is too complex and peer code already uses XML for that case.

## JPA or Hibernate

Common signs:

- `@Entity`
- `JpaRepository`
- `CrudRepository`
- JPQL or derived query methods

Preferred pattern:

- Reuse existing entity mapping conventions
- Reuse repository method naming style
- Prefer specification, criteria, or query annotations only if the project already uses that style

Do not mix JPA and MyBatis for the same aggregate unless the repository already does so intentionally.

## SQL and Migration Rules

When a schema change is required:

- First check whether the repository uses Flyway, Liquibase, or manual SQL scripts
- Put the script in the existing migration location
- Match version naming and file naming conventions

When only query logic changes:

- Do not create migration files for non-schema changes
- Keep SQL in the project's existing query location

## Result Mapping and Objects

Prefer the repository's existing model boundaries:

- entity or DO for persistence objects
- DTO or VO for external transport
- converter or assembler for transformation

Avoid leaking persistence objects directly to controller responses unless the project already accepts that pattern.
