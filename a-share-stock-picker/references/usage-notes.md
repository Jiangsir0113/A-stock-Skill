# Usage Notes

Use this file for practical response shaping.

## Default Positioning

Default to:

- `盘前选股战报`
- `观察池`
- `候选名单`
- `条件交易计划`

Prefer these over hard, context-free buy/sell touting.

## Balanced-Style Preference

If the user asks for a `均衡型` list, bias toward:

- industry leaders
- strong liquidity
- clearer disclosure/fundamental support
- lower dependence on pure rumor-driven momentum

## When To Be More Cautious

Be extra cautious when:

- the request is specifically for `明天买什么`
- exact prices cannot be freshly verified
- the market is highly sentiment-driven
- the best candidates are all thinly traded or highly extended

In those cases, keep the plan conditional and explain the skip conditions clearly.

## Execution Preference

Prefer this execution sequence:

1. Run `scripts/fetch_quotes.py` for candidate tickers
2. If machine-readable Tonghuashun data is available, use it as the anchor
3. If Tonghuashun fails, keep Eastmoney/Sina as context-only fallback unless you can parse them confidently
4. Run `scripts/build_watchlist.py` on the fetched JSON to score and bucket candidates
5. Run `scripts/fetch_catalysts.py` for lightweight catalyst/title clues
6. Run `scripts/indicators.py` for MA/ATR/MACD clue and volume-ratio context
7. Run `scripts/fetch_news_summary.py` for lightweight page summaries
8. Run `scripts/render_report.py` on the watchlist JSON to produce the Chinese markdown output
9. Or use `scripts/run_picker.py` as the one-shot wrapper
10. Upgrade to exact price plans only after verifying freshness and structure

## Tail-Entry Preference

If the user wants a practical `T+1` short-term workflow:

1. use the normal post-close or pre-open flow to build a larger candidate pool
2. during trading day `D`, refresh quotes in the final hour
3. run `scripts/fetch_intraday_snapshot.py` on the quote payload
4. run `scripts/build_tail_watchlist.py` to score names for tail entry quality
5. render the result with `scripts/render_t1_plan.py`
6. or use `scripts/run_t1_tail_trade.py` as the one-shot wrapper

In this mode, prefer wording such as:

- `今日尾盘建仓计划`
- `D+1卖出计划`
- `高开先兑现`
- `低开跌破隔夜止损线则保护离场`
