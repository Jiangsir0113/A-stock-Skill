# Engineering Quality Rules

Use this guide to keep implementations extensible, correct, and maintainable.

## Extensibility

Interfaces and method design should allow reasonable future growth.

Prefer:

- extension points over hardcoded branches
- enums, strategy objects, handlers, or configuration when business types may grow
- clear parameter objects when the input is likely to expand
- small focused methods and classes

Avoid:

- tightly coupling unrelated business rules
- encoding future-variant logic as scattered `if/else` branches
- designing APIs that cannot evolve without breaking callers

## Cache

Use cache only when the business and repository patterns justify it.

Before adding or changing cache behavior, consider:

- cache key design
- consistency requirements
- invalidation timing
- stale data tolerance
- hot key risk
- failure fallback

Do not add cache just because something feels slow.

## MQ

Use MQ only when asynchronous decoupling is actually needed and the repository already supports the pattern or the user accepts the architecture change.

Before using MQ, consider:

- message ordering
- idempotency
- retry behavior
- consumer failure
- duplicate delivery
- transaction boundaries

## Transactions

Transactions should be used according to the business consistency boundary.

Before adding or changing transactions, consider:

- what data must commit atomically
- whether downstream remote calls belong inside the transaction
- rollback rules
- nested transaction behavior
- lock duration and contention

Do not blindly expand transaction scope.

## Locks

Use locks only when concurrency control really requires them.

Before adding a lock, consider:

- what shared resource is being protected
- lock granularity
- deadlock risk
- timeout behavior
- whether the database, unique index, or existing idempotency mechanism already solves the issue

## Threads and Async Work

Use threads, pools, or async processing carefully.

Before adding asynchronous logic, consider:

- whether the task is CPU-bound or I/O-bound
- thread pool ownership
- timeout and cancellation
- context propagation
- error handling
- observability

Do not create unmanaged threads casually.

## Logic Rigor

Business logic should be strict and explicit.

Check:

- null paths
- empty collections
- duplicate requests
- invalid status transitions
- concurrent updates
- retry side effects
- rollback expectations
- boundary values

The goal is to prevent avoidable review churn. Logic should be thought through early enough that repeated reviews without requirement changes do not keep revealing basic new problems.

## Loop And Data Access Rules

Control loop complexity aggressively.

Default rules:

- loop nesting should not exceed 2 levels
- do not place SQL execution, mapper calls, repository queries, or database round-trips inside loops

If bulk data is needed, prefer:

- batch query first, then in-memory mapping
- grouping or indexing data before iteration
- set-based SQL instead of repeated single-row queries
- batch insert or batch update when the repository already supports it

If a loop appears to need database access, stop and redesign the flow first.

## Commenting Standards

As a default rule for newly written code:

- class declarations should have a comment above them
- method declarations should have a comment above them
- non-trivial logic should include detailed explanatory comments
- aim for explanatory comments roughly every 3-5 lines in dense business logic
- if a method grows beyond 100 lines, split it unless the local project clearly prefers another pattern
- if loop nesting would exceed 2 levels, refactor the logic into preprocessing, helper methods, lookup maps, or batch operations

If the local project already has a stronger commenting or formatting rule, follow the local rule first.

## Final Check

Before finishing, confirm:

- the design is extensible enough for nearby future change
- cache, MQ, transaction, lock, and thread usage are justified
- business logic covers edge cases
- comments explain intent, not just syntax
- long methods were split where practical
- newly added or modified methods were checked against their expected task goals
- method-level review and feature-level review have already absorbed the obvious issues so later reviews do not keep surfacing new avoidable problems
- if a later review still finds a genuine problem, it must be treated as a real defect rather than suppressed; the hard requirement is to reduce avoidable misses through better logic, design, and foresight
