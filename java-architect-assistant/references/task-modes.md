# Task Modes

Use this guide to choose the correct working mode before changing code.

## Core Rule

Do not treat every request as feature development. First identify whether the main task is:

- feature development
- bug fixing
- performance optimization
- code review

Then follow the matching workflow while still respecting repository conventions.

## 1. Feature Development

Choose this mode when the user asks to:

- add a new API or page capability
- add a new business flow
- support a new field or status
- add SQL, mapper methods, config, scheduled jobs, or integration points

Working pattern:

1. learn the target module structure
2. inspect peer implementations
3. identify the end-to-end delivery chain
4. add files in the right places
5. keep style consistent with nearby code
6. avoid touching old code unless necessary and approved

## 2. Bug Fixing

Choose this mode when the user reports:

- an exception
- wrong data
- wrong business behavior
- failed save, query, or callback
- a screenshot or stack trace
- "why does this not work" style symptoms

Working pattern:

1. define the visible symptom
2. identify the request entry or execution trigger
3. trace the likely path through controller, service, mapper, SQL, config, cache, or remote call layers
4. find the root cause
5. apply the smallest correct fix
6. verify the broken scenario and nearby regressions

Common root-cause buckets:

- null handling
- enum or code mismatch
- missing conversion or mapping
- SQL condition errors
- transaction boundary issues
- stale cache or incorrect cache key
- concurrency assumptions
- remote dependency failure handling
- pagination boundary bugs

## 3. Performance Optimization

Choose this mode when the user reports:

- slow API response
- slow list query
- timeout
- high CPU
- heavy memory usage
- too many SQL queries or repeated remote calls

Working pattern:

1. identify the hot path
2. inspect the slowest layer first
3. find the bottleneck category
4. optimize with the narrowest safe change
5. preserve business semantics
6. verify that the optimization did not break the existing contract

Common optimization targets:

- N+1 database access
- missing or weak pagination
- oversized query result sets
- repeated object conversion
- repeated remote calls in loops
- unnecessary serialization or parsing
- poor cache usage
- blocking I/O inside hot paths

## 4. Code Review

Choose this mode when the user asks to:

- review code
- check whether the implementation matches the requirement
- inspect business logic correctness
- inspect performance, SQL quality, maintainability, or code bloat
- identify bugs, regressions, or risky design choices in an existing change

Working pattern:

1. identify the review target and expected behavior
2. compare the code to the requirement or intended behavior
3. inspect correctness and regression risk first
4. inspect performance, SQL, concurrency, transaction, and data consistency risks
5. inspect maintainability, extensibility, readability, and code bloat
6. report concrete findings before summary

Common review buckets:

- requirement mismatch
- missing business rule
- wrong edge-case behavior
- null or boundary bugs
- transaction or concurrency risks
- SQL or index inefficiency
- cache or MQ misuse
- overlong or bloated methods
- duplicate logic
- missing validation or weak exception handling
- inadequate comments or poor readability

## Switching Modes

It is acceptable to switch modes during investigation:

- a reported bug may require a small feature-like compatibility addition
- an optimization may expose a hidden bug
- a feature request may require fixing an old broken flow first

If the mode changes materially, say so briefly and explain why.
