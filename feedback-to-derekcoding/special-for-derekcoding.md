# Special for derekcoding-framework · 多 Agent 生产力系列研究成果回馈

> 定位：本系列调研 + 实证 + 写作过程中，对 derekcoding-framework **方法论缺口 / 可强化点**的系统化回馈。以文档形式交付给 derekcoding 团队，供其判断是否内化进 methodology。
> 版本：v1.0 ｜ 日期：2026-09-05 ｜ 编写：derekwang85 × AI
> 纪律：每条给明确落点（对应哪个 methodology 文件、建议新增哪节/新文件），统一标注"待内化确认"，不替 derekcoding 拍板。

---

## 摘要

本系列以 derekcoding #19（多模型约束求解）+ SmartQuant（多 Agent 调度）为母版，对照 GitHub 高分多 Agent 项目做了方法论对比。以下是从"生产方视角"（derekcoding 是框架，聚焦约束与开发）与"调度方视角"（SmartQuant 是运行时，聚焦路由与门禁）交叉生出的、现有 methodology 未充分覆盖的沉淀。

---

## 建议一：新增「多 Agent 调度层」方法论（建议新文件 methodology/20-agent-dispatch.md）

**现状缺口**：#19 解决"多模型选型/校验"，13-swarm 解决"决策多视角"，但缺少一层**"多 Agent 在运行时如何被调度、路由、门禁、审计"**的完整方法论（对应 SmartQuant 的三层路由 + 9 角色 + decision.db）。

**建议内容**（供 derekcoding 判断）：
- 三层路由（L1 意图层 / L2 能力层 / L3 执行层）的定义与适用边界。
- 9 角色 registry 的责任切分模式：strategy / backtest / improvement / factor_mining / market_monitor / statistical / briefing / governance 等。
- 调度与 #19 的衔接：Resolver 选模型 → 调度选 Agent → Observer 观测 → Governance 门禁。

**关联现有资产**：#19 约束求解、13-swarm、16 模式 12/15、17 原则 2/8。

## 建议二：强化「门禁与审计的量化雏形」

**现状**：#19 Golden Data 讲了基准对照与参数版本快照；SmartQuant 有 G1-G7 与 decision.db。

**建议强化点**：
- 给门禁设"证据必须可归档"显式硬闸（从隐性要求升格）。
- 审计建议"结果到参数版本快照"归因链，避免"跑得出结果却说不清参数组合"。
- 可考虑补一节"审核密度分级"：多大项目配多严门禁与多细审计。

**落点**：#19 Golden Data 节 + 03-gate-design + 07-fulltest-regression。

## 建议三：补齐「能耗/成本护栏」方法论分支

**现状**：#19 只言"单模型够用就别上多模型"（原则 2）。

**建议**：把"上多 Agent 前的成本-收益自检"独立成一节：token/延迟/编排复杂度 vs 覆盖/可信收益的可量化权衡。可对齐我们调研中 OpenAI Swarm"实验性"定位的反面教训。

**落点**：#19 与 17 原则 2。

## 建议四：观察记录（供 derekcoding 参考，非必须内化）

- 头部分级项目中，MetaGPT 的"结构化报文"、RD-Agent 的"回测硬门禁"、TradingAgents 的"对抗辩论+审批"，与我们已有资产的理念同构（契约层、门禁、swarm）。这些可作为 #19 与 future 调度方法论的"外部参照表"素材。
- 一个可留意的反模式：多数 Agent 框架"缺宣称对齐"，也是审查报告常见批评点；derekcoding #19 已内化该点，是优势，可对外作为差异化宣传。

---

## 交付与内化流程建议

1. derekcoding 团队审阅本文件，勾选内化项。
2. 建议一（调度层）若采纳，建议落为 methodology/20 新文件。
3. 内化完成后，可在 derekcoding README 登记"外部反馈来源"，并回链接本系列，形成双向闭环。

---

*本文件由 MultiAgentFabrication 系列产出。关联：[../SERIES-PLAN.md](../SERIES-PLAN.md)、[../docs/multi-agent-survey.md](../docs/multi-agent-survey.md)。*