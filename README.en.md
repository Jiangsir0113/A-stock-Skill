# Codex Skills Collection

## Overview

This repository contains two reusable skills for Codex:

- `a-share-stock-picker`: selects mainland A-share candidates and produces watchlists or conditional trade plans for the post-close to pre-open window
- `java-architect-assistant`: supports requirement analysis, feature delivery, bug fixing, performance work, and code review in existing Java projects

These are not generic prompt snippets. Each skill includes a defined workflow, reference materials, helper scripts, and output standards.

## Repository Structure

```text
.
├── README.md
├── README.en.md
├── LICENSE
├── a-share-stock-picker
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
└── java-architect-assistant
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

## Skills At A Glance

| Skill | Best for | Highlights |
| --- | --- | --- |
| `a-share-stock-picker` | A-share ideas, pre-open watchlists, short/medium/long horizon candidates, conditional trade plans | Uses the latest completed trading session as the anchor, combines price history, catalysts, disclosures, and horizon-based scoring, and defaults to watchlist-style output instead of blind buy calls |
| `java-architect-assistant` | Java feature work, bug fixing, performance optimization, code review, PRD/prototype analysis | Learns the requirement and project structure first, plans before coding, favors low-intrusion delivery, and requires explicit confirmation before changing old code or old methods |

## Installation

### Option 1: Copy skills into the Codex skills directory

Copy the skill folders you want into your local Codex skills directory:

```bash
cp -R a-share-stock-picker ~/.codex/skills/
cp -R java-architect-assistant ~/.codex/skills/
```

You can install either skill independently or both together.

### Option 2: Keep this repository as a local skill workspace

If you want to maintain or extend the skills, keep the whole repository locally and sync individual skill folders into `~/.codex/skills/` when needed.

## Usage

### 1. `a-share-stock-picker`

#### Typical use cases

- `推荐股票`
- `盘前选股`
- `按收盘后信息做观察池`
- `给我短中长线标的`
- `给我条件交易计划`

#### How it works

- Covers short-term, medium-term, and long-term horizons by default
- Uses the latest completed trading session as the main price anchor
- Interprets names against 5-day, 20-60 day, and 6-12 month history windows
- Prefers `watchlist / candidate list / conditional plan` wording
- Only gives more exact entry, stop, and target levels when price freshness is verified

#### Built-in capabilities

- Fetches A-share quotes and recent price history
- Calculates MA, ATR, MACD clues, volume ratio, and related indicators
- Pulls catalyst hints, lightweight news summaries, and market context
- Renders a Chinese Markdown watchlist report

#### Main scripts

- `scripts/fetch_quotes.py`
- `scripts/build_watchlist.py`
- `scripts/fetch_catalysts.py`
- `scripts/indicators.py`
- `scripts/fetch_news_summary.py`
- `scripts/render_report.py`
- `scripts/run_picker.py`

#### Example prompts

```text
Use $a-share-stock-picker to build a pre-open A-share watchlist with 3 short-term, 3 medium-term, and 3 long-term names.
```

```text
Use $a-share-stock-picker to generate a balanced candidate list and conditional trade plan based on post-close information.
```

#### Notes

- Mainland A-shares only
- Best suited for the post-close to pre-open operating window
- Should not be used for absolute buy/sell calls when prices are stale or unverified

### 2. `java-architect-assistant`

#### Typical use cases

- Java feature development
- Bug fixing
- Performance optimization
- Code review
- PRD, prototype, screenshot, and Lanhu requirement analysis
- Generating Java, SQL, and config changes that match the current repository style

#### How it works

- Understands the requirement first, then inspects project structure and coding conventions
- Produces a plan before implementation
- Defaults to low-intrusion delivery
- Prefers adding new files or extension points over risky rewrites
- Requires explicit confirmation before modifying existing code, especially existing methods

#### Key capabilities

- Discovers modules, package layout, layers, and resource directories
- Learns local templates for controllers, services, mappers, DTOs, VOs, and related artifacts
- Plans for SQL, transaction, cache, MQ, lock, thread, and interface impact before coding
- Supports URL-based requirement intake through the built-in MCP URL reader

#### Example prompts

```text
Use $java-architect-assistant to handle this requirement.
First analyze the requirement and the current project style, then produce a plan, then implement.
Do not modify existing methods without my approval; if reuse is possible, ask whether to edit the old method or create a new one.
```

```text
Use $java-architect-assistant to fix this bug.
I will provide logs and related code. First locate the root cause and give me a repair plan.
```

```text
Use $java-architect-assistant to show the usage guide.
```

#### URL / PRD access

When the requirement comes from a URL, PRD, or Lanhu page, start the local MCP helper first:

```bash
bash /Users/tudoushaoyangyu/.codex/skills/java-architect-assistant/scripts/start_url_reader_mcp.sh
```

If the page requires authentication, provide the necessary headers, cookies, or other access context as well.

## Design Principles

### `a-share-stock-picker`

- Evidence first
- Watchlist-first phrasing when certainty is limited
- Exact price plans only when based on fresh, verified data plus recent structure

### `java-architect-assistant`

- Understanding before editing
- Planning before coding
- Extension before rewrite
- Configuration, constants, and enums before hardcoded literals
- No old-code or old-method changes without explicit confirmation

## Who This Repo Is For

- People who want reusable Codex workflows instead of one-off prompts
- Teams that want to package domain-specific process, scripts, and references into skills
- Users who want a more repeatable workflow for stock analysis or Java delivery tasks

## Contributing

1. Fork the repository
2. Create a new branch for your changes
3. Update `SKILL.md`, `references/`, or `scripts/` as needed
4. Submit a Pull Request

## License

This repository is licensed under the terms described in [LICENSE](./LICENSE).
