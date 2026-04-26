# Momo Paper Example Site Execution Plan

Status: planned only. Do not implement from this document automatically.

## Goal

Build a static example site for **Momo Paper** that explains:

- what the system does
- how the routing model works
- what document types are supported
- what diagram primitives are supported
- how the design style and document-first thinking fit together

The site should also demonstrate all current public templates in the repository.

## Audience

Primary audience:
- developers
- agent users
- system maintainers

Secondary audience:
- people evaluating Momo Paper as a document design system

## Site strategy

Use a **main site + document-type subpages** structure.

The content theme should be **Momo Paper itself** rather than an unrelated fictional brand.

Language mode:
- Chinese main site
- English mirror pages for each document type

The site remains static:
- no framework
- no build step
- relative paths only

## Information architecture

### Main entry

File:
- `assets/showcase/index.html`

Purpose:
- explain Momo Paper as a routed design system
- link to every public document type page
- explain templates, route logic, diagrams, and auto-chart rules

Main sections:
1. Hero
2. What Momo Paper solves
3. Routing model: `document_type -> route -> template`
4. Design principles and visual style
5. Template matrix
6. Diagram system and auto-chart logic
7. How to use the system
8. Full gallery of document-type pages

### Document-type example pages

Directories:
- `assets/showcase/zh/`
- `assets/showcase/en/`

Each public `document_type` gets:
- one Chinese page
- one English mirror page

Each page must show:
- public `document_type`
- internal route
- template file path
- when to use
- locale switch link

### Diagram library page

File:
- `assets/showcase/diagrams.html`

Purpose:
- show all diagram primitives
- explain when to use each one
- show template path
- show one anti-pattern reminder per diagram

## Page inventory

### Chinese pages

- `assets/showcase/zh/one-pager.html`
- `assets/showcase/zh/long-doc.html`
- `assets/showcase/zh/letter.html`
- `assets/showcase/zh/portfolio.html`
- `assets/showcase/zh/resume.html`
- `assets/showcase/zh/slides.html`
- `assets/showcase/zh/equity-report.html`
- `assets/showcase/zh/changelog.html`
- `assets/showcase/zh/process-flow.html`
- `assets/showcase/zh/timeline.html`
- `assets/showcase/zh/faq-page.html`
- `assets/showcase/zh/case-study.html`
- `assets/showcase/zh/research-summary.html`
- `assets/showcase/zh/stats-report.html`
- `assets/showcase/zh/infographic.html`

### English mirror pages

- `assets/showcase/en/one-pager.html`
- `assets/showcase/en/long-doc.html`
- `assets/showcase/en/letter.html`
- `assets/showcase/en/portfolio.html`
- `assets/showcase/en/resume.html`
- `assets/showcase/en/slides.html`
- `assets/showcase/en/equity-report.html`
- `assets/showcase/en/changelog.html`
- `assets/showcase/en/process-flow.html`
- `assets/showcase/en/timeline.html`
- `assets/showcase/en/faq-page.html`
- `assets/showcase/en/case-study.html`
- `assets/showcase/en/research-summary.html`
- `assets/showcase/en/stats-report.html`
- `assets/showcase/en/infographic.html`

## Content mapping by document type

Use Momo Paper itself as the subject of every page, but give each page a different storytelling job.

- `one_pager`
  - executive overview of Momo Paper
  - should feel like a concise decision memo

- `long_doc`
  - full explanation of design philosophy, routing model, and system method
  - should include at least one diagram and longer narrative sections

- `letter`
  - a memo-style note to builders explaining why Momo Paper exists
  - should stay formal and compressed

- `portfolio`
  - showcase multiple modules of the system as curated “works”
  - should emphasize selection, composition, and system range

- `resume`
  - portray Momo Paper as a “system profile”
  - should adapt the resume structure to a system identity page

- `slides`
  - a browser-readable preview of a deck structure
  - should explain slide rhythm and link to `assets/templates/slides.py` and `assets/templates/slides-en.py`

- `equity_report`
  - use a clearly labeled hypothetical adoption / valuation framing
  - must explain that the data is demo data, not real market analysis

- `changelog`
  - show Momo Paper’s version history and capability milestones
  - breaking changes should be explicit

- `process_flow`
  - explain how routing, template selection, and checklist review work

- `timeline`
  - explain the system’s evolution and roadmap

- `faq_page`
  - answer when to use which document type, why dashboard is excluded, and how chart/diagram selection works

- `case_study`
  - tell the story of one Momo Paper rollout from problem to outcome

- `research_summary`
  - summarize the design judgments behind Momo Paper

- `stats_report`
  - present demo adoption and coverage metrics

- `infographic`
  - condense the core system into a single high-density visual narrative

## Shared demo data

Use one consistent demo dataset across data-driven pages.

All demo data must be explicitly labeled as illustrative.

Recommended shared metrics:
- public document types: `15`
- route count: `15`
- locale templates: `30`
- diagram primitives: `14`
- style drift reduction: `68%`
- review time reduction: `42%`
- print-safe pass rate: `93%`
- routing accuracy proxy: `96%`

Recommended time series sample:
- Q1 adoption: `14`
- Q2 adoption: `29`
- Q3 adoption: `47`
- Q4 adoption: `71`

Recommended distribution sample:
- one-pager usage: `24%`
- long-doc usage: `18%`
- slides usage: `16%`
- research-summary usage: `14%`
- remaining routes: `28%`

## Diagram coverage

The site must show the diagram system in two ways:

1. dedicated library page
2. embedded figures in actual document pages

Minimum embedded coverage:
- `long_doc`: `architecture` + `flowchart`
- `portfolio`: `quadrant` + `venn`
- `slides`: `timeline` + `layer_stack`
- `equity_report`: `candlestick` + `waterfall`
- `research_summary`: `line_chart` + `donut_chart`

Diagram rule:
- diagrams are primitives inside pages
- never present them as standalone document types
- only draw when they teach better than prose

## Reuse of current showcase assets

Keep the current `assets/showcase/showcase.css` visual language.

Existing pages should be migrated or redirected:
- current explainer showcase -> `zh/one-pager.html`
- current process flow showcase -> `zh/process-flow.html`
- current timeline showcase -> `zh/timeline.html`
- current resume showcase -> `zh/resume.html`
- current infographic showcase -> `zh/infographic.html`

Old gallery behavior:
- `assets/showcase/showcase-gallery.html` should redirect to or clearly point to the new main entry

Compatibility behavior for old page paths:
- keep them as redirects if preserving old links matters

## Navigation rules

Main site navigation must allow:
- index -> every Chinese page
- Chinese page -> English mirror
- English page -> Chinese mirror
- all pages -> index
- all pages -> diagram library

Slides page must also link to:
- `assets/templates/slides.py`
- `assets/templates/slides-en.py`

README should link to the main site entry.

## Visual and editorial rules

Reuse current Momo Paper visual language:
- quiet editorial hierarchy
- warm paper surface
- restrained card system
- document-first rhythm

Do not redesign the brand.

The example site should explain:
- function
- design system structure
- design style
- routing logic
- why the system exists

## Suggested implementation approach

Preferred implementation pattern:
- keep `index.html` and `diagrams.html` handcrafted
- use one shared rendering structure for `zh/en` document-type pages
- allow shared CSS and optional shared JS if it reduces duplication without introducing a build step

Constraints:
- no framework
- no bundler
- no server requirement
- static relative file paths only

## Acceptance checklist

### Coverage

- all 15 public document types have `zh` and `en` pages
- all pages expose `document_type`, route, template path, and locale switch
- `slides` has a real preview page and links to both template files

### Brand consistency

- site hero uses `Momo Paper`
- site hero uses `A routed design system for documents and visual narratives.`
- no old brand strings remain in the site

### Content quality

- main site introduces features, design scheme, style, and thinking clearly
- each document page has a different narrative purpose
- demo data stays internally consistent

### Diagram coverage

- `diagrams.html` lists all 14 diagram primitives
- at least 5 different diagram types are embedded into actual pages
- auto-chart rules are visible in the site

### Static integrity

- all links work through relative paths
- no build step is required
- main site acts as the single clear entry

## Current non-goals

- do not introduce a new framework
- do not build a dashboard route
- do not redesign Momo Paper’s core visual language
- do not turn the example site into a generic marketing homepage
