# Landing Template

Surface: `landing`
Document Shape: `landing`
Legacy alias: None (special marketing page type)

## Notes
- Uses the root Momo Paper design token contract through a landing-specific adapter in `landing.html.j2`.
- Default rendering is light and paper-based; a root-token-derived dark mode toggle is supported.
- One-page marketing structure, not a document surface.
- Rendered via JSON engine only (no direct-edit HTML template in `assets/templates/`).

## Fixed section recipe
1. Hero (headline, description, CTA buttons, optional pipeline)
2. Features (heading, feature cards with icons)
3. Workflows (optional: heading, workflow cards with tags and highlights)
4. Document Types (optional: heading, type grid with icons and descriptions)
5. Comparison (optional: old vs new comparison cards)
6. Numbers (optional: metric strip with values and labels)
7. Ecosystem (optional: tools grid with names and descriptions)
8. Bottom CTA (heading, description, button)

## Layout notes
- Responsive grid layouts for features, workflows, doc types, ecosystem
- Theme toggle button fixed at top-right
- Hero section preserves the current centered landing-page composition
- Card hover effects with border color transitions
- Mobile-responsive breakpoints at 1024px, 860px, 768px, 500px

## Example scaffold
```yaml
hero:
  badge: "Momo Paper / Routed Design System"
  headline: "A routed design system for documents and visual narratives."
  description: "用一套路由规则统一 one-pager、长文、简历、幻灯片、研报、信息图与文档内图示。"
  cta_buttons:
    - label: "Get Started"
      url: "/guide/"
      style: "btn-primary"
    - label: "View Demo"
      url: "/demo/"
      style: "btn-secondary"
  pipeline:
    - label: "document_type"
      desc: "选择文档类型"
    - label: "locale"
      desc: "选择语言"
    - label: "render"
      desc: "渲染输出"

features:
  label: "Why Momo Paper"
  heading: "One system, many documents."
  description: "从 15 种文档类型到 5 种可编程图表，一套设计令牌驱动所有输出。"
  cards:
    - icon: "R"
      icon_class: "charts"
      title: "设计令牌驱动"
      description: "所有 30 个模板共享同一套色彩、字体、间距系统，输出一致。"
    - icon: "D"
      icon_class: "diagrams"
      title: "图示原语"
      description: "14 种 SVG 图示原语可嵌入文档，教学优先，不装饰。"
    - icon: "P"
      icon_class: "print"
      title: "打印安全"
      description: "web_dual 表面保证浏览器可读和打印安全，结论率先。"

bottom_cta:
  heading: "Ready to start?"
  description: "Pick a document type and let Momo Paper handle the rest."
  button_label: "Get Started"
  button_url: "/guide/"
```

## Allowed components
- hero_block
- feature_card
- workflow_card
- doc_type_card
- comparison_card
- number_strip
- ecosystem_card
- cta_block

## Allowed patterns
- hero
- features_grid
- workflow_showcase
- doc_type_grid
- comparison
- numbers
- ecosystem
- bottom_cta

## Forbidden uses
- Do not use document-style prose sections.
- Do not add chart frames or diagram primitives.
- Do not treat this as a document surface.
