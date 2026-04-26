# Editorial Article Template

Surface: `web_dual`
Document Shape: `editorial_article`
Legacy alias: `article`

## Fixed section recipe
1. Thesis
2. Summary
3. Sections
4. Evidence breaks
5. Closing
6. Meta

## Layout notes
- single-column reading width
- `calm` reading rhythm within a `web_dual` page shell
- serif-forward hierarchy
- keep reading comfort ahead of layout novelty

## Example scaffold
```yaml
thesis:
  components: [eyebrow, title_block, summary_strip]
sections:
  components: [body_paragraph, fact_card]
evidence_breaks:
  components: [body_paragraph, quote_block, chart_frame]
closing:
  components: [summary_strip, body_paragraph]
meta:
  components: [method_note, footer_meta]
```
