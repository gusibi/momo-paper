"""Parser for Momo Paper Markdown DSL.

The parser intentionally supports a small YAML-like subset so the runtime has
no external dependencies. It is designed for Agent-generated documents: clear
syntax, fail-fast errors, and source line numbers.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from .errors import DslError

TAG_RE = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass
class MarkdownNode:
    text: str
    line: int


@dataclass
class BlockNode:
    name: str
    props: Any
    line: int


@dataclass
class Document:
    meta: dict[str, Any]
    nodes: list[MarkdownNode | BlockNode]
    path: str | None = None


def parse_file(path: str | Path) -> Document:
    source = Path(path)
    return parse_text(source.read_text(encoding="utf-8"), path=str(source))


def parse_text(text: str, path: str | None = None) -> Document:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise DslError("missing frontmatter opening ---", path=path, line=1)

    end = _find_frontmatter_end(lines, path)
    frontmatter = _parse_data(lines[1:end], path=path, start_line=2, context="frontmatter")
    if not isinstance(frontmatter, dict):
        raise DslError("frontmatter must be key/value data", path=path, line=1)

    nodes: list[MarkdownNode | BlockNode] = []
    markdown_buffer: list[str] = []
    markdown_start = end + 2
    i = end + 1

    def flush_markdown() -> None:
        nonlocal markdown_buffer, markdown_start
        raw = "\n".join(markdown_buffer).strip()
        if raw:
            nodes.append(MarkdownNode(text=raw, line=markdown_start))
        markdown_buffer = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith(":::") and stripped != ":::":
            flush_markdown()
            block_name = stripped[3:].strip()
            block_line = i + 1
            if not TAG_RE.match(block_name):
                raise DslError("invalid block tag name", path=path, line=block_line, block=block_name)
            body_start = i + 1
            close = _find_block_end(lines, body_start, path, block_name, block_line)
            props = _parse_data(
                lines[body_start:close],
                path=path,
                start_line=body_start + 1,
                context=f"block {block_name}",
            )
            nodes.append(BlockNode(name=block_name, props=props, line=block_line))
            i = close + 1
            markdown_start = i + 1
            continue

        if not markdown_buffer and stripped:
            markdown_start = i + 1
        markdown_buffer.append(line)
        i += 1

    flush_markdown()
    document = Document(meta=frontmatter, nodes=nodes, path=path)
    validate_document(document)
    return document


def validate_document(document: Document) -> None:
    meta = document.meta
    path = document.path
    doc_type = meta.get("document_type")
    if not doc_type:
        raise DslError("frontmatter missing required field: document_type", path=path, line=1)
    if doc_type == "dashboard":
        raise DslError("dashboard is not a valid document_type", path=path, line=1)
    if not meta.get("locale"):
        raise DslError("frontmatter missing required field: locale", path=path, line=1)
    if not meta.get("title"):
        raise DslError("frontmatter missing required field: title", path=path, line=1)

    for node in document.nodes:
        if isinstance(node, BlockNode) and not TAG_RE.match(node.name):
            raise DslError("invalid block tag name", path=path, line=node.line, block=node.name)


def _find_frontmatter_end(lines: list[str], path: str | None) -> int:
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i
    raise DslError("missing frontmatter closing ---", path=path, line=len(lines))


def _find_block_end(
    lines: list[str],
    start: int,
    path: str | None,
    block_name: str,
    block_line: int,
) -> int:
    for i in range(start, len(lines)):
        if lines[i].strip() == ":::":
            return i
    raise DslError("unclosed block directive", path=path, line=block_line, block=block_name)


def _parse_data(lines: list[str], path: str | None, start_line: int, context: str) -> Any:
    tokens: list[tuple[int, str, int]] = []
    for offset, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise DslError("tabs are not supported for indentation", path=path, line=start_line + offset)
        indent = len(raw) - len(raw.lstrip(" "))
        tokens.append((indent, raw.strip(), start_line + offset))

    if not tokens:
        return {}

    value, index = _parse_container(tokens, 0, tokens[0][0], path, context)
    if index != len(tokens):
        _, _, line = tokens[index]
        raise DslError("could not parse remaining data", path=path, line=line)
    return value


def _parse_container(
    tokens: list[tuple[int, str, int]],
    index: int,
    indent: int,
    path: str | None,
    context: str,
) -> tuple[Any, int]:
    if index >= len(tokens):
        return {}, index
    current_indent, text, _ = tokens[index]
    if current_indent < indent:
        return {}, index
    if text.startswith("- "):
        return _parse_list(tokens, index, current_indent, path, context)
    return _parse_mapping(tokens, index, current_indent, path, context)


def _parse_mapping(
    tokens: list[tuple[int, str, int]],
    index: int,
    indent: int,
    path: str | None,
    context: str,
) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(tokens):
        current_indent, text, line = tokens[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise DslError("unexpected indentation", path=path, line=line)
        if text.startswith("- "):
            break
        key, raw_value = _split_key_value(text, path, line, context)
        index += 1
        if raw_value == "":
            if index < len(tokens) and tokens[index][0] > current_indent:
                value, index = _parse_container(tokens, index, tokens[index][0], path, context)
            else:
                value = {}
        else:
            value = _parse_scalar(raw_value)
        result[key] = value
    return result, index


def _parse_list(
    tokens: list[tuple[int, str, int]],
    index: int,
    indent: int,
    path: str | None,
    context: str,
) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(tokens):
        current_indent, text, line = tokens[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise DslError("unexpected indentation", path=path, line=line)
        if not text.startswith("- "):
            break

        item_text = text[2:].strip()
        index += 1
        if item_text == "":
            if index < len(tokens) and tokens[index][0] > current_indent:
                item, index = _parse_container(tokens, index, tokens[index][0], path, context)
            else:
                item = ""
        elif ":" in item_text and not _looks_like_url(item_text):
            key, raw_value = _split_key_value(item_text, path, line, context)
            item = {key: _parse_scalar(raw_value) if raw_value else {}}
            if index < len(tokens) and tokens[index][0] > current_indent:
                nested, index = _parse_mapping(tokens, index, tokens[index][0], path, context)
                item.update(nested)
        else:
            item = _parse_scalar(item_text)
        result.append(item)
    return result, index


def _split_key_value(text: str, path: str | None, line: int, context: str) -> tuple[str, str]:
    if ":" not in text:
        raise DslError(f"expected key/value data in {context}", path=path, line=line)
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise DslError("empty key is not allowed", path=path, line=line)
    return key, value.strip()


def _parse_scalar(value: str) -> Any:
    if value in {"true", "false"}:
        return value == "true"
    if value in {"null", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _looks_like_url(text: str) -> bool:
    return "://" in text
