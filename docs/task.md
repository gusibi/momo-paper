# Momo Paper 2.0 Task Plan

## Goal

Build Momo Paper 2.0 as an isolated Markdown DSL parser and HTML converter under `v2/`. The runtime should parse Agent-generated Markdown DSL, validate syntax and metadata, and generate standard standalone HTML. It should not define business components in Python.

## Assumptions

- Phase 1 supports Markdown DSL to standalone HTML.
- Phase 1 validates `document_type`; `dashboard` is invalid.
- Tags such as `hero`, `feature-grid`, `timeline`, and `cta` are Agent-facing DSL conventions, not hard-coded Python component classes.
- The parser accepts any syntactically valid `:::tag-name` block and renders it generically.
- Existing functionality remains untouched until 2.0 is complete enough to replace it.
- Implementation keeps all new runtime code, tests, examples, and docs under `v2/`.

## Phase 1 Tasks

### 1. Create isolated v2 package

- [ ] Create `v2/README.md`.
- [ ] Create `v2/pyproject.toml`.
- [ ] Create `v2/momo_dsl/__init__.py`.
- [ ] Create `v2/momo_dsl/cli.py`.
- [ ] Create `v2/momo_dsl/parser.py`.
- [ ] Create `v2/momo_dsl/renderer.py`.
- [ ] Create `v2/momo_dsl/errors.py`.
- [ ] Create `v2/examples/landing.md`.
- [ ] Create `v2/tests/test_parser.py`.
- [ ] Create `v2/tests/test_renderer.py`.
- [ ] Create `v2/tests/test_cli.py`.

### 2. Define Agent-facing DSL documentation

- [ ] Document required frontmatter fields in `v2/README.md`.
- [ ] Document supported Markdown subset in `v2/README.md`.
- [ ] Document generic block syntax: `:::tag-name ... :::`.
- [ ] Document recommended Phase 1 tags for landing generation: `hero`, `section`, `feature-grid`, `timeline`, `comparison`, `stats`, `cta`, `faq`.
- [ ] Document that tags are conventions for Agent output, not Python components.
- [ ] Document that `dashboard` is invalid as `document_type`.
- [ ] Add a complete landing example for Agent reference.

### 3. Implement parser

- [ ] Parse frontmatter delimited by `---`.
- [ ] Parse Markdown content outside block directives.
- [ ] Parse block directives in the form `:::tag-name ... :::`.
- [ ] Parse block body as a small YAML-like data subset.
- [ ] Preserve node order.
- [ ] Track source line numbers.
- [ ] Reject missing or malformed frontmatter.
- [ ] Reject invalid tag names.
- [ ] Reject unclosed block directives.
- [ ] Reject malformed block fields.

### 4. Implement validation

- [ ] Require `document_type`.
- [ ] Reject `document_type: dashboard`.
- [ ] Require `locale`.
- [ ] Require `title`.
- [ ] Validate tag names with a conservative pattern.
- [ ] Validate that block bodies parse to key/value data, lists, or strings.
- [ ] Return clear errors with file path, line number, and block name when possible.

### 5. Implement generic HTML renderer

- [ ] Render a full standalone HTML document.
- [ ] Embed minimal CSS directly in the HTML.
- [ ] Escape user-provided text by default.
- [ ] Render Markdown headings, paragraphs, lists, links, bold, italic, and inline code.
- [ ] Render each DSL block generically as a semantic `<section>`.
- [ ] Preserve the original tag name in `data-block`.
- [ ] Render scalar fields, nested objects, and lists into readable HTML.
- [ ] Ensure output works by opening the generated HTML file directly in a browser.

### 6. Implement CLI

- [ ] Add `momo2 validate <input.md>`.
- [ ] Add `momo2 render <input.md> -o <output.html>`.
- [ ] Print validation errors clearly.
- [ ] Return non-zero exit codes on parse or validation failure.
- [ ] Create output directories when needed.
- [ ] Add CLI tests for success and failure cases.

### 7. Add examples

- [ ] Add `v2/examples/landing.md`.
- [ ] Include recommended Phase 1 tags in the example.
- [ ] Render the example during verification.

### 8. Add tests

- [ ] Test valid frontmatter parsing.
- [ ] Test malformed frontmatter failure.
- [ ] Test block parsing.
- [ ] Test nested block data parsing.
- [ ] Test unclosed block failure.
- [ ] Test invalid tag name failure.
- [ ] Test `document_type: dashboard` failure.
- [ ] Test missing `locale` failure.
- [ ] Test HTML render contains expected `data-block` sections.
- [ ] Test CLI `validate`.
- [ ] Test CLI `render`.

### 9. Verify Phase 1

- [ ] Run v2 unit tests.
- [ ] Render `v2/examples/landing.md` to an HTML file.
- [ ] Inspect the generated HTML.
- [ ] Confirm no files outside `v2/` are required for runtime.
- [ ] Confirm current JSON engine remains untouched.
- [ ] Update `docs/td.md` if implementation decisions changed.

## Phase 2 Backlog

### Additional validation

- [ ] Add optional tag schema files for stricter Agent guidance.
- [ ] Add warnings for misspelled recommended tags.
- [ ] Add document-type-specific recommended tag sets.
- [ ] Add machine-readable Agent reference output.

### Additional outputs

- [ ] Add PDF export.
- [ ] Add PPT export.
- [ ] Add PNG or long-image export.
- [ ] Add structured JSON export.
- [ ] Add batch static-site output.

### Advanced capabilities

- [ ] Add theme system.
- [ ] Add user-provided render templates.
- [ ] Add multi-file include.
- [ ] Add asset copying and path rewriting.
- [ ] Add chart and diagram rendering from generic DSL data.
- [ ] Add AI repair suggestions for invalid DSL.
- [ ] Add schema documentation generation.
- [ ] Plan migration from old runtime to v2.
- [ ] Delete old runtime only after v2 covers required production routes.
