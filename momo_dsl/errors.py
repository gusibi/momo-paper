"""Error types for Momo Paper DSL parsing and rendering."""

from dataclasses import dataclass


@dataclass
class DslError(Exception):
    """A user-facing DSL error with source context."""

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
