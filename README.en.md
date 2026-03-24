# A Share Stock Picker

## Overview

`a-share-stock-picker` is a Codex skill for mainland A-share selection. It is designed for the post-close to pre-open window, where it can build watchlists, analyze short/medium/long horizon candidates, and produce conditional trade plans.

This repository is a complete skill package rather than a plain prompt. It includes:

- `SKILL.md`: the core skill behavior definition
- `references/`: selection frameworks, price rules, output templates, and usage notes
- `scripts/`: helpers for quote fetching, scoring, indicators, catalysts, and report generation
- `agents/`: agent configuration

## Best For

- `推荐股票`
- `盘前选股`
- `按收盘后信息做观察池`
- `给我短中长线标的`
- `给我条件交易计划`

## Key Characteristics

- Mainland A-shares only
- Covers short-term, medium-term, and long-term horizons by default
- Uses the latest completed trading session as the main price anchor
- Interprets setups against 5-day, 20-60 day, and 6-12 month history windows
- Prefers `watchlist / candidate list / conditional trade plan` wording
- Avoids hard buy/sell claims when data freshness or verification is insufficient

## Repository Layout

```text
.
├── LICENSE
├── README.md
├── README.en.md
└── a-share-stock-picker
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

The actual folder to install into Codex is:

```text
a-share-stock-picker/a-share-stock-picker
```

## Built-in Capabilities

### Data and analysis

- Fetches A-share quotes and recent price history
- Calculates MA, ATR, MACD clues, volume ratio, and related indicators
- Pulls catalyst hints, lightweight news summaries, and supporting context
- Scores and buckets candidates into short-, medium-, and long-term groups

### Output behavior

- Produces Chinese Markdown stock-picking reports
- Supports structured table output
- Prefers conditional trading language
- Upgrades to more exact price plans only when the underlying data is fresh and verified

## Main Scripts

- `scripts/fetch_quotes.py`
- `scripts/build_watchlist.py`
- `scripts/fetch_catalysts.py`
- `scripts/indicators.py`
- `scripts/fetch_news_summary.py`
- `scripts/render_report.py`
- `scripts/run_picker.py`

## Usage

### Install into Codex

```bash
cp -R a-share-stock-picker ~/.codex/skills/
```

### Example prompts

```text
Use $a-share-stock-picker to build a pre-open A-share watchlist with 3 short-term, 3 medium-term, and 3 long-term names.
```

```text
Use $a-share-stock-picker to generate a balanced candidate list and a conditional trade plan based on post-close information.
```

### Recommended workflow

- Fetch quotes and recent history first
- Add catalyst, news, and disclosure context
- Produce a watchlist or conditional trade plan last

If exact entry, stop, or target levels are required, the underlying price data should be freshly verified first.

## Notes

- Best suited for the post-close to pre-open window
- Avoid exact conclusions when intraday or stale data has not been verified
- Fall back to watchlist or conditional-plan language when evidence is not strong enough

## License

This repository is licensed under the terms described in [LICENSE](./LICENSE).
