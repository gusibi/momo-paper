# Task Plan: Momo Paper 推广执行包

## Goal
先完成直接影响推广转化的产品改造：统一试用入口，修复 Quick Start，建立首页 CTA 与英雄案例承接，并验证陌生用户可运行第一份文档。

## Current Phase
Phase 5

## Phases

### Phase 1: 审查推广短板
- [x] 明确 ICP、核心场景、主张和 CTA
- [x] 检查渠道规则、现有素材和转化路径
- [x] 建立短板优先级
- **Status:** complete

### Phase 2: 制定执行计划
- [x] 设计 30 天节奏、渠道分工和指标
- [x] 明确每天/每周交付物和停止条件
- [x] 区分仓库准备与外部账号操作
- **Status:** complete

### Phase 3: 生产推广资产
- [x] 完成长文、社区帖、短帖、图片轮播和私信文案
- [x] 准备中英文版本、CTA 与 UTM 规则
- [x] 创建案例模板和发布台账
- **Status:** complete

### Phase 4: 验证与交付
- [x] 核对所有产品声明与仓库能力一致
- [x] 检查文档链接、格式和可直接使用性
- [x] 输出执行优先级与人工发布清单
- **Status:** complete

### Phase 5: 转化路径改造
- [x] 修复 README 中不存在的 `cd v2` 路径
- [x] 统一 CLI 安装与自包含 Skill wrapper 两条试用路径
- [x] 安装命令统一为 `momo`，保留 `momo2` 兼容别名
- [x] 首页主 CTA 指向 GitHub Quick Start，次 CTA 指向研报成品
- [x] 首页与指南增加可复制的 equity report Quick Start
- [x] 导航增加长期可见的 GitHub 试用入口
- [x] 补齐站点 favicon，消除首屏资源 404
- [x] 用干净环境验证 CLI 与 Skill wrapper
- [x] 验证站点构建、测试与桌面端首屏
- **Status:** complete

## Success Criteria
- 有一个明确 ICP、一个主场景、一个首发主张、一个统一 CTA。
- 至少覆盖 6 个渠道，但首周只执行 2 个主渠道。
- 至少交付 1 篇长文、4 篇社区帖、6 条短帖、1 套轮播脚本、3 组私信模板。
- 所有数字和能力声明可核验，不使用尚未完成的 benchmark 结果。
- 外部发布后能按曝光→点击→安装/克隆→首份渲染进行人工归因。

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 推广优先，功能仅解除转化阻塞 | 用户已明确功能服务于推广 |
| 首发主场景定为 Agent 生成正式研究/投资报告 | 现有示例最完整，最能展示结构、图表和打印价值 |
| 首周聚焦 GitHub + 一个中文技术社区 | 同时铺满渠道会稀释反馈，先验证主张与安装路径 |
| 公开命令统一为 `momo` | 品牌与命令一致，降低推广文案和用户记忆成本；保留 `momo2` 避免破坏兼容性 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| Web search backend network error | 1 | 改用已知官方规则页直接访问；若仍失败则以保守发布规范处理并注明发布前复核 |
| Web direct-open backend network error | 2 | 使用 curl 获取官方页面；Reddit 无法读取则采用保守策略 |
| Browser DOM snapshot capability error | 1 | 改用只读 evaluate + screenshot 验证首屏 |
| Browser mobile viewport check timeout | 2 | 恢复默认 viewport；以构建产物和现有响应式 CSS 做静态核验，不声称移动端自动验收通过 |
| 浏览器请求 `/favicon.ico` 返回 404 | 1 | 增加符合设计令牌的 `favicon.svg` 并在构建页面显式声明 |
