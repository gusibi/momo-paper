# Resume Profile Template

Surface: `web_dual`
Document Shape: `resume_profile`

## Fixed section recipe
1. Profile hero
2. Expertise
3. Experience
4. Selected impact
5. Meta

## Layout notes
- identity and current role must appear immediately
- maintain document dignity rather than landing-page theatrics
- support browser reading and PDF export
- use cards only to support structured profile content

## Example scaffold
```yaml
profile_hero:
  components: [eyebrow, title_block, summary_strip]
expertise:
  components: [body_paragraph, fact_card]
experience:
  components: [body_paragraph, fact_card]
selected_impact:
  components: [fact_card, insight_callout]
meta:
  components: [footer_meta]
```
