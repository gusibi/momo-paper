---
document_type: faq_page
locale: zh-CN
title: 常见问题示例
description: FAQ 类型支持分组问答、引导语和总结说明。适合产品帮助中心、事件回应、政策说明。
---

FAQ 类型将问答内容按组分类，每组有独立标题。每个问答以卡片形式呈现——问题加粗突出，回答以次级文字显示。适合产品帮助中心、活动常见问题、政策解读等场景。

## 关于此类型

:::faq
items:
  - question: faq_page 类型适合哪些场景？
    answer: 适合需要结构化呈现「问答」内容的场景，如产品帮助中心、活动常见问题、政策解读、社区指南等。分组机制让你可以按主题组织问题，方便用户快速定位。
  - question: FAQ 卡片支持什么内容？
    answer: 每个 FAQ 卡片包含一个问题（question）和一个回答（answer），都是纯文本字段。卡片自动以 surface 色为背景，和页面整体设计令牌保持一致。
:::

## 使用方式

:::faq
items:
  - question: 如何创建 FAQ 页面？
    answer: 在 frontmatter 声明 document_type 为 faq_page，正文用 :::faq 块组织问答，items 是一个列表，每个元素有 question 和 answer 字段，块以 ::: 结束。
  - question: 可以有多少个分组？
    answer: 分组数量没有限制。每个分组用一个 :::faq 块表示，块前用 Markdown 标题作为分组名。每个分组内的条目数量也没有限制。
:::

:::footer-note
title: 开始使用
body: 这是 faq_page 类型的演示示例。实际使用时，你可以根据需要创建任意数量的分组和问答条目。
:::
