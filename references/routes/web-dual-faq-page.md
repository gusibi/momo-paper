# FAQ Page Template

Surface: `web_dual`
Document Shape: `faq_page`

## Fixed section recipe
1. Lead
2. Grouped FAQs
3. Decision summary
4. Next step

## Layout notes
- questions should cluster by theme rather than one long list
- answers must remain concise and operational
- preserve heading structure for print/PDF
- avoid mixing showcase content into the Q&A path

## Example scaffold
```yaml
lead:
  components: [eyebrow, title_block, summary_strip]
grouped_faqs:
  pattern: faq
  components: [body_paragraph, fact_card]
decision_summary:
  components: [insight_callout, body_paragraph]
next_step:
  components: [footer_meta]
```
