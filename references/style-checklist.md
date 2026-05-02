# Style Checklist

Run this checklist before any artifact is finalized.

## 1. Route integrity
- The request resolves to one legal `document_type` or one legal `surface + document_shape` route in `../assets/artifact-presets.json`.
- If a legacy `artifact_type` is present, it matches the resolved route.
- `comparison_matrix` and `topic_cover` are treated as pattern candidates, not document types.
- Only whitelisted components, patterns, chart types, and diagram primitives are used.
- Density mode matches the selected route.

## 2. Template and locale integrity
- The correct CN or EN starter template was selected.
- The final output language matches the chosen locale.
- Public document type copy and internal route copy do not contradict each other.

## 3. Visual consistency
- All colors come from `../assets/design-tokens.json`.
- No extra gradient, glow, neon, or novelty texture appears.
- Typography uses only approved font families.
- Spacing follows token scale only.
- Borders, radius, and shadows stay within token rules.

## 4. Information hierarchy
- The main conclusion is visible in the first screen, first slide, or first section.
- Titles are factual and short.
- Each section has one main purpose.
- Long artifacts alternate dense and calm rhythm where applicable.
- For `web_dual`, the first printed page still reveals the main conclusion and section structure.
- Motion is optional and never required to understand the page.

## 5. Diagrams and charts
- A diagram is only present if it teaches better than a paragraph.
- Structured numerical data uses an appropriate chart type or a conscious no-chart choice is evident.
- Every chart has a clear title.
- Every chart has one explicit takeaway.
- Number formats are internally consistent.
- Gridlines and legends are visually secondary.
- Method/source note exists when the claim depends on data credibility.

## 6. Voice quality
- Copy is clear, restrained, and specific.
- No hype, slogan, or generic AI filler language appears.
- Evidence is stated or uncertainty is admitted.
- Final takeaway is operational, not theatrical.

## 7. Fail conditions
Revise before shipping if any of these are true:
- The route was guessed because no legal match existed.
- The wrong locale template was used.
- A section introduces a new visual language not defined in the system.
- A chart uses decorative color rather than informative color.
- The layout becomes crowded because spacing rules were ignored.
- The copy sounds more like marketing than analysis.
- A `web_dual` page only works on screen and loses its structure when printed.
