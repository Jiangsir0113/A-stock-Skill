#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def to_float(v):
    try:
        return float(v)
    except Exception:
        return None


def pct(a, b):
    if a in (None, 0) or b is None:
        return None
    return (b - a) / a * 100.0


def summarize_rows(rows):
    if not rows:
        return {}
    closes = [to_float(r.get('close')) for r in rows if to_float(r.get('close')) is not None]
    highs = [to_float(r.get('high')) for r in rows if to_float(r.get('high')) is not None]
    lows = [to_float(r.get('low')) for r in rows if to_float(r.get('low')) is not None]
    vols = [to_float(r.get('volume')) for r in rows if to_float(r.get('volume')) is not None]
    if not closes:
        return {}
    last_close = closes[-1]
    prev_close = closes[-2] if len(closes) >= 2 else None
    return {
        'last_close': last_close,
        'prev_close': prev_close,
        'chg_1d': pct(prev_close, last_close) if prev_close is not None else None,
        'high_5': max(highs[-5:]) if highs else None,
        'low_5': min(lows[-5:]) if lows else None,
        'high_20': max(highs[-20:]) if highs else (max(highs) if highs else None),
        'low_20': min(lows[-20:]) if lows else (min(lows) if lows else None),
        'avg_vol_5': sum(vols[-5:]) / len(vols[-5:]) if len(vols) >= 5 else (sum(vols) / len(vols) if vols else None),
        'rows': len(rows),
    }


def score_bucket(summary, status):
    short = 40
    medium = 45
    long = 50
    if status == 'verified':
        short += 10; medium += 10; long += 10
    chg = summary.get('chg_1d')
    if chg is not None:
        if 0 < chg < 4:
            short += 12; medium += 8
        elif chg >= 4:
            short += 6; medium += 4
        elif chg < 0:
            short -= 6; medium -= 4
    rows = summary.get('rows', 0)
    if rows >= 20:
        medium += 10; long += 8
    if rows >= 60:
        long += 10
    last_close = summary.get('last_close')
    high_20 = summary.get('high_20')
    low_20 = summary.get('low_20')
    high_5 = summary.get('high_5')
    low_5 = summary.get('low_5')
    if None not in (last_close, high_20, low_20) and high_20 != low_20:
        pos20 = (last_close - low_20) / (high_20 - low_20)
        if pos20 > 0.7:
            short += 8; medium += 8
        elif pos20 < 0.3:
            long += 4
    if None not in (last_close, high_5, low_5) and high_5 != low_5:
        pos5 = (last_close - low_5) / (high_5 - low_5)
        if pos5 > 0.8:
            short += 10
    return {
        'short': max(0, min(100, round(short))),
        'medium': max(0, min(100, round(medium))),
        'long': max(0, min(100, round(long))),
    }


def primary_horizon(scores, summary):
    chg = summary.get('chg_1d')
    if chg is not None and chg > 1.5 and scores['short'] >= scores['medium'] - 2:
        return 'short'
    if scores['long'] >= scores['medium'] and scores['long'] >= scores['short']:
        return 'long'
    if scores['medium'] >= scores['short']:
        return 'medium'
    return 'short'


def build_row(item):
    data = item.get('sources', {})
    last_rows = data.get('10jqka_last') or []
    anchor = data.get('10jqka_today') or {}
    status = 'verified' if last_rows or anchor else 'fallback-only'
    summary = summarize_rows(last_rows)
    scores = score_bucket(summary, status)
    primary = primary_horizon(scores, summary)
    row = {
        'ticker': item.get('ticker'),
        'market': item.get('market'),
        'anchorDate': anchor.get('date') if isinstance(anchor, dict) else None,
        'open': anchor.get('open') if isinstance(anchor, dict) and anchor.get('open') else (last_rows[-1].get('open') if last_rows else None),
        'close': anchor.get('close') if isinstance(anchor, dict) and anchor.get('close') else (last_rows[-1].get('close') if last_rows else None),
        'status': status,
        'scores': scores,
        'primaryHorizon': primary,
        'summary': summary,
        'plan': '条件观察' if status != 'verified' else '可进一步细化',
    }
    return row


def ensure_minimum_buckets(out, rows):
    for bucket in ('short', 'medium', 'long'):
        if not out[bucket]:
            sorted_rows = sorted(rows, key=lambda r: r['scores'][bucket], reverse=True)
            for row in sorted_rows[:3]:
                if row not in out[bucket]:
                    out[bucket].append(row)


def main():
    if len(sys.argv) != 2:
        print('Usage: build_watchlist.py <quotes.json>', file=sys.stderr)
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    out = {'short': [], 'medium': [], 'long': [], 'notes': []}
    rows = [build_row(item) for item in data]
    for row in rows:
        out[row['primaryHorizon']].append(row)
        out['notes'].append(f"{row['ticker']}: short={row['scores']['short']} medium={row['scores']['medium']} long={row['scores']['long']} status={row['status']}")
    ensure_minimum_buckets(out, rows)
    for key in ('short','medium','long'):
        out[key] = sorted(out[key], key=lambda r: r['scores'][key], reverse=True)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
