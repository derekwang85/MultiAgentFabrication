# 框架能力改进提案（针对 derekwritting-framework）

> 提案方：MultiAgentFabrication 项目（derekwang85 × AI）
> 提案日期：2026-09-26 ｜ 状态：**待框架侧裁决**（不擅自改动框架 methodology/config 默认值）
> 背景：本项目在"框架→项目"注入已深度落地的前提下，识别出框架侧可补齐的若干能力位，使"项目→框架"回流能机制化而非依赖自觉。

以下条目按 objective 的 S 档展开，均为**框架能力改进建议**，不含动代码合理性的占用。

---

## S1 · 为 EXPERIENCE-INTAKE 定义"回源节奏"（流程改进）

**问题**：`derekwritting-framework/docs/EXPERIENCE-INTAKE.md` 定义了六步外部吸收流程，但**没有明确"什么频率触发吸收"**。实测项目中 lesson-capture 从未被触发，直接原因之一就是缺少自然触发点。

**建议**：在 EXPERIENCE-INTAKE 增加节奏约定表：

| 节奏点 | 触发动作 |
|--------|----------|
| 每写完 1 篇（CP） | 运行 `dw-lesson-capture.py` 沉淀 pattern（4h 窗口） |
| 每个 series 里程碑 | 全量 capture + 生成 Promote 申请草案 |
| 每季度 | 审计 `counters.json` total_assets/stale，对账各项目回流量 |

**落点**：`docs/EXPERIENCE-INTAKE.md` 新增「节奏与触发」小节（项目侧已落地于 `docs/CP-LOOP-LESSON-CAPTURE.md` 第五节，可直接回迁）。

## S2 · 把科研形态适配值反哺为"框架可配模板"（契约层改进）

**问题**：本项目在科研×blog 混合形态下，把 gate 阈值从 3.5 上提至 3.8、给 review_swarm 叠加"方法论论证审计员、读者代表"两个 extra_roles。但框架默认仍是单一 3.5 + 5正面1反方，**混合形态作为一个可复选的形态模板在 config 层面缺位**。

**建议**：在 `framework.config.json` 的形态（format/variant）选型中，新增一类 `research_blog_hybrid` 内置模板，一键映射：
- `g5_rubric_mean_threshold: 3.8`
- `review_swarm.extra_roles: ["方法论论证审计员", "读者代表"]`
- 双语隔离 + derekinside 活注脚作为该形态的纪律项

**落点**：`framework.config.json` 支持形态预设；`tools/review-swarm-prompt.md` 支持通过 `extra_roles` 配置注入额外评审角色提示词（本项目 `writing-harness/review-swarm-prompt.md` 已实现 Phase 1.5 附加角色作为可参照样例）。

## S3 · 在 patrol 中新增 `intake_backlog` 对账项（工具层改进）

**问题**：母版全仓无 `patrol.py`；且现有 patrol/对账逻辑未把"成员项目已产生新适配值但未回流团队仓"作为可自动侦测项，导致"回流休眠"只能靠自觉。

**建议**：在设计制外巡检/对账时，新增 `intake_backlog` 检查项，自动：
1. 扫描各成员项目 `framework.config.json` 的 `adaptation_note` / review_swarm / gates 覆盖值；
2. 比对团队仓 `patterns/<owner>/`、`decisions/<owner>/` 是否已有对应资产卡；
3. 输出"有适配值但无回流资产卡"的缺口清单，作为下次 lesson-capture 的待办。

**落点**：母版巡检/调度脚本新增 `intake_backlog` 检测；本项目 `writing-harness/patrol-log.json` 已预留 assets_checked 结构作承载样例。

## S4 · 参照姊妹项目落下反哺档案（已完成 ✅）

本项目已在 `docs/LEARNINGS-REFER-BACK-derekwritting-framework.md` 落下反哺回执档案，与 RefactoringSoftwareEngineering 同构，实现多项目共享记忆网络。此条已完成。

---

## 落地状态对照

| 项 | 框架侧状态 | 项目侧已落地 |
|----|-----------|--------------|
| S1 回源节奏 | 待 EXPERIENCE-INTAKE 采纳 | `docs/CP-LOOP-LESSON-CAPTURE.md` 第五节 |
| S2 可配模板 | 待 `framework.config.json` 采纳 | `writing-harness/review-swarm-prompt.md` Phase 1.5 已示范 |
| S3 intake_backlog | 待 patrol 设计采纳 | `writing-harness/patrol-log.json` 预留 |
| S4 反哺档案 | — | `docs/LEARNINGS-REFER-BACK-derekwritting-framework.md` ✅ |

## 说明（对齐 EXPERIENCE-INTAKE 原则）

按框架 `intake.auto_adopt=false` 与 S-GTRANS 免打扰原则，以上 S1-S3 均为**提案**，最终强度与是否采纳由 derekcoding 团队 / 用户裁决，不擅自改写框架 methodology、config 默认值或工具。

---

*提案方：MultiAgentFabrication ｜ 关联：`docs/LEARNINGS-REFER-BACK-derekwritting-framework.md`、`docs/CP-LOOP-LESSON-CAPTURE.md`、母版 `LEARNINGS-MultiAgentFabrication.md`。*