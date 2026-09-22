# 门禁=验证而非宣告 Gate as Verification
> **一句话定义**：只有通过可执行的检查 / 测试才算有效证据；Agent 或人不能"无证据宣告成功"，confidence ≠ correctness。
> 来源：[[source-writing-harness]] · [[source-evolution-skill]] · ../writing-harness/GATES.md
> 相关：[[harness-gates-g1-g6]] [[reviewer-writer-separation]]
> 实证：`writing-harness/writing-gates.py` 对 G1-G6 自动检查，退出码区分通过 / 未过 / 用法错误

## 定义

质量判断的唯一合法输入是可回验的证据：代码要过测试、文字要过门禁、数字要带来源、评分要先改 JSON 再跑脚本校验。宣告"完成了"不等于完成，必须由环境印证。门禁在发布前而非写作中执行；生产方与验证方合一则宣告不可信，需分离或自动执行。对应变量：通过 = 0，未过 = 1，用法错误 = 2。

## 证据出处

- `writing-harness/GATES.md`：G1-G6 门禁的定义与硬性规则。
- `writing-harness/writing-gates.py`：自动检查实现。
- `docs/WRITING-FRAMEWORK.md` 第三节：门禁取舍"全开 + 收紧 G3 事实门禁"。

## 相关概念

- [[reviewer-writer-separation]]：验证方与生产方分离，证据才可信。
- [[harness-gates-g1-g6]]：门禁流水线的具体构成。

## 内化级别

- **A 强内化**（项目默认）：门禁是发布前置的自动化验证，是系列质量控制的地基。

## 门禁评审留痕（W1-W4）

- 本概念页按 wiki 元规约 W1-W4 校订定稿；结构完整度 4.0/5（四段齐全、定义一句话、不复制源文）。