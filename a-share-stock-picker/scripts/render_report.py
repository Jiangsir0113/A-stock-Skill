#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

TITLE = {'short': '短线标的', 'medium': '中线标的', 'long': '长线标的'}
BASE = Path(__file__).resolve().parent.parent
NAMES_PATH = BASE / 'references' / 'ticker_names.json'


def load_json_map(path, key='ticker'):
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding='utf-8'))
    return {item[key]: item for item in data}


def load_names():
    if NAMES_PATH.exists():
        return json.loads(NAMES_PATH.read_text(encoding='utf-8'))
    return {}


def fmt(v):
    if v is None:
        return '待确认'
    if isinstance(v, float):
        return f'{v:.2f}'
    return str(v)


def clean_line(text):
    text = re.sub(r'\s+', ' ', str(text)).strip()
    text = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9()（）、，。：；_ /\-]+', '', text)
    return text


def rr(trigger, stop, t1):
    try:
        if None in (trigger, stop, t1):
            return '条件计划'
        risk = abs(trigger - stop)
        reward = abs(t1 - trigger)
        if risk <= 0:
            return '条件计划'
        ratio = reward / risk
        return f'1:{min(max(ratio, 0.5), 5.0):.1f}'
    except Exception:
        return '条件计划'


def shape(row, bucket):
    s = row.get('summary', {})
    last_close, high20, low20 = s.get('last_close'), s.get('high_20'), s.get('low_20')
    if bucket == 'short':
        return '突破型' if last_close and high20 and last_close >= high20 * 0.98 else '趋势型'
    if bucket == 'medium':
        return '趋势型' if last_close and low20 and last_close > low20 * 1.08 else '回踩型'
    return '震荡低吸型' if last_close and high20 and last_close < high20 * 0.85 else '趋势型'


def buy_time(bucket):
    return {'short':'明日 9:35-10:30','medium':'未来 1-5 个交易日分批','long':'未来 5-20 个交易日分批'}[bucket]


def hold(bucket):
    return {'short':'1-5天','medium':'2-8周','long':'3-12个月'}[bucket]


def sell_time(bucket):
    return {'short':'冲高至第一目标减仓，跌破承接位离场','medium':'2-8 周内到目标位分批兑现','long':'季报/半年报后复核，分批处理'}[bucket]


def no_buy(_row):
    return '高开过多、放量不续强、数据失真时不买'


def levels(row, bucket, ind):
    s = row.get('summary', {})
    close = s.get('last_close')
    low5, high5, high20, low20 = s.get('low_5'), s.get('high_5'), s.get('high_20'), s.get('low_20')
    atr14 = ind.get('atr14')
    if close is None:
        return ('待确认','待确认','待确认',None,None,None,'条件计划',None)
    atr_buf = atr14 if isinstance(atr14, (int, float)) else close * 0.02
    if bucket == 'short':
        support = low5 or close - atr_buf
        resist = high5 or close + atr_buf
        trigger_num = round(close, 2)
        trigger_text = f'{trigger_num:.2f} 附近站稳再看'
        t1, t2 = resist, min(resist + atr_buf, resist * 1.05)
    elif bucket == 'medium':
        support = low20 or close - atr_buf * 2
        resist = high20 or close + atr_buf * 2
        trigger_num = round(close * 0.99, 2)
        trigger_text = f'{trigger_num:.2f}-{close:.2f} 回踩观察'
        t1, t2 = resist, min(resist + atr_buf * 1.5, resist * 1.10)
    else:
        support = low20 or close - atr_buf * 3
        resist = high20 or close + atr_buf * 2
        trigger_num = round(close * 0.98, 2)
        trigger_text = f'{trigger_num:.2f}-{round(close*1.01,2):.2f} 分批观察'
        t1, t2 = resist, min(resist + atr_buf * 1.5, resist * 1.12)
    stop = support * 0.99 if isinstance(support, (int, float)) else None
    return (support, resist, trigger_text, stop, t1, t2, rr(trigger_num, stop, t1), trigger_num)


def core_logic(row, bucket, meta, ind):
    sector = meta.get('sector', '待补充')
    vr = ind.get('vol_ratio')
    ma20 = ind.get('ma20')
    if bucket == 'short':
        return f'{sector}方向活跃度较高，量比 {fmt(vr)}，看次日承接强弱'
    if bucket == 'medium':
        return f'{sector}方向 20 日结构更完整，MA20={fmt(ma20)}，适合回踩跟踪'
    return f'{sector}方向更适合均衡型底仓，分批观察更稳妥'


def evidence_lines(row, meta, cat, ind, news):
    titles = [clean_line(t) for t in cat.get('titles', []) if clean_line(t)]
    title_text = '；'.join(titles[:2]) if titles else '暂无自动抓取到有效标题'
    summary = clean_line(news.get('summary') or '暂无摘要')
    s = row.get('summary', {})
    return [
        f"- **{meta.get('name', row['ticker'])} {row['ticker']}**：行业 `{meta.get('sector', '待补充')}`；短/中/长评分 `{row['scores']['short']}/{row['scores']['medium']}/{row['scores']['long']}`。",
        f"  - 价格结构：近 1 日涨跌 `{fmt(s.get('chg_1d'))}%`，MA5/20/60 `{fmt(ind.get('ma5'))}/{fmt(ind.get('ma20'))}/{fmt(ind.get('ma60'))}`，ATR14 `{fmt(ind.get('atr14'))}`，量比 `{fmt(ind.get('vol_ratio'))}`。",
        f"  - 催化剂线索：{title_text}",
        f"  - 摘要：{summary}",
    ]


def render_bucket(bucket, rows, names, catalysts, indicators, news):
    out = [f"## {TITLE[bucket]}", "| 股票 | 上个交易日开盘价 | 上个交易日收盘价 | 形态类型 | 关键支撑 | 关键阻力 | 核心逻辑 | 买入时间 | 触发买价 | 止损价 | 第一目标 | 第二目标 | 风险收益比 | 卖出时间 | 持有周期 | 不买条件 |", "|---|---:|---:|---|---:|---:|---|---|---|---:|---:|---:|---|---|---|---|"]
    for row in rows[:3]:
        meta = names.get(row['ticker'], {})
        ind = indicators.get(row['ticker'], {})
        display = f"{meta.get('name', row['ticker'])} {row['ticker']}"
        support, resist, trigger, stop, t1, t2, ratio, _ = levels(row, bucket, ind)
        out.append(f"| {display} | {fmt(row.get('open'))} | {fmt(row.get('close'))} | {shape(row, bucket)} | {fmt(support)} | {fmt(resist)} | {core_logic(row, bucket, meta, ind)} | {buy_time(bucket)} | {trigger} | {fmt(stop)} | {fmt(t1)} | {fmt(t2)} | {ratio} | {sell_time(bucket)} | {hold(bucket)} | {no_buy(row)} |")
    out.append('')
    out.append(f"### {TITLE[bucket]}说明")
    for row in rows[:3]:
        meta = names.get(row['ticker'], {})
        cat = catalysts.get(row['ticker'], {})
        ind = indicators.get(row['ticker'], {})
        nw = news.get(row['ticker'], {})
        out.extend(evidence_lines(row, meta, cat, ind, nw))
    out.append('')
    return '\n'.join(out)


def main():
    if len(sys.argv) not in (2, 3, 4, 5):
        print('Usage: render_report.py <watchlist.json> [catalysts.json] [indicators.json] [news_summary.json]', file=sys.stderr)
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    names = load_names()
    catalysts = load_json_map(sys.argv[2]) if len(sys.argv) >= 3 else {}
    indicators = load_json_map(sys.argv[3]) if len(sys.argv) >= 4 else {}
    news = load_json_map(sys.argv[4]) if len(sys.argv) >= 5 else {}
    parts = ['# A股盘前选股战报', '说明：以下内容为盘前观察池 / 条件交易计划，不构成无条件买入建议。', '']
    for bucket in ('short','medium','long'):
        parts.append(render_bucket(bucket, data.get(bucket, []), names, catalysts, indicators, news))
    if data.get('notes'):
        parts.append('## 补充备注')
        for n in data['notes']:
            parts.append(f'- {n}')
    print('\n'.join(parts))


if __name__ == '__main__':
    main()
