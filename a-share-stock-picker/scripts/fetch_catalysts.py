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


def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[_|]+', ' ', text)
    return text


def extract_titles(text, limit=5):
    titles = re.findall(r'<title>(.*?)</title>', text, re.I | re.S)
    cleaned = []
    for t in titles:
        t = clean_text(t)
        if any(ord(ch) < 32 for ch in t):
            continue
        if t and t not in cleaned:
            cleaned.append(t)
        if len(cleaned) >= limit:
            break
    return cleaned


def main():
    if len(sys.argv) < 2:
        print('Usage: fetch_catalysts.py <ticker...>', file=sys.stderr)
        sys.exit(1)
    out = []
    for ticker in sys.argv[1:]:
        ticker = ticker.strip()
        urls = [
            f'https://stockpage.10jqka.com.cn/{ticker}/',
            f'https://basic.10jqka.com.cn/{ticker}/',
        ]
        item = {'ticker': ticker, 'titles': [], 'errors': []}
        for url in urls:
            try:
                txt = fetch(url)
                item['titles'].extend(extract_titles(txt))
            except (URLError, HTTPError, TimeoutError, Exception) as e:
                item['errors'].append(str(e))
        seen = []
        for t in item['titles']:
            if t not in seen and len(t) >= 4:
                seen.append(t)
        item['titles'] = seen[:5]
        out.append(item)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
