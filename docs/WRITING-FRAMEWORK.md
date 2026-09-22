# 写作框架总纲 · MultiAgent Fabrication

> 版本：v2.0 ｜ 更新：2026-09-12（同步母版 derekwritting-framework v2）｜ 初版：2026-09-06 ｜ 作者：derekwang85（腾讯云 TVP / 架构师名人堂）
> 定位：本系列**怎么把一篇多 Agent 方法论文章写出来**的唯一工作入口。引用母版 `derekwritting-framework`（Apache 2.0），按本系列"多 Agent 形成生产力 / 可自证"的定位做参数化适配。
> 优先级：constitution/README.md > 本总纲 > 各篇 spec > writing-harness 脚本。
> 真值：本文档的**机器可读适配值以 `framework.config.json` 为唯一真值**，本文档是给人读的镜像；二者冲突时以 config 为准并回写本文档。

---

## 一、母版与适配方式

本框架**不是从零设计**，而是把 [derekwritting-framework](..%2F..%2Fderekwritting-framework%2FREADME.md) 的规约体系注入本系列，再按本项目的身份差异化。母版方法论内核来自《驾驭 AI · AI Harness Engineering》系列与 TraeWork 写作经验；本项目只做**参数化覆盖**，不改母版脚本。

| 差异项 | 母版默认 | 本系列适配值 |
|--------|---------|-------------|
| 项目形态 | 通用 / 博客 | **科研型深度方法论 × 博客发布的混合形态** |
| 门禁取舍 G1-G5 | 全开，默认阈值 | 全开；**G3 事实门禁收紧**（带来源 + 年份，禁虚构数据） |
| rubric 侧重 | 通用 10 维 | Trustworthiness、Specificity、Point of View 加权 |
| rubric 均值阈值 | 3.5 / 5 | **人工尺度下保持 ≥ 3.8 / 5**（未接 LLM 时用 `--selfcheck`） |
| 评审角色 | 5 正面 + 1 反方 | 保留**反方**，另加"方法评论证审计员"与"读者代表" |
| 引用配比 | 管理 / 科技史 / 人文 | 向**系统论 / 组织管理 / 开源历史 / 哲人名言**新矿偏移（见第六节） |
| 文章配方 | 方法论 + 实证 + 清单 | 方法论 ~40% + 项目实证 ~40%（可指认文件）+ 可复制清单 ~20%，每篇附 derekcoding 活注脚 |

> 覆盖载体是**项目自身的 `framework.config.json`（机器可读）+ 本总纲（人读镜像）+ `writing-harness/evaluation-scoreboard.json`**。仅当确有差异时才落配置；**不修改注入脚本本体**。母版脚本为独立副本（`writing-harness/harness-sync.json` 指向 AIHanessMethodology 源），升级回源走 UPGRADE 纪律，见第九节。

**母版 v2 资产对齐表**（本轮随 derekwritting-framework v2 同步；母版源见 `C:\Users\A\Documents\derekwritting-framework`）：

| 母版 v2 资产 | 本地落位 | 状态 |
|-------------|---------|------|
| `framework.config.json` 配置契约（门禁/评分/评审配比） | `framework.config.json` | ✅ 已补 `review_swarm`，g5 阈值 3.5→3.8 |
| `constitution/allusion-isolation.md`（中英典故隔离表） | `constitution/allusion-isolation.md` | ✅ 已适配（见第四节） |
| `SKILL-REGISTRY.md`（技能注册表，3 次晋升） | `docs/SKILL-REGISTRY.md` | ✅ 已建（见第九节） |
| `tools/review-swarm-prompt.md`（G5 分离评审模板） | 待回源 → `writing-harness/` | ⏳ 母版已就位，用前按需拷贝 |
| `tools/scannability-check.py`（可扫读信号） | 待回源 → `writing-harness/` | ⏳ 母版已就位，G1 人工补充用 |
| `methodology/08-rubric-weights-en.md`（英文 rubric 权重） | `writing-harness/EVALUATION-EN.md` | ✅ 本地已有英文 eval 规约，权重口径在 config `judge` 注明对齐 |

> 待回源项属框架可执行/模板资产，升级走 UPGRADE 对账（`derekwritting-framework/docs/UPGRADE.md`）：脚本跟框架、配置跟项目。

---

## 二、写作约束金字塔（本系列落位）

从上到下，上层约束越清晰，下层 AI 生成越一致：

```
战略层  README.md · docs/positioning.md · docs/multi-agent-survey.md
        （边界 / 定位 / 三大差异支柱 A-D / 调研底稿 / 单一事实来源）
   ↕
架构层  constitution/README.md（本文件之上）
        （三条不写铁律 / 固定三段配方 / 行为底线 / 工程现实纪律）
   ↕
契约层  本文件 docs/WRITING-FRAMEWORK.md · SERIES-PLAN.md · 各篇 spec
        （写作配方七条骨架 / 七段工序 / 篇目清单与目标分）
   ↕
门禁层  writing-harness/（GATES.md · EVALUATION.md · writing-gates.py · evaluate.py）
        （G0-G6 门禁 + 进化评估闭环，独立计分）
   ↕
实现层  articles/<NN-*.md>（受约束的多 Agent 方法论稿件）
```

**单一事实来源约定**：一切定义、篇目标题、目标分、引用占用、突破维度占用，都以 `SERIES-PLAN.md` + `writing-harness/evaluation-scoreboard.json` 为准。改动先改这些母版，再改衍生文档，防止多篇之间表述漂移。

---

## 三、适配决策：本系列门禁怎么做

本项目是"深度方法论为里、技术博客为表"，因此**五道门禁全开，并收紧事实门禁**：

| 门禁 | 原名 | 本系列检查要点 | 执行方式 |
|------|------|---------------|---------|
| G0 | 立项 | 这篇解决"多 Agent 生产力"哪个真问题？增量是什么？ | 动笔前人工 |
| G1 | 风格 | 信号词密度 < 6/千字；风格五维 ≥ 35/50 | `writing-gates.py --gate g1` |
| G2 | 结构 | 段首给答案、每段一事、问题先于答案 | `--gate g2` |
| G3 | 事实 | 统计主张带来源+年份；项目数字可指认具体文件；**不引精确 star 数**；未核实标置信度 | `--gate g3`，**人工复审** |
| G4 | 链接 | 内链篇号 / 术语 / 数字一致；derekinside 注脚符合宪法 | `--gate g4` |
| G5 | 评审 | rubric 均值 ≥ 3.8 / 5；**评审与写作分离**；记录剩留问题 | `judge.py` 或 `--selfcheck` |
| G6 | 发布 | 涟漪检查 / 宪法合规 / 暗线合规 / 清单可操作 / 平台适配 | 非写作者人工 |

**硬规则**：顺序不可逆（G0 不过不动笔，G1 不过不进 G2）；门禁是发布前不是写作中；失败回对应阶段修订但不带病进下道；门禁通过 ≠ 完美，剩留问题必须记录。

---

## 四、写作配方（适配版，对标母版方法论 06）

好的多 Agent 方法论文章 = **一套方法论 + 一两个真实项目实证 + 一份"第一天就能用"的清单**。展开为七条骨架：

1. **开篇是场景，不是定义**——用真实踩坑（"五 Agent 一起写代码，最后收获一群需要盯的共犯"）开场，第一屏就必须有画面。
2. **问题先于答案**——先讲透"为什么线性 fallback 是陷阱 / 为什么多数投票会多数弱智"，再给解法；矛盾对比用表格。
3. **真实挫败是论据主体**——每个实证（SmartQuant / derekcoding #19 / derekinside）都能指认到真实文件、真实数字；无法回验的标注"项目一手统计 / 无法回验"。
4. **引经据典是论据，不是装饰**——每篇 2-3 处，去前序未用矿源（组织学 / 系统论 / 开源历史 / 哲人），删掉后论证变弱才算有效。
5. **诚实面对反方**——主动给"什么时候不值得上多 Agent"的边界（对齐：单模型够用就别上多模型），明确软 / 硬约束区别。
6. **收束导向行动并预告下篇**——结尾用"读者自检"收束，并埋下篇钩子。
7. **清单今天就能用**——结尾是可勾选动作，假设读者只读清单也能独立成立。

> 写配方时，作者注意力放前六条，AI 味交给发布前门禁机器判。多 Agent 特有的边界：**每个"我们做到了"的机制都必须可指认**，否则改写为"设计目标 / 规划"。

---

## 五、写作工序（适配版，对标母版方法论 07）

一次写作动作按七段推进，省返工：

1. **写前对口径**——动笔前确认：本篇用哪个项目哪个文件实证、引用配比、图片与命名规则，写进任务说明。
2. **从母版取料**——定义 / 地图 / 引用占用 / 目标分全部取自 `SERIES-PLAN.md`，不回滚到散落素材。
3. **成文立骨**——按第四节七条骨架立章；章节标题重内容轻格式，避免"框架工具逐条报菜名"。
4. **配图并进**——核心图 / 金句卡与论证逻辑对齐，走 derekimage-evolution 闭环，命名统一。
5. **门禁评分双确认**——先 `writing-gates.py` 过 G1-G6，再 `evaluate.py --record` 评判定超基准；双闸门缺一不放行。
6. **发布包三件套**——核心图 / 金句卡 + 行动清单 + 平台定制 CTA（腾讯云主阵地）。
7. **跨文件同步**——正文改动同步 `SERIES-PLAN` 状态表、`docs/article-evaluation-system.md` 评分表、README 目录，状态标记前后一致。

**两道前置判断**：判断每一篇的转化路径（引向哪个方法论落点）；面向海外读者时**重写而非翻译**（保留论点，重组织句子与例证）。

---

## 六、进化评估与突破维度（对标母版 + derekwritting-evolution）

- **逐篇评分**：10 分制，新文须**严格 > 前序均值**（当前序章 8.8，下篇目标 > 8.80，建议 9.00+）。
- **突破是硬要求**：每篇至少落实一个前序未用过的突破维度，并在正文可见处体现。
- **矿源占用现状**（本系列不可复用）：AIHarness 已占 德鲁克 / 维纳 / 麦肯锡 / 汉谟拉比 / 泰勒福特 / 戴明 / 克劳塞维茨 / 凯文·凯利 / 博尔赫斯 / 海明威 / Dijkstra / 孙子 / CMM / 康威。后可向 **开源历史（如 Linux/Git 治理）、系统论、管理组织学、哲人名言** 未开采方向求新。
- **中英典故隔离**：任何引用先过 `constitution/allusion-isolation.md` 的 R1-R4 判定（软约束，G5 评审人工核对）。中文稿禁西方冷门典故直用，英文稿禁中文成语/名句直译；双语成稿时翻译稿必须重跑一次隔离表。
- **数据源唯一真值**：`writing-harness/evaluation-scoreboard.json`；评分先改 JSON，由 `evaluate.py --check` 校验，再镜像到 `docs/article-evaluation-system.md`。

---

## 七、运行本系列的入口命令

```bash
# 动笔前亮基准（读当前分数板，给出下篇目标分）
python writing-harness/evaluate.py --next

# 完稿过门禁（一次一个文件；含空格路径加引号）
python writing-harness/writing-gates.py "articles/01-*.md"

# 评分录入（新篇 --record，重写 --update；脚本判定是否严格>前序均值）
python writing-harness/evaluate.py --record "articles/01-*.md" --score 9.0 --breakthrough "..." --note "..."

# 校验数据源合法
python writing-harness/evaluate.py --check
```

---

## 八、文档地图

| 写作环节 | 用哪个文件 | 作用 |
|----------|-----------|------|
| 开工前定边界 | `constitution/README.md` | 身份 / 铁律 / 工程原则 / derekcoding 回馈纪律 |
| 引用前查隔离 | `constitution/allusion-isolation.md` | 中英典故隔离表（R1-R4，软约束） |
| 定一篇写什么 | `templates/article-spec.md` | 单篇设计图（范围 / 实证 / 结构 / 验收） |
| 改动前宣言 | `templates/writing-manifest.md` | >3 文件或 >30 分钟任务必填 |
| 全系列编排 | `SERIES-PLAN.md` | 篇目清单 / 目标分 / 突破方向 |
| 质量管控 | `writing-harness/GATES.md` + `EVALUATION.md` | 门禁 + 进化评估（中文版） |
| 英文质量管控 | `writing-harness/EVALUATION-EN.md` + `evaluate-en.py` | 英文门禁 E1-E6 + 英文进化评估 |
| 分离评审模板 | `writing-harness/review-swarm-prompt.md`（待回源） | G5 反方 + 5 角色评审，评审与写作分离 |
| 可扫读信号 | `writing-harness/scannability-check.py`（待回源） | G1 的人工补充信号检查 |
| 检索知识资产 | `wiki/`（入口 `wiki/index.md`） | llm-wiki 可查询知识库：概念五层分类 + 一手源溯源（W1-W4 门禁，双读者） |
| 适配配置 | `framework.config.json` | 门禁阈值 / rubric / review_swarm 的机器可读真值 |
| 技能注册 | `docs/SKILL-REGISTRY.md` | 写作技能单一事实来源（3 次晋升机制） |
| 调研 & 定位 | `docs/multi-agent-survey.md` · `docs/positioning.md` | 横向对比底稿与差异支柱 |
| 评分表 | `docs/article-evaluation-system.md` | 人类可读评分表（镜像 scoreboard JSON） |
| 回馈 | `feedback-to-derekcoding/special-for-derekcoding.md` | 研究成果反向回馈 derekcoding |

---

## 九、回写与升级纪律

1. 每篇落地后回写三处：scoreboard JSON / `docs/article-evaluation-system.md` / `SERIES-PLAN.md`。
2. 本文档涉及的门禁阈值、评审配比等机器可读值，一律以 `framework.config.json` 为准；改配置后回写本文档同步。
3. 新增可复用写作流程 → 按 `docs/SKILL-REGISTRY.md` 的 3 次晋升机制登记；晋升须跨项目真实复用并留记录。
4. 门禁反复拦下的同类问题，走 `GATES.md` 的"反馈回写通道"升级对应层，而非在单篇打补丁。
5. 对 derekcoding 的发现与缺口，沉淀进 `feedback-to-derekcoding/`，标"待内化确认"，不替其拍板。
6. 母版升级时参照 `derekwritting-framework/docs/UPGRADE.md` 做增量回源：脚本跟框架、配置跟项目，可安全覆盖未改动的 `tools/*.py`，保留本系列自有的 `framework.config.json`、宪法与 skill。

---

## 评审记录（G5）

- 评审方式：rubric 自评（评审者与写作者分离）
- rubric 均值：3.9 / 5
  - 目的对齐度 4.0：显式声明母版 v2 来源 + 参数化适配，落到本系列定位
  - 结构完整度 4.0：金字塔 / 门禁 / 配方 / 工序 / 评估 / 地图 / 升级纪律七段闭环
  - 可迁移性 4.0：任何一篇都可按工序 + 配方执行，不与既有文件冲突
  - 事实溯源 3.8：母版 v2 口径来自 derekwritting-framework 最新文档与本系列宪法、config、SERIES-PLAN 实况
  - 可用性 3.8：第五节工序 + 第七节命令可直接跑
- 剩留问题：G3 收紧后的 rubric 阈值（3.8）为经验值，待多篇实测后回填校准；`review-swarm-prompt.md` 与 `scannability-check.py` 为待回源项，首次 G5 实战前需拷贝到 `writing-harness/` 并对齐 config `patrol.assets` 指向；本文件需随系列推进持续迭代，重大改动走 ADR 流程。

*本总纲由 derekwritting-framework（Apache 2.0）注入并参数化适配，与 constitution、writing-harness、SERIES-PLAN 保持一致。*