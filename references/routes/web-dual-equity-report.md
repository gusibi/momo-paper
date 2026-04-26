# Equity Report Route Reference

Surface: `web_dual`
Document Shape: `equity_report`
Public document type: `equity_report`

## Fixed section recipe
1. Thesis
2. Business snapshot
3. Price history or drivers
4. Valuation
5. Risks and catalysts
6. Recommendation and disclosure

## Layout notes
- state the investment thesis early
- use candlestick or line only when price history matters
- never omit risk and disclosure context

## Example scaffold
```yaml
thesis:
  components: [eyebrow, title_block, summary_strip]
business_snapshot:
  components: [fact_card, body_paragraph]
valuation:
  components: [chart_frame, insight_callout, table_block]
recommendation_and_disclosure:
  components: [method_note, footer_meta]
```
