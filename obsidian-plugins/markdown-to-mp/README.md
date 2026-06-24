# Markdown to 公众号

把 Obsidian 当前打开的笔记一键转换成**微信公众号排版**，复制即可直接粘贴到公众号编辑器。支持把本地图片自动上传到 **Cloudflare R2 / S3** 图床。

## 功能

- **右侧实时预览面板**：点左侧 Ribbon 的剪贴板图标（或命令「打开公众号预览面板」），右侧边栏会出现预览面板。顶部下拉可**切换模板，预览实时更新**；切换笔记或编辑内容时预览自动刷新。看满意了点面板里的「复制」即可。
- **一键复制公众号格式**：预览面板里的「复制」按钮，或命令面板「复制为公众号格式」（用当前模板，不开面板）。复制后直接在公众号编辑器 `Ctrl/Cmd+V`，样式完整保留（全内联样式，不依赖外部 CSS）。
- **本地图片自动上传**：公众号无法粘贴本地图片。检测到本地图片时（可选）弹窗询问是否上传到图床，上传后自动把图片替换成公开链接。仅支持 **R2** 和 **S3**（两者都是 S3 兼容协议）。
- **两套设计风格**：
  - **Momo Paper（暖米书卷）**：源自仓库根目录 `DESIGN.md`。暖米底色、衬线标题、导航蓝 + 赤陶点缀，适合长文 / 观点文。
  - **Vercel Geist（极简）**：源自 `vercel.DESIGN.md`。黑白灰 + 蓝色点缀，干净克制，适合技术 / 产品文。

## 代码高亮的选择（已替你定好）

你说不好判断哪种高亮更搭，所以我为每套设计各配了一种**同源**的高亮，配色直接取自对应设计系统的色板，而不是套用通用主题：

- **Momo Paper → 「Warm Paper」暖纸浅色**：代码块用暖米底 `#F4EFE6` + 米色描边，关键字=导航蓝 `#244C7A`、字符串=墨绿 `#2F6B4F`、数字=赤陶 `#B65C3A`、注释=低饱和米灰。低对比、和正文同色系，读起来像同一张纸上的内容，不会跳脱。
- **Vercel Geist → 「Geist Minimal」极简浅色**：近白底 `#fafafa` + `#eaeaea` 细描边，token 以灰阶为主，仅用紫 / 绿 / 蓝做少量点缀（取自 Geist 调色板），保持极简观感。

> 为什么不用 Dracula / Monokai 这类深色主题？它们是高饱和深色，和你这两套都偏浅、偏克制的设计冲突，粘到公众号里会显得很重。浅色同源方案更统一。

## 安装

```bash
cd obsidian-plugins/markdown-to-mp
npm install
npm run build   # 生成 main.js
```

把 `manifest.json`、`main.js`、`styles.css` 复制到你的库目录
`<vault>/.obsidian/plugins/markdown-to-mp/` 下，然后在 Obsidian 设置 → 第三方插件中启用。

开发模式：`npm run dev`（监听重建）。

## 图床配置（设置面板）

| 字段 | R2 | S3 |
| --- | --- | --- |
| 服务商 | Cloudflare R2 | Amazon S3 / 兼容 |
| Account ID | Cloudflare 账号 ID | — |
| Endpoint | 留空（用 Account ID 自动拼接） | 可选，如 `https://s3.us-east-1.amazonaws.com` |
| Region | `auto` | 桶所在区域，如 `us-east-1` |
| Bucket | 存储桶名 | 存储桶名 |
| Access Key / Secret | R2 API Token 的 S3 凭证 | IAM 凭证 |
| 公开访问前缀 URL | 公开域名或 `https://pub-xxx.r2.dev/` | 如 `https://<bucket>.s3.<region>.amazonaws.com/` |
| key 前缀 | 可选，如 `wechat/` | 同左 |

> R2 需要为存储桶**开启公开访问**（绑定自定义域名或 r2.dev），否则上传后的链接公众号无法读取。
> 上传请求通过 Obsidian 的 `requestUrl` 发送（绕过浏览器 CORS），并用 AWS Signature V4 自行签名。

## 工作原理

1. 读取当前笔记 Markdown。
2. 扫描本地图片引用（`![[..]]` 与 `![](..)`），按配置可选上传到图床并在 Markdown 中替换为公开链接。
3. 复用 Obsidian 自带的 Markdown / Prism 渲染，再把所有 class 转成**内联样式**（公众号会丢弃 `<style>`、class 和自定义字体）。
4. 写入剪贴板（`text/html` + `text/plain`），粘贴即所见即所得。
