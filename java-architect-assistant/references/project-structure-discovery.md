# Project Structure Discovery

Use this guide when the repository layout is not immediately obvious.

## Discovery Order

Inspect in this order:

1. Root-level build and module files
2. Main application modules and starter classes
3. Existing package layout under `src/main/java`
4. Resource layout under `src/main/resources`
5. Neighbor implementations for the same business area

## Placement Heuristics

### Java files

- `controller`: HTTP or RPC entry layer
- `service` or `service/impl`: business orchestration
- `manager`: cross-aggregate coordination if the project already uses it
- `repository`, `dao`, or `mapper`: persistence layer
- `domain`, `entity`, `model`: persistence or domain objects
- `dto`, `req`, `resp`, `vo`: transport models
- `enums`: controlled code sets
- `config`: Spring or framework configuration
- `job`, `schedule`, `task`: scheduled work

Always place a new file next to the closest existing file with the same responsibility.

### SQL and database files

Prefer the repository's existing convention:

- `src/main/resources/mapper/**/*.xml` for MyBatis XML
- `src/main/resources/sql/` for manual SQL scripts
- `src/main/resources/db/migration/` or `db/changelog/` for versioned migrations
- Dedicated module folders when the project is multi-module

Do not invent a new SQL directory if the repository already has one.

### Config files

Check for:

- `application.yml`
- `application.yaml`
- `application.properties`
- environment-specific variants such as `application-dev.yml`
- module-local config under `bootstrap.yml`, `META-INF`, or custom `config/`

Add new configuration where the project already manages that concern.

## Framework Signals

### Spring Boot

Look for:

- `@SpringBootApplication`
- `application.yml`
- `@ConfigurationProperties`
- `@RestController`

### MyBatis or MyBatis-Plus

Look for:

- `@Mapper`
- `BaseMapper`
- `mapperLocations`
- `*Mapper.xml`

### JPA or Hibernate

Look for:

- `@Entity`
- `JpaRepository`
- `CrudRepository`
- `@Table`

### Multi-module projects

If the repository contains multiple modules, determine:

- Which module owns the API
- Which module owns domain logic
- Which module owns persistence
- Which module already contains similar features

Do not place files in a shared or starter module unless that is where peer functionality already lives.

## Safety Checks Before Coding

Before generating files, confirm:

- The target package matches peer packages
- The target resources folder is already used for that file type
- Naming style matches nearby code
- The change fits the module boundary
- There is no existing implementation that should be extended instead
