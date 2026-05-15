#!/usr/bin/env python3
"""Selection-quality helpers for A-share recommendation workflows."""

from collections import defaultdict


GRADE_RANK = {"A": 3, "B": 2, "C": 1, "D": 0}


def to_float(value):
    try:
        return float(value)
    except Exception:
        return None


def sector_key(meta):
    sector = (meta or {}).get("sector") or "待补充"
    return str(sector).split("/")[0].split("／")[0].strip() or "待补充"


def hard_exclusion(row, meta=None, mode="default"):
    reasons = []
    meta = meta or {}
    name = str(meta.get("name") or row.get("name") or "").upper()
    ticker = str(row.get("ticker") or "")
    metrics = row.get("marketMetrics") or {}

    if "ST" in name or "退" in name:
        reasons.append("风险警示/ST")
    if name.startswith(("N", "C")):
        reasons.append("新股/次新首日风险")

    amount = to_float(metrics.get("amount"))
    turnover = to_float(metrics.get("turnoverPct"))
    if amount is not None and amount < 200_000_000:
        reasons.append("成交额过低")
    if turnover is not None and turnover < 0.5:
        reasons.append("换手不足")
    if turnover is not None and turnover > 45:
        reasons.append("换手过热")

    if mode == "tail" and row.get("todayClose") is None:
        reasons.append("缺少尾盘分时价格")
    elif mode != "tail" and not (row.get("open") and row.get("close")):
        reasons.append("缺少锚点开收盘价")

    if ticker.startswith(("8", "4")):
        reasons.append("非沪深主板/创业板/科创板常规A股池")

    return {"excluded": bool(reasons), "reasons": reasons}


def money_flow_ratio(metrics):
    net = to_float((metrics or {}).get("netInflow"))
    amount = to_float((metrics or {}).get("amount"))
    if net is None or amount in (None, 0):
        return None
    return net / amount


def tradability_score(row, tail=False):
    metrics = row.get("marketMetrics") or {}
    amount = to_float(metrics.get("amount"))
    turnover = to_float(metrics.get("turnoverPct"))
    net = to_float(metrics.get("netInflow"))
    rows = int(row.get("summary", {}).get("rows") or 0)
    score = 50
    reasons = []

    if amount is not None:
        if amount >= 3_000_000_000:
            score += 22
            reasons.append("成交额充足")
        elif amount >= 1_000_000_000:
            score += 15
            reasons.append("成交额较好")
        elif amount >= 500_000_000:
            score += 8
        elif amount < 200_000_000:
            score -= 18
            reasons.append("成交额偏低")

    if turnover is not None:
        if 3 <= turnover <= 20:
            score += 12
            reasons.append("换手适中")
        elif 1 <= turnover < 3:
            score += 4
        elif turnover < 1:
            score -= 8
            reasons.append("换手偏低")
        elif turnover > 25:
            score -= 6
            reasons.append("换手偏热")

    ratio = money_flow_ratio(metrics)
    if net is not None:
        if net >= 500_000_000:
            score += 14
            reasons.append("主力净流入强")
        elif net >= 100_000_000:
            score += 8
        elif net <= -500_000_000:
            score -= 18
            reasons.append("主力净流出强")
        elif net < 0:
            score -= 8
    if ratio is not None:
        if ratio >= 0.08:
            score += 8
        elif ratio <= -0.08:
            score -= 10

    if rows >= 60:
        score += 6
    elif rows >= 20:
        score += 3
    elif rows and rows < 10:
        score -= 5

    if tail:
        change_1400 = to_float(row.get("changeFrom1400Pct"))
        range_position = to_float(row.get("rangePosition"))
        late_volume_share = to_float(row.get("lateVolumeShare"))
        day_change = to_float(row.get("dayChangePct"))
        if change_1400 is not None:
            if change_1400 >= 0.8:
                score += 10
                reasons.append("14:00后回流")
            elif change_1400 <= -0.5:
                score -= 12
                reasons.append("尾盘转弱")
        if range_position is not None:
            if range_position >= 0.8:
                score += 8
                reasons.append("收在日内高位")
            elif range_position <= 0.35:
                score -= 10
                reasons.append("日内位置偏弱")
        if late_volume_share is not None:
            if late_volume_share >= 0.22:
                score += 4
            elif late_volume_share <= 0.12:
                score -= 4
        if day_change is not None and day_change > 7:
            score -= 8
            reasons.append("涨幅偏大")

    return {"score": max(0, min(100, round(score))), "reasons": reasons}


def evidence_grade(meta, cat, news, row):
    components = []
    meta = meta or {}
    cat = cat or {}
    news = news or {}
    metrics = row.get("marketMetrics") or {}

    if row.get("open") and row.get("close") or row.get("todayOpen") and row.get("todayClose"):
        components.append("价格锚点")
    if row.get("summary", {}).get("rows", 0) >= 20:
        components.append("历史窗口")
    if to_float(metrics.get("netInflow")) is not None:
        components.append("资金流")
    if meta.get("sector") and meta.get("sector") != "待补充":
        components.append("行业归属")
    if cat.get("titles") or cat.get("sectionHighlights"):
        components.append("公告/上下文")
    if news.get("summary") and news.get("summary") != "暂无自动摘要":
        components.append("新闻摘要")
    if row.get("tradabilityScore", 0) >= 70:
        components.append("可交易性")

    if len(components) >= 6:
        grade = "A"
    elif len(components) >= 4:
        grade = "B"
    elif len(components) >= 2:
        grade = "C"
    else:
        grade = "D"
    return {"grade": grade, "components": components}


def market_regime_from_universe(data):
    universe = (data or {}).get("universe", [])
    changes = []
    inflows = []
    for item in universe:
        metrics = item.get("metrics") or {}
        chg = to_float(metrics.get("chgPct"))
        net = to_float(metrics.get("netInflow"))
        if chg is not None:
            changes.append(chg)
        if net is not None:
            inflows.append(net)
    if not changes:
        return {"label": "状态待确认", "positiveRatio": None, "netInflowSum": None}

    positive_ratio = sum(1 for value in changes if value > 0) / len(changes)
    avg_change = sum(changes) / len(changes)
    net_sum = sum(inflows) if inflows else None
    inflow_ratio = (sum(1 for value in inflows if value > 0) / len(inflows)) if inflows else None

    if positive_ratio >= 0.65 and avg_change >= 1 and (inflow_ratio is None or inflow_ratio >= 0.55):
        label = "强势偏多"
    elif positive_ratio >= 0.55 and avg_change >= 0:
        label = "震荡偏强"
    elif positive_ratio <= 0.30 and avg_change <= -1:
        label = "退潮防守"
    elif positive_ratio <= 0.45 and avg_change < 0:
        label = "震荡偏弱"
    else:
        label = "震荡均衡"

    return {
        "label": label,
        "positiveRatio": round(positive_ratio, 4),
        "avgChangePct": round(avg_change, 4),
        "netInflowSum": net_sum,
        "inflowRatio": round(inflow_ratio, 4) if inflow_ratio is not None else None,
    }


def regime_score_adjustment(regime_label, bucket):
    label = regime_label or ""
    if label == "强势偏多":
        return {"short": 6, "medium": 3, "long": -1}.get(bucket, 0)
    if label == "震荡偏强":
        return {"short": 3, "medium": 2, "long": 0}.get(bucket, 0)
    if label == "震荡偏弱":
        return {"short": -6, "medium": -2, "long": 4}.get(bucket, 0)
    if label == "退潮防守":
        return {"short": -12, "medium": -5, "long": 6}.get(bucket, 0)
    return 0


def recommendation_role(row, bucket, meta=None):
    sector = sector_key(meta)
    tradability = row.get("tradabilityScore", 0)
    metrics = row.get("marketMetrics") or {}
    net = to_float(metrics.get("netInflow"))
    if bucket == "short":
        if tradability >= 80 and net is not None and net > 0:
            return f"{sector}强势承接"
        return f"{sector}条件观察"
    if bucket == "medium":
        return f"{sector}趋势跟踪"
    return f"{sector}配置观察"


def next_day_exit_risk(row):
    reasons = []
    day_change = to_float(row.get("dayChangePct"))
    range_position = to_float(row.get("rangePosition"))
    change_1400 = to_float(row.get("changeFrom1400Pct"))
    net = to_float((row.get("marketMetrics") or {}).get("netInflow"))

    if day_change is not None and day_change > 7:
        reasons.append("涨幅过大")
    if range_position is not None and range_position < 0.35:
        reasons.append("日内收位偏弱")
    if change_1400 is not None and change_1400 <= -0.5:
        reasons.append("尾盘转弱")
    if net is not None and net < 0:
        reasons.append("主力净流出")

    if len(reasons) >= 2:
        level = "高"
    elif reasons:
        level = "中"
    else:
        level = "低"
    return {"level": level, "reasons": reasons or ["尾盘结构和资金未触发明显退出风险"]}


def apply_portfolio_constraints(rows, bucket, names, limit=5, max_per_sector=2):
    selected = []
    sector_counts = defaultdict(int)
    seen = set()
    sorted_rows = sorted(
        rows,
        key=lambda row: (
            GRADE_RANK.get(row.get("evidenceGrade", "C"), 1),
            row.get("tradabilityScore", 0),
            row.get("scores", {}).get(bucket, row.get("score", 0)),
        ),
        reverse=True,
    )
    for row in sorted_rows:
        ticker = row.get("ticker")
        if not ticker or ticker in seen:
            continue
        sector = sector_key((names or {}).get(ticker, {}))
        if sector_counts[sector] >= max_per_sector:
            continue
        selected.append(row)
        seen.add(ticker)
        sector_counts[sector] += 1
        if len(selected) >= limit:
            break
    return selected
