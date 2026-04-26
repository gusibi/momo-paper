# Explainer Template

Surface: `web_dual`
Document Shape: `explainer`
Legacy alias: `web_page`

## Fixed section recipe
1. Lead
2. Summary strip
3. Themed sections
4. Evidence
5. Conclusion
6. Meta

## Layout notes
- browser-readable and print-safe
- `standard` density
- max 1 hero pattern
- alternate calm and dense sections on long pages

## Example scaffold
```yaml
lead:
  components: [eyebrow, title_block, summary_strip]
themed_sections:
  components: [title_block, body_paragraph]
evidence:
  components: [chart_frame, insight_callout]
conclusion:
  components: [fact_card, body_paragraph]
meta:
  components: [footer_meta]
```
