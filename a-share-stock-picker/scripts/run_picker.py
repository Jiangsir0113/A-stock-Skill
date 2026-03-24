#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def run(cmd, outfile):
    with open(outfile, 'w', encoding='utf-8') as f:
        subprocess.run(cmd, check=True, stdout=f)


def main():
    if len(sys.argv) < 2:
        print('Usage: run_picker.py <ticker...>', file=sys.stderr)
        sys.exit(1)
    tickers = sys.argv[1:]
    work = Path.cwd()
    quotes = work / 'quotes.json'
    watchlist = work / 'watchlist.json'
    catalysts = work / 'catalysts.json'
    indicators = work / 'indicators.json'
    news = work / 'news_summary.json'
    report = work / 'report.md'
    run(['python3', str(BASE / 'fetch_quotes.py'), *tickers], quotes)
    run(['python3', str(BASE / 'build_watchlist.py'), str(quotes)], watchlist)
    run(['python3', str(BASE / 'fetch_catalysts.py'), *[t[-6:] for t in tickers]], catalysts)
    run(['python3', str(BASE / 'indicators.py'), str(quotes)], indicators)
    run(['python3', str(BASE / 'fetch_news_summary.py'), *[t[-6:] for t in tickers]], news)
    run(['python3', str(BASE / 'render_report.py'), str(watchlist), str(catalysts), str(indicators), str(news)], report)
    print(json.dumps({
        'quotes': str(quotes),
        'watchlist': str(watchlist),
        'catalysts': str(catalysts),
        'indicators': str(indicators),
        'news_summary': str(news),
        'report': str(report)
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
