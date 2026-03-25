#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
NAMES_PATH = BASE / "references" / "ticker_names.json"
TAIL_ENTRY_COUNT = 5


def load_names():
    if NAMES_PATH.exists():
        return json.loads(NAMES_PATH.read_text(encoding="utf-8"))
    return {}


def load_json_map(path, key="ticker"):
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {item[key]: item for item in data}


def fmt(value):
    if value is None:
        return "待确认"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def clean_line(text):
    text = re.sub(r"\s+", " ", str(text)).strip()
    text = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9()（）、，。：；_ /\-]+", "", text)
    return text


def evidence_lines(row, meta, cat, news):
    titles = [clean_line(title) for title in cat.get("titles", []) if clean_line(title)]
    summary = clean_line(news.get("summary") or "暂无自动摘要")
    reasons = "；".join(row.get("scoreNotes", [])[:3]) or "尾盘模式分数较高"
    return [
        f"- **{meta.get('name', row['ticker'])} {row['ticker']}**：行业 `{meta.get('sector', '待补充')}`；尾盘评分 `{row.get('score')}`。",
        f"  - 入选原因：{reasons}",
        f"  - 价格结构：D日参考价 `{fmt(row.get('todayClose'))}`，14:00 后变化 `{fmt(row.get('changeFrom1400Pct'))}%`，尾盘量能占比 `{fmt((row.get('lateVolumeShare') or 0) * 100)}%`。",
        f"  - 催化/上下文：{'；'.join(titles[:2]) if titles else '暂无额外页面标题线索'}",
        f"  - 摘要：{summary}",
    ]


def main():
    if len(sys.argv) not in (2, 3, 4):
        print("Usage: render_t1_plan.py <tail_watchlist.json> [catalysts.json] [news_summary.json]", file=sys.stderr)
        sys.exit(1)
    watchlist = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    catalysts = load_json_map(sys.argv[2]) if len(sys.argv) >= 3 else {}
    news = load_json_map(sys.argv[3]) if len(sys.argv) >= 4 else {}
    names = load_names()
    rows = watchlist.get("tail_entry", [])[:TAIL_ENTRY_COUNT]

    parts = [
        "# A股T+1尾盘建仓计划",
        "说明：本模式用于 D 日尾盘建仓、D+1 日卖出，适配 A 股 T+1 规则。",
        "",
        "## 今日尾盘建仓计划",
        "| 股票 | D日开盘价 | D日参考价 | 形态类型 | 尾盘支撑 | 尾盘阻力 | 核心逻辑 | 建仓时间 | 建仓价格区间 | 隔夜止损线 | 次日止盈一 | 次日止盈二 | 风险收益比 | 次日卖出时间 | 预计持有 | 放弃条件 |",
        "|---|---:|---:|---|---:|---:|---|---|---|---:|---:|---:|---|---|---|---|",
    ]

    for row in rows:
        meta = names.get(row["ticker"], {})
        display = f"{meta.get('name', row['ticker'])} {row['ticker']}"
        entry_zone = f"{fmt(row.get('entryLow'))}-{fmt(row.get('entryHigh'))}"
        parts.append(
            f"| {display} | {fmt(row.get('todayOpen'))} | {fmt(row.get('todayClose'))} | {row.get('setupType')} | {fmt(row.get('support'))} | {fmt(row.get('resistance'))} | {row.get('coreLogic')} | {row.get('buyWindow')} | {entry_zone} | {fmt(row.get('stop'))} | {fmt(row.get('target1'))} | {fmt(row.get('target2'))} | {row.get('riskReward')} | {row.get('sellWindow')} | {row.get('holdWindow')} | {row.get('skipCondition')} |"
        )

    parts.extend(
        [
            "",
            "## 次日卖出原则",
        ]
    )
    for row in rows:
        meta = names.get(row["ticker"], {})
        parts.append(
            f"- `{meta.get('name', row['ticker'])} {row['ticker']}`：{row.get('nextDayPlan')} 若次日竞价明显高于 `第一目标`，优先兑现一部分；若低开并跌破 `隔夜止损线`，不恋战。"
        )

    parts.extend(["", "## 入选说明"])
    for row in rows:
        meta = names.get(row["ticker"], {})
        cat = catalysts.get(row["ticker"], {})
        nw = news.get(row["ticker"], {})
        parts.extend(evidence_lines(row, meta, cat, nw))

    if watchlist.get("notes"):
        parts.extend(["", "## 调度备注"])
        for note in watchlist["notes"]:
            parts.append(f"- {note}")

    print("\n".join(parts))


if __name__ == "__main__":
    main()
