# ADR-0001 · 多 Agent 生产力系列的独立立项与命名

> 状态：已接受 ｜ 日期：2026-09-05 ｜ 作者：derekwang85

## 上下文

用户发起本系列，源出 derekcoding #19 与 SmartQuant 多 Agent 经验，要求：
1. 项目内单独一套文件夹管理；
2. 继承并发挥 AIHarness 现有写作优势；
3. 对照 GitHub 高分多 Agent 项目做方法论对比与升华；
4. 调研成果回馈 derekcoding-framework；
5. 系列完成后并入"软件工程"体系；
6. 软件工程重构系列单独立项、不同于 AIHarness 目录。

澄清确认：用户要**两个独立顶级英文项目**（多 Agent 系列 + 重构软件工程系列），并行于 AIHarnessMethodology，均集成写作技巧与规约体系，通过软链接/嵌套互连，多 Agent 成果以文档回馈 derekcoding。

## 决策

1. 新建立顶级项目 `MultiAgentFabrication`（多 Agent 生产力编织）。
2. 命名理由：`fabrication` 兼含"生产制造"与"构建装配"双重语义，与"形成生产力"精准咬合；不同于"orchestration/coordination"这类已被占用的词，能凸显"制造出可交付的生产力"这一特色主张。
3. 复用 AIHarness 的写作技巧与规约体系（templates + writing-harness），**副本落地 + 各自独立 scoreboard**，形成独立进化闭环，避免跨系列分数混算。
4. derekcoding 回馈落于 `feedback-to-derekcoding/special-for-derekcoding.md`，带明确落点与"待内化"标注。
5. 姊妹项目 `RefactoringSoftwareEngineering` 同时立项，见其 own ADR。

## 后果

- 正面：系列独立自主，assessment 闭环纯净；feature 定位清晰（"形成生产力"）。
- 代价：笔记/教训需要在两项目间同步，需维护 SERIES-PLAN 交叉引用。
- 风险管理：writing-harness 副本若 AIHarness 升级脚本，需手动同步；通过 `harness-sync.json` 记录来源与同步日期。