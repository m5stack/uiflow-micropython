"""Build and sync the UIFlow2 docs into the uiflow2-coder skill."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LOCAL_SKILL_DIR = SCRIPT_DIR / "uiflow2-coder"
DEFAULT_SKILL_DIR = Path.home() / ".agents" / "skills" / "uiflow2-coder"
DOC_TREE_BEGIN = "<!-- BEGIN_DOC_TREE -->"
DOC_TREE_END = "<!-- END_DOC_TREE -->"


def run(cmd: list[str], cwd: Path = REPO_ROOT) -> None:
    print("+", " ".join(str(part) for part in cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def assert_safe_child(path: Path, parent: Path) -> None:
    resolved = path.resolve()
    resolved_parent = parent.resolve()
    if resolved == resolved_parent or resolved_parent not in resolved.parents:
        raise RuntimeError(f"Refusing to remove path outside {resolved_parent}: {resolved}")


def replace_dir(src: Path, dst: Path, safe_parent: Path) -> None:
    if not src.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {src}")
    if dst.exists():
        assert_safe_child(dst, safe_parent)
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def wrap_items(prefix: str, items: list[str], width: int = 118) -> list[str]:
    if not items:
        return [prefix.rstrip()]
    lines: list[str] = []
    current = prefix
    continuation = " " * len(prefix)
    for item in items:
        token = item if current == prefix else f", {item}"
        if len(current) + len(token) > width and current != prefix:
            lines.append(current)
            current = continuation + item
        else:
            current += token
    lines.append(current)
    return lines


def compact_doc_index(directory: Path, root_name: str = "docs") -> str:
    md_count = sum(1 for path in directory.rglob("*.md") if path.is_file())
    dir_count = sum(1 for path in directory.rglob("*") if path.is_dir())
    lines = [
        f"{root_name}/  ({md_count} Markdown files, {dir_count} directories; .md suffix omitted)",
        "Rule: an entry like unit/env means docs/unit/env.md; entries ending in / are directories.",
    ]

    def file_label(path: Path) -> str:
        return path.stem if path.suffix.lower() == ".md" else path.name

    def walk(path: Path, indent: int = 0, label: str = "root") -> None:
        files = sorted((item for item in path.iterdir() if item.is_file()), key=lambda item: item.name.lower())
        dirs = sorted((item for item in path.iterdir() if item.is_dir()), key=lambda item: item.name.lower())
        names = [file_label(item) for item in files]
        prefix = "  " * indent + f"- {label}: "
        if names:
            lines.extend(wrap_items(prefix, names))
        elif indent > 0:
            lines.append(("  " * indent) + f"- {label}/")
        for child in dirs:
            walk(child, indent + 1, f"{child.name}/")

    walk(directory)
    return "\n".join(lines) + "\n"


def render_doc_tree_block(docs_dir: Path) -> str:
    return (
        f"{DOC_TREE_BEGIN}\n"
        "```text\n"
        f"{compact_doc_index(docs_dir, 'docs')}"
        "```\n"
        f"{DOC_TREE_END}"
    )


def generate_docs(output_dir: Path) -> None:
    run([sys.executable, str(SCRIPT_DIR / "rst2md_en.py"), "--dst", str(output_dir)])


def copy_current_skill_to_repo(skill_dir: Path) -> None:
    print(f"Copying current skill shell: {skill_dir} -> {LOCAL_SKILL_DIR}")
    replace_dir(skill_dir, LOCAL_SKILL_DIR, SCRIPT_DIR)


def copy_repo_skill_to_system(skill_dir: Path) -> None:
    print(f"Copying repo skill to system skill: {LOCAL_SKILL_DIR} -> {skill_dir}")
    replace_dir(LOCAL_SKILL_DIR, skill_dir, skill_dir.parent)


def update_skill_doc_tree(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    docs_dir = skill_dir / "docs"
    text = skill_md.read_text(encoding="utf-8")
    tree_block = render_doc_tree_block(docs_dir)
    if DOC_TREE_BEGIN in text and DOC_TREE_END in text:
        before, rest = text.split(DOC_TREE_BEGIN, 1)
        _, after = rest.split(DOC_TREE_END, 1)
        text = before.rstrip() + "\n\n" + tree_block + after
    else:
        anchor = "\n## UIFlow2 "
        if anchor not in text:
            raise RuntimeError(f"Cannot find documentation tree insertion anchor in {skill_md}")
        section = (
            "## \u6587\u6863\u7d27\u51d1\u7d22\u5f15\n\n"
            "\u4ee5\u4e0b\u7d22\u5f15\u968f\u6587\u6863\u540c\u6b65\u81ea\u52a8\u66f4\u65b0\uff1b"
            "\u7edf\u4e00\u7701\u7565 `.md` \u540e\u7f00\u4ee5\u51cf\u5c11\u91cd\u590d\uff0c"
            "\u5148\u6839\u636e\u8fd9\u91cc\u5b9a\u4f4d\u6587\u4ef6\uff0c"
            "\u518d\u8bfb\u53d6\u5bf9\u5e94 `docs/...` \u539f\u6587\u3002\n\n"
        )
        text = text.replace(anchor, "\n\n" + section + tree_block + "\n" + anchor.lstrip("\n"), 1)
    skill_md.write_text(text, encoding="utf-8", newline="\n")


def sync_docs_to_skill(generated_docs: Path, skill_dir: Path) -> None:
    for target in (LOCAL_SKILL_DIR, skill_dir):
        if not target.is_dir():
            raise FileNotFoundError(f"Skill directory does not exist: {target}")
        docs_dir = target / "docs"
        print(f"Syncing generated docs into: {docs_dir}")
        replace_dir(generated_docs, docs_dir, target)
        (target / "file_tree.txt").write_text(
            compact_doc_index(docs_dir, "docs"),
            encoding="utf-8",
            newline="\n",
        )
        update_skill_doc_tree(target)


def read_utf8_checked(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError(f"UTF-8 BOM found in {path}")
    text = data.decode("utf-8")
    if "\ufffd" in text:
        raise RuntimeError(f"Replacement character found in {path}")
    return text


def file_map(root: Path) -> dict[str, Path]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): path
        for path in root.rglob("*")
        if path.is_file()
    }


def assert_same_tree(left: Path, right: Path) -> None:
    left_files = file_map(left)
    right_files = file_map(right)
    missing = sorted(set(left_files) - set(right_files))
    extra = sorted(set(right_files) - set(left_files))
    different = sorted(
        rel
        for rel in set(left_files) & set(right_files)
        if left_files[rel].read_bytes() != right_files[rel].read_bytes()
    )
    if missing or extra or different:
        raise RuntimeError(
            "Repo/system skill mismatch: "
            f"missing={missing[:10]}, extra={extra[:10]}, different={different[:10]}"
        )


def report_doc_quality(target: Path) -> None:
    docs_dir = target / "docs"
    patterns = {
        "rst_directive_comments": "<!-- ..",
        "failed_find": "Failed to find",
        "raw_param_fields": ":param",
        "raw_return_fields": ":returns:",
        "raw_rtype_fields": ":rtype:",
        "raw_code_block_directives": ".. code-block::",
        "visual_code_block_labels": "UiFlow2 Code Block:",
        "visual_code_block_upper_labels": "UIFLOW2 Code Block:",
        "micropython_code_block_labels": "MicroPython Code Block:",
        "micropython_code_block_alt_labels": "Micropython Code Block:",
        "visual_example_labels": "UiFlow2 Example:",
        "visual_example_upper_labels": "UIFLOW2 Example:",
        "visual_example_headings": "## UiFlow2 Example",
        "visual_standalone_labels": "UIFLOW2:",
        "visual_project_files": ".m5f2",
    }
    for label, pattern in patterns.items():
        files = 0
        hits = 0
        for path in docs_dir.rglob("*.md"):
            text = read_utf8_checked(path)
            count = text.count(pattern)
            if count:
                files += 1
                hits += count
        print(f"Quality {target.name}: {label}={hits} hits in {files} files")


def validate(skill_dir: Path) -> None:
    for target in (LOCAL_SKILL_DIR, skill_dir):
        docs_dir = target / "docs"
        md_files = list(docs_dir.rglob("*.md"))
        if not md_files:
            raise RuntimeError(f"No markdown files found in {docs_dir}")
        for path in md_files:
            text = read_utf8_checked(path)
            if "D:\\" in text or "/tmp/" in text:
                raise RuntimeError(f"Local absolute path leaked into {path}")
        for path in (target / "file_tree.txt", target / "SKILL.md"):
            read_utf8_checked(path)
        if (target / "SKILL.md").read_bytes()[:3] != b"---":
            raise RuntimeError(f"SKILL.md frontmatter does not start at byte 0: {target / 'SKILL.md'}")
        print(
            f"Validated {target}: {len(md_files)} markdown files, "
            f"{sum(1 for p in docs_dir.rglob('*') if p.is_dir())} directories"
        )
        report_doc_quality(target)
    assert_same_tree(LOCAL_SKILL_DIR, skill_dir)
    print("Validated repo/system skill trees are byte-identical.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument("--source-docs", type=Path, help="Use an existing generated docs directory instead of regenerating.")
    parser.add_argument(
        "--skip-copy-shell",
        action="store_true",
        help="Keep the repo skill shell as the source of truth instead of copying the current system skill first.",
    )
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    if not skill_dir.is_dir():
        raise FileNotFoundError(f"Skill directory does not exist: {skill_dir}")

    if args.skip_copy_shell:
        print(f"Keeping repo skill shell: {LOCAL_SKILL_DIR}")
    else:
        copy_current_skill_to_repo(skill_dir)
    if args.source_docs:
        source_docs = args.source_docs.resolve()
        if not source_docs.is_dir():
            raise FileNotFoundError(f"Generated docs directory does not exist: {source_docs}")
        with tempfile.TemporaryDirectory(prefix="uiflow2-docs-source-") as tmp:
            generated_docs = Path(tmp) / "docs"
            shutil.copytree(source_docs, generated_docs)
            sync_docs_to_skill(generated_docs, skill_dir)
    else:
        with tempfile.TemporaryDirectory(prefix="uiflow2-docs-") as tmp:
            generated_docs = Path(tmp) / "docs"
            generate_docs(generated_docs)
            sync_docs_to_skill(generated_docs, skill_dir)
    copy_repo_skill_to_system(skill_dir)
    validate(skill_dir)


if __name__ == "__main__":
    main()
