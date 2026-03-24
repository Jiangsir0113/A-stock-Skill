# API Conventions

Use this guide to learn and reuse the current repository's API-layer conventions.

## Response Wrapper

Before generating any endpoint, inspect whether the project uses:

- a common `Result`, `Response`, `ApiResponse`, `CommonResult`, `R`, or similar wrapper
- direct object return for internal services
- helper factories such as `success()`, `fail()`, `ok()`, `error()`

Reuse the existing wrapper and factory methods. Do not introduce a new response envelope if the repository already has one.

If multiple wrappers exist, use the one already used in the target module.

## Pagination

Before adding query endpoints, inspect whether pagination uses:

- MyBatis-Plus `Page<T>` or `IPage<T>`
- custom `PageResult`, `PageResponse`, `PageVO`, `PageDTO`
- request types such as `PageQuery`, `PageReq`, `BasePageReq`
- controller-level page parameters or encapsulated request objects

Reuse the exact local pattern:

- request field names such as `pageNum`, `pageNo`, `current`, `pageSize`
- response field names such as `total`, `records`, `list`, `rows`
- conversion utilities or page assemblers

Do not create a new pagination model if the project already has a standard one.

## Exception Codes

Before handling business errors, inspect whether the project uses:

- enum-based error codes
- static constants
- custom exception classes carrying code and message
- global exception handlers with standard response mapping

Reuse the existing code source and throw pattern.

Do not hardcode business error messages or integer codes in service logic if the repository already centralizes them.

## Logging

Before writing logs, inspect:

- whether the project uses `@Slf4j`, `LoggerFactory`, or inherited loggers
- message style such as key-value, plain Chinese, plain English, or parameterized placeholders
- what layers are expected to log business events
- whether request parameters or sensitive fields are masked

Reuse the local logging pattern.

Avoid:

- noisy logs on hot paths without precedent
- logging sensitive data
- mixing several log styles in one module

## Controller and DTO Shape

Before generating `Controller`, `DTO`, `Req`, `Resp`, or `VO`, inspect:

- whether validation annotations are placed on DTO fields or controller method params
- whether swagger or OpenAPI annotations are already used
- whether field comments are written as Javadoc, Swagger annotations, or not at all
- whether `VO` and `DTO` are distinct concepts in the repository

Follow the local convention instead of trying to standardize it.
