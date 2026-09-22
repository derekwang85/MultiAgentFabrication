# Harness 门禁流水线 G0-G6 Harness Gates
> **一句话定义**：每篇从立项到发布依次经过 G0-G6 七道门禁，越靠前成本越低，越靠后兜住的问题越严重。
> 来源：[[source-writing-harness]] · ../writing-harness/GATES.md
> 相关：[[gate-as-verification]] [[reviewer-writer-separation]]
> 实证：`writing-harness/writing-gates.py` 提供全套自动检查与 `--gate gN` 单道运行

## 定义

门禁流水线将质量管控拆为七个阶段，前段拦成本低的问题、后段兜风险大的问题：G0 立项（值不值得写，动笔前）→ G1 风格（信号词密度与五维自评）→ G2 结构（段首给答案、每段一事）→ G3 事实（统计主张带来源、项目数字可指认、不引精确 star 数）→ G4 链接（外链有效、内链对得上、术语统一、derekinside 对齐）→ G5 评审（10 维 rubric 均值过线）→ G6 发布（涟漪检查、宪法合规、暗线合规、清单可操作、平台适配）。纪律：顺序不可逆、门禁在发布前而非写作中、失败回原文修、通过 ≠ 完美、G5/G6 评审写作分离、反复拦截的同类问题走反馈回写通道升级对应层。

## 证据出处

- `writing-harness/GATES.md`：七道门禁逐条定义（G0-G6）与门禁纪律六条。
- `framework.config.json` `gates`：`g5_rubric_mean_threshold` 按本系列科研定位目标收紧至 3.8（注：脚本判据仍取 GATES.md 的 3.5，3.8 作为人工收紧基准待实测校准，见 docs/WRITING-FRAMEWORK.md 剩留问题）。

## 相关概念

- [[gate-as-verification]]：门禁是验证而非宣告的机制化。
- [[reviewer-writer-separation]]：G5 / G6 由独立评审执行，不由写作者自己判定。

## 内化级别

- **A 强内化**（项目默认）：门禁流水线是本系列质量控制的骨架机制。