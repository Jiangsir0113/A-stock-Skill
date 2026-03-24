# Planning Rules

Use this guide before any code addition or modification.

## Core Rule

No code changes before a plan, but the plan depth should match the change size and risk.

Before creating files, editing files, changing SQL, or modifying configuration, first output either:

- a detailed execution plan for substantial changes
- a lightweight plan for very small low-risk changes

## What The Plan Must Include

The plan should cover:

1. task mode
2. requirement understanding
3. unresolved questions
4. target modules
5. task breakdown into small tasks
6. expected goal for each task
7. files to add
8. files to modify
9. ordered implementation steps
10. data and interface impact
11. cache, MQ, transaction, lock, thread considerations when relevant
12. verification steps
13. risks and rollback concerns

## Task Breakdown Rule

For development work, break the requirement into small executable tasks before implementation.

Each task should:

- have a clear scope
- map to one meaningful delivery step
- have an expected goal or outcome

For substantial development work, prefer method-level task breakdown when practical.

That means the plan should not stop at:

- add service
- add controller
- add mapper

when the real work is better described as:

- add `validateCreateRequest` method
- add `buildOrderEntity` method
- add `loadRelatedRecordsBatch` method
- add `saveAndPublishEvent` method

Examples:

- task: inspect the order module controller and request wrapper pattern
  expected goal: determine the correct controller style and request/response conventions
- task: add request DTO and validation annotations
  expected goal: define stable input structure for the new API
- task: add one batch mapper query
  expected goal: fetch related records without per-item database access

Do not keep the whole requirement as one vague task when it can be split into clear smaller steps.

## Method-Level Completion Check

When the plan is split down to methods, each method task should include an expected goal.

After completing a method, check:

1. whether the method now satisfies its expected goal
2. whether its inputs and outputs match the plan
3. whether it introduced side effects or regressions outside its intended scope

Only after that check should the next method-level task continue.

## Review Convergence Rule

For substantial development work, build review checkpoints into the plan:

1. one review after each completed method-level task
2. one review after the full feature flow is completed

If the requirement has not changed, the third review should not reveal new issues that should reasonably have been caught in the first two reviews.

This is a code-quality expectation, not permission to ignore defects. If a real issue still exists in the third review, it must still be raised. The point is to plan and implement carefully enough that avoidable basic issues are already removed before reaching that stage.

Plan with this standard in mind:

- think through edge cases earlier
- do not postpone obvious design or logic problems
- reduce avoidable churn before asking for another review

## Lightweight Plan Cases

A lightweight plan is acceptable only when the change is clearly small and low risk.

Typical examples:

- typo or comment fixes
- import cleanup
- formatting adjustments
- very small local fixes that do not change business flow or interfaces

A lightweight plan should still state:

1. what will change
2. which file will be touched
3. why it is low risk
4. how it will be verified

Lightweight plans do not need full task breakdown if the change is truly trivial.

## Detail Level

The plan should be specific enough that another senior engineer could follow it without guessing the implementation path.

Avoid vague plans such as:

- "add controller"
- "write service"
- "optimize SQL"

Prefer plans such as:

- "inspect the existing order module controller and follow its request/response wrapper pattern"
- "add a new request DTO in the same package as peer create APIs"
- "extend the mapper with one batch query to avoid per-item database access"
- "verify whether the current transaction boundary already covers the new persistence flow"

For lightweight plans, short examples like these are acceptable:

- "fix a typo in the request field comment in one DTO file and verify no behavior changes"
- "remove an unused import in one service class and verify the file still compiles cleanly"

## Stop Conditions

Do not start implementation yet if:

- requirement logic is unclear
- the target module is still uncertain
- existing code changes may be required but not yet confirmed
- the consistency strategy for cache, MQ, transaction, lock, or thread usage is unclear

Also do not use a lightweight plan if:

- more than one or two files are likely involved
- business logic may change
- SQL or configuration may change
- interfaces, DTOs, responses, or state transitions may change
- regression risk is not obviously small

## Code Review Exception

For pure code review tasks, output a review plan or review scope summary first, then the findings.

## Transition To Implementation

Only after the plan is clear and blocking ambiguities are resolved should implementation begin.
