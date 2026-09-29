# 反哺回执 · LEARNINGS-REFER-BACK-derekwritting-framework

> 反哺日期：2026-09-26 ｜ Owner：derekwang85 ｜ 目标：`C:\Users\A\Documents\derekwritting-framework\team-memory`
> 性质：本项目（MultiAgentFabrication）**内部经验 → 团队共享资产** 的回流（scope-rules G-TRANS: personal → team）。
> 方向说明：与 `docs/EXPERIENCE-INTAKE.md`（外部吸收）方向相反——本文件记录"本项目**发出**了什么经验、依据哪层资产、在团队仓的落点"，作本项目经验可追溯性的一手证据。姊妹项目 RefactoringSoftwareEngineering 已有同构反哺文档（`../RefactoringSoftwareEngineering/docs/LEARNINGS-REFER-BACK-derekwritting-framework.md`）。

---

## 一、反哺立项（对应 EXPERIENCE-INTAKE 步骤 1 的方向）

- **反哺什么**：本项目在"多 Agent 形成生产力方法论"科研×博客混合系列（约束求解六件套 + 调度编排 + 可自证闭环）13 篇写作实证中，产出的若干**本项目独有、未见于 derekwritting-framework 既有 methodology/config 的适配参数与方法论**。
- **为什么值得反哺**：这些是框架"棘轮式演进"期望的上游实证回传——本项目把框架的门禁阈值、评审角色、形态模板在真实科研型内容上跑出了差异化的实证值，回灌团队仓后可供生态内其它成员项目（尤其是科研定位项目）回溯复用。
- **成功的判据**：① 适配值参数化记录（本文件）；② 沉淀为 `visibility: team` + 一手 `sources:` 的团队资产卡；③ 能被 `dw-recall.py` 实测回溯命中；④ 若跨项目验证通用，进一步 promote 回框架 `methodology/` / config 默认值。

## 二、反哺条目（基于一手证据，证据出处逐条标注）

### R1 · 科研×博客混合形态下的门禁阈值收紧（阈值实证）
- **现象/做法**：本项目 `framework.config.json` 将 `g5_rubric_mean_threshold` 从母版默认 `3.5` 上调至 `3.8`；理由：科研型深度方法论 content，`trust # robustness` 加权下人工尺度阈值需上提，故事化、可读性权重下降、严谨性上升。
- **提炼落点**：契约层门禁（阈值可由 `framework.config.json` 覆盖，正合 EXPERIENCE-INTAKE 步骤 4 的 A 档可配位）。
- **证据出处**：`framework.config.json` → `gates.note`；`docs/WRITING-FRAMEWORK.md`（科研形态定位）。
- **缺什么（回灌后待提炼）**：建议框架为"混合形态"提供内置阈值建议档位（可信科研 > 单口径科普），而非仅单一 `3.5` 默认。

### R2 · 科研形态的 review_swarm 附加角色（评审角色扩充）
- **现象/做法**：在母版默认"5 正面 + 1 反方"基础上，新增 `extra_roles: ["方法论论证审计员", "读者代表"]`，用于科研×博客混合稿的 G5 分离评审——前者盯"论证是否成方法论而非个人经验记录"，后者盯"可扫读落地 vs 考据严谨的两端平衡"。
- **提炼落点**：工具层模板（`writing-harness/review-swarm-prompt.md` 已回源并叠加附加角色）+ 契约层。
- **证据出处**：`framework.config.json` → `review_swarm.extra_roles`；`writing-harness/review-swarm-prompt.md`（Phase 1.5 附加角色）。
- **缺什么**：框架 `tools/review-swarm-prompt.md` 默认仍为 5+1，未把"附加角色可通过 config 注入提示词模板"做成可配位。

### R3 · 中英双语隔离 + derekinside 活注脚（双语写作工艺）
- **现象/做法**：本项目把 `allusion-isolation` 强化为中英典故隔离 + 双语重跑；并首创 "derekinside 活注脚"——每篇强制带一段作者自己打自己脸的实时反思注脚，链到具体 article 文件，作为"人等 AI、清醒 POV"的落地工艺。
- **提炼落点**：纪律层（写作工艺）+ 契约层（评审强制项）。
- **证据出处**：`constitution/README.md`（回馈纪律）；13 篇稿件 derekinside 段落；`docs/WRITING-FRAMEWORK.md`。
- **缺什么**：框架未把"中文典故与英文典故池隔离、双语需重跑门禁""作者活注脚"固化为通用工艺项。

### R4 · 多 Agent 方法论可反哺框架的 4 条建议（契约层候选）
- **现象/做法**：本项目在调研 + 实证 + 写作中，给 derekcoding 框架提炼了 4 条方法论建议：① 新增「多 Agent 调度层」方法论（`methodology/20-agent-dispatch.md`：三层路由 + 角色 registry + 调度-检测-门禁衔接）；② 门禁与审计量化雏形（证据可归档硬闸 + 参数版本归因链）；③ 能耗/成本护栏；④ 外部参照表（MetaGPT/RD-Agent/TradingAgents 理念同构）。
- **提炼落点**：契约层新 methodology（建议一）+ 门禁强化（建议二）+ 契约层成本护栏（建议三）+ 参考素材（建议四，软约束）。
- **证据出处**：`feedback-to-derekcoding/special-for-derekcoding.md`（v1.0）；已改写为母版侧吸收文档 `derekwritting-framework/LEARNINGS-MultiAgentFabrication.md`。
- **缺什么**：需 derekcoding 团队 / 用户裁决是否内化进 methodology（A/B 强度见吸收文档步骤 4）。

## 三、内化决议（回灌 A/B）

- R1、R3 在本项目侧为 A 强资产（纳入默认系列流程）；团队仓侧以 `type: decision` + `visibility: team` 引用卡回灌。
- R2 在工具模板已落位（本项目 review-swarm-prompt 已回源叠加角色）；团队仓侧沉淀并可促框架默认支持 extra_roles。
- R4 在母版侧为"待内化"吸收文档（`LEARNINGS-MultiAgentFabrication.md`），A/B 强度待用户裁决，不擅自改 framework methodology。

> 保持一致性与 G-TRANS 免打扰：先以团队共享资产沉淀引用卡，待跨项目验证通用后再 promote 回框架本体。

## 四、登记确认（对应 EXPERIENCE-INTAKE 步骤 5）

- [x] 反哺档案已建（本文件）
- [x] source 侧回馈文档已存在（`feedback-to-derekcoding/special-for-derekcoding.md`）
- [x] 吸收侧文档已建（`derekwritting-framework/LEARNINGS-MultiAgentFabrication.md` 并在 README 登记）
- [ ] 团队仓资产卡已写入 `team-memory/decisions/derekwang85/`（R1~R4）——待 dw-lesson-capture / verify-write-asset 跑通
- [ ] 每张卡通过 `verify-write-asset.py` fail-closed 校验
- [ ] `dw-recall.py` 实测回溯命中
- [ ] 第三层 promote 建议卡已生成并跑 `check-drift`

## 五、评审记录（G5）

- rubric 自评：目标明确（沉淀科研形态适配参数 + 方法论建议）、读者具体（团队仓维护者 / 框架生态成员 / 科研定位项目）、立场清晰（回流而非吸收）。
- 剩留问题：
  1. R1~R4 若需落成团队仓资产卡，需运行母版 `dw-lesson-capture.py` / `verify-write-asset.py` 生成 front-matter 资产并回写 `counters.json`；当前以本文件为可追溯性档案，资产卡生成待工具验证。
  2. 母版 `EXPERIENCE-INTAKE.md` 剩留问题①"尚未用真实吸收验证全流程"——本项目可成为其首个跑通对象，需用户确认后走通步骤 6。
- 复校日期：2026-09-26。

---

*本反哺档案由 MultiAgentFabrication 系列产出，作为项目→框架回流资产。关联：`feedback-to-derekcoding/special-for-derekcoding.md`、`derekwritting-framework/LEARNINGS-MultiAgentFabrication.md`、`derekwritting-framework/team-memory`。*