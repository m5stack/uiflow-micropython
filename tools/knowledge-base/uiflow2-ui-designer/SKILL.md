---
name: uiflow2-ui-designer
description: Design, generate, beautify, optimize, or review UIFlow2 interfaces, graphics, dashboards, gauges, animations, round-screen layouts, e-paper screens, and LED-matrix experiences for M5Stack devices. Use with uiflow2-coder when MicroPython API correctness or hardware compatibility matters; do not use for generic web, mobile, or desktop UI.
---

# UIFlow2 UI Designer

为 M5Stack UIFlow2 设备设计有明确视觉层级、交互反馈和性能边界的界面。既可以从零生成，也可以审查并优化现有 MicroPython UI。默认用中文说明，代码和 API 名保持英文。

本 skill 负责设计决策；相邻的 `uiflow2-coder` 负责官方 API 事实。不要复制 Web 端布局、CSS 动效或字体假设到嵌入式屏幕。

## 强制边界

- 先确认目标板卡、旋转后的宽高、屏幕形状、显示类型、输入方式和内容优先级。缺少信息但仍可合理推进时，明确假设；只有会导致 API 或布局路线错误时才追问。
- 一个界面只选一个主要渲染体系。默认按能力阶梯选择：`m5ui` 原生控件 → 同一 LVGL 页上的 `m5ui.M5Canvas` → `M5.Widgets` → `M5.Lcd`/`M5.Display` + M5GFX Canvas。不要因为熟悉底层接口就跳过上层方案。
- 写代码前读取相邻 coder skill 的官方资料。常用入口是 [m5ui overview](../uiflow2-coder/docs/m5ui/_overview.md)、[display](../uiflow2-coder/docs/hardware/display.md) 和 [Widgets overview](../uiflow2-coder/docs/widgets/_overview.md)。
- API、字体、控件参数或板卡支持范围无法从官方资料确认时，不要猜测。若相邻 coder skill 不存在，在仓库环境读取 `docs/source` 和 `m5stack/libs`；否则报告缺少依赖。
- `M5.update()` 必须持续执行。动画和传感器更新使用有界帧率、`time.ticks_ms()` 和 `time.ticks_diff()`，不阻塞事件处理。
- 不能仅凭代码或串口结果声称视觉 PASS。没有新鲜相机画面或人工实机观察时，视觉结果标记为 `NOT RUN` 或 `PARTIAL`。

## 工作流

1. 建立显示档案：板卡、旋转后尺寸、矩形/圆形、LCD/EPD/LED matrix、触摸/按键、可用 RAM/PSRAM 和语言字体。
2. 按 [rendering-strategy.md](references/rendering-strategy.md) 探测并选择渲染体系：
   - 有 `lvgl`、`m5ui.M5Page` 和所需控件时，优先用 m5ui 原生控件。
   - 需要自定义图形、图标、仪表或动画时，先在 m5ui 页面上使用 `m5ui.M5Canvas`；用 `begin_draw()`/`end_draw()` 或双 Canvas 组织整帧。
   - m5ui 缺失、目标固件未冻结 LVGL 或资源预算不允许时，再用 `M5.Widgets` 的轻量组件；它没有 LVGL 的布局、样式和事件体系。
   - 只有上述方案不可用，或目标是极简/像素级绘图时才使用 `M5.Lcd`/`M5.Display`。多步绘制必须使用复用的 `M5.Lcd.newCanvas()`，不能直接逐笔画到屏幕。
3. 定义一个清晰的视觉方向和最小 token 集：背景、表面、主色、文本、弱文本、状态色、间距、圆角、边框和字体层级。
4. 先规划静态布局、文本溢出和 normal/pressed/disabled/loading/empty/error/offline 状态，再添加有意义的动效。
5. 读取所需参考资料和官方 API 文档，生成或优化代码。优先复用对象、buffer 和布局计算，不在循环中创建页面或大对象。
6. 自查 API、刷新范围、帧率、内存、输入反馈和退化路径，并给出可观察的设备验收步骤。

## 参考资料路由

- 每个任务先读 [display-profiles.md](references/display-profiles.md) 和 [visual-system.md](references/visual-system.md)。
- 选择控件和图形能力时读 [api-patterns.md](references/api-patterns.md)。
- 涉及动画、转场、粒子、传感器驱动效果或闪烁时读 [motion-and-effects.md](references/motion-and-effects.md)。
- 需要常见页面结构或特殊显示形态时读 [layout-recipes.md](references/layout-recipes.md)。
- 审查或重写现有界面，以及交付前终检时读 [review-checklist.md](references/review-checklist.md)。

## 设计结果要求

- 层级一眼可辨：每屏一个主任务、一个主视觉焦点，次要信息明显降级。
- 坐标来自屏幕尺寸、边距、网格和文本测量，不靠大量无规律 magic numbers。
- 文本在真实字体下测量；长内容有换行、裁切、省略或滚动策略，不能覆盖相邻元素。
- 颜色不作为唯一状态信号；关键状态同时使用文字、图形、亮度、轮廓或运动变化。
- 交互控件有稳定尺寸和按压反馈；动画只解释状态变化，不持续抢占注意力。
- 静态元素只绘制一次；动态区域优先使用 LVGL 局部刷新或复用的离屏 Canvas。直接调用底层绘图时要证明不会暴露中间帧。
- 界面要有一个与用途匹配的设计概念，但装饰不能牺牲信息密度、可读性、功耗或帧率。

## 禁止清单

- 禁止混用不同 UI 体系管理同一批界面元素。
- 禁止照搬 HTML、CSS、Tailwind、SVG icon library、hover、cursor 或浏览器响应式规则。
- 禁止使用 emoji 充当图标；使用图形 primitive、像素图标或已验证的本地图片资源。
- 禁止假设所有 LVGL 字体、CJK 字体、触摸屏或 PSRAM 在所有板卡上可用。
- 禁止为了“高级感”堆叠渐变、阴影、描边和持续动画；每种效果必须有信息或交互目的。
- 禁止在主循环持续 `fillScreen()`、`clear()`、重新初始化控件或分配全屏 buffer。
- 禁止在 EPD 上设计连续动画，或在 16 x 16 matrix 上套用普通文本界面。

## 回答方式

用户要代码时先给可运行代码，再简要说明视觉方向、关键 token、查过的官方文档和验证步骤。用户要审查时先列 P0/P1/P2 问题和证据，再给最小修改建议。始终区分静态检查、运行通过和视觉实机验证。
