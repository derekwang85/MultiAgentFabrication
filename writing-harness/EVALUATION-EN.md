# 英文进化评估规约（EVALUATION-EN.md）

本规约是《驾驭 AI · AI Harness Engineering》系列**英文版（essay）**写作流程中，与
`writing-harness/GATES.md`、中文版 `writing-harness/EVALUATION.md` 并行的第三条纪律。
它是中文版进化评估体系的英文专属版：门禁从 G1-G5 换成 E1-E6，进化方向从"中文可读/圈层/
故事性"换成"英文 native / 可证语料 / 英文预读者共鸣"。

一句话：**英文门禁保证"这篇英文没坏"，英文进化评估保证"整个英文系列在变好"。**

## 一、门禁与进化评估的分工

| 维度 | 门禁（GATES.md / E1-E6） | 进化评估（本规约） |
|------|--------------------------|--------------------|
| 对象 | 单篇英文是否达标 | 整条英文系列是否在变好 |
| 判据 | 固定检查项（slop/翻译腔/首屏/证据/本地化/评审） | 无固定指标，只对照"前序均值"和"五个突破维度" |
| 自动化 | `writing-gates-en.py`（脚本可执行） | `evaluate-en.py`（脚本可执行） |
| 态度 | 守下限：不像 native 就拦住 | 拉上限：不破前均就不算进步 |

## 二、core rules（与中文版一致，仅对象换成英文 essay）

1. **逐篇评分**：每篇英文正文（含序章，不支持附录/修订记录）完成后评一个综合分，10 分制，可带一位小数。
2. **前序为基准**：新 essay 的合格线 = 前序全部已评分英文 essay 分数的算术平均，要求**严格大于**。
3. **每次重写重新计**：无论首稿还是升级重写，一旦落稿评分，就把新分数写回 `evaluation-scoreboard-en.json`，并重算滚动平均，作为下一篇基准。
4. **突破是硬要求**：每篇至少落实一个突破维度标注（见第四节），并在正文可见处体现；无突破标注不通过。
5. **评分在门禁之后**：先过 `writing-gates-en.py` 的 E1-E6，再评综合分；门禁不过不进评分。

## 三、数据契约

所有英文分数与元信息落在单一数据源：

```
writing-harness/evaluation-scoreboard-en.json
```

字段约定与 `evaluation-scoreboard.json` 一致：`key` 唯一、`file` 指向 `articles/*.en.md`、
`score` 当前分、`score_history`（重写轨迹）、`breakthrough` 突破描述、`note` 评分理由。
英文版额外约定：`breakthrough` 与 `note` 用**英文**书写，`file` 一律以 `.en.md` 结尾。

## 四、突破维度（英文专属，五个方向）

与中文版"遣词造句/经典案例/名言引用"不同，英文版更贴英文读者的接收习惯：

| 突破维度 | 要求 |
|---------|------|
| **native-voice** | 读起来像 native 工程师写的，而非翻译文档——语序、语气、句长节奏符合英语习惯 |
| **reproducible-evidence** | 数字/文件/命令指向可复核的位置（[ORIGINAL DATA]、README、commit），不靠"据说" |
| **english-allusions** | 引用/案例是英文读者本就知道的出处，或已充分本地化（禁中文典故直译） |
| **scannability** | 句首大写功能小标题、首屏亮牌，读者 30 秒内能抓主线 |
| **memorable-phrasing** | 有一句读者愿意引用的英文金句（符合英文韵律，而非中文对仗硬翻） |

首次基线（2026-08-30）：英文序章 `00-prologue.en` 立项，`native-voice` 突破
（1968 开篇改写成主动态的第一人称怀疑式叙述；把中文"可控的速度"金句翻成
"Fast isn't fast if you can't control it"）。基线分刻意定在中文版 8.7 之下 0.1
（8.6），留出余量，直到独立母语评审通过后视情况微调。

## 五、操作时序

1. **动手前**：`cd writing-harness && python evaluate-en.py --next`，读当前英文基准，定本片目标（须 > 基准，建议留 0.2 余量）与计划突破维度。
2. **写作**：按英文 native 标准写，突破维度落在正文可见处。
3. **过门禁**：`python writing-gates-en.py articles/<文件>.en.md`，确认 E1-E6 全 PASS。
4. **评审**：正文尾部补"Review record"块，包含 native / reviewed by / rubric / remaining issues 等 E6 期望词。
5. **录入**：`python evaluate-en.py --record articles/<文件>.en.md --score <分> --breakthrough "<突破>" --note "<理由>"` 或 `--update` 更新既有篇目。
6. **同步**：把新分数回写到 `docs/article-evaluation-system-en.md` 人类可读评分表，保持两处一致。

## 六、当前目标

英文分数板（2026-08-30 快照）：1 篇在册，平均 **8.6**，下一篇目标须 **> 8.6**。
在独立母语评审通过前，后续 essay 评分仍需参照本规约并保留评审留痕。