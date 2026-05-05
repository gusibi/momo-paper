# Momo Paper Document Types

This file is the authoritative public routing table for Momo Paper.

Use it when the user speaks in document names rather than internal routes.

## Selection rule

1. Match the user's wording to a public `document_type`.
2. Resolve the internal route from `../assets/artifact-presets.json`.
3. Pick the correct CN or EN starter template.
4. If the wording is ambiguous, ask a one-liner rather than guess.

## Document type table

| User says | Document Type | Internal Route | CN template | EN template |
| --- | --- | --- | --- | --- |
| `one-pager / 方案 / 执行摘要 / exec summary` | `one_pager` | `web_dual.explainer` | `assets/templates/one-pager.html` | `assets/templates/one-pager-en.html` |
| `white paper / 白皮书 / 长文 / 年度总结 / technical report` | `long_doc` | `web_dual.editorial_article` | `assets/templates/long-doc.html` | `assets/templates/long-doc-en.html` |
| `formal letter / 信件 / 辞职信 / 推荐信 / memo` | `letter` | `web_dual.letter` | `assets/templates/letter.html` | `assets/templates/letter-en.html` |
| `portfolio / 作品集 / case studies` | `portfolio` | `web_dual.portfolio` | `assets/templates/portfolio.html` | `assets/templates/portfolio-en.html` |
| `resume / CV / 简历` | `resume` | `web_dual.resume_profile` | `assets/templates/resume.html` | `assets/templates/resume-en.html` |
| `slides / PPT / deck / 演示` | `slides` | `slides.explainer` | `assets/templates/slides.py` | `assets/templates/slides-en.py` |
| `个股研报 / equity report / 估值分析 / investment memo / 股票分析` | `equity_report` | `web_dual.equity_report` | `assets/templates/equity-report.html` | `assets/templates/equity-report-en.html` |
| `更新日志 / changelog / release notes / 版本记录` | `changelog` | `web_dual.changelog` | `assets/templates/changelog.html` | `assets/templates/changelog-en.html` |
| `流程图说明 / workflow page / SOP` | `process_flow` | `web_dual.process_flow` | `assets/templates/process-flow.html` | `assets/templates/process-flow-en.html` |
| `timeline / 时间线 / roadmap / milestone page` | `timeline` | `web_dual.timeline` | `assets/templates/timeline.html` | `assets/templates/timeline-en.html` |
| `faq / 常见问题 / help center page` | `faq_page` | `web_dual.faq_page` | `assets/templates/faq-page.html` | `assets/templates/faq-page-en.html` |
| `case study / 案例拆解 / 项目复盘` | `case_study` | `web_dual.case_study` | `assets/templates/case-study.html` | `assets/templates/case-study-en.html` |
| `research summary / 研究摘要 / brief report` | `research_summary` | `web_dual.research_summary` | `assets/templates/research-summary.html` | `assets/templates/research-summary-en.html` |
| `stats report / 数据报告 / KPI report` | `stats_report` | `web_dual.stats_report` | `assets/templates/stats-report.html` | `assets/templates/stats-report-en.html` |
| `infographic / 信息图 / visual summary` | `infographic` | `visual_sheet.infographic` | `assets/templates/infographic.html` | `assets/templates/infographic-en.html` |
| `landing page / 首页 / 产品页` | `landing` | `landing.landing` | `scripts/json-engine/momo_paper/templates/landing.html.j2` | `scripts/json-engine/momo_paper/templates/landing.html.j2` |

## Notes

- `one_pager` is the public entry for `web_dual.explainer`.
- `long_doc` is the public entry for `web_dual.editorial_article`.
- `resume` stays public-facing even though the internal route remains `resume_profile`.
- `process_flow`, `timeline`, `faq_page`, `case_study`, `research_summary`, `stats_report`, and `infographic` are already routable and stay visible as public document types.
- Long deck (>20 slides): also read Deck Recipe in `references/DESIGN.md` section 8.
- `dashboard` remains out of scope.
- `comparison_matrix` and `topic_cover` remain pattern candidates, not public document types.
