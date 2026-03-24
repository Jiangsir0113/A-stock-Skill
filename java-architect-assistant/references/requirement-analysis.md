# Requirement Analysis

Use this guide whenever the user provides a prototype, PRD, screenshot, file, or Lanhu link.

## Core Principle

Do not start coding just because a screen looks simple. First understand the real business requirement behind the prototype or PRD.

## What To Extract

Before implementation, identify:

- business goal
- target users and usage scenario
- operation flow
- field meanings
- required versus optional fields
- default values
- validation rules
- status values and transitions
- permissions and visibility scope
- external dependencies
- side effects such as notifications, MQ events, cache refresh, audit records, or async tasks
- unreasonable, conflicting, or high-risk requirement points

## Prototype Analysis Rules

When reading a prototype or screenshot:

- distinguish display fields from persisted fields
- distinguish button labels from actual backend operations
- infer whether the page is query, detail, create, edit, submit, approve, or batch operation
- identify hidden state transitions behind visible actions
- identify list filters, sort rules, pagination rules, and export behavior if present

Do not assume missing backend logic from UI visuals alone.

## PRD Analysis Rules

When reading a PRD:

- separate mandatory requirements from examples
- identify business rules, edge cases, and forbidden operations
- note any contradictory text or missing data rules
- identify whether the PRD changes interface contracts, status machines, or existing behavior

## Mandatory Clarification Rule

If any of the following is unclear, ask the user before implementation:

- business rule conflicts
- state transition ambiguity
- field semantics that affect persistence or validation
- permission ambiguity
- callback or downstream behavior ambiguity
- data source ambiguity
- success or failure handling ambiguity

Do not pretend certainty when the requirement is incomplete.

If any of the following appears unreasonable, point it out and ask for confirmation before implementation:

- requirement conflicts with existing system boundaries or architecture
- requirement introduces high complexity for low value
- requirement creates obvious performance, consistency, or maintainability risk
- requirement duplicates an existing capability in a worse way
- requirement forces poor UX or weak business control

Do not simply obey a weak requirement when a better option is obvious.

## Suggestion Rule

When calling out an unreasonable requirement, always provide:

1. the problematic point
2. why it is problematic
3. one or more effective alternatives
4. your recommended option

## Output During Analysis

Before coding, summarize:

1. what the requirement is asking for
2. what backend behaviors are implied
3. what is already clear
4. what still needs clarification
5. what looks unreasonable and what you recommend instead
