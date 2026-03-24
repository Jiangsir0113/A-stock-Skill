# Codex Skills Collection

## 介绍

这是一个面向 Codex 的技能仓库，当前包含两个可直接复用的 skill：

- `a-share-stock-picker`：用于 A 股盘后到次日开盘前的选股、观察池整理和条件交易计划输出
- `java-architect-assistant`：用于既有 Java 项目的需求分析、功能开发、Bug 修复、性能优化和代码审查

这两个 skill 都不是“泛用提示词模板”，而是带有明确工作流、参考资料、脚本和输出规范的可执行技能目录。

## 仓库结构

```text
.
├── README.md
├── README.en.md
├── LICENSE
├── a-share-stock-picker
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
└── java-architect-assistant
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

## Skill 概览

| Skill | 适用场景 | 核心特点 |
| --- | --- | --- |
| `a-share-stock-picker` | 推荐 A 股标的、盘前观察池、短中长线候选、条件交易计划 | 以最近一个完整交易日为价格锚点，结合历史走势、催化、披露和结构化打分，默认输出观察池而非生硬喊单 |
| `java-architect-assistant` | Java 功能开发、修复 bug、性能优化、代码审查、PRD/原型分析 | 先分析需求和项目结构，再输出计划；默认低侵入；修改旧代码和旧方法前要求显式确认 |

## 安装方式

### 方式一：手动安装到 Codex skills 目录

将需要的 skill 目录复制到本机 Codex skills 目录，例如：

```bash
cp -R a-share-stock-picker ~/.codex/skills/
cp -R java-architect-assistant ~/.codex/skills/
```

如果你要同时使用两个 skill，可以一起复制。

### 方式二：作为本地技能仓库维护

如果你希望持续维护或二次开发这些 skill，可以保留整个仓库，并按需同步其中某个 skill 到 `~/.codex/skills/`。

## 使用说明

### 1. `a-share-stock-picker`

#### 适合做什么

- `推荐股票`
- `盘前选股`
- `按收盘后信息做观察池`
- `给我短中长线标的`
- `给我条件交易计划`

#### 工作方式

- 默认覆盖短线、中线、长线三个周期
- 使用最近一个已完成交易日作为主要价格锚点
- 结合近 5 日、20-60 日、6-12 个月历史窗口判断结构
- 优先输出 `观察池 / 候选名单 / 条件计划`
- 只有在价格新鲜且已验证时，才给出更精确的买入、止损和目标位

#### 内置能力

- 拉取 A 股行情与历史数据
- 计算均线、ATR、MACD 线索和量比等技术指标
- 获取个股催化、新闻摘要和基础上下文
- 生成中文 Markdown 选股报告

#### 主要脚本

- `scripts/fetch_quotes.py`
- `scripts/build_watchlist.py`
- `scripts/fetch_catalysts.py`
- `scripts/indicators.py`
- `scripts/fetch_news_summary.py`
- `scripts/render_report.py`
- `scripts/run_picker.py`

#### 调用示例

```text
使用 $a-share-stock-picker 给我一份盘前 A 股观察池，按短线、中线、长线各给 3 个标的。
```

```text
使用 $a-share-stock-picker 基于收盘后信息，输出均衡型候选名单和条件交易计划。
```

#### 注意事项

- 仅覆盖中国大陆 A 股
- 更适合盘后到次日开盘前窗口
- 不建议在数据未验证时直接给出绝对化买卖结论

### 2. `java-architect-assistant`

#### 适合做什么

- Java 功能开发
- Bug 修复
- 性能优化
- 代码审查
- PRD、原型图、截图、蓝湖链接分析
- 按当前工程风格生成 Java/SQL/配置代码

#### 工作方式

- 先理解需求，再学习项目结构和代码风格
- 先给计划，再实施
- 默认优先走低侵入方案
- 能新增文件解决时，尽量不直接改旧逻辑
- 修改现有代码、尤其是修改旧方法前，要求用户明确确认

#### 关键能力

- 自动识别模块、包结构、分层和资源目录
- 根据现有代码学习 Controller、Service、Mapper、DTO、VO 等模板风格
- 对 SQL、事务、缓存、MQ、锁、线程和接口影响做实现前规划
- 支持 URL 类需求输入，并优先通过内置 MCP URL Reader 读取内容

#### 调用示例

```text
使用 $java-architect-assistant 处理这个需求。
先分析需求和当前工程风格，输出计划，再开始改代码。
未经我同意不要改原有方法；如果要复用旧方法，先问我是改原方法还是新写方法。
```

```text
使用 $java-architect-assistant 修复这个 bug。
我会提供报错日志和相关代码，你先定位根因并给修复计划。
```

```text
使用 $java-architect-assistant 显示使用说明
```

#### URL / PRD 读取

当需求来自 URL、PRD 或蓝湖时，建议先启动本地 MCP：

```bash
bash /Users/tudoushaoyangyu/.codex/skills/java-architect-assistant/scripts/start_url_reader_mcp.sh
```

如果页面依赖登录态，还需要向 skill 提供必要的 headers、cookies 或其他访问上下文。

## 设计原则

### `a-share-stock-picker`

- 证据优先，不凭印象喊单
- 观察池优先，不在证据不足时强行给绝对建议
- 价格计划必须基于最新已验证数据和历史结构

### `java-architect-assistant`

- 理解优先于修改
- 规划优先于编码
- 扩展优先于重写
- 配置、常量、枚举优先于硬编码
- 未经确认不修改旧代码和旧方法

## 适合谁使用

- 想把 Codex 变成“可复用工作流”而不只是单次对话的人
- 需要沉淀领域化开发规范、脚本和参考文档的团队
- 希望让选股分析或 Java 交付过程更稳定、更可复制的人

## 贡献方式

1. Fork 本仓库
2. 新建分支进行修改
3. 补充或更新 `SKILL.md`、`references/`、`scripts/`
4. 提交变更并发起 Pull Request

## License

本仓库使用 [LICENSE](./LICENSE) 中声明的许可证。
