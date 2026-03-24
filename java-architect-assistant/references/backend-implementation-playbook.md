# Backend Implementation Playbook

Use this guide when turning a requirement into concrete backend code changes.

## Default Delivery Chain

For standard business requirements, inspect and implement in this order:

1. Request entry
2. Request and response models
3. Service contract
4. Business orchestration
5. Persistence contract
6. Persistence implementation
7. Config, enum, constant, and test updates

For non-trivial feature or behavior changes, do not stop at manual verification if the repository already has an established automated test style. Add or update tests when the change can be covered reasonably.

## Layer Responsibilities

### Controller or facade

Responsible for:

- Request mapping
- Parameter binding and validation
- Calling the service layer
- Returning the repository's existing response wrapper style

Avoid placing core business logic in controllers.

### DTO, request, response, VO

Use peer naming conventions such as:

- `CreateXxxReq`
- `UpdateXxxReq`
- `QueryXxxReq`
- `XxxResp`
- `XxxVO`

If the project already splits internal DTOs and external request objects, keep that separation.

### Service

Service interfaces define business capabilities.

Service implementations handle:

- Transaction boundaries when appropriate
- Business validation not handled by annotations
- Cross-component coordination
- Calls to manager, repository, mapper, or DAO layers

### Manager or domain service

If the project uses `manager` or domain-service style classes, place reusable domain orchestration there instead of bloating service implementations.

### Persistence layer

Use the project's existing persistence abstraction:

- `Mapper` for MyBatis or MyBatis-Plus
- `Repository` for JPA
- `DAO` when the project already names it that way

## Typical Requirement Mapping

### Add a new query API

Usually involves:

- controller endpoint
- request object
- response object or VO
- service method
- mapper or repository method
- SQL or XML if needed

### Add a create or update flow

Usually involves:

- controller endpoint
- validated request object
- service method
- transaction handling
- entity or DO mapping
- persistence insert or update
- enum or config additions if status or type values are introduced

### Add backend support for a new UI field

Trace the field through the full chain:

1. API contract
2. request or response object
3. service logic
4. converter or assembler
5. entity or DO
6. SQL or repository projection

Do not patch only one layer and assume the flow is complete.

## Naming and Reuse

Prefer extending existing nearby methods over inventing a second style for the same capability.

Reuse existing:

- validation annotations
- response wrappers
- converters
- page query wrappers
- exception patterns
- logging style

## Final Checks

Before finishing, confirm:

- The implementation follows the repository's existing layer boundaries
- No business logic was stuffed into controllers
- New types and statuses use enums or constants where appropriate
- The request-to-database chain is complete
- Newly added or modified methods have been checked against their planned expected goals
