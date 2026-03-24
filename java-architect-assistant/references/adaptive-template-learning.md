# Adaptive Template Learning

Use this guide when the user wants templates or code generation, but the repository already has existing conventions.

## Core Principle

Templates must be learned from the current project, not imposed from outside.

Before generating any new `Controller`, `Service`, `Mapper`, `DTO`, `VO`, `Entity`, or related file, inspect nearby peer implementations and infer the local style.

## Learning Order

Inspect in this order:

1. Same module, same business domain, same layer
2. Same module, similar business domain, same layer
3. Same repository, same layer
4. Shared base abstractions or starter patterns

Prefer the nearest peer style over a more general repository-wide style.

## What To Extract

For each new file type, extract these conventions from existing code:

- class naming pattern
- package naming pattern
- annotations used
- inheritance and interface pattern
- constructor injection or field injection style
- method naming and parameter order
- request and response object naming
- converter or assembler usage
- return wrapper style
- pagination style
- logger declaration style
- file header style

## Minimum Evidence Rule

Before imitating a style, try to inspect at least 2 peer files of the same kind.

If only 1 peer file exists, follow it but note that the pattern confidence is lower.

If no peer files exist:

- fall back to repository-wide patterns
- keep the implementation conservative
- avoid inventing framework-heavy abstractions

## Multi-Style Repositories

If the repository contains multiple styles:

- do not normalize the whole codebase
- compare the closest target-module style with other recent styles in the repository
- prefer the style that is structurally cleaner and more recent when that choice will not create obvious inconsistency with the target area
- if the nearest target-module style is clearly required for local compatibility, keep following it and say so briefly
- keep new code consistent with that local area

## Cleanliness And Recency Preference

When judging between multiple existing styles, prefer the one that has:

- clearer layering
- cleaner naming
- less bloated structure
- fewer obvious historical leftovers
- more recent usage dates or more recently edited peer files

Do not choose an older messy pattern just because it exists nearby, unless the target module is tightly coupled to that exact style and changing the local pattern would raise compatibility risk.

## Generated Template Behavior

When producing a new file, the template should be described mentally as:

- "same as the nearest peer, with the business names and fields replaced"

not as:

- "a generic Spring Boot template"

## Things To Never Fix Globally

Do not force replacement of existing project styles for:

- logger framework choice
- pagination model type
- result wrapper class
- exception hierarchy
- DTO versus VO naming
- `Service` versus `Manager` split
- `Mapper` versus `Repository` naming

The repository decides these, not the skill.
