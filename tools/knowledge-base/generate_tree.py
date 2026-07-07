from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
TARGET_DIR = SCRIPT_DIR / "uiflow2-docs"
OUTPUT_FILE = SCRIPT_DIR / "file_tree.txt"

def generate_tree(directory, prefix="", is_last=True, stats=None):
    """递归生成目录树结构"""
    if stats is None:
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'file_types': defaultdict(int),
            'total_size': 0
        }

    lines = []
    path = Path(directory)

    if not path.exists():
        return ["目录不存在"], stats

    # 获取所有项目并排序（目录在前，文件在后）
    try:
        items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    except PermissionError:
        return [f"{prefix}[权限拒绝]"], stats

    for index, item in enumerate(items):
        is_last_item = index == len(items) - 1

        # 构建树形符号
        if is_last:
            current_prefix = prefix + "└── "
            next_prefix = prefix + "    "
        else:
            current_prefix = prefix + "├── "
            next_prefix = prefix + "│   "

        if item.is_dir():
            stats['total_dirs'] += 1
            lines.append(f"{current_prefix}{item.name}/")
            # 递归处理子目录
            sub_lines, stats = generate_tree(item, next_prefix, is_last_item, stats)
            lines.extend(sub_lines)
        else:
            stats['total_files'] += 1
            # 统计文件类型
            ext = item.suffix.lower() if item.suffix else '[无扩展名]'
            stats['file_types'][ext] += 1
            # 统计文件大小
            try:
                file_size = item.stat().st_size
                stats['total_size'] += file_size
            except:
                pass

            lines.append(f"{current_prefix}{item.name}")

    return lines, stats

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def main():
    print(f"Scanning directory: {TARGET_DIR}")
    print("生成文件树中...")

    # 生成树形结构
    stats = {
        'total_files': 0,
        'total_dirs': 0,
        'file_types': defaultdict(int),
        'total_size': 0
    }

    tree_lines = [f"{TARGET_DIR.name}/"]
    sub_lines, stats = generate_tree(TARGET_DIR, "", True, stats)
    tree_lines.extend(sub_lines)

    # 生成统计信息
    stats_lines = [
        "\n" + "="*60,
        "统计信息",
        "="*60,
        f"总目录数: {stats['total_dirs']}",
        f"总文件数: {stats['total_files']}",
        f"总大小: {format_size(stats['total_size'])}",
        "\n文件类型分布:",
        "-"*60
    ]

    # 按文件数量排序文件类型
    sorted_types = sorted(stats['file_types'].items(), key=lambda x: x[1], reverse=True)
    for ext, count in sorted_types:
        percentage = (count / stats['total_files'] * 100) if stats['total_files'] > 0 else 0
        stats_lines.append(f"  {ext:20s}: {count:5d} 个 ({percentage:5.2f}%)")

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(tree_lines))
        f.write('\n'.join(stats_lines))

    print(f"\n文件树已保存到: {OUTPUT_FILE}")
    print("\n" + "="*60)
    print("统计信息")
    print("="*60)
    print(f"总目录数: {stats['total_dirs']}")
    print(f"总文件数: {stats['total_files']}")
    print(f"总大小: {format_size(stats['total_size'])}")
    print("\n文件类型分布 (Top 10):")
    print("-"*60)
    for ext, count in sorted_types[:10]:
        percentage = (count / stats['total_files'] * 100) if stats['total_files'] > 0 else 0
        print(f"  {ext:20s}: {count:5d} 个 ({percentage:5.2f}%)")

    if len(sorted_types) > 10:
        print(f"  ... 还有 {len(sorted_types) - 10} 种文件类型")

if __name__ == "__main__":
    main()
