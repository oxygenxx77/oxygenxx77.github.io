#!/bin/bash
# 把 index.html 导出成 A4 PDF（打印样式写在 index.html 的 @media print 里）
# 用法：tools/export_pdf.sh [输出文件]，默认输出到仓库根目录的 portfolio.pdf
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/portfolio.pdf}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PROFILE="$(mktemp -d)"
trap 'rm -rf "$PROFILE"' EXIT
mkdir -p "$(dirname "$OUT")"

"$CHROME" --headless=new --disable-gpu --no-first-run --user-data-dir="$PROFILE" \
  --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf="$OUT" "file://$ROOT/index.html" 2>/dev/null

echo "已导出：$OUT（$(du -h "$OUT" | cut -f1)）"
