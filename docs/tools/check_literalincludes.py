# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT
"""Check literalinclude targets, including declarations in RST comments."""

import argparse
from pathlib import Path
import re
import sys


DIRECTIVE = re.compile(r"^\s*\.\.\s+literalinclude::\s*(.*?)\s*$")


def check_literalincludes(source):
    count = 0
    missing = []
    for rst in sorted(source.rglob("*.rst")):
        for number, line in enumerate(rst.read_text(encoding="utf-8").splitlines(), 1):
            match = DIRECTIVE.match(line)
            if match is None:
                continue
            count += 1
            name = match.group(1)
            # Sphinx resolves an initial slash relative to the source directory.
            target = source / name.lstrip("/") if name.startswith("/") else rst.parent / name
            if not name or not target.is_file():
                missing.append((rst.relative_to(source), number, name))
    return count, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "source",
        help="Sphinx source directory (defaults to docs/source)",
    )
    source = parser.parse_args().source.resolve()
    if not source.is_dir():
        parser.error("source directory does not exist: %s" % source)
    count, missing = check_literalincludes(source)
    for rst, number, name in missing:
        print("%s:%d: missing literalinclude target: %s" % (rst, number, name), file=sys.stderr)
    print("Checked %d literalinclude targets; %d missing." % (count, len(missing)))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
