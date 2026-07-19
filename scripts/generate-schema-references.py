#!/usr/bin/env python3
"""Generate compact Skill template references from machine schemas."""

from __future__ import annotations

import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "momo_dsl" / "schemas"
OUTPUT_DIR = ROOT / "momo-paper-skill" / "references" / "templates"


def _load_schemas() -> list[dict]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(SCHEMA_DIR.glob("*.json"))
    ]


def _type_text(rule: dict) -> str:
    if "$ref" in rule:
        return rule["$ref"]
    value = rule.get("type", "any")
    return " | ".join(value) if isinstance(value, list) else str(value)


def _resolve_rule(rule: dict, definitions: dict) -> dict:
    if "$ref" not in rule:
        return rule
    resolved = dict(definitions[rule["$ref"]])
    resolved.update({key: value for key, value in rule.items() if key != "$ref"})
    return resolved


def _describe_fields(rule: dict, definitions: dict, prefix: str = "", depth: int = 0) -> list[str]:
    rule = _resolve_rule(rule, definitions)
    required = set(rule.get("required", []))
    lines: list[str] = []
    for name, raw_child in rule.get("properties", {}).items():
        child = _resolve_rule(raw_child, definitions)
        marker = "required" if name in required else "optional"
        field_name = f"{prefix}.{name}" if prefix else name
        lines.append(f"{'  ' * depth}- `{field_name}` — {_type_text(raw_child)}, {marker}")
        if child.get("type") == "object" or "properties" in child:
            lines.extend(_describe_fields(child, definitions, field_name, depth + 1))
        if child.get("type") == "array" and isinstance(child.get("items"), dict):
            item = _resolve_rule(child["items"], definitions)
            if item.get("type") == "object" or "properties" in item:
                lines.extend(_describe_fields(item, definitions, f"{field_name}[]", depth + 1))
    return lines


def _field_lines(schema: dict, block_schema: dict) -> list[str]:
    lines = _describe_fields(block_schema, schema.get("definitions", {}))
    return lines or ["- No formal fields are defined."]


def _render_schema(schema: dict) -> str:
    composition = schema.get("composition", {})
    required_blocks = composition.get("required_blocks", [])
    allowed_blocks = composition.get("allowed_blocks", [])
    frontmatter_required = schema.get("frontmatter", {}).get("required", [])
    document_types = schema.get("document_types", [])
    lines = [
        "<!-- Generated from momo_dsl/schemas. Do not edit by hand. -->",
        "",
        f"# {schema.get('title', schema['name'])}",
        "",
        schema.get("description", ""),
        "",
        "## Selection",
        "",
        f"- Schema: `{schema['name']}`",
        f"- Accepted `document_type`: {', '.join(f'`{item}`' for item in document_types)}",
        f"- Required frontmatter: {', '.join(f'`{item}`' for item in frontmatter_required)}",
        "",
        "## Document Contract",
        "",
        f"- Required blocks: {', '.join(f'`{item}`' for item in required_blocks) or '(none)'}",
        f"- Allowed blocks: {', '.join(f'`{item}`' for item in allowed_blocks)}",
    ]
    ordering = composition.get("ordering", [])
    if ordering:
        lines.extend(["- Ordering rules:"] + [f"  - `{before}` before `{after}`" for before, after in ordering])

    lines.extend(["", "## Block Fields", ""])
    for block_name, block_schema in schema.get("blocks", {}).items():
        lines.extend([f"### `{block_name}`", ""])
        lines.extend(_field_lines(schema, block_schema))
        lines.append("")

    if "sources" in schema.get("blocks", {}):
        lines.extend(
            [
                "## Citations",
                "",
                "Declare sources in `:::sources` with a unique `id`. Fields that allow `citations` must list those IDs. `momo validate --json` reports duplicate IDs and unresolved references.",
                "",
            ]
        )

    lines.extend(
        [
            "## Workflow",
            "",
            "```bash",
            f'"$SKILL_DIR/momo" validate input.md --schema {schema["name"]} --json',
            f'"$SKILL_DIR/momo" render input.md --schema {schema["name"]} -o output.html',
            "```",
            "",
            "If validation reports errors, repair the DSL and validate again before rendering the final document.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    schemas = _load_schemas()
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    index = [
        "<!-- Generated from momo_dsl/schemas. Do not edit by hand. -->",
        "",
        "# Formal Template Schemas",
        "",
        "Read only the reference for the selected template, then run validate before render.",
        "",
    ]
    for schema in schemas:
        path = OUTPUT_DIR / f"{schema['name']}.md"
        path.write_text(_render_schema(schema), encoding="utf-8")
        index.append(
            f"- [{schema.get('title', schema['name'])}](./{schema['name']}.md) — {schema.get('description', '')}"
        )
    (OUTPUT_DIR / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"generated {len(schemas)} template references in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
