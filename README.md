# A Share Stock Picker

## 介绍

`a-share-stock-picker` 是一个面向 Codex 的 A 股选股 skill，适用于盘后到次日开盘前的观察池整理、短中长线候选分析和条件交易计划输出。

这个仓库提供的不是单纯提示词，而是一套完整的 skill 包，包含：

- `SKILL.md`：核心行为定义
- `references/`：选股框架、价格规则、输出模板和使用说明
- `scripts/`：行情抓取、候选打分、指标计算、催化抓取和报告生成脚本
- `agents/`：agent 配置

## 适用场景

- `推荐股票`
- `盘前选股`
- `按收盘后信息做观察池`
- `给我短中长线标的`
- `给我条件交易计划`

## 核心特点

- 仅覆盖中国大陆 A 股
- 默认同时覆盖短线、中线、长线三个周期
- 使用最近一个已完成交易日作为主要价格锚点
- 结合近 5 日、20-60 日、6-12 个月历史窗口判断结构
- 优先输出 `观察池 / 候选名单 / 条件交易计划`
- 数据验证不足时，不强行给出绝对化买卖建议

## 仓库结构

```text
.
├── LICENSE
├── README.md
├── README.en.md
└── a-share-stock-picker
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

实际安装到 Codex 的 skill 目录是：

```text
a-share-stock-picker/a-share-stock-picker
```

## 内置能力

### 数据与分析

- 拉取 A 股行情与历史数据
- 计算均线、ATR、MACD 线索和量比等技术指标
- 获取个股催化、新闻摘要和上下文信息
- 将候选按短线、中线、长线进行打分和分桶

### 输出与表达

- 生成中文 Markdown 选股报告
- 支持结构化表格输出
- 优先使用条件触发式交易语言
- 在数据新鲜且验证充分时，才升级到更精确的价格计划

## 主要脚本

- `scripts/fetch_quotes.py`
- `scripts/build_watchlist.py`
- `scripts/fetch_catalysts.py`
- `scripts/indicators.py`
- `scripts/fetch_news_summary.py`
- `scripts/render_report.py`
- `scripts/run_picker.py`

## 使用方式

### 安装到 Codex

```bash
cp -R a-share-stock-picker ~/.codex/skills/
```

### 调用示例

```text
使用 $a-share-stock-picker 给我一份盘前 A 股观察池，短线、中线、长线各 3 只。
```

```text
使用 $a-share-stock-picker 基于收盘后信息，输出均衡型候选名单和条件交易计划。
```

### 推荐工作方式

- 先抓取行情和历史数据
- 再结合催化、新闻和披露信息
- 最后输出观察池或条件交易计划

如果要给出精确买点、止损和目标位，应确保底层价格数据是最新且已验证的。

## 注意事项

- 最适合盘后到次日开盘前时段
- 不建议在盘中未校验数据的情况下直接下精确结论
- 如果证据不足，应退回观察池或条件计划表达

## License

本仓库使用 [LICENSE](./LICENSE) 中声明的许可证。
