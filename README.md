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

十四篇正文（第 1-12 篇核心 + 收尾），组织骨架：**总纲 → 约束求解六件套展开 → 调度编排 → 实证项目全景 → 收尾与并入**。加序章（第 0 篇）与后记（第 13 篇），全系列十六篇。

| # | 标题（暂定） | 核心钩子 | 项目实证 | 对标 GitHub 项目 |
|:-:|------|------|---------|------------|
| 0 | 序章：很多 Agent，然后呢？ | 从"会干活的 Agent"到"一群共犯" | SmartQuant 多 Agent 演进 | — |
| 1 | 约束即配置：从硬编码 if-else 到声明式画像 | 加模型 = 加配置，别改核心 | method 19 Registry + SmartQuant | LangChain / Ollama |
| 2 | 选型是求解：为什么线性 fallback 是陷阱 | 约束求解 > 预设备胎路径 | method 19 Pipeline Resolver | LangGraph |
| 3 | 模型要测不要猜：golden data 自评估 | 双阶段探测、震荡冻结 | method 19 Profiler + derekinside | — |
| 4 | 搭便车的观测：零成本被动监控 | 观测 walk 的 side-effect | method 19 Passive Observer | — |
| 5 | 少数派也能对：加权共识与防分母错觉 | 确定性规则 > 多数弱智 | method 19 Consensus Engine + derekinside | AutoGen |
| 6 | 宣称要和事实对齐：评测基线与自证 | 没有基准的分是假分 | method 19 Golden Data + SmartQuant 审查 | promptfoo / langfuse |
| 7 | 角色编排：从裸 Agent 到 9 角色调度 | 把责任切成注册表 | SmartQuant 9 角色 + ARCHITECTURE | CrewAI / MetaGPT |
| 8 | 三层路由与门禁：向谁说话、能做什么 | L1/L2/L3 + MCP 三档权限 | SmartQuant multi-agent 集成 | — |
| 9 | 人工进圈：HITL 闸门与反馈回流 | 人不是看客是循环的一环 | SmartQuant HITL + decision.db | — |
| 10 | 审计即记忆：把每次决策留在 decision.db | 可归因、可复盘、可回流 | SmartQuant decision.db | langfuse |
| 11 | 方法论对比：18+ 高分项目的共识与分歧 | 从 MetaGPT 到 STORM 的谱系 | 调研报告 | MetaGPT/AutoGen/STORM... |
| 12 | 特色主张：什么样的多 Agent 才叫生产力 | 把六件套拧成一个自证闭环 | 全系列收束 | — |
| 13 | 后记：并入《重构软件工程》 | 多 Agent 是工程重构的一环 | 交棒 | — |

每篇同一个配方：**方法论 + 真实项目实证 + 可复制清单 + derekinside 活注脚**。

---

## 写作优势与配方

本系列完全继承 AIHarnessMethodology 已验证的写作方法（见 [constitution/README.md](constitution/README.md)）：

- **进化评估闭环**：逐篇评分**严格超前序均值**，至少落实一个**前序未用过的突破维度**，分数记入 `writing-harness/evaluation-scoreboard.json`（复用 `evaluate.py --next / --record`）。
- **写作门禁**：完稿先过 `writing-harness/writing-gates.py` 的 G1-G5，门禁不过不进评分。
- **固定三段配方**：方法论 ~40% + 项目实证 ~40%（每条可指认具体文件）+ 可复制清单 ~20%。
- **derekinside 活注脚**：每篇结尾留一句"这个机制在 derekinside / derekcoding 里长这样"。
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
├── SERIES-PLAN.md                 # 系列策划（v1 十六篇版）
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
├── wiki/                          # llm-wiki 可查询知识库（概念五层分类 + 一手源溯源，W1-W4 门禁）
├── feedback-to-derekcoding/       # 回馈 derekcoding-framework 的交付物目录
│   └── special-for-derekcoding.md # 多 Agent 系列研究成果（专为 derekcoding 定制）
└── articles/
    └── 00-prologue.md             # 序章（样稿待审）
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

1. **不写框架教程**——Menu 级对接教程是红海。
2. **不写泛 Agent 科普**——多 Agent 是什么，别人已写烂。
3. **只写「方法论 + 真实项目实证 + 可复制清单」**，实证优先指认 derekcoding / derekinside / SmartQuant 的具体文件。
4. **不引精确 GitHub star 数**——只用相对定位（调研环境曾出现数据污染）。
5. **每条实证都能自证**——能跑出来的才写，宣称必须对齐事实。