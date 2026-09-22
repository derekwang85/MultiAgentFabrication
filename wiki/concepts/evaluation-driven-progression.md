# 评分超前均的进化评估 Evaluation-Driven Progression
> **一句话定义**：每篇必须严格优于前序平均（建议留约 0.2 余量），用分数板与突破维度固定进化而非凭感觉。
> 来源：[[source-writing-harness]] · [[source-evolution-skill]] · ../writing-harness/EVALUATION.md
> 相关：[[reviewer-writer-separation]] [[gate-as-verification]]
> 实证：`evaluate-scoreboard.json` 记录分数与突破，`evaluate.py --record/--update` 当场判定是否严格超前均

## 定义

系列质量要随篇目单向上升。其判据是：新篇分数必须严格大于基准（基准 = 不含本篇的前序平均），并在正文可见处落实至少一个前序未用过的突破维度（新矿引用 / 新案例 / 记忆点）。分数板 `evaluation-scoreboard.json` 是唯一真值，评分先改 JSON 再跑脚本校验，不允许门禁未过或分数未超基准就写"已完成"。

## 证据出处

- `writing-harness/EVALUATION.md`：进化评估规约，定义基准与突破维度。
- `writing-harness/evaluate.py`：`--next` 亮基准、`--record`/`--update` 判定进出。
- `docs/WRITING-FRAMEWORK.md` 第四节/第六节：参看配方七条与突破维度矿源占用。

## 相关概念

- [[reviewer-writer-separation]]：评测由独立角色驱动，分数才可信。
- [[gate-as-verification]]：门禁是发布前的验证，评分是进化的判据。

## 内化级别

- **A 强内化**（项目默认）：进化闭环是本系列核心机制，脚本硬件判定。

## 门禁评审留痕（W1-W4）

- 本概念页按 wiki 元规约 W1-W4 校订定稿；结构完整度 4.0/5（四段齐全、定义一句话、不复制源文）。