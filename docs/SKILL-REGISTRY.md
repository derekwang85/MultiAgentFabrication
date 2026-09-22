# SKILL-REGISTRY · 技能注册表（写作）

> 来源：适配自 derekwritting-framework `SKILL-REGISTRY.md`（Apache 2.0）的注册表机制：**3 次晋升阈值 + 注册表**。
> 用途：本系列《MultiAgent Fabrication》全部写作/发布技能的**单一事实来源**；新增、晋升、退役必须在此登记。
> 对账：注册表（本文档） ↔ skills 安装位置（TraeWork skills 目录） ↔ `framework.config.json` `patrol.assets`，三者必须可互相解释。

## 晋升规则（3 次阈值）

| 等级 | 条件 | 位置 |
|------|------|------|
| 🟡 实验 | 首次提出，未经验证 | 待验证 / 首次真实使用前 |
| 🟢 可用 | 完成 1 次真实使用验证 | 本系列实际写作中使用过 |
| 🟣 晋升 | 完成 **3 次真实复用** 且跨项目 | 标注"晋升" + 跨项目复用记录 |

晋升检查项（每项都过才算 3 次复用）：
- [ ] 三次真实使用（不同项目/场景），每次有交付物
- [ ] 每次使用记录了问题与改进
- [ ] SKILL.md 无项目特定残留，可跨项目引用

## 已登记技能（本系列写作闭环）

| 技能 | 职责 | 状态 | 登记说明 |
|------|------|------|---------|
| derekwritting-evolution | 中文《AI Harness》系列写作进化守卫（评分超前均 + 突破 + 门禁） | 🟢 可用 | 本系列中文主场复用的核心写作守卫；晋升记录待 3 次跨项目复用后补登 |
| derekwritting-evolution-en | 英文 essay 写作进化守卫（英文门禁 E1-E6 + 英文专属突破） | 🟡 实验 | 首次使用前待本项目英文 essay 实测后转 🟢 |
| derekppt-craft | PPT 叙事与文案打磨（kicker 规约 + 分-总公式收口） | 🟢 可用 | 发布配套的演讲/分享转化载体 |
| derekimage-evolution | 配图进化闭环（评分超前均 + 门禁/评估双确认） | 🟢 可用 | 每篇核心图/金句卡走本闭环，命名统一 |
| deredkflavor | 去 AI 味：保真改写 + 检测 + 注入人味 | 🟢 可用 | 发布前 G1 门禁通过后的人工补充提质层 |
| derekwritting-media-bot | 巡检机器人：聚合新评论/私信/提及，草拟回复 | 🟡 实验 | 发布后互动监控；待真实数据接入后转 🟢 |
| derekwritting-media-matrix | 按媒体矩阵自动发布系列文章并管理互动 | 🟡 实验 | 多平台分发；待接入真实发布流程后转 🟢 |
| 浏览器控制（plugin: browser） | AI 驱动内置浏览器自动化 | 🟢 可用 | 调研/配图素材/平台操作的浏览器能力，非写作流程技能，登记备查 |
| visual-image-generator / Seedream / Seedance（plugin） | 视觉生成（配图/封面/视频） | 🟢 可用 | 配图资源的生产入口；受 derekimage-evolution 调度 |

## 维护纪律

1. **新增技能** → 按晋升规则标注 🟡，登记一行
2. **技能晋升** → 更新状态 + 晋升记录；同步 `docs/WRITING-FRAMEWORK.md`
3. **技能退役** → 登记退役原因；不得默默删除
4. **一致性** → 注册表 ↔ skills 安装目录 ↔ `framework.config.json` `patrol.assets`，三者必须可互相解释

## 一致性核对

- [ ] 注册表：本系列写作闭环技能全部登记
- [ ] `framework.config.json` `patrol.assets`：`skill_registry` 指向本文件
- [ ] 当前生效的写作流程：derekwritting-evolution（正文）→ deredkflavor（去 AI 味）→ derekimage-evolution（配图）→ G1-G5 门禁 → 发布 → media-bot/matrix（后发布）