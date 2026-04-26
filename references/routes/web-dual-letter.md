# Letter Route Reference

Surface: `web_dual`
Document Shape: `letter`
Public document type: `letter`

## Fixed section recipe
1. Sender context
2. Opening statement
3. Body
4. Request or recommendation
5. Signoff

## Layout notes
- keep the route formal and compressed
- avoid charts and decorative panels
- place the action request or recommendation clearly

## Example scaffold
```yaml
sender_context:
  components: [eyebrow, title_block]
body:
  components: [body_paragraph]
request_or_recommendation:
  components: [body_paragraph]
signoff:
  components: [footer_meta]
```
