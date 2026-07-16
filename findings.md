# Findings & Decisions

## Requirements
- 制定真正以推广为目标的计划。
- 补齐现有 launch kit 的执行短板。
- 生产可直接发布的推广文案。
- 功能工作只在直接支持传播或转化时进行。

## Initial Findings
- 现有 `docs/launch-kit.md` 只有文案骨架，缺完整成稿、内容日历、ICP、渠道目标、评论回复、私信和复盘模板。
- 项目最可信的主张是“Agent 写结构，Momo Paper 负责校验和渲染”，目前没有公开 A/B 数据，因此不能把具体 token 百分比作为首发标题。
- 最成熟的展示场景是研究/投资报告：现有 equity report、research summary、图表、HTML/PDF 和打印支持可共同展示价值。
- 当前公开安装入口存在 `momo`、`momo2` 两套称呼；推广文案应优先引导到 GitHub/使用指南，不在短帖里堆安装细节。
- 实际对外发布需要用户账号，本轮在仓库内交付可复制文案、素材脚本、UTM 和台账。
- README 原 Quick Start 以不存在的 `cd v2` 开始，是首个安装转化阻塞。
- 首页原主 CTA 进入长指南、次 CTA 进入组件目录，没有把推广流量直接承接到可运行入口和英雄案例。
- 当前最稳定的首次成功路径是：克隆仓库 → venv → `pip install -e .` → `momo2 validate/render examples/equity-report.md`。
- 自包含 Skill wrapper 无需安装 package，可直接执行同一示例；应与 CLI 路径清晰分开，避免 `momo` / `momo2` 混淆。
- package 现已同时安装 `momo` 与 `momo2`；所有新文档使用 `momo`，旧别名经过干净环境验证仍可用。

## Channel Rule Findings
- Hacker News 官方规则要求标题克制、提交原始来源、不要索取点赞，也不应把 HN 主要当推广渠道。
- Show HN 必须是用户能直接试用的本人作品，最好无注册门槛；单纯文章、落地页和等待名单不适合 Show HN。
- HN 当前规则明确写明不要发布生成式或 AI 编辑文本。因此本轮只提供 HN 事实提纲，用户必须亲自重写，不能直接粘贴生成文案。
- Reddit 官方帮助页被 Cloudflare 阻断，无法核验具体条款；采用保守策略：发帖前逐个阅读 subreddit 规则、披露作者身份、避免重复跨发和硬推销。
- V2EX 帮助页可访问，页面说明包含 Spam 告示；发帖应选匹配节点、真实描述开发过程，并把反馈问题置于链接之前。

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 内容先讲痛点和成品，不先讲 DSL 语法 | 非用户不关心实现，成品与工作流更能触发试用 |
| 暂不把 benchmark 设为发布门槛 | 可先用不带具体数字的真实产品演示推广，避免因实验拖延分发 |
| 长文一稿多用，但各渠道重写开头和 CTA | 保持生产效率，同时避免机械跨平台复制 |
| 首页主 CTA 直接指向 GitHub Quick Start | 推广流量需要最短激活路径，长指南是辅助材料 |
| 首个示例统一使用 equity report | 与首发推广场景和英雄案例一致，减少认知切换 |

## Resources
- `docs/launch-kit.md`
- `docs/benchmark-protocol.md`
- `README.md`
- `site/content/index.md`
- `site/content/guide.md`
- `examples/equity-report.md`
- Hacker News Guidelines: https://news.ycombinator.com/newsguidelines.html
- Show HN Guidelines: https://news.ycombinator.com/showhn.html
- V2EX Help: https://www.v2ex.com/help
