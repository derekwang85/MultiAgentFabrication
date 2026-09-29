# CP 闭环 · 写毕沉淀接入指南（lesson-capture）

> 目标：把"写完即沉淀"接入本项目 CP（Current Post）写作闭环，让每篇实测落入团队仓 `patterns/derekwang85/`，实现项目→框架的经验回流可追溯。
> 依据：母版 `tools/team-core/dw-lesson-capture.py`（derekcoding-framework 移植，Apache 归属保留）。
> 状态：2026-09-26 建档。

## 一、为什么需要这条闭环

本项目此前 13 篇写作实证（全 9.8 分）沉淀出的适配值——门禁阈值 3.8、科研×博客混合形态、额外评审角色、双语隔离 + derekinside 活注脚——**全部只停留在项目本地，团队仓零沉积**（`team-memory/patterns/` 下无 `derekwang85/` 目录）。写毕沉淀闭环的作用：把每篇"踩坑-修根因-结论"在发布后自动捕获进团队仓，让姊妹项目与框架后续能回溯复用。

## 二、闭环触发点（接在发布复盘之后）

```
写稿 → 发布复盘(retro) → dw-lesson-capture.py --team → verify-write-asset.py 校验 → 原子 commit → 团队仓 patterns/derekwang85/
```

每完成 1 篇（CP 进下一题 index 前），在母版框架仓运行：

```bash
# 在 derekwritting-framework 仓根目录执行
python3 tools/team-core/dw-lesson-capture.py \
  --since=4h \
  --source=git,review,retro,learnings \
  --team="C:\Users\A\Documents\derekwritting-framework\team-memory" \
  --owner=derekwang85 \
  --auto-commit
```

- `--source`：写作仓的 git 提交、评审记录（`**/review*.md`）、发布复盘（`**/retro*.md` / `**/*复盘*.md`）、LEARNINGS 与 wiki/log。
- `--owner=derekwang85`：追加写 `team-memory/patterns/derekwang85/`。
- 写盘始终先本地（成员主权双写 M3），团队仓不可用时 fail-closed 拒绝入库、本地不丢。
- 每个通过校验的条目 = 一次原子 git commit（失败安全）。

## 三、写入的资产类型与校验

| 类型 | 目录落点 | 校验工具 | 约束 |
|------|----------|----------|------|
| pattern（经验模式） | `patterns/derekwang85/` | `verify-write-asset.py` | fail-closed，未经校验不入团队仓 |
| decision（决策/适配值） | `team-memory/decisions/derekwang85/` | `verify-write-asset.py` | 含一手 `sources:`，`visibility: team` |
| handoff（交接/复用点） | `team-memory/handoffs/dw/` | 同上 | sources 指向知识点来源 |
| learnings 汇总 | `team-memory/learnings/` | 同上 | 跨项目通用后 promote |

## 四、首条沉淀：科研形态适配值（R1-R4）

详见 `docs/LEARNINGS-REFER-BACK-derekwritting-framework.md`（反哺回执档案）。首次真正跑通 lesson-capture 时，应将 R1-R4 落成团队仓资产卡：

- R1 阈值收紧 3.5→3.8 → `decisions/derekwang85/r1-threshold-3.8.md`
- R2 额外评审角色 → `decisions/derekwang85/r2-review-extra-roles.md`
- R3 双语隔离 + 活注脚 → `patterns/derekwang85/r3-allusion-isolation-bilingual.md`
- R4 四条 methodology 建议 → 已在母版 `LEARNINGS-MultiAgentFabrication.md` 吸收（A/B 待用户裁决）

> 注意：`team-memory/patterns/derekwang85/` 目录当前不存在。首次运行 `--owner=derekwang85` 时会按其 write-asset 契约创建；若脚本要求目录预建，需先行 `mkdir` 该目录。

## 五、回源节奏（S 档建议固化）

| 节奏点 | 动作 |
|--------|------|
| 每写完 1 篇 | 跑 lesson-capture（4h 窗口），沉淀该篇 pattern/decision |
| 每个系列（series）结束 | 跑一次全量 capture + 生成 promote 申请草案 |
| 每季度 | 审计 `counters.json` total_assets 与 stale，对账本项目回流量 |

## 六、当前状态

- [x] 反哺档案已建（`docs/LEARNINGS-REFER-BACK-derekwritting-framework.md`）
- [x] 母版吸收文档已建（`derekwritting-framework/LEARNINGS-MultiAgentFabrication.md`，README 已登记）
- [x] 两个待回源脚本已回源（`writing-harness/`），config 已更新，`patrol-log.json` 已建档
- [ ] 首次 lesson-capture 落 team 资产卡（需在母版仓运行命令，人工确认）
- [ ] `verify-write-asset.py` 校验通过
- [ ] `dw-recall.py` 回溯命中

---

*接入人：derekwang85 × AI ｜ 建档日期：2026-09-26 ｜ 本文件是 CP 闭环写毕沉淀的操作契约。*