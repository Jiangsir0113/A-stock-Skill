#!/usr/bin/env python3
import json
import re
import sys
import urllib.request
from urllib.error import URLError, HTTPError

UA = "Mozilla/5.0 (OpenClaw Skill a-share-stock-picker)"
TIMEOUT = 12


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read()
        for enc in ('utf-8', 'gb18030', 'gbk', 'latin1'):
            try:
                return raw.decode(enc)
            except Exception:
                pass
        return raw.decode('utf-8', errors='ignore')


def clean(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('同花顺财经','同花顺财经')
    return text[:220]


def main():
    if len(sys.argv) < 2:
        print('Usage: fetch_news_summary.py <ticker...>', file=sys.stderr)
        sys.exit(1)
    out = []
    for ticker in sys.argv[1:]:
        ticker = ticker[-6:]
        url = f'https://stockpage.10jqka.com.cn/{ticker}/'
        item = {'ticker': ticker, 'summary': None, 'errors': []}
        try:
            txt = fetch(url)
            m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', txt, re.I)
            if m:
                item['summary'] = clean(m.group(1))
            else:
                item['summary'] = clean(txt)
        except (URLError, HTTPError, TimeoutError, Exception) as e:
            item['errors'].append(str(e))
        out.append(item)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
