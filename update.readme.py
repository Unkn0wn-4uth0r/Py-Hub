#!/usr/bin/env python3
import os
ROOT = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(ROOT, "Python")
out = os.path.join(ROOT, "README.md")

lines = ["# Python Hub (Auto-generated)\n", "\n", "## Categories\n\n"]
if not os.path.exists(PY):
    lines.append("No Python/ folder found.\n")
else:
    for cat in sorted([d for d in os.listdir(PY) if os.path.isdir(os.path.join(PY, d))]):
        lines.append(f"### {cat}\n\n")
        files = sorted([f for f in os.listdir(os.path.join(PY, cat)) if not f.startswith('.')])
        if not files:
            lines.append("- (empty)\n\n")
            continue
        for f in files:
            lines.append(f"- {f}\n")
        lines.append("\n")

with open(out, "w", encoding="utf-8") as fh:
    fh.writelines(lines)
print("README.md updated.")
