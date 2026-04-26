# Changelog Route Reference

Surface: `web_dual`
Document Shape: `changelog`
Public document type: `changelog`

## Fixed section recipe
1. Release header
2. Highlights
3. Grouped changes
4. Migration notes
5. Metadata

## Layout notes
- make breaking changes obvious
- group entries by user impact or subsystem
- avoid vague marketing bullets

## Example scaffold
```yaml
release_header:
  components: [eyebrow, title_block, summary_strip]
grouped_changes:
  components: [fact_card, body_paragraph]
migration_notes:
  components: [body_paragraph, fact_card]
metadata:
  components: [footer_meta]
```
