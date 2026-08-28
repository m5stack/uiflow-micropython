# AGENTS.md

本目录负责维护 `uiflow2-coder` 和 `uiflow2-ui-designer` 两个 UIFlow2 skill：
前者生成/同步官方 API `docs`、`SKILL.md` 内嵌索引和辅助描述文件，后者维护
面向 UI 设计、动效和视觉审查的规则与参考资料。

## 目标

- 源头：`D:\git\uiflow_micropython\docs\source` 和 `D:\git\uiflow_micropython\m5stack\libs`。
- 本地 skill 副本：`D:\git\uiflow_micropython\tools\knowledge-base\uiflow2-coder`。
- 实际生效 skill：`C:\Users\15515\.agents\skills\uiflow2-coder`。
- UI 设计 skill 源：`D:\git\uiflow_micropython\tools\knowledge-base\uiflow2-ui-designer`。
- UI 设计 skill 实际生效目录：`C:\Users\15515\.agents\skills\uiflow2-ui-designer`。
- 不再保留独立的 `tools\knowledge-base\uiflow2-docs` 中间产物；脚本用临时目录生成后直接同步到 skill。

## UIFlow2 UI Designer 更新

`uiflow2-ui-designer` 是 `uiflow2-coder` 的独立伴生 skill。它不复制官方
API 文档，不修改 coder 的行为；API 事实继续以 coder 的 `docs/` 和当前仓库
`m5stack/libs` 为准。设计资料按渐进式参考维护在 `references/`：

- `display-profiles.md`：LCD、小屏、圆屏、EPD、16 x 16 LED Matrix 的分流约束。
- `visual-system.md`：视觉 token、字体、层级、文本和交互状态。
- `api-patterns.md`：`m5ui`、`M5.Widgets`、`M5.Lcd` 和 Canvas 的选择。
- `rendering-strategy.md`：m5ui → m5ui Canvas → Widgets → M5.Lcd Canvas 的能力探测和降级决策。
- `motion-and-effects.md`：帧率、状态机、局部重绘、双缓冲和内存预算。
- `layout-recipes.md`：仪表盘、列表、状态页、圆屏、EPD 和 Matrix 版式。
- `review-checklist.md`：设备、视觉、交互、性能和验证审查清单。

在仓库根目录同步并校验 UI 设计 skill：

```powershell
python tools\knowledge-base\sync_uiflow2_ui_designer.py
```

只读验证已安装副本和仓库副本：

```powershell
python tools\knowledge-base\sync_uiflow2_ui_designer.py --check-only
```

脚本会先校验仓库副本，再同步到系统目录，检查 UTF-8 无 BOM、Markdown
相对链接、Python fenced code、官方 `quick_validate.py` 和逐文件字节一致性。
若已安装副本与仓库副本存在差异，默认拒绝覆盖；确认差异来自旧版本后才使用
`--force`。同步和校验均不执行烧录、擦除、推送或其他设备操作。

## 标准更新流程

在仓库根目录运行：

```powershell
python tools\knowledge-base\sync_uiflow2_skill.py
```

`sync_uiflow2_skill.py` 会：

1. 先把系统里的 `uiflow2-coder` skill 复制到本目录的 `uiflow2-coder` 副本。
2. 在临时目录中从 `docs\source` 生成最新 Markdown。
3. 批量同步到系统 skill 和本地副本的 `docs` 目录。
4. 生成 skill 根目录的紧凑 `file_tree.txt`。
5. 刷新 `SKILL.md` 内的 `BEGIN_DOC_TREE` / `END_DOC_TREE` 紧凑索引。
6. 按 `complex_examples.json` 精选清单，将仓库中的复杂示例同步到 skill 的 `assets\examples`，并生成 `references\complex-examples.md` 索引。
7. 最后把本地 skill 副本整体复制到系统 skill，确保脚本、`SKILL.md`、`file_tree.txt`、`docs`、`references` 和 `assets` 字节一致。

如果正在修改本目录中的 `SKILL.md`、`scripts` 或生成脚本，不要让旧系统 skill 反向覆盖仓库副本，改用：

```powershell
python tools\knowledge-base\sync_uiflow2_skill.py --skip-copy-shell
```

如需使用已有生成目录，可显式指定：

```powershell
python tools\knowledge-base\sync_uiflow2_skill.py --source-docs C:\path\to\docs
```

## 维护规则

- 不要手动编辑 skill 的 `docs` 目录；要改内容，优先改 `docs\source` 或转换脚本。
- 复杂示例的唯一源码放在仓库 `examples\` 对应 UI 体系或功能目录；不要手动维护 `assets\examples` 镜像。通用 UI 示例优先按 UI 体系和屏幕分辨率分类，不要无必要地绑定主机名称。只有经开发者确认适合作为标准参考的示例才能登记到 `complex_examples.json`，并且要如实填写硬件验证状态。
- 只有包含实质性整体指导的 `index.rst` 会转换为 `_overview.md`；纯 `toctree` 目录页不要生成 overview，因为文件树已经覆盖导航信息。
- `SKILL.md` 内嵌索引统一省略 `.md` 后缀，例如 `unit/env` 表示 `docs/unit/env.md`。
- `file_tree.txt` 保留在 skill 根目录，只作为外部工具、人工 diff 和脚本验证的冗余索引。
- 生成器会解析常见 RST 标题、代码块、autodoc API 签名、字段列表和简单 Python class alias；不要把这些内容退回到 HTML 注释形式。
- 生成器会删除 UIFlow/Blockly 可视化积木残留、`.m5f2` 工程引用、纯导航/截图占位和空示例输出；skill 面向 MicroPython 编程，保留 MicroPython 示例、API、返回值和兼容性信息。
- 生成的 Markdown 要去掉尾随空白、多余 EOF 空行，并保持 UTF-8。
- `contribute/template.rst` 这类面向文档贡献者的模板不进入 skill；skill 只保留对 UIFlow2 编码有用的资料。

## 验证清单

```powershell
python -m py_compile tools\knowledge-base\rst2md_en.py tools\knowledge-base\generate_tree.py tools\knowledge-base\sync_uiflow2_skill.py
git diff --check -- tools\knowledge-base
python -X utf8 C:\Users\15515\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\15515\.agents\skills\uiflow2-coder
python -X utf8 C:\Users\15515\.codex\skills\.system\skill-creator\scripts\quick_validate.py tools\knowledge-base\uiflow2-coder
python -X utf8 C:\Users\15515\.codex\skills\.system\skill-creator\scripts\quick_validate.py tools\knowledge-base\uiflow2-ui-designer
python -X utf8 C:\Users\15515\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\15515\.agents\skills\uiflow2-ui-designer
```

还要用 Python 检查：

- 所有 `.md` 可用 `encoding="utf-8"` 解码。
- 没有 `U+FFFD` replacement character。
- skill 文档中没有本机绝对路径残留。
- 系统 skill 和本地副本内容一致。
- `uiflow2-ui-designer` 仓库副本和系统副本逐文件字节一致。
- 两个 skill 之间的官方文档相对链接可解析，设计 skill 的 Python fenced code 可解析。
- 生成质量计数应为 0：`Failed to find`、`<!-- ..`、裸 `:param`/`:returns:`/`:rtype:`、裸 `.. code-block::`、RST 显式链接和裸 `:meth:`/`:class:`/`:ref:` 角色。
- 低价值 UIFlow/Blockly 残留计数应为 0：`UiFlow2 Code Block:`、`MicroPython Code Block:`、`UiFlow2 Example:`、`.m5f2`。

## Windows 编码注意

- 写中文文件优先用 `apply_patch` 或明确 UTF-8 的 Python 脚本。
- 不要用 PowerShell here-string/stdin 管道写大段中文到文件。
- 写完中文文件后用 Python 读取原始字节，确认 UTF-8 可解码且没有异常 `?` 或 `U+FFFD`。
