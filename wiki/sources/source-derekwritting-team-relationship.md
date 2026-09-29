# 一手源 · 与 derekwritting-framework 的团队-个人关系
> 框架路径：`c:\Users\A\Documents\derekwritting-framework`（GitHub: `derekwang85/derekwritting-framework`）。
> 作用：记录本项目（MultiAgent Fabrication）如何引用 derekwritting-framework，以及两者之间「团队-个人」的关系契约与经验回流通道。

## 引用方式（通道 A 注入 + 通道 C/D 回流）

按 derekwritting-framework `docs/USAGE-CONNECTING-PROJECTS.md` 的连接模型，本项目采用「**A 注入 + C/D 回流**」组合：

| 通道 | 方向 | 本项目落位 | 状态 |
|------|------|-----------|------|
| A 注入 | 框架 → 项目 | `writing-harness/` 独立副本 + `framework.config.json` 差异化适配 | ✅ 已完成（adapted-lite） |
| D 自动接入 | Agent → 框架 | `dw-project-onboard.py` 探知/配置/挂接三步 | ✅ 2026-09-22 完成 |
| C 回流 | 项目 ↔ 团队仓 | 写前回溯 recall + 写毕沉淀 lesson-capture 到 `team-memory/` | ✅ 通道已接通 |

**核心纪律**：脚本跟着框架、配置跟着项目；差异只落在 `framework.config.json` 与 `IDENTITY.md`，不修改 `writing-harness/*` 脚本（升级回源走 `docs/UPGRADE.md`）。

## 团队-个人关系契约（对齐框架 ADR-001 三层作用域）

| 层 | 归属 | 本项目落位 |
|:--|:--|:--|
| 方法论/工具层（天然共享） | derekwritting git 仓 | 本项目继承其 constitution / methodology / skill / wiki 口径 |
| 成员写作项目层（默认 private） | derekwang85（个人） | MultiAgent Fabrication 项目本体，本地 / 个人 repo |
| 团队共享层（显式 `visibility: team`） | team-memory 仓 | 本项目经验经回溯/沉淀通道回流，个人私稿绝不入仓 |

**成员归属**：本项目作者 `derekwang85` 作为 derekwritting-framework 团队成员（个人），其名下写作项目（含本项目 MultiAgent Fabrication 与姊妹系列 RefactoringSoftwareEngineering）共享经验到团队仓。成员卡：`derekwritting-framework/team-memory/members/derekwang85.md`。

## 经验回流通道（本项目已接通）

- 写前回溯：`python <framework>/tools/team-core/dw-recall.py --team <framework>/team-memory --query "<主题>"`
- 写毕沉淀：`python <framework>/tools/team-core/dw-lesson-capture.py --team <framework>/team-memory --owner derekwang85`
- 契约要求：沉淀资产必须 `visibility: team` + 一手 `sources:`，否则校验 fail-closed 拒写

## 提炼吸收表

| 吸收的经验 | 落位 | 内化级别 |
|-----------|------|---------|
| 引用方式：A 注入 + C/D 回流（不并入框架本体） | `../docs/WRITING-FRAMEWORK.md` 第一节 | A 强 |
| 团队-个人边界：项目默认 private，显式才共享 | `wiki/sources/source-derekwritting-team-relationship.md` | A 强 |
| 历史回源纪律：脚本跟框架、配置跟项目 | `../docs/WRITING-FRAMEWORK.md` 第九节 | A 强 |

## 舍弃表

| 未吸收 | 原因（一致性判定） |
|--------|------|
| 把 framework.config 与 IDENTITY 的父子关系强绑定为一个 owner 多项目 | 框架按 owner 建成员卡，一个 author 多项目共享一张卡，靠项目清单区分 |

## 来源归属

- derekwritting-framework（Apache 2.0）由 derekwang85 维护；本页记录本项目与其连接关系，未改动框架本体。

## 门禁评审留痕（W1-W4）

- 溯源完整度 4.0/5：一手文件可指认（`USAGE-CONNECTING-PROJECTS.md`、`ADR-001`、成员卡），吸收/舍弃双向成表。