# llm-wiki 元规约 · AGENTS.md

**评审记录**：本文件为 wiki 元规约（协议文件），不适用 G5 内容评审；其质量由 [../docs/WRITING-FRAMEWORK.md](../docs/WRITING-FRAMEWORK.md) 评审记录统一留痕。

> 本目录（`wiki/`）是本项目（MultiAgent Fabrication）的**可查询知识库**：把本项目自身的方法论资产与所依赖的写作 skill 蒸馏成概念级条目。
> 区别于 `constitution/`（规约本体）、`docs/`（写作框架与调研），wiki 是**跨资产收敛后的概念索引**，服务 AI Agent 与人工的快速检索与交叉引用。任何 Agent 在本目录操作前，必须先读本文件与 `index.md`。

## 一、入口

- **导航**：`index.md` 是唯一入口，先读它。概念条目按"约束金字塔"五层组织：战略 / 架构 / 契约 / 门禁 / 实现。
- **建设规约 + 门禁**：W1-W4 见本文档第五节。
- **项目规约本体**：`../constitution/`。
- **写作框架总纲**：`../docs/WRITING-FRAMEWORK.md`。
- **门禁与评估脚本**：`../writing-harness/`。

## 二、目录职责

| 子目录 | 内容 | 与原文关系 |
|--------|------|-----------|
| `concepts/` | 跨资产收敛后的概念页 | 从 `../constitution/*`、`../docs/WRITING-FRAMEWORK.md`、`../writing-harness/*` 或依赖 skill 提炼，**每个概念必带来源标注** |
| `concepts/drafts/` | AI 生成的 `.draft.md` | **未定稿**，不参与导航引用 |
| `sources/` | 源索引页 | 每个一手资产一页：溯源 + 吸收/舍弃表 |
| `concepts/taxonomy.md` | 五层分类法说明 | 解释 wiki 如何把概念映射到框架层 |

## 三、链接语法

- 一律用 wikilink：`[[concept-name]]`、`[[source-name]]`。
- 链接目标必须存在于本 wiki（或回指 `../constitution/`、`../docs/`、`../writing-harness/`）。
- 需要同时指回框架原文时，用相对路径 markdown 链接。

## 四、条目规范

每条概念页必须含四段（顺序固定）：

```markdown
# <概念名> (English)
> **一句话定义**：……
> 来源：[[source-name]] · ../docs/WRITING-FRAMEWORK.md
> 相关：[[concept-a]] [[concept-b]]
> 实证：[[source-p]] 或 项目框架内实证

## 定义
## 证据出处
## 相关概念
## 内化级别     // A 强内化（项目默认/可配阈值）｜ B 弱内化（软约束/参考）
```

`taxonomy.md` 说明层级归属的判定口径：**该概念主要约束哪个写作/工程决策，就归到哪一层。**

## 五、门禁（W1-W4）

新增 / 修订条目必须过四道门禁：

- **W1 溯源门禁**：每个概念必须有来源（项目 `constitution/*`、`docs/WRITING-FRAMEWORK.md`、`writing-harness/*`，或依赖 skill / 外部 URL / 本地路径）。无出处 = 不合格；实证必须可指认。
- **W2 结构门禁**：四段齐全；定义一句话；不复制 source 或方法论文本原文。
- **W3 语言门禁**：信号词密度 < 6/千字；无"毫无疑问""毋庸置疑"等断言词。
- **W4 链接门禁**：wikilink 有效、双向可达；用 `../writing-harness/link-check.py`（如存在）或人工核对自动校验。

## 六、生成方式（失败安全）

- AI 可生成 `.draft.md` 草稿，**但定稿写入本目录必须人工确认**。

## 七、变更记录

每次新增 / 修订在 `log.md` 记一行：改了什么 / 为何 / 来源。