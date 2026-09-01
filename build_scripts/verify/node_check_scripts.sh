#!/bin/bash
# Extract every <script> block of each file and run node --check on it.
set -e
OUT=$(mktemp -d)
for f in memory-items.html limitations.html; do
  python3 - "$f" "$OUT" <<'PY'
import re, sys
f, out = sys.argv[1], sys.argv[2]
html = open(f, encoding="utf-8").read()
blocks = re.findall(r"<script>(.*?)</script>", html, re.S)
for i, b in enumerate(blocks, 1):
    open(f"{out}/{f}.script{i}.js", "w", encoding="utf-8").write(b)
print(f"{f}: {len(blocks)} script blocks extracted")
PY
  for js in "$OUT"/"$f".script*.js; do
    node --check "$js" && echo "node --check $(basename "$js"): OK"
  done
done
