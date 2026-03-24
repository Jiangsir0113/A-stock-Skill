# Usage Guide

Use this guide when the user asks for help, manual, or usage instructions for `$java-architect-assistant`.

## Core Invocation

The safest way to use this skill is to call it explicitly:

`使用 $java-architect-assistant ...`

## Help Commands

Before development, the user can call the usage guide with prompts like:

- `使用 $java-architect-assistant 显示使用说明`
- `使用 $java-architect-assistant 先给我使用说明`
- `使用 $java-architect-assistant 帮助`
- `使用 $java-architect-assistant 告诉我怎么用`

When the user asks for help this way, show the usage guide first instead of starting implementation immediately.

## What The Skill Supports

This skill supports:

- feature development
- bug fixing
- performance optimization
- code review

It also supports:

- PRD analysis
- prototype and screenshot analysis
- Lanhu-based requirement intake
- URL access through the built-in MCP URL reader
- Java project structure discovery
- adaptive template learning from the current repository
- SQL and index design review
- old-code modification confirmation flow

## Recommended User Prompt Structure

A good request usually includes:

1. task type
2. requirement source
3. target module or page
4. whether old code may be modified
5. whether old methods may be modified
6. any testing, performance, or compatibility expectations

## Recommended Standard Prompt

```text
使用 $java-architect-assistant 处理这个需求。
先分析需求/原型/PRD，学习当前工程风格，输出计划，再执行。
未经我同意不要改原有方法；如果要复用旧方法，先问我是改原方法还是新写方法。
```

## Common Examples

### Feature development

```text
使用 $java-architect-assistant 根据这份 PRD 和蓝湖链接实现功能。
先给我详细执行计划，再开始改代码。
```

### Bug fixing

```text
使用 $java-architect-assistant 修复这个 bug。
我会提供报错日志和相关代码，你先定位根因并给修复计划。
```

### Performance optimization

```text
使用 $java-architect-assistant 优化这个慢接口。
先分析瓶颈、SQL 和循环查库问题，再给优化方案。
```

### Code review

```text
使用 $java-architect-assistant 审查这次改动。
重点检查需求符合度、业务逻辑、性能、SQL、事务风险、代码臃肿度。
```

### Show usage guide first

```text
使用 $java-architect-assistant 显示使用说明
```

### URL-based requirement intake

```text
使用 $java-architect-assistant 分析这个 PRD 链接。
先通过 MCP 访问网址内容，再给我需求分析和执行计划。
```

Before URL-based work, start the local MCP first:

```bash
bash /Users/tudoushaoyangyu/.codex/skills/java-architect-assistant/scripts/start_url_reader_mcp.sh
```

If the page needs login, also tell the skill that headers or cookies may be required.

## Key Behavior Guarantees

The skill will generally:

- analyze requirement sources before coding
- ask for clarification when logic is unclear
- point out unreasonable requirements and give alternatives
- learn the current project structure and style first
- output a detailed or lightweight plan before code changes
- avoid changing old methods without approval
- ask whether to modify an old method or create a new one when reuse is possible
- prefer low-intrusion implementation
- check SQL, performance, loops, and maintainability

## What The User Should Confirm Explicitly

The user should answer clearly when asked about:

- whether old code can be modified
- whether existing methods can be modified
- whether to modify an existing method or add a new one
- which alternative to choose if the requirement is unreasonable
- whether higher-impact changes such as transaction boundary, cache, MQ, lock, or async changes are acceptable
