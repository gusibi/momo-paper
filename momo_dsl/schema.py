"""Machine-readable template schemas and semantic validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .errors import ValidationIssue, ValidationReport
from .parser import BlockNode, Document

SCHEMA_DIR = Path(__file__).parent / "schemas"


@dataclass(frozen=True)
class SchemaSummary:
    name: str
    title: str
    description: str
    document_types: tuple[str, ...]


def _schema_files() -> list[Path]:
    return sorted(SCHEMA_DIR.glob("*.json"))


def _load_schemas() -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for path in _schema_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        name = data.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(f"schema has no valid name: {path}")
        if name in schemas:
            raise ValueError(f"duplicate schema name: {name}")
        schemas[name] = data
    return schemas


def list_schemas() -> list[SchemaSummary]:
    return [
        SchemaSummary(
            name=schema["name"],
            title=schema.get("title", schema["name"]),
            description=schema.get("description", ""),
            document_types=tuple(schema.get("document_types", [])),
        )
        for schema in _load_schemas().values()
    ]


def describe_schema(name: str) -> dict[str, Any]:
    schemas = _load_schemas()
    if name not in schemas:
        raise KeyError(name)
    return schemas[name]


def infer_schema(document: Document) -> tuple[str | None, tuple[str, ...]]:
    schemas = _load_schemas()
    document_type = document.meta.get("document_type")
    type_matches = [
        name
        for name, schema in schemas.items()
        if document_type in schema.get("document_types", [])
    ]
    if isinstance(document_type, str) and document_type and not type_matches:
        return None, ()
    candidates = type_matches or list(schemas)
    block_names = {
        node.name for node in document.nodes if isinstance(node, BlockNode)
    }
    if len(type_matches) == 1 and document_type != type_matches[0]:
        allowed = set(schemas[type_matches[0]].get("composition", {}).get("allowed_blocks", []))
        if not block_names.issubset(allowed):
            return None, ()
    distinctive_matches = [
        name
        for name in candidates
        if block_names.intersection(schemas[name].get("distinctive_blocks", []))
    ]
    if distinctive_matches:
        candidates = distinctive_matches
    elif not type_matches:
        candidates = []
    candidates = sorted(candidates)
    return (candidates[0] if len(candidates) == 1 else None, tuple(candidates))


def validate_document(
    document: Document, schema_name: str | None = None
) -> ValidationReport:
    schemas = _load_schemas()
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    if schema_name is not None:
        if schema_name not in schemas:
            _validate_universal(document, errors)
            errors.append(
                _issue(
                    document,
                    code="unknown_schema",
                    message=f"unknown schema: {schema_name}",
                    field="document_type",
                )
            )
            return ValidationReport(
                mode="strict",
                schema=schema_name,
                candidates=(),
                errors=tuple(errors),
                warnings=tuple(warnings),
            )
        selected = schema_name
        candidates = (schema_name,)
    else:
        selected, candidates = infer_schema(document)
        if selected is None:
            _validate_universal(document, errors)
            code = "schema_ambiguous" if candidates else "schema_not_inferred"
            message = (
                f"document matches multiple schemas: {', '.join(candidates)}"
                if candidates
                else "no formal schema was inferred; validating in free mode"
            )
            warnings.append(
                _issue(
                    document,
                    code=code,
                    message=message,
                    severity="warning",
                    field="document_type",
                )
            )
            return ValidationReport(
                mode="free",
                schema=None,
                candidates=candidates,
                errors=tuple(errors),
                warnings=tuple(warnings),
            )

    _validate_schema(document, schemas[selected], errors)
    return ValidationReport(
        mode="strict",
        schema=selected,
        candidates=candidates,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )


def _validate_universal(document: Document, errors: list[ValidationIssue]) -> None:
    for field in ("document_type", "locale", "title"):
        value = document.meta.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(
                _issue(
                    document,
                    code="missing_frontmatter_field",
                    message=f"frontmatter missing required field: {field}",
                    field=field,
                )
            )
    if document.meta.get("document_type") == "dashboard":
        errors.append(
            _issue(
                document,
                code="invalid_document_type",
                message="dashboard is not a valid document_type",
                field="document_type",
            )
        )


def _validate_schema(
    document: Document, schema: dict[str, Any], errors: list[ValidationIssue]
) -> None:
    definitions = schema.get("definitions", {})
    _validate_value(
        document.meta,
        schema.get("frontmatter", {}),
        document,
        errors,
        definitions,
        block=None,
        field_path="",
        line_map=document.meta_lines,
    )

    composition = schema.get("composition", {})
    allowed_blocks = set(composition.get("allowed_blocks", []))
    block_nodes = [node for node in document.nodes if isinstance(node, BlockNode)]
    by_name: dict[str, list[BlockNode]] = {}
    for node in block_nodes:
        by_name.setdefault(node.name, []).append(node)
        if node.name not in allowed_blocks:
            errors.append(
                _issue(
                    document,
                    code="unknown_block",
                    message=f"block '{node.name}' is not allowed by schema '{schema['name']}'",
                    line=node.line,
                    block=node.name,
                )
            )
            continue
        block_schema = schema.get("blocks", {}).get(node.name, {})
        _validate_value(
            node.props,
            block_schema,
            document,
            errors,
            definitions,
            block=node,
            field_path="",
            line_map=node.prop_lines,
        )

    for name in composition.get("required_blocks", []):
        if name not in by_name:
            errors.append(
                _issue(
                    document,
                    code="missing_block",
                    message=f"required block is missing: {name}",
                    block=name,
                )
            )

    for name, block_schema in schema.get("blocks", {}).items():
        count = len(by_name.get(name, []))
        minimum = block_schema.get("min_occurs", 0)
        maximum = block_schema.get("max_occurs")
        if count < minimum and name not in composition.get("required_blocks", []):
            errors.append(
                _issue(
                    document,
                    code="missing_block",
                    message=f"block '{name}' must appear at least {minimum} time(s)",
                    block=name,
                )
            )
        if maximum is not None and count > maximum:
            for node in by_name[name][maximum:]:
                errors.append(
                    _issue(
                        document,
                        code="too_many_blocks",
                        message=f"block '{name}' may appear at most {maximum} time(s)",
                        line=node.line,
                        block=name,
                    )
                )

    positions: dict[str, int] = {}
    for index, node in enumerate(block_nodes):
        positions.setdefault(node.name, index)
    for before, after in composition.get("ordering", []):
        if before in positions and after in positions and positions[before] > positions[after]:
            node = by_name[after][0]
            errors.append(
                _issue(
                    document,
                    code="block_order",
                    message=f"block '{before}' must appear before '{after}'",
                    line=node.line,
                    block=after,
                )
            )

    _validate_citations(document, block_nodes, errors)


def _resolve_rule(rule: dict[str, Any], definitions: dict[str, Any]) -> dict[str, Any]:
    if "$ref" not in rule:
        return rule
    name = rule["$ref"]
    if name not in definitions:
        raise ValueError(f"unknown schema definition: {name}")
    resolved = dict(definitions[name])
    resolved.update({key: value for key, value in rule.items() if key != "$ref"})
    return resolved


def _validate_value(
    value: Any,
    raw_rule: dict[str, Any],
    document: Document,
    errors: list[ValidationIssue],
    definitions: dict[str, Any],
    block: BlockNode | None,
    field_path: str,
    line_map: dict[str, int],
) -> None:
    rule = _resolve_rule(raw_rule, definitions)
    expected = rule.get("type")
    if expected is not None and not _matches_type(value, expected):
        errors.append(
            _field_issue(
                document,
                block,
                line_map,
                field_path,
                code="invalid_type",
                message=f"field '{field_path or '<root>'}' must be {_type_label(expected)}",
            )
        )
        return

    if isinstance(value, dict):
        required = rule.get("required", [])
        properties = rule.get("properties", {})
        for name in required:
            if name not in value:
                path = _join_path(field_path, name)
                errors.append(
                    _field_issue(
                        document,
                        block,
                        line_map,
                        path,
                        code="missing_field",
                        message=f"required field is missing: {path}",
                    )
                )
        if rule.get("additional_properties", True) is False:
            for name in value:
                if name not in properties:
                    path = _join_path(field_path, name)
                    errors.append(
                        _field_issue(
                            document,
                            block,
                            line_map,
                            path,
                            code="unknown_field",
                            message=f"field '{path}' is not allowed",
                        )
                    )
        for name, child in value.items():
            if name in properties:
                _validate_value(
                    child,
                    properties[name],
                    document,
                    errors,
                    definitions,
                    block,
                    _join_path(field_path, name),
                    line_map,
                )

    if isinstance(value, list):
        minimum = rule.get("min_items")
        if minimum is not None and len(value) < minimum:
            errors.append(
                _field_issue(
                    document,
                    block,
                    line_map,
                    field_path,
                    code="too_few_items",
                    message=f"field '{field_path}' must contain at least {minimum} item(s)",
                )
            )
        item_rule = rule.get("items")
        if item_rule:
            for index, child in enumerate(value):
                _validate_value(
                    child,
                    item_rule,
                    document,
                    errors,
                    definitions,
                    block,
                    f"{field_path}[{index}]",
                    line_map,
                )

    if isinstance(value, str):
        minimum = rule.get("min_length")
        if minimum is not None and len(value.strip()) < minimum:
            errors.append(
                _field_issue(
                    document,
                    block,
                    line_map,
                    field_path,
                    code="empty_value",
                    message=f"field '{field_path}' must not be empty",
                )
            )

    if "enum" in rule and value not in rule["enum"]:
        allowed = ", ".join(str(item) for item in rule["enum"])
        errors.append(
            _field_issue(
                document,
                block,
                line_map,
                field_path,
                code="invalid_value",
                message=f"field '{field_path}' must be one of: {allowed}",
            )
        )

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in rule and value < rule["minimum"]:
            errors.append(
                _field_issue(
                    document,
                    block,
                    line_map,
                    field_path,
                    code="value_too_small",
                    message=f"field '{field_path}' must be at least {rule['minimum']}",
                )
            )
        if "maximum" in rule and value > rule["maximum"]:
            errors.append(
                _field_issue(
                    document,
                    block,
                    line_map,
                    field_path,
                    code="value_too_large",
                    message=f"field '{field_path}' must be at most {rule['maximum']}",
                )
            )


def _validate_citations(
    document: Document, nodes: list[BlockNode], errors: list[ValidationIssue]
) -> None:
    source_ids: set[str] = set()
    for node in nodes:
        if node.name != "sources" or not isinstance(node.props, dict):
            continue
        items = node.props.get("items", [])
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                continue
            source_id = item["id"]
            path = f"items[{index}].id"
            if source_id in source_ids:
                errors.append(
                    _field_issue(
                        document,
                        node,
                        node.prop_lines,
                        path,
                        code="duplicate_source_id",
                        message=f"duplicate source id: {source_id}",
                    )
                )
            source_ids.add(source_id)

    for node in nodes:
        for field_path, citation in _walk_citations(node.props):
            if citation not in source_ids:
                errors.append(
                    _field_issue(
                        document,
                        node,
                        node.prop_lines,
                        field_path,
                        code="unresolved_citation",
                        message=f"citation does not resolve to a source id: {citation}",
                    )
                )


def _walk_citations(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = _join_path(path, key)
            if key == "citations" and isinstance(child, list):
                for index, citation in enumerate(child):
                    if isinstance(citation, str):
                        yield f"{child_path}[{index}]", citation
            else:
                yield from _walk_citations(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_citations(child, f"{path}[{index}]")


def _matches_type(value: Any, expected: str | list[str]) -> bool:
    types = [expected] if isinstance(expected, str) else expected
    return any(_matches_single_type(value, item) for item in types)


def _matches_single_type(value: Any, expected: str) -> bool:
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "null":
        return value is None
    raise ValueError(f"unsupported schema type: {expected}")


def _type_label(expected: str | list[str]) -> str:
    if isinstance(expected, str):
        return expected
    return " or ".join(expected)


def _join_path(parent: str, child: str) -> str:
    return f"{parent}.{child}" if parent else child


def _field_issue(
    document: Document,
    block: BlockNode | None,
    line_map: dict[str, int],
    field_path: str,
    code: str,
    message: str,
) -> ValidationIssue:
    line = _line_for_path(line_map, field_path)
    if line is None:
        line = block.line if block else 1
    return _issue(
        document,
        code=code,
        message=message,
        line=line,
        block=block.name if block else None,
        field=field_path or None,
    )


def _line_for_path(line_map: dict[str, int], field_path: str) -> int | None:
    current = field_path
    while current:
        if current in line_map:
            return line_map[current]
        if "." in current:
            current = current.rsplit(".", 1)[0]
        elif "[" in current:
            current = current.rsplit("[", 1)[0]
        else:
            break
    return None


def _issue(
    document: Document,
    code: str,
    message: str,
    line: int | None = None,
    block: str | None = None,
    field: str | None = None,
    severity: str = "error",
) -> ValidationIssue:
    return ValidationIssue(
        code=code,
        message=message,
        path=document.path,
        line=line,
        block=block,
        field=field,
        severity=severity,
    )
