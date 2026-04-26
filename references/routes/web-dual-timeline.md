# Timeline Template

Surface: `web_dual`
Document Shape: `timeline`

## Fixed section recipe
1. Lead
2. Milestone spine
3. Phase detail
4. Implication
5. Meta

## Layout notes
- chronology must be obvious without animation
- keep each milestone compact and scannable
- use calm spacing between major phases
- preserve milestone order in print/PDF

## Example scaffold
```yaml
lead:
  components: [eyebrow, title_block, summary_strip]
milestone_spine:
  components: [fact_card, body_paragraph]
phase_detail:
  components: [fact_card, insight_callout]
implication:
  components: [body_paragraph, insight_callout]
meta:
  components: [method_note, footer_meta]
```
