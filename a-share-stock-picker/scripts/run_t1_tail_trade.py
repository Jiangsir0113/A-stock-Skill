#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def run(cmd, outfile):
    with open(outfile, "w", encoding="utf-8") as handle:
        subprocess.run(cmd, check=True, stdout=handle)


def main():
    if len(sys.argv) < 2:
        print("Usage: run_t1_tail_trade.py <ticker...>", file=sys.stderr)
        sys.exit(1)
    tickers = [ticker[-6:] for ticker in sys.argv[1:]]
    work = Path.cwd()
    quotes = work / "tail_quotes.json"
    snapshot = work / "intraday_snapshot.json"
    watchlist = work / "tail_watchlist.json"
    catalysts = work / "tail_catalysts.json"
    news = work / "tail_news_summary.json"
    report = work / "t1_tail_plan.md"

    run(["python3", str(BASE / "fetch_quotes.py"), *tickers], quotes)
    run(["python3", str(BASE / "fetch_intraday_snapshot.py"), str(quotes)], snapshot)
    run(["python3", str(BASE / "build_tail_watchlist.py"), str(quotes), str(snapshot)], watchlist)
    run(["python3", str(BASE / "fetch_catalysts.py"), *tickers], catalysts)
    run(["python3", str(BASE / "fetch_news_summary.py"), *tickers], news)
    run(["python3", str(BASE / "render_t1_plan.py"), str(watchlist), str(catalysts), str(news)], report)

    print(
        json.dumps(
            {
                "quotes": str(quotes),
                "intraday_snapshot": str(snapshot),
                "tail_watchlist": str(watchlist),
                "catalysts": str(catalysts),
                "news_summary": str(news),
                "report": str(report),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
