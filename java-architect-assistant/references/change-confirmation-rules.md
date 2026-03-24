# Change Confirmation Rules

Use this guide whenever an implementation may require edits to existing code.

## Default Principle

Old code is protected by default. Prefer adding new files, new enum values, new config, new mapper methods, or new extension points first.

Existing methods are also protected by default. Do not directly edit an existing method unless the user has clearly approved that path.

## Changes That Require Explicit User Confirmation

- Editing existing business logic branches
- Editing existing methods, especially reused or shared methods
- Editing shared utilities or base classes
- Editing existing controller contracts
- Editing existing DTOs used by old callers
- Editing existing mapper XML with behavior changes
- Editing shared configuration or startup wiring
- Editing authentication, permission, transaction, or scheduler behavior
- Editing public interfaces used across modules

## Recommended Confirmation Message Shape

When confirmation is needed, summarize:

1. why a new-file-only approach is insufficient
2. which existing files need to change
3. which existing methods would be changed, if known
4. whether the alternative is to keep the original method and add a new method instead
5. what behavior may be affected
6. why the risk is acceptable if approved

## Examples

### Safe without confirmation

- Add a new enum
- Add a new request DTO
- Add a new controller endpoint
- Add a new mapper method and matching SQL statement
- Add a new service implementation class
- Add a new migration file in the established folder

### Needs confirmation

- Change an existing method that is already reused elsewhere
- Change a shared service method used by multiple endpoints
- Rewrite a common query used in several reports
- Add fields to an existing response object consumed by old clients
- Change a base class used by many modules
- Modify an existing scheduled task's execution logic

## Reuse Decision Rule

When an existing method looks reusable, do not assume the correct path.

Ask the user to choose between:

1. modify the original method
2. preserve the original method and add a new method modeled after it

Default preference:

- preserve the original method and add a new method unless the user explicitly prefers modifying the original and the risk is acceptable

## After Approval

Even after the user approves:

- keep the edit scope as small as possible
- do not refactor unrelated old code in the same pass
- preserve behavior outside the requested change
