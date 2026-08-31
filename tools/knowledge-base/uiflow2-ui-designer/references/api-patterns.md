# UIFlow2 API Patterns

本文只记录设计层面的 API 选择。构造函数、参数、返回值和版本兼容性必须回到相邻 `uiflow2-coder` 的官方文档确认。

## 选择矩阵

| 需求 | 首选体系 | 依据与限制 |
| --- | --- | --- |
| 多页、触摸、控件状态、表单 | `m5ui` / LVGL 原生控件 | 首选。页面和控件有统一父对象；控件通常传 `parent=page0`。 |
| m5ui 页面上的自定义图形、仪表、动画 | 同一 LVGL 页面 + `m5ui.M5Canvas` | 第二选择。Canvas 与 m5ui 同一体系，可使用 LVGL 局部刷新、批量提交和双 Canvas。 |
| m5ui 不可用时的简单标签、图片和兼容旧程序 | `M5.Widgets` | 轻量组件层，底层基于 M5Unified/M5GFX；没有 LVGL 的布局、样式和完整事件体系。 |
| 没有可用上层组件的极简绘图或像素效果 | `M5.Lcd`/`M5.Display` + `newCanvas` | 最后兜底。直接绘制只适合单个小更新，多步帧必须离屏后一次 `push()`。 |

具体控件先读 [m5ui overview](../../uiflow2-coder/docs/m5ui/_overview.md) 和对应文档，例如 [button](../../uiflow2-coder/docs/m5ui/button.md)、[label](../../uiflow2-coder/docs/m5ui/label.md)、[canvas](../../uiflow2-coder/docs/m5ui/canvas.md)、[chart](../../uiflow2-coder/docs/m5ui/chart.md)。

## 语义组件优先

不要用标签和 Canvas 仿造已有控件。先按意图选择当前 m5ui 实际提供的组件，再读
对应文档确认构造参数、事件和样式。

| 意图 | 首选组件 |
| --- | --- |
| 标题、说明、只读短文字 | `M5Label` |
| 点击动作 | `M5Button` |
| 开/关 | `M5Switch` |
| 带勾选的布尔项 | `M5Checkbox` |
| 线性进度或非交互水平值 | `M5Bar` |
| 连续数值调节 | `M5Slider` |
| 精确步进数值 | `M5Spinbox` |
| 折叠选项或滚轮选项 | `M5Dropdown` / `M5Roller` |
| 无刻度环形值 | `M5Arc` |
| 带刻度、标签的仪表 | `M5Scale` |
| 趋势和序列数据 | `M5Chart` |
| 简单状态灯或加载 | `M5LED` / `M5Spinner` |
| 简单统一行、表格、日期 | `M5List` / `M5Table` / `M5Calendar` |
| 页面导航和分区 | `M5TabView` / `M5Menu` / `M5Win` |
| 对话与错误确认 | `M5Msgbox` |
| 编辑文字 | `M5TextArea` + 需要时的 `M5Keyboard` |
| 图片 | `M5Image` |
| 自定义图形或专用控件无法表达的动画 | `M5Canvas` |

- `M5Label` 是静态/只读文字和数值的兜底，不是默认的“万能组件”。按钮使用 `M5Button` 的
  `text`/`set_btn_text()`，不要再叠一个 label 模拟按钮标题。
- 带刻度速度表、温度表和压力表优先 `M5Scale`；只有不需要刻度/标签的环形进度才
  使用 `M5Arc`。
- `M5List` 适合 `add_text()`/`add_button()` 能表达的简单统一行。需要副标题、
  右侧开关、多个字段或不同行高时，不要假设存在 `M5Obj`：先查当前源码能否安全
  使用原生 `lv.obj`，否则改用已文档化的 table/menu/tab/page 结构，或用 Canvas
  画背景并把实际可交互控件放在上层。
- 自定义外观不能牺牲语义。Canvas 画出的“按钮”若需要点击，必须配合真实可点击
  控件或经过官方文档确认的触摸处理，不能只有视觉形状。

## M5.Widgets 的真实边界

`M5.Widgets` 不是另一套高级布局引擎。当前仓库的 `M5.Widgets` C 绑定
（`mpy_m5widgets.cpp`/`m5unified_widgets.c`）暴露 Label、Image、Line、Circle、
Triangle、Rectangle、QRCode 等轻量对象，并提供 `fillScreen`、`setRotation` 和
亮度辅助入口；对象默认使用 `M5.Display`，也可按文档把 display/canvas 作为 parent。
仓库另有顶层 Python `widgets` 包，不能把它和 `M5.Widgets` 的 C API 当成同一个接口。

- `M5.Widgets.Label.setText()` 会先擦除旧文本，再立即绘制新文本；适合低频状态值，
  不适合逐帧动画。
- `M5.Widgets.Image` 默认直接解码并绘制到 parent；它不会因为使用 `M5.Widgets`
  就自动获得双缓冲。要稳定更新，显式将它挂到已创建的 M5GFX Canvas，或直接在
  Canvas 上完成整帧后一次 `push()`。
- 顶层 Python `widgets.Image(use_sprite=True)` 的 sprite 行为只适用于该包的实现，
  不能据此推断 `M5.Widgets.Image` 具备相同能力。
- `Widgets.fillRect()`、`Widgets.drawRect()` 不是合法绘图调用；矩形等底层图形仍由
  `M5.Lcd`/`M5.Display` 提供。
- Widgets 对象的父级是 M5GFX display 或 canvas，不要和 `m5ui.M5Page`、LVGL
  控件混用管理同一界面。

## M5.Lcd 图形底座

官方 [display API](../../uiflow2-coder/docs/hardware/display.md) 提供 `fillScreen`、`fillRect`、`fillRoundRect`、`fillCircle`、`fillEllipse`、`drawLine`、`drawArc`、`drawTriangle`、`drawImage`、文本测量和 `newCanvas` 等能力。

- 背景、静态框架和装饰在初始化或页面切换时绘制一次。
- 动态图元优先擦除旧区域后重绘；重绘底层后要补画被覆盖的上层。
- 多个图元组成一帧时创建一个可复用 Canvas，完成后用一次 `push(x, y)` 呈现，减少撕裂和闪烁。此处的 Canvas 是 M5GFX Canvas，不是 `m5ui.M5Canvas`。
- 绘图 API 的颜色按文档使用 RGB888；不要把 LVGL `lv.color_hex()` 对象传给 `M5.Lcd`。
- 文本使用 `setFont`、`textWidth`、`fontHeight` 和 `drawString` 组合；不要凭字符数量估算宽度。
- `startWrite()`/`endWrite()` 只在官方 API 和目标驱动支持时使用，批量绘制也不能阻塞事件循环。

## M5UI / LVGL 样式

`m5ui` 是 UIFlow2 对 LVGL 9.3 的 MicroPython 封装。当前仓库的 `m5ui/manifest.py`
冻结完整模块集合，但只有包含该 manifest 的板卡固件才可导入；当前 overview 列出的
支持控制器包括 Core2、CoreS3、Dial、StackChan、StopWatch、Tab5/Tab5X、Tough
和 ToughC5。实际目标仍必须通过导入探测确认。

`m5ui` 包装器和 LVGL 对象支持背景色、渐变背景、透明度、圆角、边框、文本颜色、阴影和部分 transition。常见设计调用包括：

```python
button.set_style_radius(8, lv.PART.MAIN)
button.set_bg_color(lv.color_hex(COLOR_PRIMARY), lv.OPA.COVER, lv.PART.MAIN)
button.set_style_text_color(lv.color_hex(COLOR_TEXT), lv.PART.MAIN)
```

上面的调用只展示设计意图；方法签名必须以当前 `m5ui` 文档为准。不要假设所有控件都拥有相同的 `set_*` 包装器。

- 背景渐变只用来表达层级或方向，不要让文字落在复杂渐变上。
- 阴影用低不透明度和小偏移表达浮层关系；数据面板通常不需要阴影。
- 圆角和边框在同一页面保持少量档位，避免每个控件一个半径。
- 过渡用于 pressed/selected 等离散状态，不用于每帧写入动画属性。
- 控件需要 `parent=page0` 时必须显式传递；否则页面切换后可能不可见。

## Part、State 与默认样式

- 先设置页面背景，再检查每个可见控件的构造默认色。当前源码中 button/bar/list/
  chart/checkbox/canvas 等带有蓝、白或浅灰默认值，主题页不能只改 page。
- 样式只能作用于当前控件文档或源码确认的 part/state。`lv.PART.MAIN`、
  `INDICATOR`、`KNOB`、`ITEMS`、`TICKS` 不是所有组件都支持的通用集合。
- normal、pressed、checked、selected、focused、disabled 分别核对。不要为了按压
  反馈改变组件宽高并引发布局位移。
- `M5Arc`、`M5Scale`、`M5Spinner` 和透明 label/canvas 等叠加元素要检查背板是否
  与父级协调；透明度和背景 API 必须来自当前版本事实。
- 普通 page、dashboard、header、footer 和静态分组不应意外滚动。只有在当前源码/
  文档确认 `SCROLLABLE` flag 或 scrollbar part 的情况下修改滚动行为。

## M5Canvas 图形组合

[M5Canvas 文档](../../uiflow2-coder/docs/m5ui/canvas.md) 的 `begin_draw()`/`end_draw()`、`fill_bg()`、`draw_rect()`、`draw_line()`、`draw_arc()`、`draw_label()` 和 `draw_image()` 适合把一组图元组成一个局部画面。

- 在 `begin_draw()` 和 `end_draw()` 之间完成一帧；不要在同一帧中频繁提交。
- 高速动画可准备前后两个 LVGL Canvas，先完成后一个，再切换 `HIDDEN` 标志，避免露出空白帧。可参考 [hourglass sample](../../uiflow2-coder/assets/examples/m5ui/hourglass_320x240.py)。
- `lv.draw_buf_create()` 的颜色格式和 buffer 数量应按目标 RAM/PSRAM 验算；不要默认双全屏 RGB565 总能分配。
- 静态 m5ui 控件和动态 Canvas 要有明确 z-order，Canvas 不应遮住必须接收触摸的控件。
- `m5ui.init()` 会初始化 LVGL 显示、触摸读取和定时事件循环；只在确认采用 m5ui 后调用一次。`import m5ui` 本身不等于已经初始化。
- `M5Canvas` 默认颜色格式是 ARGB8888；全屏或双 Canvas 在弱设备上可能很贵。只有
  在确认内存余量后才选择更高颜色深度，优先局部 Canvas 或文档确认的 RGB565。

## 图表与数据

`m5ui.M5Chart` 适合有坐标轴和多序列语义的数据；读 [chart 文档](../../uiflow2-coder/docs/m5ui/chart.md) 确认 series、范围和追加方式。

- 图表只显示支持决策的趋势；小屏优先最新值、方向和阈值，不要塞完整图例。
- 数据更新优先追加或局部改变，不要每次重新创建 chart、series 或全部控件。
- 真实数据为空、过期或请求失败时分别显示 empty、stale、offline 状态。

## 输入与事件

- m5ui 事件回调只修改轻量状态或置位请求标志；网络、文件和大计算放在主循环的有界阶段。
- 按钮和触摸区域使用固定尺寸，视觉边界和命中区域都要可解释。
- 回调中不要重新初始化页面、创建大 buffer、长时间 `sleep` 或持续打印日志。
- 具体事件过滤器和回调签名以控件文档为准，不凭其他 LVGL 版本猜测。

## 闪烁诊断

- 逐笔 `M5.Lcd`/`M5.Display` 绘制时，清除和重画的中间状态会直接出现在屏幕上；这是典型闪烁来源。
- m5ui 控件更新通常由 LVGL 的部分刷新合并提交，但在 Canvas 上连续调用绘图 API 仍应包在 `begin_draw()`/`end_draw()` 中。
- M5GFX Canvas 也不是自动双缓冲；必须复用同一 Canvas、先完成整帧再一次 `push()`。复杂整帧再考虑双 Canvas。
- 若闪烁仍存在，先减小脏区、降低帧率和合并更新，再检查是否有多个路径同时刷新同一区域；不要用更快的 `sleep` 掩盖问题。
