---
name: a-share-stock-picker
description: Analyze mainland A-share candidates across short-, medium-, and long-term horizons using the latest completed session as the price anchor plus recent history, market context, policy/news catalysts, and official disclosures. Use when asked to review, rank, or produce an A-share watchlist or trading plan for the post-close to pre-open window, especially requests such as "推荐股票", "盘前选股", "给我短中长线标的", or "按收盘后信息做观察池/交易计划". Do not use for blind direct buy/sell touting without evidence; prefer evidence-based watchlists and conditional plans.
---

# A Share Stock Picker

## Overview

Recommend mainland A-share candidates for three horizons in one pass: short term, medium term, and long term. Use the latest completed trading session plus overnight information up to the answer time.

Default to an evidence-based watchlist with conditional entry plans rather than unconditional "buy these tomorrow" language. If the user explicitly wants exact entry, stop, and target levels, provide them only when the underlying price data is fresh and verified.

Only cover mainland A-shares. Do not recommend Hong Kong stocks, US equities, ETFs, funds, or convertibles unless the user explicitly asks for them.

## Scripts

Use bundled scripts when possible:

- `scripts/fetch_quotes.py <ticker...>`: fetch machine-readable Tonghuashun data plus public fallback sources for one or more A-share tickers
- `scripts/build_watchlist.py <quotes.json>`: score candidates and convert fetched quote data into short/medium/long watchlist buckets
- `scripts/fetch_catalysts.py <ticker...>`: fetch lightweight catalyst/title clues from public stock pages
- `scripts/indicators.py <quotes.json>`: calculate basic technical indicators such as MA, ATR, MACD clue, and volume ratio
- `scripts/fetch_news_summary.py <ticker...>`: fetch lightweight page-description summaries as catalyst context
- `scripts/render_report.py <watchlist.json> [catalysts.json] [indicators.json] [news_summary.json]`: render a Chinese markdown watchlist report with names, sectors, indicators, and conditional trade-plan wording
- `scripts/run_picker.py <ticker...>`: one-shot entry point that fetches quotes, scores candidates, pulls catalyst clues, computes indicators, and writes the final report

## Operating Window

Default operating window:

- Start: after the previous trading day officially closes
- End: before the next trading day opens

Use the latest completed session as the main price anchor. Add overnight policy, company, and macro updates that arrive before the answer is produced.

If the user asks during trading hours, say that this skill is optimized for the post-close to pre-open window and adapt cautiously.

## Workflow

### 1. Confirm the scope

Assume the user wants:

- Exactly 3 short-term A-share picks
- Exactly 3 medium-term A-share picks
- Exactly 3 long-term A-share picks

Do not duplicate names across horizons by default. Reuse a name across horizons only if it is unusually strong and you explicitly justify the overlap.

### 2. Pull data proactively

Always fetch market data yourself. Do not rely on the user to provide prices.

For A-shares, start with bundled probing scripts and Tonghuashun machine-readable endpoints first, then use page snippets and fallback public quote pages for context:

- `scripts/fetch_quotes.py <ticker...>`
- `https://d.10jqka.com.cn/v2/line/<market>_<ticker>/01/today.js`
- `https://d.10jqka.com.cn/v2/line/<market>_<ticker>/01/last.js`
- `https://d.10jqka.com.cn/v6/time/hs_<ticker>/defer/last.js`
- `https://stockpage.10jqka.com.cn/<ticker>/`
- `https://basic.10jqka.com.cn/<ticker>/`
- `https://q.10jqka.com.cn/`
- Eastmoney and Sina public quote pages as fallback context sources

Where:

- `<market>` is `sh` for Shanghai tickers and `sz` for Shenzhen tickers
- `<ticker>` is the 6-digit A-share code

Use the endpoints in this order:

1. `today.js` for the latest completed session's exact open, high, low, close, amount, and turnover
2. `last.js` for recent daily history and the previous trading session's open and close
3. `v6/time/.../defer/last.js` for intraday or same-day minute structure when needed
4. `stockpage.10jqka.com.cn` and `q.10jqka.com.cn` for news, reports, sector strength, and concept context

Use them to retrieve:

- Latest completed-session close
- Latest completed-session open
- Recent highs and lows
- Recent turnover,成交额, and volume behavior
- Sector or concept strength
- Recent relative performance
- Same-day minute path when short-term execution depends on intraday behavior

Minimum history windows:

- Short term: at least 5 trading days
- Medium term: at least 20-60 trading days
- Long term: at least 6-12 months

Never base a recommendation on the latest completed session alone. The latest day is only the anchor day. Every recommendation must be interpreted against the relevant historical window above.

If an exact buy or sell price is provided, it must be anchored to the latest completed session and recent price structure. Do not invent precise levels from stale data.

If Tonghuashun exposes a machine-readable price endpoint, prefer it over scraping visible HTML text from the page.

### 3. Build the evidence pack

For each candidate, collect evidence from three buckets:

1. Price and market structure
2. Policy, news, or company-specific catalysts
3. Official disclosures or company fundamentals

Every final pick should have at least:

- One price/volume reason
- One policy/news/company-event reason
- One structural reason such as industry position, earnings trend, or valuation support

Prefer:

- Tonghuashun quote and market pages for price/history/context
- Exchange and company disclosures for official facts
- Official policy sources and reputable financial media for catalyst context

### 4. Score by horizon

Use the horizon-specific framework in the references:

- Short term: momentum, sentiment, turnover, trigger quality, next-session tradability
- Medium term: earnings momentum, estimate revisions, 20-60 day structure, next-quarter catalysts
- Long term: business quality, balance sheet, valuation band, long-duration thesis

When the user wants exact buy, stop, or target prices, also load:

- `references/price-plan-rules.md`

### 5. Produce the final list

Default output:

- 3 short-term picks
- 3 medium-term picks
- 3 long-term picks

If you genuinely cannot support 3 high-quality names for a horizon, say that clearly and explain what evidence is missing. Do not pad with weak names just to fill the quota.

Prefer "观察池 / 候选名单 / 条件计划" wording. When a direct buy recommendation would be too speculative, convert the answer into conditional language such as:

- `若明日放量站稳前高再看`
- `仅在回踩支撑不破时考虑`
- `高开过多则放弃`

## Safety And Quality Guardrails

- Do not pretend to have live verified prices if the sources cannot be fetched.
- Do not invent exact buy, stop, or target levels from stale or conflicting data.
- Do not force all 9 names if the evidence quality is weak.
- Prefer large, liquid, information-rich names when the user asks for a balanced style.
- If the market regime is unclear, say so and bias toward watchlist language and risk controls.

## Output Standard

Use three sections in this order:

1. Short-term picks
2. Medium-term picks
3. Long-term picks

Each section should start with a compact table:

`股票 | 上个交易日开盘价 | 上个交易日收盘价 | 形态类型 | 关键支撑 | 关键阻力 | 核心逻辑 | 买入时间 | 触发买价 | 止损价 | 第一目标 | 第二目标 | 风险收益比 | 卖出时间 | 持有周期 | 不买条件`

Write the section as a Markdown table in this shape:

```markdown
| 股票 | 上个交易日开盘价 | 上个交易日收盘价 | 形态类型 | 关键支撑 | 关键阻力 | 核心逻辑 | 买入时间 | 触发买价 | 止损价 | 第一目标 | 第二目标 | 风险收益比 | 卖出时间 | 持有周期 | 不买条件 |
|---|---:|---:|---|---:|---:|---|---|---:|---:|---:|---:|---|---|---|---|
| 示例股票 `000000` | 10.00 | 10.20 | 突破型 | 9.85 | 10.60 | 一句话说明逻辑 | 2026-03-20 9:35-10:30 | 10.22 | 9.84 | 10.60 | 11.00 | 1:2.1 | 第一目标减仓，第二目标再评估 | 1-3天 | 高开过猛且放量不续强则不买 |
```

Below each table, add short evidence notes for each name:

- Why it was selected
- Which policy/news/disclosure mattered
- Which price/history facts mattered

## Price Rules

- Exact price levels must be based on the latest completed session plus recent history
- Every stock row must include the previous trading session's open and close
- Prefer `today.js` for the current anchor day and `last.js` for the previous session and recent daily structure
- Use `v6/time/.../defer/last.js` only as a supplement for minute-path confirmation, not as the sole source for previous-session OHLC
- Never derive buy, stop, or target levels from same-day OHLC alone; use the relevant 5-day, 20-60 day, or 6-12 month structure first
- Exact prices are allowed only when the anchor price is fresh and clearly verified
- If freshness or verification is insufficient, switch to conditional trigger language
- If a new verified price conflicts with an older working price, discard the old plan immediately

## Buy And Sell Timing Rules

Use horizon-appropriate timing language:

- Short term: next trading day opening session, early pullback, breakout confirmation, or next 1-3 trading days
- Medium term: next 1-5 trading days for entry, next 2-12 weeks for exit or review
- Long term: staged entry over the next 5-20 trading days, thesis review over 6-24 months

When giving exact levels, explain them as structure-based levels derived from Tonghuashun session data, recent highs/lows, and turnover behavior rather than as guarantees.

## Reference Files

Load:

- `references/data-sources-and-window.md` for source priority and operating window
- `references/horizon-selection-framework.md` for short/medium/long scoring
- `references/price-plan-rules.md` for buy, stop, and target derivation
- `references/output-template.md` for the final answer format
- `references/usage-notes.md` for watchlist-first phrasing and balanced-style response shaping
