# 一手源 · 门禁与进化评估（writing-harness/）
> 项目路径：`c:\Users\A\Documents\MultiAgentFabrication\writing-harness\`。
> 作用：把"每篇必须比前序更好"的进化方法论固化为可执行闭环；中英双语文档与脚本。

## 一手素材清单

| 文件 | 定位 |
|------|------|
| `writing-harness/GATES.md` | 门禁规约：G1 风格 / G2 结构 / G3 事实 / G4 链接 / G5 评审 / G6 发布 |
| `writing-harness/EVALUATION.md` | 进化评估规约（中文）：基准 = 不含本篇的前序平均，突破维度必填 |
| `writing-harness/EVALUATION-EN.md` | 进化评估规约（英文）：英文门禁 E1-E6 + 英文专属突破维度 |
| `writing-harness/evaluate.py` / `evaluate-en.py` | 分数板录入脚本：`--record`（新篇）/ `--update`（升级），判定严格超前均 |
| `writing-harness/writing-gates.py` / `writing-gates-en.py` | 门禁脚本：一次一个文件，G1-G6 检查 |
| `writing-harness/evaluation-scoreboard.json` | 分数板（机器真值） |
| `writing-harness/harness-sync.json` | 与 AIHanessMethodology 源同步状态记录 |

## 提炼吸收表

| 吸收的经验 | 落位 | 内化级别 |
|-----------|------|---------|
| 门禁=验证而非宣告 | `[[gate-as-verification]]` | A 强 |
| G1-G6 门禁流水线 | `[[harness-gates-g1-g6]]` | A 强 |
| 评分超前均 + 突破维度 + 门禁评估双确认 | `[[evaluation-driven-progression]]` | A 强 |
| 失败安全：门禁不过不可硬写盘、不向计划表写"已完成" | `[[gate-as-verification]]` | A 强 |

## 舍弃表

| 未吸收 | 原因（一致性判定） |
|--------|------|
| 中英脚本的具体实现差异细节 | 属工程实现，不进概念层，见脚本注释 |

## 来源归属

- 副本源自《驾驭 AI · AI Harness Engineering》写作门禁，由 AIHanessMethodology 注入并维护；独立计分。