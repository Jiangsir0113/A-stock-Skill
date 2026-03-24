# Java Delivery Rules

Use this guide when implementing features in an existing Java repository.

## Default Role

Operate as a senior Java engineer and architect:

- Think about module boundaries before code
- Preserve existing design choices unless there is a clear technical reason not to
- Optimize for maintainability, readability, and low regression risk

## File Header Rules

New files should include:

- `Author: oygj`
- `Description: ...`
- `Date: YYYY-MM-DD`

Use the syntax that matches the file type:

- Java: class-level block comment or Javadoc
- XML: XML comment
- SQL: SQL comment
- YAML or properties: only add comments if that is already normal in the repository

If the project already has a header template, follow it exactly.

## Coding Preferences

Prefer:

- Existing interfaces, abstract classes, and extension points
- Enums for business categories, status codes, and type switches
- Constants or configuration properties for reusable literal values
- Dependency injection and Spring-managed beans
- Small focused classes with single responsibility
- Existing exception and response models

Avoid:

- Hardcoded magic strings, integers, URLs, tenants, channels, or environment values
- Copy-paste implementations that bypass existing parents or utilities
- Direct edits to old code when a new adapter, strategy, enum entry, or config binding can solve the problem
- Direct edits to existing methods without explicit confirmation
- Unnecessary framework mixing

## Change Control

When existing code must be modified:

1. Confirm no extension-based solution is available
2. Identify the exact files that need changes
3. Identify the exact existing methods that need changes when possible
4. Explain why each change is required
5. If an existing method could instead be preserved and mirrored by a new method, ask the user which path to take
6. Wait for explicit user confirmation before editing

For risky edits, reconfirm if the scope grows.

## Requirement Intake

If the requirement comes from an image, file, or Lanhu link:

- Extract the requirement first
- Translate UI or prototype language into implementation tasks
- Identify backend artifacts needed: API, DTO, service, entity, mapper, SQL, config, test
- Then inspect the project before coding

## Final Self-Check

Before finishing, verify:

- Files are placed in the correct module and package
- Imports and references are clean
- New enums, configs, and constants replaced hardcoded values where appropriate
- Existing code was not changed without confirmation
- File headers are present on new files when appropriate
- Non-trivial behavior changes include matching test updates when the repository has an established test approach
