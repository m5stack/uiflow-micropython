# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from pathlib import Path
import sys, shutil, subprocess

r = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
s = r / "stubs"
l = r / "m5stack/libs"

if s.exists():
    shutil.rmtree(s)
s.mkdir()

for p in sorted(l.iterdir()):
    if p.is_dir() and not p.name.startswith("__"):
        subprocess.run(["pyright", "--createstub", f"m5stack.libs.{p.name}"], cwd=r)