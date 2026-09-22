# wiki 变更日志 · log.md

**评审记录**：本文件为变更日志（记录性文件），非成稿文章，适用 W 门禁而不适用 G5 内容评审；质量留痕见 [../docs/WRITING-FRAMEWORK.md](../docs/WRITING-FRAMEWORK.md) 评审记录。

> 每次新增 / 修订记一行：改了什么 / 为何 / 来源。对齐 wiki 元规约 `AGENTS.md` §七。

## 维护说明

- 按时间顺序追加，一条记一行；同一次批处理合并成一个小节。
- 每条必含：改动对象 / 原因 / 依据来源（本地路径）。
- 涉及删除或降级条目需标注理由，不允许默默移除。

## 2026-09-12 · 初始建库（同步母版 derekwritting-framework v2 补齐 llm-wiki）

- 新增 `AGENTS.md`、`GUIDE.md`、`index.md`、`concepts/taxonomy.md`：确立 wiki 元规约（wikilink + W1-W4 门禁 + 失败安全生成）、双读者使用指南、检索入口与五层分类口径。
- 新增 `sources/` 5 个一手源页：source-constitution、source-writing-framework、source-writing-harness、source-skill-registry、source-evolution-skill；各含一手溯源 + 吸收/舍弃表。
- 新增 `concepts/` 12 条概念页（不含 taxonomy）：knowledge-as-asset、reviewer-writer-separation、evaluation-driven-progression、retrieval-over-content、writing-recipe-seven、progressive-disclosure、gate-as-verification、harness-gates-g1-g6、allusion-isolation、experience-retention、skill-registry-promotion、derekinside-note。
- 依据：母版 `C:\Users\A\Documents\derekwritting-framework\wiki\` 于前两轮适配后新增 llm-wiki 体系；本轮按"本项目自身的知识资产 + 依赖 skill"做了参数化建库，而非照搬母版对七个外部参考源的收敛（那些不属于本项目方法论）。
- 一致性契约：`framework.config.json` `patrol.assets` 应登记 wiki 资产；README 使用纪律补登记 llm-wiki 维护条款。