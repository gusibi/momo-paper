#!/usr/bin/env bash
#
# sync-skill.sh — mirror the canonical engine into the bundled skill copy.
#
# Single source of truth (edit these):
#   momo_dsl/            engine: parser, renderer, cli, styles
#   REFERENCE.md         DSL reference
#   examples/*.md        example DSL sources
#
# Generated bundle (NEVER hand-edit — overwritten by this script):
#   momo-paper-skill/runtime/momo_dsl/
#   momo-paper-skill/references/REFERENCE.md
#   momo-paper-skill/examples/*.md
#
# Run before committing/releasing whenever you change the engine, the
# reference doc, or the examples. The skill stays self-contained (zero
# install) because the runtime is bundled — this keeps that bundle a
# build artifact instead of a second copy you maintain by hand.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$ROOT/momo-paper-skill"

EXCLUDES=(--exclude '__pycache__/' --exclude '*.pyc' --exclude '.DS_Store')

# 1. Engine code + bundled CSS -> runtime/momo_dsl (exact mirror).
rsync -a --delete "${EXCLUDES[@]}" \
  "$ROOT/momo_dsl/" "$SKILL/runtime/momo_dsl/"

# 2. Reference doc.
mkdir -p "$SKILL/references"
cp "$ROOT/REFERENCE.md" "$SKILL/references/REFERENCE.md"

# 3. Example DSL sources (*.md only).
mkdir -p "$SKILL/examples"
rsync -a "${EXCLUDES[@]}" --include '*.md' --exclude '*' \
  "$ROOT/examples/" "$SKILL/examples/"

echo "synced: momo_dsl/        -> $SKILL/runtime/momo_dsl/"
echo "synced: REFERENCE.md     -> $SKILL/references/REFERENCE.md"
echo "synced: examples/*.md    -> $SKILL/examples/"
