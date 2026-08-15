#!/bin/sh
# Check the source manifest, replay the exact-verification supplement, and
# build the manuscript with Tectonic into a disposable temporary directory,
# leaving no build products in the repository. Pass --no-latex to skip the
# manuscript build.
#
# Requirements: a Linux environment with GNU coreutils; uv; and Tectonic
# for the manuscript build. The root pyproject.toml and uv.lock own one
# frozen Python environment for the supplement.

set -eu
cd "$(dirname "$0")"

NICE="nice -n 10"
BUILD_LATEX=yes
[ "${1:-}" = "--no-latex" ] && BUILD_LATEX=no

echo "== Repository environment layout"
test -f pyproject.toml
test -f uv.lock

echo "== Source manifest"
$NICE sha256sum -c SHA256SUMS

echo "== Small-support certificate"
$NICE uv run python verify/verify.py

if [ "$BUILD_LATEX" = yes ]; then
  echo "== Manuscript build (Tectonic)"
  BUILD_DIR=$(mktemp -d)
  trap 'rm -rf "$BUILD_DIR"' EXIT
  $NICE tectonic --outdir "$BUILD_DIR" --reruns 9 paper/main.tex
  test -f "$BUILD_DIR/main.pdf"
  echo "built main.pdf ($(stat -c%s "$BUILD_DIR/main.pdf") bytes, discarded)"
fi

echo "== All checks passed"
