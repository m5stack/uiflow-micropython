# Rendering Strategy

这是 UIFlow2 显示任务的强制决策树。目标不是追求抽象层级，而是在可用固件上获得稳定、可读、可验证的画面。

## 先探测，再初始化

`m5ui` 只在部分控制器固件中随 manifest 冻结，且 `m5ui.init()` 会启动 LVGL
事件循环。因此先做轻量能力探测，不要无条件初始化：

```python
def probe_m5ui():
    try:
        import lvgl as lv
        import m5ui
        has_page = hasattr(m5ui, "M5Page")
        has_canvas = hasattr(m5ui, "M5Canvas")
        return lv, m5ui, has_page, has_canvas
    except (ImportError, AttributeError):
        return None, None, False, False
```

这段探测只确认模块和关键类是否可导入，不证明目标页面所需的每个控件、字体、
触摸驱动或 RAM 都可用。需要的 `M5Chart`、`M5TabView` 等类仍逐项检查，并以
[m5ui overview](../../uiflow2-coder/docs/m5ui/_overview.md) 和具体文档为准。

## 决策树

### Level 1: m5ui 原生控件

适用于多页、表单、按钮、列表、图表、触摸和有明确控件状态的界面。

1. `M5.begin()`。
2. `m5ui.init()` 一次。
3. 创建 `M5Page`。
4. 所有控件显式 `parent=page0`。
5. `page0.screen_load()`。
6. 主循环持续 `M5.update()`。

优点是 LVGL 负责对象树、事件、样式和部分刷新；缺点是需要 LVGL/m5ui
固件能力和额外内存。不要因为页面简单就混入 Widgets 或直接 M5.Lcd 绘图。

### Level 2: m5ui.M5Canvas

适用于自定义图形、仪表、图表装饰、图标、粒子和动画，同时仍需要 LVGL
页面、触摸控件或样式。

- 在同一个 `M5Page` 下创建 `M5Canvas`，不要把它当作 M5GFX Canvas。
- 固定大小、固定颜色格式和复用 buffer；不要每帧重新创建。
- 多个图元用 `begin_draw()`/`end_draw()` 批量提交。
- 复杂整帧可创建前后两个 LVGL Canvas，在新帧完成后切换 `lv.obj.FLAG.HIDDEN`。
- Canvas z-order 要低于需要点击的控件，或明确设置不可点击属性并在页面结构中验证。

`M5Canvas` 默认使用 ARGB8888，仍受 LVGL draw buffer 和目标内存限制。创建失败或运行掉帧时，减少
Canvas 区域、颜色格式、粒子数量和刷新频率；不要直接退回逐笔刷屏。

### Level 3: M5.Widgets

适用于没有 m5ui、没有 LVGL，或资源预算明确不足但仍需要少量标签/图片组件的设备。

- 使用 `M5.Widgets.Label`、`M5.Widgets.Image` 等已验证组件；它们默认直接绘制，
  不是 LVGL 控件，也不自动提供双缓冲。
- 静态背景用 `M5.Widgets.fillScreen()` 或父级显示对象初始化一次。
- 低频文本更新可以使用 Label；动画和多图元合成改用父级的 M5GFX Canvas，
  完成后一次 `push()`。不要把顶层 `widgets.Image(use_sprite=True)` 的行为套到
  `M5.Widgets.Image` 上。
- 不要创建 `m5ui.M5Page`，也不要将 Widgets 对象塞进 LVGL 页面。
- 先确认当前固件实际冻结了 `widgets` 包；不能仅凭产品名推断。

### Level 4: M5.Lcd/M5.Display + M5GFX Canvas

这是没有上层能力时的最后方案，不是默认方案。

- 单个像素、线、矩形或低频局部更新可以直接画。
- 多个操作组成一个视觉帧时，先创建一次 `M5.Lcd.newCanvas()`（或当前文档确认的
  `M5.Display.newCanvas()`），在 Canvas 上完成整帧，再一次 `push()`。
- Canvas 尺寸只覆盖动态区域；`bpp`、PSRAM 和 buffer 数量按目标内存估算。
- 背景、静态装饰和字体设置不要在循环中重复执行。
- `M5.Lcd` 与 `M5.Display` 的可用名称以当前官方文档和目标示例为准，不要在同一
  程序中未经确认地混用两个对象名。

## 选择失败时的降级

按以下顺序记录失败原因：

1. import 缺失：说明固件没有对应模块，降级到下一层。
2. 目标控件缺失：保留 m5ui 页面，改用已有控件或 m5ui Canvas；不要导入未确认的类。
3. buffer/RAM 不足：缩小区域、降低颜色深度、减小对象数量或改用局部刷新。
4. 帧率/触摸不稳定：降低刷新频率，拆分数据采样和绘制，检查事件循环和 `M5.update()`。
5. 视觉闪烁：先改为批量提交或离屏 Canvas，再考虑进一步减少脏区。

每次降级都要说明损失：样式、动画、触摸状态、字体、分辨率或刷新质量。不得把
“代码能运行”写成“视觉等价”。

## 最小验收表

- [ ] 目标固件对所选层级的 import 和关键类探测通过。
- [ ] 没有混用两个体系管理相同元素。
- [ ] 多步绘制不会把清屏和中间图元暴露给用户。
- [ ] Canvas/buffer 只创建一次，尺寸和颜色格式有预算。
- [ ] `M5.update()` 持续运行，数据、输入和绘制有界。
- [ ] 无真机画面时，闪烁、残影和触摸体验标记为 `NOT RUN` 或 `PARTIAL`。
