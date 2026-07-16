"""Error types for Momo Paper DSL parsing and validation."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class DslError(Exception):
    """A user-facing DSL syntax error with source context."""

    message: str
    path: str | None = None
    line: int | None = None
    block: str | None = None

    def __str__(self) -> str:
        parts: list[str] = []
        if self.path:
            parts.append(self.path)
        if self.line is not None:
            parts.append(f"line {self.line}")
        if self.block:
            parts.append(f"block {self.block}")
        prefix = ": ".join(parts)
        return f"{prefix}: {self.message}" if prefix else self.message


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: str | None = None
    line: int | None = None
    block: str | None = None
    field: str | None = None
    severity: Literal["error", "warning"] = "error"


@dataclass(frozen=True)
class ValidationReport:
    mode: Literal["strict", "free"]
    schema: str | None
    candidates: tuple[str, ...]
    errors: tuple[ValidationIssue, ...]
    warnings: tuple[ValidationIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.errors
