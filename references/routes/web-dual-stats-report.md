# Stats Report Template

Surface: `web_dual`
Document Shape: `stats_report`
Legacy alias: `stats_report`

## Fixed section recipe
1. Header and date range
2. KPI row
3. Trend grid
4. Segment panels
5. Anomaly / alert
6. Method / meta

## Layout notes
- 12-column grid
- `dense` density
- strict chart consistency
- method transparency required
- must remain printable and legible

## Example scaffold
```yaml
header_date_range:
  components: [title_block, summary_strip]
kpi_row:
  pattern: kpi_row
  components: [kpi_card]
trend_grid:
  components: [chart_frame, insight_callout]
segment_panels:
  components: [chart_frame, table_block]
anomaly_alert:
  components: [insight_callout, table_block]
method_meta:
  components: [method_note, footer_meta]
```
