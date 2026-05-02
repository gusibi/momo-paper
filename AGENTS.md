# AGENTS.md

Repository instructions for coding agents working on **Momo Paper**.

## What this repo is

Momo Paper is a routed design system for documents and visual narratives. It is not a generic UI kit and it is not a dashboard framework.

The repository is split into two operating layers:
- `SKILL.md`: runtime usage rules for agents generating content
- `AGENTS.md`: maintenance rules for agents extending the repository

## Source of truth

Canonical system files:

- [README.md](./README.md): public usage entrypoint
- [DESIGN.md](./DESIGN.md): taxonomy, foundations, deck recipe, non-negotiables
- [prompt-contracts.md](./prompt-contracts.md): route workflow, input contract, and operating rules
- [VOICE.md](./VOICE.md): copy tone
- [design-tokens.json](./design-tokens.json): machine-readable tokens
- [artifact-presets.json](./artifact-presets.json): route registry, document type overlay, and diagram maps
- [style-checklist.md](./style-checklist.md): final QA gate
- [references/document-types.md](./references/document-types.md): public document type routing table
- [references/diagrams.md](./references/diagrams.md): diagram selection and anti-patterns
- [references/routes/](./references/routes/): internal route references

Reference assets that should stay aligned with the system:

- [assets/templates/](./assets/templates/): public CN/EN starter templates
- [assets/diagrams/](./assets/diagrams/): SVG diagram primitives
- [assets/showcase/](./assets/showcase/): branded showcase pages

If two files disagree, fix the disagreement. Do not leave the system half-migrated.

## Core model

Public overlay:
- `document_type`: `one_pager | long_doc | letter | portfolio | resume | slides | equity_report | changelog | process_flow | timeline | faq_page | case_study | research_summary | stats_report | infographic`
- `locale`: `zh-CN | en`
- `diagram_type`: optional explicit override

Internal route model:
- `surface`: `web_dual | slides | visual_sheet`
- `document_shape`: `explainer | editorial_article | letter | portfolio | process_flow | timeline | resume_profile | faq_page | case_study | research_summary | stats_report | equity_report | changelog | infographic`

Legacy aliases remain for compatibility only:
- `web_page` -> `web_dual.explainer`
- `ppt_slide` -> `slides.explainer`
- `infographic` -> `visual_sheet.infographic`
- `article` -> `web_dual.editorial_article`
- `stats_report` -> `web_dual.stats_report`

Do not reintroduce `preset_id` as a parallel public model.

## Hard constraints

- `dashboard` is out of scope for the current system.
- `comparison_matrix` and `topic_cover` are pattern candidates, not document types.
- `web_dual` must stay browser-readable and print-safe.
- Unsupported route combinations must fail fast. Do not guess a nearest route.
- Visual changes must stay within `design-tokens.json` and the Momo Paper direction.
- Diagrams are primitives inside documents, not standalone document types.

## When editing this repo

### If you change the route registry

Always update these together:

1. [artifact-presets.json](./artifact-presets.json)
2. [prompt-contracts.md](./prompt-contracts.md)
3. [DESIGN.md](./DESIGN.md)
4. [style-checklist.md](./style-checklist.md)
5. [references/document-types.md](./references/document-types.md)
6. The relevant route reference in [references/routes/](./references/routes/)
7. The matching template path in [assets/templates/](./assets/templates/)
8. Any affected showcase copy in [assets/showcase/](./assets/showcase/)

### If you add a new public document type

A document type is only valid when all of these exist:

- `documentTypeMap` entry in `artifact-presets.json`
- `localeTemplateMap` entry in `artifact-presets.json`
- internal route exists and is fully specified
- route reference exists in `references/routes/` if the route is new
- CN + EN starter templates exist in `assets/templates/`
- `references/document-types.md` is updated
- `README.md`, `SKILL.md`, and `prompt-contracts.md` are updated

Do not add a document type name without all of the above.

### If you add a new diagram primitive

Always update these together:

1. `diagramTypeMap` in [artifact-presets.json](./artifact-presets.json)
2. [references/diagrams.md](./references/diagrams.md)
3. the matching SVG wrapper in [assets/diagrams/](./assets/diagrams/)
4. README / SKILL / prompt contract if public behavior changed

### If you change tokens or style rules

Update:
- [design-tokens.json](./design-tokens.json)
- [DESIGN.md](./DESIGN.md)
- any affected template, diagram, or showcase copy

Do not change HTML/CSS examples in a way that silently violates tokens while leaving the written rules untouched.

## Editing style

- Keep changes surgical. This repo is mostly system definition, so wording drift matters.
- Prefer adding or tightening constraints over adding vague inspirational language.
- Keep machine-readable files and prose docs aligned.
- Preserve the current visual direction; Momo Paper borrowed Kami's method, not Kami's skin.

## Validation

Before finishing a change, run lightweight checks when applicable:

```bash
node -e "JSON.parse(require('fs').readFileSync('artifact-presets.json','utf8')); JSON.parse(require('fs').readFileSync('design-tokens.json','utf8')); console.log('json ok')"
```

Use `rg` to catch stale naming or taxonomy:

```bash
rg -n "web_page|ppt_slide|artifact_type|preset_id|dashboard|comparison_matrix|topic_cover" .
```

If you changed branding, also grep for stale previous-brand strings in showcase hero copy and footers before finishing.

## Preferred workflow

1. Decide whether the change affects public usage, internal routing, diagrams, or branding.
2. Update machine-readable contracts first.
3. Sync README / SKILL / DESIGN / prompt-contracts.
4. Add or revise route references, templates, and diagram assets.
5. Update showcase copy only after the registry is stable.
6. Run lightweight validation.

## What not to do

- Do not treat this repo as a freeform design playground.
- Do not add dashboard language back into templates or examples.
- Do not invent new route combinations outside the registry.
- Do not leave legacy aliases documented as if they were the preferred interface.
