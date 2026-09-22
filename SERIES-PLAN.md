# 《MultiAgent Fabrication · 多 Agent 生产力编织》系列策划

> 状态：定稿 v1.0 ｜ 日期：2026-09-05 ｜ 作者：derekwang85（腾讯云 TVP / 架构师名人堂）
> 定位：一套原创「多 Agent 形成生产力」方法论，以 derekcoding #19 约束求解 + SmartQuant 多 Agent 调度为母版，对照 GitHub 高分项目做对比与升华。完成后并入《RefactoringSoftwareEngineering》体系。

---

## 一、核心定位

**一句话：** 多 Agent 的生产力不在编排得漂亮，而在选型 / 调用 / 校验 / 自愈四链路闭环、全部声明式且可自证，外加"宣称对齐"的诚信底线。

**差异三问（别人没回答）：**
1. 怎么选模型？（约束求解，非 fallback）
2. 怎么让输出可信？（golden data 自评 + 精度加权共识 + 防分母错觉）
3. 怎么证明真的更高效？（基准对照 + 参数快照 + decision.db 审计）

## 二、差异化

- 主流框架（MetaGPT / AutoGen / LangGraph / CrewAI / Swarm）教你"组织长什么样"，不教你"怎么证明它更高效、为什么值得上多 Agent"。
- 我们补上这块空白：把"多 Agent 形成生产力"当作一个**可度量、可自证、可回流生产流程**的工程命题。

## 三、系列文章清单（十六篇，0 + 1-12 正文 + 13 后记）

| # | 选题 | 核心钩子 | 项目实证 | 对标 GitHub | 建议目标分 |
|:-:|------|---------|---------|------------|:---:|
| 0 | 序章：很多 Agent，然后呢？ | 从会干活到一群共犯 | SmartQuant 演进 | — | 8.7 |
| 1 | 约束即配置 | 加模型 = 加配置 | #19 Registry | LangChain/Ollama | 8.8 |
| 2 | 选型是求解 | fallback 是陷阱 | #19 Resolver | LangGraph | 8.8 |
| 3 | 模型要测不要猜 | golden data 自评 | #19 Profiler + derekinside | — | 8.9 |
| 4 | 搭便车的观测 | 零成本被动监控 | #19 Observer | — | 8.9 |
| 5 | 少数派也能对 | 加权共识防分母错觉 | #19 Consensus + derekinside | AutoGen | 8.9 |
| 6 | 宣称要和事实对齐 | 没有基准的分是假分 | #19 Golden Data + SmartQuant 审查 | promptfoo/langfuse | 8.9 |
| 7 | 角色编排 | 裸 Agent 到 9 角色 | SmartQuant 9 角色 + ARCHITECTURE | CrewAI/MetaGPT | 9.0 |
| 8 | 三层路由与门禁 | 向谁说话、能做什么 | SmartQuant L1/L2/L3 + MCP 权限 | — | 9.0 |
| 9 | 人工进圈 | HITL 闸门与反馈回流 | SmartQuant HITL + decision.db | AutoGen | 9.0 |
| 10 | 审计即记忆 | 决策留痕可复盘 | SmartQuant decision.db | langfuse | 9.0 |
| 11 | 方法论对比 | 18+ 高分项目共识与分歧 | 调研报告 | 全谱系 | 9.1 |
| 12 | 特色主张收束 | 什么才叫生产力 | 全系列收束 | — | 9.1 |
| 13 | 后记：并入《重构软件工程》 | 多 Agent 是工程重构一环 | 交棒 | — | 9.2 |

> 篇号说明：0 + 1-12 正文 + 13 后记，共 16 篇。基层基准从 AIHarness 成熟均分 8.7 起步，逐篇递进留 0.2 余量。

## 四、写作纪律与质量关卡

完全套用 derekwritting-evolution 进化闭环，并遵循 `docs/WRITING-FRAMEWORK.md`（写作框架总纲：引用 derekwritting-framework 适配的配方 / 工序 / 门禁）：

1. 每篇动笔前：`python writing-harness/evaluate.py --next` 亮基准（本系列分数板独立）。
2. 完稿先过 `python writing-harness/writing-gates.py articles/<file>.md`（G1-G5）。
3. 篇尾补"## 附：门禁评审记录"块（含 G5 期望词：评审 / rubric / 剩留问题）。
4. 自评录入：`python writing-harness/evaluate.py --record ...`，脚本判定是否严格 > 前序基准。
5. 每篇至少落实一个前序未用过的突破维度（组织学 / 系统论 / 哲人 / 开源历史新矿），不可复用 AIHarness 已占出处（德鲁克 / 维纳 / 麦肯锡 / 汉谟拉比 / 泰勒福特 / 戴明 / 克劳塞维茨 / 凯文·凯利 / 博尔赫斯 / 海明威 / Dijkstra / 孙子 / CMM / 康威）。
6. 分数回写三处：scoreboard JSON / docs/article-evaluation-system / SERIES-PLAN。

## 五、发布与配套

- 首发主场：腾讯云开发者社区（TVP）。
- 节奏：周更 1 篇，16 篇约 16 周。
- 配图：每篇一张核心图，走 derekimage-evolution 闭环。
- derekcoding 联动：每篇末尾活注脚链具体文件；调研/写作中发现的 derekcoding 方法论缺口，沉淀进 `feedback-to-derekcoding/`。
- 双语：英文重写（essay），走 derekwritting-evolution-en 门禁。

## 六、回馈 derekcoding 交付

- 系列完成（或阶段完成后）产出 `feedback-to-derekcoding/special-for-derekcoding.md`。
- 内容：多 Agent 调度模式、门禁与审计量化、约束求解实际落地观察。
- 纪律：给明确落点（对应 derekcoding 哪个 methodology）、标"待内化确认"、不拍板。

## 七、验收清单

- [ ] 十六篇均含钩子 / 论点 / 实证 / 目标分 / 突破方向
- [ ] 每篇过门禁 G1-G5 + 评估超前均 + derekcoding 活注脚
- [ ] 每篇突破维度取前序未用矿源
- [ ] 调研报告（survey）被至少一篇作为方法论对比引用源
- [ ] 回馈 derekcoding 的 special 文档已产出具落点建议
- [ ] 完成后并入《RefactoringSoftwareEngineering》并在其上登记