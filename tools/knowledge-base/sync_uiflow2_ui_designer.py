"""Validate and synchronize the UIFlow2 UI Designer skill."""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LOCAL_SKILL_DIR = SCRIPT_DIR / "uiflow2-ui-designer"
DEFAULT_SKILL_DIR = Path.home() / ".agents" / "skills" / "uiflow2-ui-designer"
QUICK_VALIDATE = (
    Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
)
SKILL_NAME = "uiflow2-ui-designer"
REQUIRED_REFERENCES = (
    "display-profiles.md",
    "visual-system.md",
    "api-patterns.md",
    "rendering-strategy.md",
    "motion-and-effects.md",
    "layout-recipes.md",
    "review-checklist.md",
)
BACKTICKS = chr(96) * 3
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PYTHON_FENCE_RE = re.compile(BACKTICKS + r"python[ \t]*\r?\n(.*?)" + BACKTICKS, re.DOTALL)


def resolve_child(path: Path, parent: Path) -> Path:
    resolved = path.resolve()
    resolved_parent = parent.resolve()
    if resolved == resolved_parent or resolved_parent not in resolved.parents:
        raise RuntimeError(f"Refusing to operate outside {resolved_parent}: {resolved}")
    return resolved


def replace_dir(src: Path, dst: Path, dst_parent: Path) -> None:
    if not src.is_dir():
        raise FileNotFoundError(f"Skill directory does not exist: {src}")
    if dst.exists():
        resolve_child(dst, dst_parent)
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def file_map(root: Path) -> dict[str, Path]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): path
        for path in root.rglob("*")
        if path.is_file()
    }


def differing_files(left: Path, right: Path) -> tuple[list[str], list[str], list[str]]:
    left_files = file_map(left)
    right_files = file_map(right)
    missing = sorted(set(left_files) - set(right_files))
    extra = sorted(set(right_files) - set(left_files))
    different = sorted(
        rel
        for rel in set(left_files) & set(right_files)
        if left_files[rel].read_bytes() != right_files[rel].read_bytes()
    )
    return missing, extra, different


def read_utf8(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError(f"UTF-8 BOM found in {path}")
    text = data.decode("utf-8")
    if "\ufffd" in text:
        raise RuntimeError(f"Replacement character found in {path}")
    if not data.endswith(b"\n"):
        raise RuntimeError(f"Missing final LF in {path}")
    if any(line.rstrip(" \t") != line for line in text.splitlines()):
        raise RuntimeError(f"Trailing whitespace found in {path}")
    return text


def validate_links(path: Path, text: str) -> int:
    checked = 0
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip()
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        checked += 1
        resolved = (path.parent / target).resolve()
        if not resolved.is_file():
            raise RuntimeError(f"Broken local Markdown link in {path}: {raw_target}")
    return checked


def validate_python_fences(path: Path, text: str) -> int:
    checked = 0
    for index, block in enumerate(PYTHON_FENCE_RE.findall(text), start=1):
        checked += 1
        try:
            ast.parse(block, filename=f"{path} fenced block {index}")
        except SyntaxError as error:
            raise RuntimeError(f"Invalid Python fence in {path}: {error}") from error
    return checked


def validate_skill(skill_dir: Path, run_quick_validate: bool) -> tuple[int, int]:
    if skill_dir.name != SKILL_NAME:
        raise RuntimeError(f"Expected skill directory named {SKILL_NAME}: {skill_dir}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(f"Missing {skill_md}")
    if skill_md.read_bytes()[:3] != b"---":
        raise RuntimeError(f"SKILL.md frontmatter does not start at byte 0: {skill_md}")

    markdown_files = list(skill_dir.rglob("*.md"))
    if not markdown_files:
        raise RuntimeError(f"No Markdown files found in {skill_dir}")
    links = 0
    fences = 0
    for path in markdown_files:
        text = read_utf8(path)
        links += validate_links(path, text)
        fences += validate_python_fences(path, text)
        if "{{" in text or "}}" in text:
            raise RuntimeError(f"Unresolved template placeholder found in {path}")

    for filename in REQUIRED_REFERENCES:
        path = skill_dir / "references" / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing required reference: {path}")

    if run_quick_validate:
        if not QUICK_VALIDATE.is_file():
            raise FileNotFoundError(f"Cannot find quick_validate.py: {QUICK_VALIDATE}")
        subprocess.run(
            [sys.executable, "-X", "utf8", str(QUICK_VALIDATE), str(skill_dir)],
            cwd=REPO_ROOT,
            check=True,
        )
    print(
        f"Validated {skill_dir}: {len(markdown_files)} Markdown files, "
        f"{links} local links, {fences} Python fences"
    )
    return len(markdown_files), links


def assert_same_tree(left: Path, right: Path) -> None:
    missing, extra, different = differing_files(left, right)
    if missing or extra or different:
        raise RuntimeError(
            "Repo/system skill mismatch: "
            f"missing={missing}, extra={extra}, different={different}"
        )
    print("Validated repo/system skill trees are byte-identical.")


def sync(local_skill: Path, system_skill: Path, force: bool) -> None:
    validate_skill(local_skill, run_quick_validate=True)
    if system_skill.exists() and not force:
        missing, extra, different = differing_files(local_skill, system_skill)
        if missing or extra or different:
            raise RuntimeError(
                "Installed skill differs; refusing to overwrite without --force: "
                f"missing={missing}, extra={extra}, different={different}"
            )
    replace_dir(local_skill, system_skill, system_skill.parent)
    validate_skill(system_skill, run_quick_validate=True)
    assert_same_tree(local_skill, system_skill)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=DEFAULT_SKILL_DIR,
        help="Installed skill directory (default: ~/.agents/skills/uiflow2-ui-designer)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate both copies and compare them without writing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow replacing an existing installed copy after validation",
    )
    args = parser.parse_args()

    local_skill = LOCAL_SKILL_DIR.resolve()
    system_skill = args.skill_dir.resolve()
    if system_skill.name != SKILL_NAME:
        raise RuntimeError(f"--skill-dir must end with {SKILL_NAME}: {system_skill}")

    if args.check_only:
        validate_skill(local_skill, run_quick_validate=True)
        if not system_skill.is_dir():
            raise FileNotFoundError(f"Installed skill directory does not exist: {system_skill}")
        validate_skill(system_skill, run_quick_validate=True)
        assert_same_tree(local_skill, system_skill)
        return

    sync(local_skill, system_skill, force=args.force)


if __name__ == "__main__":
    main()
