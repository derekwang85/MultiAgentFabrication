# MultiAgent Fabrication · 多 Agent 生产力编织

> 一套原创的「多 Agent 形成生产力」方法论，源出 [derekcoding-framework](https://github.com/derekwang85) methodology #19 的约束求解框架，与 SmartQuant 项目中多 Agent 应用与调度的真实经验，对照 GitHub 高分多 Agent 体系项目，写成可复用的工程方法论。
> 本系列完成后并入《重构软件工程》体系，作为其核心延伸；研究成果以独立文档回馈 derekcoding-framework。

<p align="center">
  <a href="#系列地图"><strong>系列地图</strong></a> ·
  <a href="#写作优势与配方">写作配方</a> ·
  <a href="#方法论对比">方法论对比</a> ·
  <a href="#目录结构">目录结构</a>
</p>

---

## 这个项目是什么

一个系列技术方法论，主题是 **Multi-Agent 如何真正形成生产力**。

社区已有的多 Agent 内容几乎全是三件事：
1. **框架教程**——教你怎么用 MetaGPT / AutoGen / LangGraph / CrewAI；
2. **概念科普**——多 Agent 是什么、有什么模式；
3. **Demo 炫技**——几个 Agent 对话出结果，看起来很美，落地就散。

本系列不重复这些，只讲一个别人不讲的问题：

> 为什么大多数"一群 Agent 一起写代码"的尝试，最后收获的是一群**需要人盯的共犯**，而极少数系统（如 SmartQuant dispatch）能把一群 Agent 拧成一股**自己转的生产力**？

核心命题一句话：

> 多 Agent 不是"很多人开工"，而是**把任务、责任与约束在多个智能体之间做分工设计**；生产力的关键是**让分工形成闭环并可度量**，而不是让 Agent 变多。

## 作者

- **王海涛 / derekwang85**
- 腾讯云 TVP（Tencent Cloud Valuable Professional）
- 腾讯云架构师名人堂

---

## 系列地图

全系列 15 篇（篇外对照专题 0.5 + 序章 0 + 正文 1-12 + 锚点篇 13），按**四幕递进**：为什么来 → 是什么 → 怎么用 → 到哪去，紧扣一条主线。篇外对照专题 0.5 在序章与篇 1 之间，正面拆解"运行时也会派子 Agent（Codex / TRAE / OpenClaw）"与"Multi-Agent 多 Agent"这一最容易看错的分野。锚点篇 13 立起双层架构（元 Agent 造系统的 / 产品 Agent 在系统里的）与 k1-k4 四层记忆手递手，作为横向脊梁回焊第 08、09、12 篇。
> **主线：多 Agent 不是让人海战术，而是把一个不透明、不可证明的单点判断器，改造成一个可分工、可校验、可审计的 Multi-Agent。** 完整论纲见 [SCOPE.md](SCOPE.md)。

| # | 标题（中/英） | 核心钩子 | 项目实证 | 对标 GitHub | drawio | 状态 |
|:-:|------|------|---------|------------|:---:|:-:|
| 0.5 | 我们 vs Subagent：一个非常容易被看错的对照 / Us vs. Subagents: the Contrast That Keeps Getting Misread | 你都 subagent 了，为什么还折腾 Multi-Agent？ | 分层记忆 / 隔离验证 / decision.db | Codex/TRAE/OpenClaw 运行时子 Agent | ✅ 八维对照图 | ✅ |
| 0 | 序章：一个不能自我证明的判断器 / The Unprovable Judge | 从黑盒判断器到 Multi-Agent | SmartQuant 演进 | 全谱系 | ✅ Multi-Agent 总览 + 全系列地图 | ✅ |
| 1 | 单个 Agent 的信任危机 / The Trust Crisis of a Single Agent | 输出有 A/B，谁是对的 | 单 Agent 失效实例 | LangChain | ✅ 判断失效模型 | ✅ |
| 2 | 分工是判断的可重构 / Division as Reconstructible Judgment | 不是人多，是责任可切 | SmartQuant 三层 | CrewAI/MetaGPT | ✅ 三层分工 | ✅ |
| 3 | 三条轨与三权 / Three Tracks & Three Powers | 分工要配问责 | 三轨制/WBS/Issue | AutoGen | ✅ 三轨 + 三权 | ✅ |
| 4 | 选型是求解 / Selection as Constraint Solving | fallback 是陷阱 | 方法 19 Resolver | LangGraph | ✅ 约束求解漏斗 | ✅ |
| 5 | 约束即配置 / Constraints as Configuration | 加模型=加配置 | 声明式画像 | LangChain/Ollama | ✅ 模型画像 schema | ✅ |
| 6 | 少数派也能对 / The Minority Can Be Right | 多数一致≠多数正确 | Swarm 对抗决策 | AutoGen | ✅ Swarm 五相 | ✅ |
| 7 | 宣称对齐事实 / Claims Aligned with Facts | 假分是最大的债 | Bad90 反欺诈 | promptfoo | ✅ 基准对照 Gauge | ✅ |
| 8 | 治理优先于调度 / Governance before Dispatch | 先立规矩再派人 | 方法 20 门禁 | MCP 权限 | ✅ 治理门禁 | ✅ |
| 9 | 人不进圈才是浪费 / Humans Inside the Loop | HITL 是闭环非妥协 | SmartQuant HITL | AutoGen | ✅ HITL 回流闭环 | ✅ |
| 10 | 组织学的一课 / A Lesson in Organization | Multi-Agent=微型组织 | 三权/制衡/问责 | 科层/一般系统论 | ✅ 组织对照 | ✅ |
| 11 | 生产力的可编程化 / The Programmability of Productivity | 判断力从人转移到可编程系统 | 全系列收束 | 政治经济学/技术史 | ✅ 生产力结构迁移 | ✅ |
| 12 | 后记：熵的账本 / Epilogue: The Ledger of Entropy | Multi-Agent 的最终计量 | 决策留痕=记忆 | 无（收官对照） | ✅ 审计记忆闭环 | ✅ |
| 13 | 两层 Agent：造系统的，与在系统里的 / Two Layers of Agents: Those Who Build, and Those Who Work Inside | 双层架构 + 记忆手递手 | 元层建造 → 产物下发 → 产品层当班 | 层级委派对照 | ✅ 双层工厂/车间 + 四层记忆总线 | ✅ |

每篇同一个配方：**钩子 → 主张（回主线）→ 实证（落地取舍）→ 原理飞升 + 交棒**；中英双语双面，配 1-2 张 drawio 并过几何 QA。锚点篇 13（A9）为横向脊梁：元层只读 k1+k2、产品层读 k1+k2+k3，经验只沿 k4 单向回流管道（ADR 审计 + 人终裁）升格为规则。

**谱系对照（2026-09-28 收缩主线）**：主体保留"序章 0 + 正文 1-12 + 锚点 13"不扩篇幅，广度靠每篇正文末尾的「谱系定位」外拓——显式点名本文落在哪一格 Agent 应用（研报/RAG 自动化、SWE Agent/编排框架、Agentic RPA/企业 Copilot、多 Agent 辩论·对抗、MCP/工具生态）、对话哪类应用、又刻意不覆盖什么。序章上线 `fig-00-key` 全系列地图，四幕 + 锚点篇 + 谱系带一张拎起，与 `fig-00-pipeline` Multi-Agent 流水线图互为表里。另在序章与篇 1 之间增补**篇外对照专题 0.5**，正面拆解"运行时 Subagent vs Multi-Agent 多 Agent"——防止读者在抵达锚点前误判"这是另一种 subagent"。

---

## 写作优势与配方

本系列完全继承 AIHarnessMethodology 已验证的写作方法（见 [constitution/README.md](constitution/README.md)）：

- **进化评估闭环（荆棘轮）**：逐篇评分**严格超前序均值**，至少落实一个**前序未用过的突破维度**，分数记入 `writing-harness/evaluation-scoreboard.json`（复用 `evaluate.py --next / --record`）。
- **写作门禁**：完稿先过 `writing-harness/writing-gates.py` 的 G1-G5，门禁不过不进评分。
- **固定配方**：钩子 → 主张（回主线）→ 实证（落地取舍）→ 原理飞升 + 交棒。
- **配图纪律**：每篇 1-2 张 drawio，走 `diagrams/` 单一数据源生成，过几何 QA（R1-R3）；排版对齐须过 [diagrams/DRAWING-GUIDE.md](diagrams/DRAWING-GUIDE.md) 的对齐规约（上对齐 / 等宽列 / 健中缝 / 居中帽带）。
- **引经据典**：每篇 2-3 处，取前序未用过的出处（组织学 / 系统论 / 开源历史）。

---

## 方法论对比与经验升华

本系列对齐了 GitHub 高分多 Agent 体系项目，调研成果沉淀在 [docs/multi-agent-survey.md](docs/multi-agent-survey.md)，核心结论：

| 谱系 | 代表项目 | 组织心智 | 我们的差异点 |
|------|---------|---------|------------|
| 流水线 SOP | MetaGPT | 按角色串行，产出标准件 | 我们强调**多模并行 + 加权共识**，不依赖单一流水 |
| 网格 / Actor | AutoGen / CAMEL | 节点自由对话 | 我们强调**约束求解式选型**，不给 Agent 自由联姻 |
| 图状态机 | LangGraph | 显式状态转移 | 我们用**声明式约束**描述迁移，更接近配置而非图 |
| 层级委派 | CrewAI | 角色层级 leader-worker | 我们用 **9 角色 + 三层路由**落责任，且带门禁与审计 |
| 辩论 + 审批 | TradingAgents / RD-Agent | 多头辩论取一致 | 我们用**精度加权 + 防分母错觉**，防"多数弱智" |
| 量化硬门禁 | RD-Agent | 回测不过不放行 | 这正是我们 **G1-G7 + 证据追溯** 的同类信念 |
| 多视角搜索 | STORM | 多专家轮询成文 | 我们用 **golden data 自评估**，不靠外部 LLM 打分 |

**我们的特色主张**（详见 [docs/positioning.md](docs/positioning.md)）：多 Agent 的生产力不在"编排得漂亮"，而在**四链路闭环可自证——选型、调用、校验、自愈全部声明式 + 可复现**，外加一条别家没有的纪律：**宣称对齐**（文档说的必须能在 CI 里跑出来）。

---

## 目录结构

```
MultiAgentFabrication/
├── README.md                      # 本文件：系列总览
├── SERIES-PLAN.md                 # 系列策划（篇外对照专题 0.5 + 四幕递进 + 锚点 0.5+0+12+13，共 15 篇）
├── SCOPE.md                       # 系列纲宪：主线、论纲、差异化、边界声明
├── framework.config.json          # 写作适配配置（门禁阈值 / rubric / 评审配比的真值）
├── constitution/                  # 项目宪法：开工前必读
│   ├── README.md                  # 项目身份 / 写作铁律 / 工程原则 / derekcoding 回馈纪律
│   └── allusion-isolation.md      # 中英典故隔离表（引用纪律的落地执行件）
├── templates/                     # 规约模板：动笔前先写
├── docs/
│   ├── adr/                       # 架构决策记录
│   ├── multi-agent-survey.md      # GitHub 高分多 Agent 项目调研报告
│   ├── positioning.md             # 本系列特色主张与差异化
│   ├── WRITING-FRAMEWORK.md       # 写作框架总纲（引用 derekwritting-framework v2 适配）
│   ├── SKILL-REGISTRY.md          # 写作技能注册表（3 次晋升机制）
│   └── article-evaluation-system.md   # 人类可读评分表（镜像 scoreboard JSON）
├── writing-harness/               # 写作门禁 + 进化评估（副本自 AIHarness，独立计分）
├── diagrams/                      # drawio 单一数据源 + 生成器 + 几何 QA
│   ├── data_src.py                # 全部图数据的单一事实来源（NODES/EDGES/COLORS）
│   ├── diagram_gen.py             # .drawio + .html 双输出生成器
│   ├── arch_qa.py                 # 几何 QA（R1 不穿节点 / R2 不共线 / R3 不越界）
│   └── out/                       # 生成的 .drawio 与 .html 产物
├── wiki/                          # llm-wiki 可查询知识库（概念五层分类 + 一手源溯源，W1-W4 门禁）
├── feedback-to-derekcoding/       # 回馈 derekcoding-framework 的交付物目录
│   └── special-for-derekcoding.md # 多 Agent 系列研究成果（专为 derekcoding 定制）
├── articles/
    ├── 00-prologue.md             # 序章（已定稿，9.8）
    ├── 00-5-subagent-vs-multiagent.zh.md   # 篇外对照专题 0.5（我们 vs Subagent，已定稿 10.0）
    ├── 01-*.zh.md … 13-two-tier-meta-product.zh.md   # 正文 1-12 + 锚点篇 13（均已定稿 9.8）
    └── en/                        # 英文 essay（双语通道，15 篇镜像）
```

---

## 配套产物与联动

| 产物 | 路径 | 说明 |
|------|------|------|
| 项目宪法 | [constitution/](constitution/README.md) | 定位 + 铁律 + 工程原则 + 回馈纪律 |
| 写作框架 | [docs/WRITING-FRAMEWORK.md](docs/WRITING-FRAMEWORK.md) | 引用 derekwritting-framework v2 适配的写作总纲（配方/工序/门禁） |
| 适配配置 | [framework.config.json](framework.config.json) | 门禁阈值 / rubric / review_swarm 的机器可读真值 |
| 典故隔离 | [constitution/allusion-isolation.md](constitution/allusion-isolation.md) | 中英典故隔离表（R1-R4 判定，软约束） |
| 技能注册 | [docs/SKILL-REGISTRY.md](docs/SKILL-REGISTRY.md) | 写作技能单一事实来源（3 次晋升机制） |
| 门禁 + 评估 | [writing-harness/](writing-harness/GATES.md) | G1-G5 门禁 + 进化评估，独立计分 |
| llm-wiki | [wiki/](wiki/index.md) | 可查询概念知识库（五层分类 + 一手源溯源，W1-W4 门禁，双读者） |
| 调研报告 | [docs/multi-agent-survey.md](docs/multi-agent-survey.md) | 高分项目方法论横向对比 |
| 特色主张 | [docs/positioning.md](docs/positioning.md) | 本系列与头部项目的差异化 |
| 回馈文档 | [feedback-to-derekcoding/special-for-derekcoding.md](feedback-to-derekcoding/special-for-derekcoding.md) | 研究成果回馈 derekcoding-framework |
| 姊妹系列 | [../RefactoringSoftwareEngineering/](..%2FRefactoringSoftwareEngineering%2FREADME.md) | 本系列完成并入的软件工程重构体系 |

---

## 写作铁律

1. **主线收紧**——每篇只回答一个 A1-A9 主张，且必须说清它如何服务"Multi-Agent"主线；读者答不出关系即跑题。
2. **实证不过度承诺**——每篇落到真实项目的取舍、门禁、留痕；写不出来的步骤标"目标值"，绝不硬说跑通了。
3. **对照不止于弄潮**——每篇与主流框架（CrewAI / AutoGen / MetaGPT / LangGraph / OpenAI Swarm）显式碰一次，讲清共识与缺口。
4. **配图过硬**——每篇 1-2 张 drawio，走单一数据源生成，几何 QA（R1-R3）全过。
5. **不引精确 GitHub star 数**——只用相对定位（调研环境曾出现数据污染）。
6. **每条实证都能自证**——能跑出来的才写，宣称必须对齐事实。