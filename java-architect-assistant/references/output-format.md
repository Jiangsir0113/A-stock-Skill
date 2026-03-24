# Output Format

Use this guide for how to present work to the user during Java development tasks.

## Core Rule

Do not go directly from request to code. First show a concise but structured understanding of the task and a planned path sized to the change.

## Default Pre-Implementation Output

Before coding, output these sections when relevant:

1. Requirement understanding
2. Prototype or PRD analysis
3. Clarifications needed
4. Project structure and style learning summary
5. Task mode
6. Detailed execution plan or lightweight plan
7. Task breakdown and expected goals
8. Files to add
9. Existing files that may need modification
10. Risks and edge cases

For code review tasks, findings replace the implementation-plan-first format.

If the requirement has unreasonable parts, add a short section before the plan:

- unreasonable points
- recommended alternatives

## Section Intent

### Requirement understanding

Summarize what the user really wants, not just the raw text.

### Prototype or PRD analysis

Summarize the backend implications:

- operations
- fields
- validations
- state transitions
- side effects

### Clarifications needed

If key logic is unclear, stop here and ask.

Do not continue pretending the requirement is complete.

If the requirement itself is weak or unreasonable, say so clearly and provide better options before moving on.

### Project structure and style learning summary

Summarize:

- target module
- likely file placement
- nearby peer classes used as reference
- learned conventions such as response wrapper, pagination, exception, log style, and comments

### Task mode

State whether the task is:

- feature development
- bug fixing
- performance optimization
- code review

### Implementation plan

Describe the intended path in detailed executable steps.

This section is mandatory before code changes.

For tiny low-risk changes, this may be a lightweight plan instead of a full detailed plan, but it must still state the intended change, touched file, risk level, and verification approach.

### Task breakdown and expected goals

For development work, split the requirement into small tasks and state the expected goal for each one.

This section should make execution and acceptance easier to follow.

For substantial development work, prefer method-level task breakdown when practical.

After implementation, report method-level goal checks when they materially affected the delivery flow.

For tiny low-risk changes, this section can be omitted if a lightweight plan is clearly enough.

### Files to add

List new files that will likely be created.

### Existing files that may need modification

List old files only when necessary. If confirmation is required, say so clearly.

### Risks and edge cases

Summarize the main technical and business risks.

## Default Post-Implementation Output

After coding, summarize:

1. what was implemented or fixed
2. which project conventions were followed
3. whether old code was modified
4. verification performed, including method-level goal checks, review checkpoints, and test updates or execution when applicable
5. whether review convergence was reached
6. remaining gaps or unverified points

## Code Review Output

For review tasks, output:

1. findings, ordered by severity
2. requirement and business logic assessment
3. performance and SQL assessment
4. maintainability and code bloat assessment
5. open questions or verification gaps
6. brief summary

If there are no findings, say that clearly.

## Brevity Rule

Be structured, but do not be verbose for no reason. Keep each section compact and decision-useful.
