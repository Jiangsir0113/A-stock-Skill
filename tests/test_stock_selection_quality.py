import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "a-share-stock-picker" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_module(name):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


quality = load_module("stock_selection_quality")


class StockSelectionQualityTest(unittest.TestCase):
    def test_hard_exclusion_rejects_st_and_poor_liquidity(self):
        row = {
            "ticker": "600000",
            "open": "10.00",
            "close": "10.30",
            "summary": {"rows": 30},
            "marketMetrics": {"amount": 90_000_000, "turnoverPct": 0.3},
        }
        meta = {"name": "*ST样例", "sector": "测试"}

        result = quality.hard_exclusion(row, meta)

        self.assertTrue(result["excluded"])
        self.assertIn("风险警示/ST", result["reasons"])
        self.assertIn("成交额过低", result["reasons"])

    def test_tradability_score_rewards_liquidity_and_penalizes_outflow(self):
        strong = {
            "marketMetrics": {"amount": 3_500_000_000, "turnoverPct": 8, "netInflow": 650_000_000},
            "summary": {"rows": 60},
        }
        weak = {
            "marketMetrics": {"amount": 180_000_000, "turnoverPct": 0.7, "netInflow": -700_000_000},
            "summary": {"rows": 8},
        }

        self.assertGreater(quality.tradability_score(strong)["score"], 80)
        self.assertLess(quality.tradability_score(weak)["score"], 45)

    def test_evidence_grade_requires_price_money_sector_and_context(self):
        row = {
            "open": "10.00",
            "close": "10.30",
            "summary": {"rows": 60},
            "marketMetrics": {"netInflow": 150_000_000, "amount": 1_200_000_000},
        }
        meta = {"sector": "电力/红利"}
        cat = {"titles": ["公司公告：签署长期协议"], "sectionHighlights": ["主营业务：水电运营"]}
        news = {"summary": "近期行业政策支持稳定分红。"}

        result = quality.evidence_grade(meta, cat, news, row)

        self.assertEqual(result["grade"], "A")
        self.assertGreaterEqual(len(result["components"]), 5)

    def test_market_regime_from_universe_classifies_breadth_and_money(self):
        strong_universe = {
            "universe": [
                {"metrics": {"chgPct": 2.1, "netInflow": 200_000_000}},
                {"metrics": {"chgPct": 1.4, "netInflow": 120_000_000}},
                {"metrics": {"chgPct": -0.2, "netInflow": 10_000_000}},
                {"metrics": {"chgPct": 3.0, "netInflow": 300_000_000}},
            ]
        }
        weak_universe = {
            "universe": [
                {"metrics": {"chgPct": -3.1, "netInflow": -300_000_000}},
                {"metrics": {"chgPct": -1.4, "netInflow": -120_000_000}},
                {"metrics": {"chgPct": 0.2, "netInflow": -10_000_000}},
                {"metrics": {"chgPct": -2.0, "netInflow": -80_000_000}},
            ]
        }

        self.assertEqual(quality.market_regime_from_universe(strong_universe)["label"], "强势偏多")
        self.assertEqual(quality.market_regime_from_universe(weak_universe)["label"], "退潮防守")

    def test_next_day_exit_risk_marks_extended_tail_trade_as_high(self):
        row = {
            "dayChangePct": 8.5,
            "rangePosition": 0.28,
            "changeFrom1400Pct": -0.7,
            "marketMetrics": {"netInflow": -250_000_000},
        }

        result = quality.next_day_exit_risk(row)

        self.assertEqual(result["level"], "高")
        self.assertIn("涨幅过大", result["reasons"])
        self.assertIn("尾盘转弱", result["reasons"])

    def test_portfolio_constraints_limit_sector_concentration(self):
        names = {
            "000001": {"sector": "AI/算力"},
            "000002": {"sector": "AI/算力"},
            "000003": {"sector": "AI/算力"},
            "000004": {"sector": "电力/红利"},
        }
        rows = [
            {"ticker": "000001", "scores": {"short": 99}, "evidenceGrade": "A"},
            {"ticker": "000002", "scores": {"short": 98}, "evidenceGrade": "A"},
            {"ticker": "000003", "scores": {"short": 97}, "evidenceGrade": "A"},
            {"ticker": "000004", "scores": {"short": 90}, "evidenceGrade": "B"},
        ]

        selected = quality.apply_portfolio_constraints(rows, "short", names, limit=4, max_per_sector=2)

        self.assertEqual([row["ticker"] for row in selected], ["000001", "000002", "000004"])


class ReviewRecommendationsTest(unittest.TestCase):
    def test_review_recommendations_reports_trigger_and_drawdown(self):
        review = load_module("review_recommendations")
        watchlist = {
            "short": [
                {
                    "ticker": "600000",
                    "close": 10.0,
                    "triggerPrice": 10.1,
                    "stopPrice": 9.7,
                    "target1": 10.8,
                }
            ]
        }
        next_quotes = [
            {
                "ticker": "600000",
                "sources": {
                    "10jqka_today": {
                        "open": "10.15",
                        "high": "10.90",
                        "low": "9.90",
                        "close": "10.50",
                        "date": "20260518",
                    }
                },
            }
        ]

        result = review.review_recommendations(watchlist, next_quotes)

        self.assertEqual(result["summary"]["total"], 1)
        self.assertEqual(result["summary"]["triggered"], 1)
        self.assertEqual(result["items"][0]["outcome"], "hit_target1")
        self.assertGreater(result["items"][0]["maxGainPct"], 7.0)


class WatchlistIntegrationTest(unittest.TestCase):
    def test_build_watchlist_row_carries_exclusion_tradability_and_role(self):
        build_watchlist = load_module("build_watchlist")
        item = {
            "ticker": "600900",
            "market": "sh",
            "sources": {
                "10jqka_today": {"date": "20260515", "open": "29.0", "close": "30.0"},
                "10jqka_last": [
                    {"open": "27", "high": "28", "low": "26", "close": "27", "volume": "1", "amount": "100"},
                    {"open": "28", "high": "31", "low": "27", "close": "30", "volume": "1", "amount": "200"},
                ]
                * 15,
            },
        }
        names = {"600900": {"name": "长江电力", "sector": "水电/红利"}}
        metrics = {"600900": {"amount": 3_200_000_000, "turnoverPct": 4.2, "netInflow": 620_000_000}}

        row = build_watchlist.build_row(item, metrics, names, {"label": "强势偏多"})

        self.assertFalse(row["excluded"])
        self.assertGreaterEqual(row["tradabilityScore"], 80)
        self.assertEqual(row["evidenceGrade"], "B")
        self.assertIn("水电", row["role"])

    def test_tail_watchlist_row_carries_next_day_exit_risk(self):
        build_tail = load_module("build_tail_watchlist")
        item = {
            "ticker": "600900",
            "market": "sh",
            "sources": {
                "10jqka_last": [
                    {"open": "27", "high": "28", "low": "26", "close": "27", "amount": "100"},
                    {"open": "28", "high": "31", "low": "27", "close": "30", "amount": "200"},
                ]
                * 15
            },
        }
        snapshots = {
            "600900": {
                "status": "verified",
                "sessionDate": "20260515",
                "latestMinute": "1456",
                "previousClose": 30.0,
                "intradayOpen": 30.2,
                "intradayClose": 32.7,
                "intradayHigh": 33.0,
                "intradayLow": 30.0,
                "priceAt1400": 33.2,
                "changeFromPrevClosePct": 9.0,
                "changeFrom1400Pct": -1.5,
                "rangePosition": 0.2,
                "lateVolumeShare": 0.10,
            }
        }
        names = {"600900": {"name": "长江电力", "sector": "水电/红利"}}
        metrics = {"600900": {"amount": 3_200_000_000, "turnoverPct": 4.2, "netInflow": -300_000_000}}

        row = build_tail.build_row(item, snapshots, metrics, names)

        self.assertEqual(row["nextDayExitRisk"], "高")
        self.assertLess(row["tradabilityScore"], 50)
        self.assertFalse(row["excluded"])


if __name__ == "__main__":
    unittest.main()
