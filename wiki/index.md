# llm-wiki 索引 · MultiAgent Fabrication

> 本目录把**本项目自身方法论资产**（宪法、写作框架、门禁评估、典故隔离、技能注册）与**所依赖的写作 skill**（derekwritting-evolution 等）蒸馏为可查询概念条目。
> 服务 AI Agent 与人工检索；这里是**概念级提取：一句话定义 + 来源 + 互链 + 内化级别**。
> 元规约见 `AGENTS.md`，使用指南见 `GUIDE.md`，五层分类口径见 `concepts/taxonomy.md`。

---

## 快速检索协议（供 LLM 导航）

当需要回答本项目方法 / 写作 / 质量 / 流程问题时，按此顺序定位：

1. **这个概念是什么？** → `concepts/` 找概念页（一句话定义 + 来源 + 互链）
2. **它落在框架哪一层？** → 看概念页 `## 内化级别` 与 `concepts/taxonomy.md`
3. **来自哪个一手资产？** → `sources/` 溯源，跳回项目文件路径
4. **它对应项目哪条规约？** → 从概念页回链 `../constitution/`、`../docs/WRITING-FRAMEWORK.md`、`../writing-harness/`

---

## 概念地图（按"约束金字塔"五层组织）

### 战略层 · 要做什么、边界在哪
- [[knowledge-as-asset]] — 知识是项目资产：把方法论沉淀为可查询知识库，而非只堆文章

### 架构层 · 为什么、边界怎么立
- [[reviewer-writer-separation]] — 评审与写作分离：G5 硬性要求，生成者与批判者不同角色
- [[evaluation-driven-progression]] — 评分超前均：每篇必须严格优于前序平均，形成进化闭环

### 契约层 · 怎么做、工序怎么稳定
- [[retrieval-over-content]] — 检索优于堆砌：先定位资产与证据，再成文
- [[writing-recipe-seven]] — 写作配方七条骨架：方法论 + 实证 + 清单的稳定结构
- [[progressive-disclosure]] — 渐进式披露：先给地图与配方，再分层展开细节

### 门禁层 · 怎么保证质量
- [[gate-as-verification]] — 门禁=验证而非宣告：只有通过检查才算发布证据
- [[harness-gates-g1-g6]] — 门禁流水线 G1-G6：风格 / 结构 / 事实 / 链接 / 评审 / 发布
- [[allusion-isolation]] — 中英典故隔离：引用先过 R1-R4 判定，软约束而非硬门禁

### 实现层 · 怎么沉淀与维护
- [[experience-retention]] — 经验回写：修好的故障与门禁教训沉淀进方法论文档
- [[skill-registry-promotion]] — 技能注册晋升：跨项目 3 次真实复用才晋升
- [[derekinside-note]] — derekinside 活注脚：以浓度 B 每篇一段嵌入系列经验

---

## 一手源索引（溯源 + 吸收/舍弃）

- [[source-constitution]] — 项目宪法（`constitution/README.md`）
- [[source-writing-framework]] — 写作框架总纲（`docs/WRITING-FRAMEWORK.md`）＋ 典故隔离（`constitution/allusion-isolation.md`）
- [[source-writing-harness]] — 门禁与进化评估（`writing-harness/`）
- [[source-skill-registry]] — 技能注册表（`docs/SKILL-REGISTRY.md`）
- [[source-evolution-skill]] — 所依赖的外部 skill：derekwritting-evolution（中文）/ derekwritting-evolution-en（英文）
- [[source-derekwritting-team-relationship]] — 与 derekwritting-framework 的团队-个人关系契约与回流通道

---

## 快速链接到项目原文

| 原文 | 路径 |
|------|------|
| 项目宪法 | [../constitution/README.md](../constitution/README.md) |
| 中英典故隔离表 | [../constitution/allusion-isolation.md](../constitution/allusion-isolation.md) |
| 写作框架总纲 | [../docs/WRITING-FRAMEWORK.md](../docs/WRITING-FRAMEWORK.md) |
| 技能注册表 | [../docs/SKILL-REGISTRY.md](../docs/SKILL-REGISTRY.md) |
| 门禁规约 | [../writing-harness/GATES.md](../writing-harness/GATES.md) |
| 进化评估规约 | [../writing-harness/EVALUATION.md](../writing-harness/EVALUATION.md) |
| 系列纲宪（主线/论纲/边界） | [../SCOPE.md](../SCOPE.md) |
| 系列策划（v2 四幕） | [../SERIES-PLAN.md](../SERIES-PLAN.md) |
| 画图纪律与几何 QA | [../diagrams/](../diagrams/diagram_gen.py) |