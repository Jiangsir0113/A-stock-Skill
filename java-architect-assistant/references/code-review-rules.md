# Code Review Rules

Use this guide when the task is to review Java code rather than directly implement it.

## Core Rule

A review is primarily about finding real issues, not describing the code. Focus on defects, risks, regressions, missing requirements, performance problems, and unnecessary complexity.

For development work that follows this skill, review should also converge. If the requirement has not changed, repeated reviews should not keep surfacing new avoidable issues that should have been found earlier.

## Review Priorities

Review in this order:

1. requirement fit
2. business logic correctness
3. regression risk
4. performance and SQL quality
5. concurrency, transaction, cache, MQ, and consistency risk
6. maintainability and code bloat
7. style and lower-level polish

## What To Check

### Requirement fit

Check whether the code:

- actually implements the requested behavior
- misses required fields, states, or flows
- changes existing behavior unexpectedly
- misunderstands the prototype or PRD

### Business logic

Check:

- status transitions
- validation rules
- permissions and visibility
- null and boundary handling
- side effects
- duplicate request handling
- rollback expectations

### Performance

Check:

- loop depth
- SQL in loops
- N+1 query patterns
- poor pagination behavior
- unnecessary object conversion
- unnecessary remote calls
- weak index support for new queries

### Maintainability and bloat

Check:

- overly long methods
- over-coupled classes
- duplicate logic
- needless abstraction
- hardcoding
- poor extensibility
- insufficient comments

## Output Rule

Present findings first, ordered by severity.

Each finding should describe:

- what is wrong
- why it matters
- where it appears
- what kind of failure or risk it can cause

If no issue is found, say so explicitly and mention any remaining uncertainty such as missing runtime verification, unclear requirements, or untested edge cases.

## Review Convergence Expectation

Expected review sequence for development work:

1. method-level review after each completed method task
2. feature-level review after the end-to-end flow is complete

If a third review happens without requirement changes, it should generally confirm stability rather than discover a fresh batch of basic logic, design, or quality problems.

Do not interpret this as "stop reporting problems on the third review." Any genuine remaining issue must still be reported. The expectation is that code quality should already be high enough that the third review does not expose new avoidable basics that should have been caught earlier.
