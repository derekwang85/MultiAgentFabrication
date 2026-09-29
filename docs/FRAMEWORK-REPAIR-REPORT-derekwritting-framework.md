# derekwritting-framework 修复与改进交接报告

> 生成：2026-09-27 · 来源项目：MultiAgentFabrication · 用途：本报告是"跨项目/跨Agent规约资产双向回流"的母版端交接手册。你在本项目的工作已收敛，剩余动作需要到 `derekwritting-framework` 仓库内完成。按本报告第 3-5 节执行即可。
>
> 交接人对母版现状已逐项核查（README / SKILL-REGISTRY / CHANGELOG / EXPERIENCE-INTAKE / 成员卡 / tools/），下表"✅"为已验证真实存在的状态，不是流程性声明。

---

## 1. 交接一句话

MultiAgentFabrication 已把它的适配创新与实际写作实证反向提交到母版（吸收文档 + README 登记 + 成员卡形态修正），但在母版的 `SKILL-REGISTRY` 与 `CHANGELOG` 两条登记链上仍未入账，且吸收流程的**终态裁决需由你（人工）执行**。你在母版侧只有 2 个必须亲手做的动作 + 2 个可挑选的增强，其余均为扫描核对。

---

## 2. 母版端现状核查（交接时真实状态，已核实）

| 契约资产 | 母版现状 | 已/未 | 证据 |
|---|---|---|---|
| `LEARNINGS-MultiAgentFabrication.md` | 已落盘，含 R1-R4 与待办 | ✅ 已写入 | 文件存在于母版根目录 |
| `README.md` 登记 | 第 87 行已登记该项目，标注"待内化确认" | ✅ 已登记 | README 目录树 + 备注 |
| 成员卡 `team-memory/members/derekwang85.md` | 第 26/30 行形态已修正为 `research×blog 混合` | ✅ 已修正 | 含本项目配置细节 |
| `tools/` 回源脚本 | `review-swarm-prompt.md`、`scannability-check.py` 已在母版 tools/ | ✅ 已存在 | filecmp 逐字节一致 |
| `SKILL-REGISTRY.md` 登记回源增强 | grep `MultiAgent` 无命中 | ❌ 未登记 | 仅框架 V2.0 自身演进项 |
| `CHANGELOG.md` 记录本项目吸收 | 无任何 `MultiAgent` 条目 | ❌ 未记录 | `git log` / 内容均无 |
| 吸收终态（EXPERIENCE-INTAKE 步骤6） | 需人工裁决，未闭环 | ⏳ 待你确认 | `intake.auto_adopt=false` |

**结论**：母版侧 `SKILL-REGISTRY` 与 `CHANGELOG` 是明确缺口；吸收终态是你的 HITL 项。

---

## 3. 你在母版必须做的 2 个动作（HITL 决策层）

### 3.1 完成吸收终态裁决（对 R1-R4 逐条判 A/B）

依据 `docs/EXPERIENCE-INTAKE.md` 步骤 4：每条反哺经验判定吸收强度——**A 档（强，进宪法/门禁/默认配置）** 或 **B 档（弱，仅进 wiki/案例）**。四条经验与建议判决（系统建议，最终由你拍板）：

| 编号 | 经验内容 | 建议判决 | 理由 |
|---|---|---|---|
| R1 | g5 均值门禁从 3.5 收紧到 3.8（13 篇全过，有效） | A 档 | 有 13 篇实证 + scoreboard 佐证，且只在提高要求不破坏兼容 |
| R2 | 评审团 +2 角色（方法论论证审计员 / 读者代表） | B 档 → 观察 | 提升明显但需更多项目复现，先案例化 |
| R3 | 中英双语隔离 + derekinside 活注脚（科研形态） | A 档（仅形态变量，非默认） | 科研输出形态下建议为可选项，不污染默认博客形态 |
| R4 | 4 条方法论建议（review-swarm-prompt 落地化等） | B 档 | 建议级，需框架作者评估通用性 |

> 若你同意以上判决，母版内化可用 **A 档直入 + B 档相对路径**：A 档写入官方文档/默认门禁，B 档写入 `wiki/` 案例。最终闭环以你在母版确认页签名为准。

### 3.2 首轮 lesson-capture 入库（可选但推荐）

运行母版 `tools/team-core/dw-lesson-capture.py` 首个真实吸收，把首条经验落成团队仓 `patterns/derekwang85/` 资产卡。这一步会把"回流数据的最后一公里"跑通——此前该方法论只完成到"文档接线"，从未用真实数据验证全流程。

```bash
# 在 derekwritting-framework 仓根目录执行；参数协议已按脚本真实接口核实
cd C:\Users\A\Documents\derekwritting-framework
python tools/team-core/dw-lesson-capture.py \
  --since=24h \
  --source=git,review,retro,learnings \
  --team="C:\Users\A\Documents\derekwritting-framework\team-memory" \
  --owner=derekwang85 \
  --auto-commit
```

> 注意：脚本接口为 `--since` / `--source` / `--team` / `--owner`，落点为 `team-memory/patterns/{owner}/`。首次运行前确认 `team-memory/patterns/derekwang85/` 已按 write-asset 契约创建（可先看脚本是否自建；不自建则手动 `mkdir`），其余协议细节见来源项目 `docs/CP-LOOP-LESSON-CAPTURE.md`。

---

## 4. 母版端待办清单（按优先级，含可直接粘贴的登记内容）

### P0：登记 `SKILL-REGISTRY`（缺，2 分钟）

在 `SKILL-REGISTRY.md` 的"V2.0 进化新增能力"表中追加下表行：

```markdown
| 能力 | 实现 | 用途 | 状态 |
|---|---|---|---|
| 科研形态适配模板（可选） | config 新增 `gates.g5_rubric_mean_threshold` 档位 + `review_swarm.extra_roles` 注入 | 科研/专栏输出形态下可选的评审配置，默认不开启 | 建议 promote（待裁决） |
| 回源脚本正式索引 | `tools/review-swarm-prompt.md`、`tools/scannability-check.py` 已在仓 | MultiAgentFabrication 已实际使用并通过实证 | 已回源 2026-09-26 |
```

### P1：补 `CHANGELOG` 记录（缺，1 分钟）

在 `CHANGELOG.md` 的 `[Unreleased] > Added` 追加：

```markdown
- Added: MultiAgentFabrication 首批经验回流——g5 阈值收紧实证（3.5→3.8）、评审角色扩展、科研形态适配值，登记于 LEARNINGS-MultiAgentFabrication.md
```

### P2：联动更新模式（改进建议，S1 承接位）

在 `docs/EXPERIENCE-INTAKE.md` 补一节"回源节奏"，约定**系列发满一批（本项目 = 13 篇）即自动触发一次回流评审**，让回流从"偶然手动"变为"里程碑自动"。完整设计见来源项目 `docs/FRAMEWORK-IMPROVEMENT-PROPOSAL.md` S1。

---

## 5. 体系建议承接位（母版可选的 3 个增强）

| 建议 | 来源项目文档 | 母版承接动作 |
|---|---|---|
| S1 回源节奏定义 | `docs/FRAMEWORK-IMPROVEMENT-PROPOSAL.md` §S1 | `EXPERIENCE-INTAKE.md` 补"回源节奏"节 |
| S2 科研形态可配模板 | 同上 §S2 | `framework.config.json` 或模板仓库加形态档位 |
| S3 patrol 增加 `intake_backlog` 对账项 | 同上 §S3 | patrol 巡检项加入"回流休眠检测" |

> 这三项均为框架侧能力增强，非本项目缺陷，你按框架演进优先级自行排期即可。

---

## 6. 交接完成验收（母版侧 checklist）

- [ ] `SKILL-REGISTRY.md` 已登记回源增强（P0）
- [ ] `CHANGELOG.md` 已记录本项目首条吸收（P1）
- [ ] R1-R4 吸收判决完成（3.1，A/B 已拍板）
- [ ] （可选）`patterns/derekwang85/` 首条资产卡已生成（3.2）
- [ ] 如需 S1-S3 框架增强，已承接或排期（第 5 节）

---

*本报告由 MultiAgentFabrication 侧自动生成。来源端（本项目）已完成三档修复并通过第二轮复检（无涟漪）；母版端以上清单为剩余交接工作。*