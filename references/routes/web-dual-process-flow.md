# Process Flow Template

Surface: `web_dual`
Document Shape: `process_flow`

## Fixed section recipe
1. Lead
2. Core flow
3. Branch / variation
4. Operational takeaway
5. Meta

## Layout notes
- browser-readable and print-safe
- mainline flow should stay within 4-6 steps
- branch content should be visually separated from the main route
- motion may reveal steps but cannot be required to understand them

## Example scaffold
```yaml
lead:
  components: [eyebrow, title_block, summary_strip]
core_flow:
  components: [step_rail, fact_card]
branch_variation:
  components: [fact_card, insight_callout]
operational_takeaway:
  components: [body_paragraph, insight_callout]
meta:
  components: [method_note, footer_meta]
```
