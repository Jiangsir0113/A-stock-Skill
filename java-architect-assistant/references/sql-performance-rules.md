# SQL Performance Rules

Use this guide whenever table DDL, indexes, mapper SQL, XML SQL, or repository queries are added or changed.

## Core Principle

SQL must be correct first, then performance-aware. Table design and indexes should match real business access patterns, not be added mechanically.

## Table Design

When creating or changing tables, consider:

- primary key strategy
- required unique constraints
- column nullability
- field length and type choice
- audit fields already required by the repository
- status and lifecycle fields
- whether large text or infrequently used fields should be separated

Do not design tables only from the UI field list. Design them from the business entity and query behavior.

## Index Design

Indexes should be justified by one or more of these:

- common query filters
- join conditions
- sorting fields
- uniqueness constraints
- high-frequency lookup paths

Before adding an index, consider:

- selectivity
- left-prefix usage for composite indexes
- write amplification cost
- overlap with existing indexes
- whether the query can actually use the index

Avoid:

- adding indexes to every column
- duplicate or nearly duplicate indexes
- indexes that do not match the real query shape

## Query SQL

Prefer SQL that:

- selects only needed columns
- filters early with selective conditions
- matches existing useful indexes
- avoids unnecessary nested queries
- avoids row-by-row query patterns
- supports pagination correctly when needed

Avoid:

- `select *` unless the repository clearly accepts it for that exact case
- SQL in loops
- unnecessary full-table scans
- functions on indexed columns in filter conditions when avoidable
- large offset pagination without repository precedent or mitigation
- repeated single-row queries when one batch query can solve it

## Joins And Batch Access

When related data is needed, compare:

- one proper join
- one batch query plus in-memory mapping
- an existing cached or precomputed path

Choose the clearest performant option that fits repository style.

## Verification Mindset

When changing SQL, ask:

- what are the main query conditions
- what index will support this query
- what data volume risk exists
- whether the query shape can degrade badly over time
- whether there is a safer batch or set-based rewrite

## Output Expectation

When table or SQL changes are part of the solution, briefly explain:

- why the table design is reasonable
- why the chosen indexes are needed
- why the SQL shape should perform acceptably
