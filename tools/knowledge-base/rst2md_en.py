from __future__ import annotations

import argparse
import ast
import os
import re
import shutil
from typing import Dict, List, Optional, Sequence, Tuple


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SRC_ROOT = os.path.join(REPO_ROOT, "docs", "source")
DEFAULT_DST_ROOT = os.path.join(SCRIPT_DIR, "uiflow2-coder", "docs")
DST_ROOT = os.environ.get("UIFLOW2_DOCS_DST", DEFAULT_DST_ROOT)
PYTHON_ROOT = os.path.join(REPO_ROOT, "m5stack", "libs")
REFS_DIR = os.path.join(SRC_ROOT, "refs")

IMAGE_EXT_PATTERN = r"(?:png|jpg|jpeg|gif|webp|bmp|svg)"
INDEX_MIN_SUBSTANTIVE_CHARS = 80
HEADING_LEVELS = {
    "=": "#",
    "-": "##",
    "~": "###",
    "^": "####",
    '"': "#####",
    "`": "######",
    "#": "#",
    "*": "##",
    "+": "###",
}
LOW_VALUE_INDEX_BLOCKS = (
    ".. toctree::",
    ".. include::",
    ".. module::",
    ".. currentmodule::",
    ".. only::",
)
SKIP_RST_REL_PATHS = {
    "contribute/template.rst",
}

AUTODOC_SIGNATURE_RE = re.compile(
    r"^\s*\.\.\s+(?:(?:py|c|cpp):{1,2})?"
    r"(function|class|method|property|staticmethod|classmethod|attribute|data|exception)::\s*(.+?)\s*$"
)
AUTODOC_CLASS_RE = re.compile(r"\.\. autoclass::\s*([^\s:]+)")
CODE_BLOCK_RE = re.compile(r"^\s*\.\.\s+(?:code-block|sourcecode)::\s*([^\s]+)?\s*$")
LITERAL_INCLUDE_RE = re.compile(r"\.\. literalinclude::\s*([^\s]+)")


def leading_spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def is_adornment(line: str, title: str = "") -> bool:
    stripped = line.strip()
    if not stripped or len(set(stripped)) != 1:
        return False
    if stripped[0] not in HEADING_LEVELS:
        return False
    return not title or len(stripped) >= len(title.strip())


def rst_heading_to_md(lines: Sequence[str]) -> List[str]:
    """Convert RST underlined and overline+underlined headings to Markdown."""
    md_lines: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if (
            i + 2 < len(lines)
            and is_adornment(line)
            and lines[i + 1].strip()
            and is_adornment(lines[i + 2], lines[i + 1])
            and line.strip()[0] == lines[i + 2].strip()[0]
        ):
            ch = line.strip()[0]
            md_lines.append(f"{HEADING_LEVELS.get(ch, '#')} {lines[i + 1].strip()}\n")
            i += 3
            continue

        if i + 1 < len(lines) and lines[i].strip() and is_adornment(lines[i + 1], line):
            ch = lines[i + 1].strip()[0]
            md_lines.append(f"{HEADING_LEVELS.get(ch, '#')} {line.strip()}\n")
            i += 2
            continue

        md_lines.append(line)
        i += 1

    return md_lines


def parse_ref_file(ref_filename: str) -> Dict[str, str]:
    image_map: Dict[str, str] = {}
    ref_path = os.path.join(REFS_DIR, ref_filename)
    if not os.path.exists(ref_path):
        return image_map

    with open(ref_path, encoding="utf-8") as f:
        ref_content = f.read()
    pattern = re.compile(r"\.\. \|([^|]+)\| image::\s*([^\n]+)")
    for name, url in pattern.findall(ref_content):
        image_map[name.strip()] = url.strip()
    return image_map


def find_python_file(module_path: str) -> Optional[str]:
    relative_path = module_path.replace(".", os.path.sep)
    python_file = os.path.join(PYTHON_ROOT, relative_path + ".py")
    if os.path.exists(python_file):
        return python_file
    return None


def module_name_from_file(python_file: str) -> str:
    rel = os.path.relpath(python_file, PYTHON_ROOT)
    return os.path.splitext(rel)[0].replace(os.path.sep, ".")


def resolve_relative_module(current_module: str, level: int, module: Optional[str]) -> Optional[str]:
    if level <= 0:
        return module

    parts = current_module.split(".")[:-1]
    if level > 1:
        parts = parts[: -(level - 1)]
    if module:
        parts.extend(module.split("."))
    return ".".join(part for part in parts if part)


def parse_python_ast(python_file: str) -> Optional[ast.Module]:
    try:
        with open(python_file, encoding="utf-8") as f:
            return ast.parse(f.read())
    except (SyntaxError, OSError):
        return None


def find_class_node(tree: ast.Module, class_name: str) -> Optional[ast.ClassDef]:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    return None


def import_aliases(tree: ast.Module, python_file: str) -> Dict[str, Tuple[str, str]]:
    aliases: Dict[str, Tuple[str, str]] = {}
    current_module = module_name_from_file(python_file)
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        module_path = resolve_relative_module(current_module, node.level, node.module)
        if not module_path:
            continue
        for alias in node.names:
            local_name = alias.asname or alias.name
            aliases[local_name] = (module_path, alias.name)
    return aliases


def assignment_aliases(tree: ast.Module) -> Dict[str, str]:
    aliases: Dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Name):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                aliases[target.id] = node.value.id
    return aliases


def resolve_class(
    python_file: str,
    class_name: str,
    seen: Optional[set[Tuple[str, str]]] = None,
) -> Optional[Tuple[str, str, ast.ClassDef]]:
    """Resolve real ClassDef nodes, including simple assignment/import aliases."""
    if seen is None:
        seen = set()
    key = (os.path.abspath(python_file), class_name)
    if key in seen:
        return None
    seen.add(key)

    tree = parse_python_ast(python_file)
    if tree is None:
        return None

    class_node = find_class_node(tree, class_name)
    if class_node is not None:
        return python_file, class_name, class_node

    imports = import_aliases(tree, python_file)
    assignments = assignment_aliases(tree)

    if class_name in assignments:
        alias_name = assignments[class_name]
        if alias_name in imports:
            module_path, imported_name = imports[alias_name]
            imported_file = find_python_file(module_path)
            if imported_file:
                return resolve_class(imported_file, imported_name, seen)
        return resolve_class(python_file, alias_name, seen)

    if class_name in imports:
        module_path, imported_name = imports[class_name]
        imported_file = find_python_file(module_path)
        if imported_file:
            return resolve_class(imported_file, imported_name, seen)

    return None


def parse_python_docstring(python_file: str, class_name: str) -> str:
    resolved = resolve_class(python_file, class_name)
    display_file = os.path.relpath(python_file, REPO_ROOT).replace(os.path.sep, "/")
    if resolved is None:
        return f"<!-- Failed to find class {class_name} in {display_file} -->"

    resolved_file, resolved_name, class_node = resolved
    md: List[str] = []

    if resolved_file != python_file or resolved_name != class_name:
        resolved_display = os.path.relpath(resolved_file, REPO_ROOT).replace(os.path.sep, "/")
        md.append(f"`{class_name}` is an alias of `{resolved_name}` in `{resolved_display}`.")
        md.append("")

    class_doc = ast.get_docstring(class_node, clean=True)
    if class_doc:
        rendered = rst_to_md(class_doc).strip()
        if rendered:
            md.append(rendered)
        md.append("")

    for node in class_node.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            md.append(f"### `{node.name}`")
            docstring = ast.get_docstring(node, clean=True)
            if docstring:
                rendered = rst_to_md(docstring).strip()
                if rendered:
                    md.append(rendered)
            md.append("")

    return "\n".join(md)


def parse_autoclass_directive(directive_line: str) -> Optional[Tuple[str, str]]:
    match = AUTODOC_CLASS_RE.match(directive_line.strip())
    if not match:
        return None
    full_path = match.group(1)
    parts = full_path.split(".")
    return ".".join(parts[:-1]), parts[-1]


def parse_literalinclude_directive(directive_line: str) -> Optional[str]:
    match = LITERAL_INCLUDE_RE.match(directive_line.strip())
    if not match:
        return None
    return match.group(1)


def strip_example_preamble(code: str) -> str:
    lines = code.splitlines()
    first_nonblank = next((i for i, line in enumerate(lines) if line.strip()), None)
    if first_nonblank is None:
        return ""
    if not lines[first_nonblank].lstrip().startswith("# SPDX-"):
        return code.rstrip() + "\n"

    i = first_nonblank
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped or stripped == "#" or stripped.startswith("# SPDX-"):
            i += 1
            continue
        break
    return "\n".join(lines[i:]).rstrip() + "\n"


def read_example_code(file_path: str, current_rst_path: Optional[str] = None) -> str:
    candidates = [os.path.abspath(file_path)]

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    candidates.append(os.path.join(project_root, file_path.lstrip(".").lstrip(os.path.sep)))

    if current_rst_path:
        candidates.append(os.path.abspath(os.path.join(os.path.dirname(current_rst_path), file_path)))

    for candidate in candidates:
        if os.path.exists(candidate):
            with open(candidate, encoding="utf-8") as f:
                return strip_example_preamble(f.read())

    return f"<!-- Failed to find example file: {file_path} -->"


def dedent_rst_block(block_lines: Sequence[str]) -> List[str]:
    lines = list(block_lines)
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return []

    indents = [leading_spaces(line) for line in lines if line.strip()]
    min_indent = min(indents) if indents else 0
    return [line[min_indent:] if len(line) >= min_indent else "" for line in lines]


def collect_indented_block(lines: Sequence[str], start: int, base_indent: int) -> Tuple[List[str], int]:
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if leading_spaces(lines[i]) > base_indent and stripped.startswith(":"):
            i += 1
            continue
        break

    block: List[str] = []
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            block.append(line)
            i += 1
            continue
        if leading_spaces(line) <= base_indent:
            break
        block.append(line)
        i += 1

    return dedent_rst_block(block), i


def append_code_block(md: List[str], code_lines: Sequence[str], language: str = "") -> None:
    if not code_lines:
        return
    fence = f"```{language}" if language else "```"
    md.append(fence)
    md.extend(code_lines)
    md.append("```")


def convert_field_list_line(line: str) -> Optional[str]:
    param = re.match(r"^(\s*):(param|keyword)\s+(?:(\S+)\s+)?([^:]+):\s*(.*)$", line)
    if param:
        indent, kind, type_name, name, desc = param.groups()
        label = "Parameter" if kind == "param" else "Keyword"
        type_text = f" (`{type_name}`)" if type_name else ""
        return f"{indent}- {label} `{name.strip()}`{type_text}: {desc}"

    type_line = re.match(r"^(\s*):type\s+([^:]+):\s*(.*)$", line)
    if type_line:
        indent, name, desc = type_line.groups()
        return f"{indent}- Type of `{name.strip()}`: {desc}"

    returns = re.match(r"^(\s*):returns?:\s*(.*)$", line)
    if returns:
        indent, desc = returns.groups()
        return f"{indent}- Returns: {desc}"

    rtype = re.match(r"^(\s*):rtype:\s*(.*)$", line)
    if rtype:
        indent, desc = rtype.groups()
        return f"{indent}- Return type: {desc}"

    return None


def convert_inline_rst(text: str) -> str:
    text = re.sub(r":(?:mod|class|func|meth|attr|data|ref):`([^`]+)`", r"`\1`", text)
    text = re.sub(r"``([^`]+)``", r"`\1`", text)
    return text


def append_admonition(md: List[str], kind: str, text: str, body: Sequence[str]) -> None:
    label = {
        "note": "Note",
        "warning": "Warning",
        "important": "Important",
        "tip": "Tip",
    }.get(kind.lower(), kind.title())
    content = [text] if text else []
    content.extend(body)
    if not content:
        return
    first = True
    for line in content:
        if first:
            md.append(f"> {label}: {line}".rstrip())
            first = False
        else:
            md.append(f"> {line}".rstrip())


def strip_index_noise(rst_text: str) -> str:
    lines = rst_text.splitlines()
    useful_lines: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if (
            i + 2 < len(lines)
            and is_adornment(lines[i])
            and lines[i + 1].strip()
            and is_adornment(lines[i + 2], lines[i + 1])
        ):
            i += 3
            continue

        if i + 1 < len(lines) and is_adornment(lines[i + 1], line):
            i += 2
            continue

        if any(stripped.startswith(block) for block in LOW_VALUE_INDEX_BLOCKS):
            base_indent = leading_spaces(line)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if not next_line.strip():
                    i += 1
                    continue
                if leading_spaces(next_line) > base_indent:
                    i += 1
                    continue
                break
            continue

        if stripped.startswith(":") or re.match(r"^[=\-\s`|]+$", stripped):
            i += 1
            continue

        useful_lines.append(line)
        i += 1

    return "\n".join(useful_lines)


def should_skip_index_rst(rst_text: str) -> bool:
    stripped = strip_index_noise(rst_text)
    substantive = "".join(ch for ch in stripped if not ch.isspace())
    return len(substantive) < INDEX_MIN_SUBSTANTIVE_CHARS


def cleanup_md_text(md_text: str, image_map: Dict[str, str]) -> str:
    md_text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", md_text)
    md_text = re.sub(
        r"[\[\]]\s*[^\n\[\]]+\." + IMAGE_EXT_PATTERN + r"\s*[\[\]|]?",
        "",
        md_text,
        flags=re.IGNORECASE,
    )
    md_text = re.sub(
        r"\|([^|\n]+\." + IMAGE_EXT_PATTERN + r")\|",
        "",
        md_text,
        flags=re.IGNORECASE,
    )
    md_text = re.sub(r"\|([^|\n]+\.m5f2)\|", r"`\1`", md_text, flags=re.IGNORECASE)
    for name in image_map.keys():
        md_text = md_text.replace(f"[{name}]", "")
        md_text = md_text.replace(f"]{name}[", "")
        md_text = md_text.replace(f"]{name}|", "")
    md_text = re.sub(r"\|([A-Za-z0-9 _+\-./]+)\|", r"\1", md_text)
    md_text = "".join(ch for ch in md_text if ch in "\n\r\t" or ord(ch) >= 32)
    md_text = remove_non_programming_noise(md_text)
    md_text = remove_empty_uiflow_sections(md_text)
    md_text = re.sub(r"\n\s*\n\s*\n+", "\n\n", md_text)
    lines = [line.rstrip() for line in md_text.splitlines()]
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + "\n"


def is_table_border(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and len(stripped) >= 5 and bool(re.fullmatch(r"[+=\-\s|:]+", stripped))


def is_m5f2_reference(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if ".m5f2" not in stripped.lower():
        return False
    return bool(
        re.fullmatch(r"`[^`]+\.m5f2`", stripped, flags=re.IGNORECASE)
        or re.fullmatch(r"`[^`]+\.m5f2`,?\s*`[^`]+\.m5f2`", stripped, flags=re.IGNORECASE)
        or re.match(r"Open the `[^`]+\.m5f2` project in UiFlow2\.?$", stripped, re.IGNORECASE)
    )


def parse_md_heading(line: str) -> Optional[Tuple[int, str]]:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.strip())
    if not match:
        return None
    title = match.group(2).strip().strip("#").strip()
    return len(match.group(1)), title


def is_visual_example_heading(line: str) -> bool:
    heading = parse_md_heading(line)
    if heading is None:
        return False
    title = heading[1].rstrip(":").lower()
    return "example" in title and "micropython" not in title and (
        "uiflow" in title or "blockly" in title
    )


def is_visual_example_label(stripped: str) -> bool:
    title = stripped.rstrip(":").lower()
    return "example" in title and "micropython" not in title and (
        "uiflow" in title or "blockly" in title
    )


def is_programming_section_heading(line: str) -> bool:
    heading = parse_md_heading(line)
    if heading is None:
        return False
    title = heading[1].strip("* ").rstrip(":").lower()
    return (
        ("micropython" in title and "example" in title)
        or title == "api"
        or title.startswith("class ")
        or title in {"constructors", "methods", "functions"}
    )


def remove_non_programming_noise(md_text: str) -> str:
    """Drop UIFlow visual-block remnants and repeated labels that do not help code generation."""
    lines = md_text.splitlines()
    out: List[str] = []
    i = 0
    in_fence = False
    removable_labels = {
        "UiFlow2 Code Block:",
        "UIFLOW2 Code Block:",
        "UiFlow2:",
        "UIFLOW2:",
        "UiFlow2",
        "UIFLOW2",
        "MicroPython Code Block:",
        "Micropython Code Block:",
        "MicroPython:",
        "Micropython:",
        "Blockly Code Block:",
        "Blockly:",
    }
    uiflow_example_labels = {
        "UIFLOW2 Example:",
        "UiFlow2 Example:",
        "UIFLOW2 TX Example:",
        "UIFLOW2 RX Example:",
        "UiFlow2 TX Example:",
        "UiFlow2 RX Example:",
    }

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            out.append(line)
            in_fence = not in_fence
            i += 1
            continue

        if in_fence:
            out.append(line)
            i += 1
            continue

        heading = parse_md_heading(line)
        if heading and is_visual_example_heading(line):
            level, _ = heading
            i += 1
            while i < len(lines):
                next_heading = parse_md_heading(lines[i])
                if next_heading and (
                    next_heading[0] <= level or is_programming_section_heading(lines[i])
                ):
                    break
                i += 1
            continue

        if stripped in removable_labels:
            i += 1
            continue

        if stripped in uiflow_example_labels or is_visual_example_label(stripped):
            i += 1
            continue

        if ".m5f2" in stripped.lower() or is_m5f2_reference(line):
            i += 1
            while i < len(lines) and lines[i].strip().lower() in {"uiflow2", "uiflow2."}:
                i += 1
            continue

        if is_table_border(line):
            i += 1
            continue

        if stripped == "Example output:":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if (
                j >= len(lines)
                or lines[j].strip() == "None"
                or lines[j].lstrip().startswith("#")
                or lines[j].strip() in removable_labels
                or lines[j].strip() in uiflow_example_labels
            ):
                i = j + 1 if j < len(lines) and lines[j].strip() == "None" else j
                continue

        out.append(line)
        i += 1

    return "\n".join(out)


def remove_empty_uiflow_sections(md_text: str) -> str:
    labels = {"UIFLOW2:", "UiFlow2", "UIFLOW2", "UiFlow2 Example", "UIFLOW2 Example"}
    lines = md_text.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped in labels:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines) or lines[j].lstrip().startswith("#") or lines[j].lstrip().startswith("### `"):
                i += 1
                continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def rst_to_md(rst_text: str, current_rst_path: Optional[str] = None) -> str:
    lines = rst_heading_to_md(rst_text.splitlines())
    md: List[str] = []
    image_map: Dict[str, str] = {}
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        base_indent = leading_spaces(line)

        if not stripped:
            md.append("")
            i += 1
            continue

        if stripped == "..":
            _, i = collect_indented_block(lines, i + 1, base_indent)
            continue

        if stripped.startswith(".. include::"):
            match = re.match(r"\.\. include::\s*([^\s]+)", stripped)
            if match:
                image_map.update(parse_ref_file(os.path.basename(match.group(1))))
            i += 1
            continue

        code_match = CODE_BLOCK_RE.match(line)
        if code_match:
            language = code_match.group(1) or ""
            block, i = collect_indented_block(lines, i + 1, base_indent)
            append_code_block(md, block, language)
            continue

        if stripped.startswith(".. literalinclude::"):
            file_path = parse_literalinclude_directive(stripped)
            if file_path:
                code = read_example_code(file_path, current_rst_path).splitlines()
                append_code_block(md, code, "python")
            else:
                md.append(f"<!-- Invalid literalinclude directive: {stripped} -->")
            i += 1
            while i < len(lines) and lines[i].strip().startswith(":"):
                i += 1
            continue

        if stripped.startswith(".. autoclass::"):
            directive = parse_autoclass_directive(stripped)
            if directive:
                module_path, class_name = directive
                python_file = find_python_file(module_path)
                if python_file:
                    md.append(f"## `{class_name}`")
                    md.append(parse_python_docstring(python_file, class_name))
                else:
                    md.append(f"<!-- Failed to find Python file for module {module_path} -->")
            else:
                md.append(f"<!-- Invalid autoclass directive: {stripped} -->")
            i += 1
            while i < len(lines) and lines[i].strip().startswith(":"):
                i += 1
            continue

        signature = AUTODOC_SIGNATURE_RE.match(line)
        if signature:
            kind, sig = signature.groups()
            prefix = "class " if kind == "class" and not sig.startswith("class ") else ""
            md.append(f"### `{prefix}{convert_inline_rst(sig)}`")
            i += 1
            continue

        admonition = re.match(r"^\s*\.\.\s+(note|warning|important|tip|admonition)::\s*(.*)$", line, re.IGNORECASE)
        if admonition:
            kind, text = admonition.groups()
            body, i = collect_indented_block(lines, i + 1, base_indent)
            append_admonition(md, kind, convert_inline_rst(text), [convert_inline_rst(x) for x in body])
            continue

        version_marker = re.match(r"^\s*\.\.\s+(deprecated|versionadded|versionchanged)::\s*(.*)$", line, re.IGNORECASE)
        if version_marker:
            kind, text = version_marker.groups()
            label = {
                "deprecated": "Deprecated",
                "versionadded": "Version added",
                "versionchanged": "Version changed",
            }[kind.lower()]
            body, i = collect_indented_block(lines, i + 1, base_indent)
            append_admonition(md, label, convert_inline_rst(text), [convert_inline_rst(x) for x in body])
            continue

        if stripped.startswith(".. toctree::"):
            _, i = collect_indented_block(lines, i + 1, base_indent)
            continue

        if stripped.startswith((".. figure::", ".. image::")):
            body, i = collect_indented_block(lines, i + 1, base_indent)
            useful_body = [convert_inline_rst(x) for x in body if not x.strip().startswith(":")]
            if useful_body:
                md.extend(useful_body)
            continue

        if stripped.startswith((".. list-table::", ".. csv-table::")):
            i += 1
            continue

        if stripped.startswith((".. only::", ".. module::", ".. py:module::", ".. currentmodule::", ".. py:currentmodule::")):
            i += 1
            continue

        if stripped.startswith(".. table::"):
            i += 1
            continue

        if re.match(r"^\.\. (?:\|[^|]+\|\s+)?(?:\w+\s+)?unicode::", stripped):
            i += 1
            continue

        if stripped.startswith(".. .."):
            i += 1
            continue

        if re.match(r"^\.\. _[^:]+:$", stripped) or stripped.lower().startswith(".. sku:"):
            i += 1
            continue

        if stripped.startswith(".. "):
            md.append(f"<!-- {stripped} -->")
            i += 1
            continue

        field_line = convert_field_list_line(line)
        if field_line is not None:
            md.append(convert_inline_rst(field_line))
            i += 1
            continue

        if stripped.startswith(":"):
            i += 1
            continue

        if re.match(r"^\s*#\.\s+", line):
            md.append(re.sub(r"^(\s*)#\.\s+", r"\g<1>1. ", convert_inline_rst(line)))
            i += 1
            continue

        if re.match(r"^\s*[*\-+]\s+", line):
            md.append(re.sub(r"^(\s*)[*\-+]\s+", r"\g<1>- ", convert_inline_rst(line)))
            i += 1
            continue

        if line.rstrip().endswith("::"):
            label = line.rstrip()[:-2].rstrip()
            if label:
                md.append(convert_inline_rst(label + ":"))
            block, next_i = collect_indented_block(lines, i + 1, base_indent)
            if block:
                language = "python" if "python" in label.lower() else ""
                append_code_block(md, block, language)
                i = next_i
                continue

        md.append(convert_inline_rst(line))
        i += 1

    return cleanup_md_text("\n".join(md), image_map)


def convert_rst_to_md(src_path: str, dst_path: str) -> None:
    with open(src_path, encoding="utf-8") as f:
        rst_text = f.read()
    md_text = rst_to_md(rst_text, src_path)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md_text)


def main(dst_root: str = DST_ROOT) -> None:
    if os.path.exists(dst_root):
        shutil.rmtree(dst_root)
    os.makedirs(dst_root, exist_ok=True)

    for root, _, files in os.walk(SRC_ROOT):
        for filename in files:
            if not filename.endswith(".rst"):
                continue

            src_file = os.path.join(root, filename)
            with open(src_file, encoding="utf-8") as rf:
                content = rf.read()
            if len("".join(content.split())) < 20:
                continue
            if filename.lower() == "index.rst" and should_skip_index_rst(content):
                rel_path = os.path.relpath(src_file, SRC_ROOT)
                print(f"Skipped low-value overview: {rel_path}")
                continue

            rel_path = os.path.relpath(src_file, SRC_ROOT)
            rel_path_normalized = rel_path.replace(os.path.sep, "/")
            if rel_path_normalized in SKIP_RST_REL_PATHS:
                print(f"Skipped skill-irrelevant source: {rel_path}")
                continue
            if filename.lower() == "index.rst":
                rel_dir = os.path.dirname(rel_path)
                rel_out = os.path.join(rel_dir, "_overview.md") if rel_dir else "_overview.md"
            else:
                rel_out = rel_path[:-4] + ".md"

            dst_file = os.path.join(dst_root, rel_out)
            convert_rst_to_md(src_file, dst_file)
            print(f"Converted: {rel_path} -> {os.path.relpath(dst_file, dst_root)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert UIFlow2 Sphinx RST docs to Markdown.")
    parser.add_argument("--dst", default=DST_ROOT, help="Output docs directory.")
    args = parser.parse_args()
    main(args.dst)
