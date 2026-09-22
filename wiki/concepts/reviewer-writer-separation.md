# 评审写作分离 Reviewer-Writer Separation
> **一句话定义**：评审者必须与写作者分离，生成者与批判者不同角色，防止自洽偏差导致"自我打分即自我宣告成功"。
> 来源：[[source-writing-harness]] · [[source-evolution-skill]] · ../writing-harness/GATES.md
> 相关：[[gate-as-verification]] [[evaluation-driven-progression]]
> 实证：G5 门禁要求评审与写作分离；`framework.config.json` 的 review_swarm 配比加入反方与独立角色

## 定义

质量判定若由生产方自己执行，会因视角一致而产生自洽偏差——写作者倾向认可自己的判断。因此评审（judge）与写作分离是硬前提：至少一个角色专门批判，评审独立于作者进行。分离是手段，目标是让"证据"可信：只有通过独立检查才算证据。

## 证据出处

- `writing-harness/GATES.md`：G5 硬性要求评审独立，评审记录须含 G5 期望词。
- `writing-harness/judge.py`：独立计分脚本。
- `framework.config.json` `review_swarm`：5 正面 + 反方 + 方法评论证审计员 + 读者代表的配比。

## 相关概念

- [[gate-as-verification]]：评审分离让门禁的"证据"成立。
- [[evaluation-driven-progression]]：评审分数驱动"严格超前均"的进化。

## 内化级别

- **A 强内化**（项目默认）：G5 评审与写作分离是不可妥协的流程前提。