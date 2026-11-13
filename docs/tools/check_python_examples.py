#!/usr/bin/env python3
"""Compile Python examples exposed by RST/docstrings and the coder mirror."""

import importlib.util
from pathlib import Path
import re
import sys


def main():
    repo = Path(__file__).resolve().parents[2]
    converter_path = repo / "tools/knowledge-base/rst2md_en.py"
    spec = importlib.util.spec_from_file_location("rst2md_examples", converter_path)
    converter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(converter)
    pattern = re.compile(r"^```python\s*\n(.*?)^```", re.M | re.S)
    blocks = 0
    errors = []
    sources = sorted((repo / "docs/source").rglob("*.rst"))
    mirrors = sorted((repo / "tools/knowledge-base/uiflow2-coder/docs").rglob("*.md"))
    for path in sources + mirrors:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".rst":
            text = converter.rst_to_md(text, str(path))
        for index, code in enumerate(pattern.findall(text), start=1):
            blocks += 1
            name = str(path.relative_to(repo)) + ":block " + str(index)
            try:
                compile(code, name, "exec")
            except (SyntaxError, ValueError) as exc:
                errors.append(name + ": " + str(exc))
    for error in errors:
        print(error, file=sys.stderr)
    print("Python example syntax: %d blocks, %d errors" % (blocks, len(errors)))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
