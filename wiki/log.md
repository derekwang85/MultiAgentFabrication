# wiki 变更日志 · log.md

**评审记录**：本文件为变更日志（记录性文件），非成稿文章，适用 W 门禁而不适用 G5 内容评审；质量留痕见 [../docs/WRITING-FRAMEWORK.md](../docs/WRITING-FRAMEWORK.md) 评审记录。

> 每次新增 / 修订记一行：改了什么 / 为何 / 来源。对齐 wiki 元规约 `AGENTS.md` §七。

## 维护说明

- 按时间顺序追加，一条记一行；同一次批处理合并成一个小节。
- 每条必含：改动对象 / 原因 / 依据来源（本地路径）。
- 涉及删除或降级条目需标注理由，不允许默默移除。

## 2026-09-12 · 初始建库（同步母版 derekwritting-framework v2 补齐 llm-wiki）

- 新增 `AGENTS.md`、`GUIDE.md`、`index.md`、`concepts/taxonomy.md`：确立 wiki 元规约（wikilink + W1-W4 门禁 + 失败安全生成）、双读者使用指南、检索入口与五层分类口径。
- 新增 `sources/` 5 个一手源页：source-constitution、source-writing-framework、source-writing-harness、source-skill-registry、source-evolution-skill；各含一手溯源 + 吸收/舍弃表。
- 新增 `concepts/` 12 条概念页（不含 taxonomy）：knowledge-as-asset、reviewer-writer-separation、evaluation-driven-progression、retrieval-over-content、writing-recipe-seven、progressive-disclosure、gate-as-verification、harness-gates-g1-g6、allusion-isolation、experience-retention、skill-registry-promotion、derekinside-note。
- 依据：母版 `C:\Users\A\Documents\derekwritting-framework\wiki\` 于前两轮适配后新增 llm-wiki 体系；本轮按"本项目自身的知识资产 + 依赖 skill"做了参数化建库，而非照搬母版对七个外部参考源的收敛（那些不属于本项目方法论）。
- 一致性契约：`framework.config.json` `patrol.assets` 应登记 wiki 资产；README 使用纪律补登记 llm-wiki 维护条款。

## 2026-09-26 · /goal 收束：双层 Agent（元/产品）架构 + k1-k4 记忆体系落进系列

- 新增锚点篇 13《两层 Agent：造系统的，与在系统里的》中英双语（主张 A9 双层结构与记忆手递手）：元层工厂流水线 → 产物下发 P13 → 产品层车间流水线，旁置 k1-k4 四层记忆，k4 单向回流（ADR 审计 + 人终裁）。
- 回改核心篇 08 治理 / 09 HITL / 12 记账本 双语，把元层只读 k1+k2、产品层读 k1+k2+k3 的不对称，与 k4 回流立为显性主线（决策库 = 产品层 k3；人 = k4 裁决座位）。
- 补齐缺失配图 `fig-13-key`（`diagrams/data_src.py` 新增数据 → 生成 `.drawio/.html` → `arch_qa.py` R1/R2/R3 实测通过；全系列 15 图全过）。
- 命名纪律：涉及具体项目一律用描述性语言（「一个多 Agent 专业研投、跨团队知识同步项目」），不出现真实项目名。
- 门禁/回归：量纲 27/27 PASS、中门禁 14 篇 G1-G5 PASS、英门禁 13 篇 E1-E6 PASS、双棘轮 `--check` 均 9.8 PASS；同步 `README.md`（A1-A9）、`SERIES-PLAN.md`、`docs/article-evaluation-system.md`（加 13 行 + 基线），重生成 `publish/` 发布正文 27 篇。
- 依据/索引：收束说明 `docs/goal-delivery-two-tier.md`；成稿 `articles/13-two-tier-meta-product.zh.md` 与 `articles/en/13-two-tier-meta-product.en.md`；配图 `diagrams/out/fig-13-key.*`。

## 2026-09-28 · /goal 收缩主线：十三篇骨架 + 谱系对照 + 全系列地图

- 结构 Review（用户第 1 点）：判定问题在重心不均而非篇数，保留十三篇骨架（序章 0 + 正文 1-12 + 锚点 13）不扩篇，收紧主线而非瘦身。
- 序章重构（用户第 2 点）：§六 全量改版为「全系列地图」`fig-00-key`，一张拎起四幕（为什么/是什么/怎么用/到哪去）+ 锚点篇 + 谱系带，替代原含错误篇号的旧 §六（幕三原误写 5-10、幕四误写 11-12）；修正文首图引用与配图说明，正文汉字 3584 PASS。
- 多用图（用户第 3 点）：`data_src.py` 新增 `fig_00_series_map`（id `fig-00-key`，27 节点四幕横排 + 底部谱系带），原 Multi-Agent 流水线图独立为 `fig-00-pipeline`；`arch_qa.py` R1/R2/R3 实测通过，全系列 16 图全过。
- 广度外拓（用户第 4 点）：在 04-13 十篇正文各插入「谱系定位」段，显式点名落在研报/RAG 自动化、SWE Agent/编排框架、Agentic RPA/企业 Copilot、多 Agent 辩论·对抗、MCP/工具生态哪一格、对话哪类应用、刻意不覆盖什么；宽度靠对照非扩篇。
- 门禁/回归：中门禁 11 篇 G1-G5 PASS（正文汉字 04:3187/05:3030/06:3062/07:3020/08:3385/09:3359/10:2982/11:3027/12:3512/13:3108 均 ≥2800）、英门禁 13 篇 E1-E6 PASS、棘轮 `--next` 基准 9.80 不退化；评分板为序章与 04-13 记谱系对照/重构注。
- 依据/索引：策划与图谱 `SERIES-PLAN.md`（篇号说明 + 篇数 16）；`README.md`（系列地图 + 谱系对照）；配图 `diagrams/out/fig-00-key.*` 与 `fig-00-pipeline.*`。

## 2026-09-28 · 新增篇外对照专题 0.5：我们 vs Subagent（为什么有了 subagent 还折腾 Multi-Agent）

- 需求（用户新增）：正面回答"Codex / TRAE / OpenClaw 运行时也会派子 Agent，你都 subagent 了为什么还折腾 Multi-Agent"这一最容易看错的分野。
- 结构裁定：主体仍不扩篇（序章 0 + 正文 1-12 + 锚点 13），改在序章与篇 1 之间插入**篇外对照专题 0.5**；序章 §六 立论站位加一嘴预告（只点题、详情交棒 0.5），防止读者在抵达锚点前误判"这是另一种 subagent"。
- 新增 `articles/00-5-subagent-vs-multiagent.zh.md`（正文汉字 3681）与 `articles/en/00-5-subagent-vs-multiagent.en.md`（2512 词）：八维对照框架（架构/生命周期/决策权责/大模型调用/可塑性/记忆归属/可证明性/可追溯性），前四维来自用户直觉（外加用户批准的生命周期+记忆归属），后四维咬住系列主线——记忆归属→k1-k4、可证明性→隔离三权验证+门禁、可追溯性→decision.db+ADR+人工终裁。突破维度取认知科学家梅林·唐纳德"个体用工具 vs 外化成公共资产的社会性思维"。
- 新增配图 `fig-00-5`（`data_src.py` 注册 id `fig-00-5`，20 节点 / 20 边，两竖列链从共享根点分岔模式满足 R1 不穿节点）；`arch_qa.py` R1/R2/R3 实测通过，全系列 17 图全过。
- 门禁/回归：中门禁 G1-G5 PASS（汉字 3681 ≥2800）、英门禁 E1-E6 PASS（2512 词 ≥1900）、棘轮 `--record` 录 10.0 对基准 9.8 PASS（越上沿宽松告警）、`--check` 通过（文章数 15，均分 9.81）；回填 `README.md`（系列地图 +0.5 行、目录结构、谱系对照）、`SERIES-PLAN.md`（结构表 +0.5 节、篇号说明 15 篇、图数 17、验收清单），重生成 `publish/`。
- 依据/索引：成稿 `articles/00-5-subagent-vs-multiagent.zh.md` 与 `articles/en/00-5-subagent-vs-multiagent.en.md`；配图 `diagrams/out/fig-00-5.*`；评分板 `writing-harness/evaluation-scoreboard.json`。