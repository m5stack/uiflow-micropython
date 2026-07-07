import os
import re
import ast
import shutil
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SRC_ROOT = os.path.join(REPO_ROOT, 'docs', 'source')
DST_ROOT = os.path.join(SCRIPT_DIR, 'uiflow2-docs')
PYTHON_ROOT = os.path.join(REPO_ROOT, 'm5stack', 'libs')
REFS_DIR = os.path.join(SRC_ROOT, 'refs')
IMAGE_EXT_PATTERN = r'(?:png|jpg|jpeg|gif|webp|bmp|svg)'

def parse_python_docstring(python_file: str, class_name: str) -> str:
    """
    解析 Python 文件中指定类的文档字符串和方法文档
    """
    with open(python_file, encoding='utf-8') as f:
        python_code = f.read()

    tree = ast.parse(python_code)

    class_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            class_node = node
            break

    if not class_node:
        return f"<!-- Failed to find class {class_name} in {python_file} -->"

    md = []

    # 添加类的文档字符串
    if class_node.body and isinstance(class_node.body[0], ast.Expr) and isinstance(class_node.body[0].value, ast.Str):
        md.append(ast.get_docstring(class_node, clean=True))
        md.append("")

    # 提取方法
    for node in class_node.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
            md.append(f"### `{node.name}`")
            docstring = ast.get_docstring(node, clean=True)
            if docstring:
                md.append(docstring)
            md.append("")

    return "\n".join(md)


def find_python_file(module_path: str) -> Optional[str]:
    """
    将模块路径转换为文件路径
    """
    # 将模块路径从 software.easysocket.tcp_server 转换为 m5stack/libs/software/easysocket/tcp_server.py
    relative_path = module_path.replace('.', os.path.sep)
    python_file = os.path.join(PYTHON_ROOT, relative_path + '.py')

    if os.path.exists(python_file):
        return python_file

    return None


def parse_autoclass_directive(directive_line: str) -> Optional[Tuple[str, str]]:
    """
    解析 .. autoclass:: 指令，提取模块和类名
    """
    match = re.match(r'\.\. autoclass::\s*([^\s:]+)', directive_line.strip())
    if match:
        full_path = match.group(1)
        parts = full_path.split('.')
        class_name = parts[-1]
        module_path = '.'.join(parts[:-1])
        return module_path, class_name

    return None


def rst_heading_to_md(lines):
    """
    将 reStructuredText 标题转换为 markdown 标题
    """
    md_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检查下一个非空行是否为下划线式标题
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            if re.match(r'^[=~\-\^"`#\*\+]{3,}$', next_line.strip()) and len(next_line.strip()) >= len(line.strip()):
                level_map = {
                    '=': '#',
                    '-': '##',
                    '~': '###',
                    '^': '####',
                    '"': '#####',
                    '`': '######',
                    '#': '######',
                    '*': '######',
                    '+': '######',
                }
                ch = next_line.strip()[0]
                md_level = level_map.get(ch, '#')
                md_lines.append(f"{md_level} {line.strip()}\n")
                i += 2
                continue
        md_lines.append(line)
        i += 1
    return md_lines

def parse_ref_file(ref_filename: str) -> Dict[str, str]:
    """
    解析 ref 文件，提取图片定义（|image.png| image:: url）
    """
    image_map = {}
    ref_path = os.path.join(REFS_DIR, ref_filename)
    if os.path.exists(ref_path):
        with open(ref_path, encoding='utf-8') as f:
            ref_content = f.read()
            # 匹配图片定义：.. |filename.png| image:: url
            pattern = re.compile(r'\.\. \|([^\|]+)\| image::\s*([^\n]+)')
            matches = pattern.findall(ref_content)
            for filename, url in matches:
                image_map[filename.strip()] = url.strip()
    return image_map


def parse_literalinclude_directive(directive_line: str) -> Optional[Dict]:
    """
    解析 .. literalinclude:: 指令，提取文件路径和参数
    """
    match = re.match(r'\.\. literalinclude::\s*([^\s]+)', directive_line.strip())
    if match:
        file_path = match.group(1)
        params = {
            'language': 'python',
            'linenos': False
        }

        return {
            'file_path': file_path,
            'params': params
        }

    return None


def read_example_code(file_path: str, current_rst_path: Optional[str] = None) -> str:
    """
    读取示例代码文件内容
    """
    # 尝试 1: 相对于当前运行目录的绝对路径
    abs_file_path = os.path.abspath(file_path)
    if os.path.exists(abs_file_path):
        with open(abs_file_path, encoding='utf-8') as f:
            return f.read()

    # 尝试 2: 从项目根目录开始查找
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    candidate_path = os.path.join(project_root, file_path.lstrip('.').lstrip(os.path.sep))
    if os.path.exists(candidate_path):
        with open(candidate_path, encoding='utf-8') as f:
            return f.read()

    # 尝试 3: 相对于 rst 文件所在目录的路径（如果提供了 rst 文件路径）
    if current_rst_path:
        rst_dir = os.path.dirname(current_rst_path)
        relative_to_rst = os.path.join(rst_dir, file_path)
        abs_from_rst = os.path.abspath(relative_to_rst)
        if os.path.exists(abs_from_rst):
            with open(abs_from_rst, encoding='utf-8') as f:
                return f.read()

    # 所有尝试都失败
    return f"<!-- Failed to find example file: {file_path} -->"


def cleanup_md_text(md_text: str, image_map: Dict[str, str]) -> str:
    """Remove image placeholders and bytes that make generated Markdown binary."""
    md_text = re.sub(r'!\[[^\]]*\]\([^\)]+\)', '', md_text)
    md_text = re.sub(r'[\[\]]\s*[^\n\[\]]+\.' + IMAGE_EXT_PATTERN + r'\s*[\[\]|]?', '', md_text, flags=re.IGNORECASE)
    md_text = re.sub(r'[\[\]]\s*[^\n\[\]]+\.' + IMAGE_EXT_PATTERN + r'\s*(?=$|\n)', '', md_text, flags=re.IGNORECASE)
    for filename in image_map.keys():
        md_text = md_text.replace(f'[{filename}]', '')
        md_text = md_text.replace(f']{filename}[', '')
        md_text = md_text.replace(f']{filename}|', '')
    md_text = ''.join(ch for ch in md_text if ch in '\n\r\t' or ord(ch) >= 32)
    return re.sub(r'\n\s*\n\s*\n+', '\n\n', md_text)

def rst_to_md(rst_text, current_rst_path=None):
    """
    简单 rst 转 md
    """
    lines = rst_text.splitlines()
    # 标题转换
    lines = rst_heading_to_md(lines)
    md = []
    in_code = False
    i = 0
    image_map = {}

    while i < len(lines):
        line = lines[i]
        # 代码块
        if line.strip().startswith('::'):
            in_code = True
            md.append('```')
            i += 1
            continue
        if in_code:
            if line.strip() == '':
                in_code = False
                md.append('```')
            else:
                md.append(line)
            i += 1
            continue
        # 列表
        if re.match(r'^\s*[\*\-\+]\s+', line):
            md.append(re.sub(r'^(\s*)[\*\-\+]\s+', r'\1- ', line))
            i += 1
            continue
        # 有序列表
        if re.match(r'^\s*\d+\.\s+', line):
            md.append(line)
            i += 1
            continue
        # 处理 autoclass 指令
        if line.strip().startswith('.. autoclass::'):
            directive = parse_autoclass_directive(line)
            if directive:
                module_path, class_name = directive
                python_file = find_python_file(module_path)
                if python_file:
                    md.append(f"## {class_name}")
                    doc_content = parse_python_docstring(python_file, class_name)
                    md.append(doc_content)
                else:
                    md.append(f"<!-- Failed to find Python file for module {module_path} -->")
            else:
                md.append(f"<!-- Invalid autoclass directive: {line.strip()} -->")
            i += 1
            # 跳过 :members: 等参数
            while i < len(lines) and lines[i].strip().startswith(':'):
                i += 1
            continue
        # 处理 literalinclude 指令
        if line.strip().startswith('.. literalinclude::'):
            directive = parse_literalinclude_directive(line)
            if directive:
                file_path = directive['file_path']
                params = directive['params']

                # 读取代码内容
                code_content = read_example_code(file_path, current_rst_path)

                # 添加代码块
                md.append(f"```python")
                md.append(code_content)
                md.append("```")
            else:
                md.append(f"<!-- Invalid literalinclude directive: {line.strip()} -->")

            i += 1
            # 跳过参数行
            while i < len(lines) and lines[i].strip().startswith(':'):
                i += 1
            continue
        # 处理 include 指令（解析 ref 文件）
        if line.strip().startswith('.. include::'):
            match = re.match(r'\.\. include::\s*([^\s]+)', line.strip())
            if match:
                include_path = match.group(1)
                # 提取 ref 文件名
                ref_filename = os.path.basename(include_path)
                # 解析 ref 文件中的图片定义
                image_map.update(parse_ref_file(ref_filename))
            md.append(f'<!-- {line.strip()} -->')
            i += 1
            continue
        # 其他块引用
        if line.strip().startswith('.. '):
            md.append(f'<!-- {line.strip()} -->')
            i += 1
            continue
        # 其他
        md.append(line)
        i += 1

    # 结尾补全代码块
    if in_code:
        md.append('```')

    md_text = '\n'.join(md)

    # Clean common rst syntax leftovers
    md_text = re.sub(r'\s*:members:\s*', '', md_text)
    md_text = re.sub(r'\|([^\|\n]+\.' + IMAGE_EXT_PATTERN + r')\|', r'[\1]', md_text, flags=re.IGNORECASE)
    md_text = cleanup_md_text(md_text, image_map)

    return md_text

def convert_rst_to_md(src_path, dst_path):
    with open(src_path, encoding='utf-8') as f:
        rst_text = f.read()
    md_text = rst_to_md(rst_text, src_path)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(md_text)

def main():
    if os.path.exists(DST_ROOT):
        shutil.rmtree(DST_ROOT)
    os.makedirs(DST_ROOT, exist_ok=True)

    for root, _, files in os.walk(SRC_ROOT):
        for f in files:
            if f.endswith('.rst') and f.lower() != 'index.rst':
                src_file = os.path.join(root, f)
                # 跳过内容少于20字符的文件
                with open(src_file, encoding='utf-8') as rf:
                    content = rf.read()
                if len(''.join(content.split())) < 20:
                    continue
                rel_path = os.path.relpath(src_file, SRC_ROOT)
                dst_file = os.path.join(DST_ROOT, rel_path).replace('.rst', '.md')
                convert_rst_to_md(src_file, dst_file)
                print(f"Converted: {rel_path} -> {os.path.relpath(dst_file, DST_ROOT)}")

if __name__ == '__main__':
    main()
