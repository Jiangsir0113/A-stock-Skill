# MyBatis Plus Guidelines

Use this guide only when the repository already uses MyBatis-Plus.

## Core Principle

Follow the repository's current MyBatis-Plus usage pattern. Do not introduce a textbook MyBatis-Plus style if the local project already narrowed or customized its usage.

## What To Inspect First

Inspect nearby peers for:

- whether `ServiceImpl` is used directly
- whether service interfaces extend `IService`
- whether mapper interfaces extend `BaseMapper`
- whether pagination uses `Page<T>` or custom wrappers
- whether wrappers use lambda style or raw column names
- whether chain wrappers are accepted or avoided
- whether XML is used for complex queries

## Mapper Pattern

If nearby mapper interfaces extend `BaseMapper<T>`, keep using that.

If the repository adds custom methods to mappers:

- keep method naming consistent
- place complex SQL where peers place it
- match XML namespace and method signatures exactly

## Service Pattern

If nearby services extend `ServiceImpl`, follow that pattern.

If the repository wraps MyBatis-Plus with custom base services, use the custom base layer instead of direct framework inheritance.

## Query Pattern

Prefer the query style already used nearby:

- `LambdaQueryWrapper`
- `LambdaUpdateWrapper`
- chained wrapper APIs
- XML SQL for complex joins

Do not force wrappers for queries that nearby code already keeps in XML.

## Pagination Pattern

If the project uses MyBatis-Plus pagination:

- copy the local page object creation pattern
- reuse the repository's request-to-page conversion
- reuse page result conversion helpers if present

Do not invent a second page conversion flow.

## Fill, Logic Delete, and Common Fields

Before handling create or update flows, inspect whether the repository uses:

- auto-fill fields
- logical delete
- optimistic locking
- tenant fields
- audit fields

Follow the local entity and meta-object handler pattern. Do not hardcode these fields in service logic if the framework or base layer already manages them.
