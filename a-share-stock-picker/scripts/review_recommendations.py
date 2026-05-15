#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def quote_anchor(item):
    sources = item.get("sources") or {}
    anchor = sources.get("10jqka_today") or {}
    if not isinstance(anchor, dict):
        anchor = {}
    return {
        "ticker": item.get("ticker"),
        "date": anchor.get("date"),
        "open": to_float(anchor.get("open")),
        "high": to_float(anchor.get("high")),
        "low": to_float(anchor.get("low")),
        "close": to_float(anchor.get("close")),
    }


def pct(base, current):
    if base in (None, 0) or current is None:
        return None
    return (current - base) / base * 100.0


def iter_recommendations(watchlist):
    for bucket in ("short", "medium", "long", "tail_entry"):
        for row in watchlist.get(bucket, []) or []:
            yield bucket, row


def row_level(row, *keys):
    for key in keys:
        value = to_float(row.get(key))
        if value is not None:
            return value
    return None


def review_recommendations(watchlist, next_quotes):
    quote_map = {item.get("ticker"): quote_anchor(item) for item in next_quotes}
    items = []
    summary = {"total": 0, "triggered": 0, "hitTarget1": 0, "stopped": 0, "noTrigger": 0}

    for bucket, row in iter_recommendations(watchlist):
        ticker = row.get("ticker")
        quote = quote_map.get(ticker) or {}
        trigger = row_level(row, "triggerPrice", "entryLow", "close", "todayClose")
        stop = row_level(row, "stopPrice", "stop")
        target1 = row_level(row, "target1")
        high = quote.get("high")
        low = quote.get("low")
        close = quote.get("close")
        summary["total"] += 1

        triggered = trigger is not None and high is not None and high >= trigger
        if not triggered:
            outcome = "not_triggered"
            summary["noTrigger"] += 1
        elif target1 is not None and high is not None and high >= target1:
            outcome = "hit_target1"
            summary["triggered"] += 1
            summary["hitTarget1"] += 1
        elif stop is not None and low is not None and low <= stop:
            outcome = "stopped"
            summary["triggered"] += 1
            summary["stopped"] += 1
        else:
            outcome = "open"
            summary["triggered"] += 1

        items.append(
            {
                "ticker": ticker,
                "bucket": bucket,
                "date": quote.get("date"),
                "triggered": triggered,
                "outcome": outcome,
                "maxGainPct": pct(trigger, high),
                "maxDrawdownPct": pct(trigger, low),
                "closeReturnPct": pct(trigger, close),
                "trigger": trigger,
                "stop": stop,
                "target1": target1,
            }
        )

    return {"summary": summary, "items": items}


def main():
    if len(sys.argv) != 3:
        print("Usage: review_recommendations.py <watchlist.json> <next_quotes.json>", file=sys.stderr)
        sys.exit(1)
    watchlist = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    next_quotes = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    print(json.dumps(review_recommendations(watchlist, next_quotes), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
