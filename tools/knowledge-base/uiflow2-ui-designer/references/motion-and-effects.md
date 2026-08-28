# Motion And Effects

动效的目标是说明状态、方向和因果。嵌入式屏幕上的高级感来自节奏、层级和稳定，而不是效果数量。

## 动效预算

开始前写下三个预算：

- **刷新预算**：普通数据动画从 20 到 30 FPS 起步；复杂 Canvas、网络仪表或小屏从 10 到 20 FPS 起步；EPD 只做事件触发刷新；矩阵从 8 到 15 FPS 起步。
- **计算预算**：一帧只处理有限数量的粒子、点或路径；传感器采样、网络请求和绘制分阶段执行。
- **内存预算**：按 `width * height * bytes_per_pixel` 估算 Canvas，再加双缓冲、LVGL、Python 和业务对象；无法证明余量时改用局部区域或单缓冲。

这些是起始值，不是真机性能保证。验收时报告实际帧间隔、掉帧、残影、功耗和温升观察结果。

## 状态机优先

把动效绑定到少量状态，而不是在循环中散落条件：

```python
STATE_IDLE = 0
STATE_LOADING = 1
STATE_READY = 2
STATE_ERROR = 3

state = STATE_IDLE
transition_started_ms = 0
```

- 状态切换时记录开始时间；循环只根据 `ticks_ms` 计算当前进度。
- 每个状态有进入、持续、退出策略；错误和离线状态不能被成功动画覆盖。
- 同一视觉属性不要同时由回调、传感器和主循环写入。

## 时间与缓动

使用单调 tick 计算进度，处理 tick 回绕：

```python
elapsed = time.ticks_diff(time.ticks_ms(), started_ms)
progress = min(1.0, max(0.0, elapsed / duration_ms))
```

常用轻量缓动：

- `ease_out`: `1 - (1 - t) * (1 - t)`，适合元素进入。
- `ease_in_out`: 前半段慢、后半段慢，适合页面转场。
- `smoothstep`: `t * t * (3 - 2 * t)`，适合仪表值和渐变。
- 线性插值只适合进度、扫描和持续匀速运动。

不要在每帧调用浮点三角函数、指数函数或创建临时大列表，除非预算和目标固件已经验证。

## LCD 动画模式

### 局部重绘

记录动态元素的旧矩形和新矩形，合并为最小脏区；先恢复背景，再画新状态。动态数字、进度条、指针和状态点通常不需要整屏刷新。

### 单 Canvas

适合少量图元和中等帧率。m5ui 页面优先使用 `m5ui.M5Canvas` 的
`begin_draw()`/`end_draw()`；没有 m5ui 时使用 M5GFX Canvas，循环中绘制后
一次 `push()`。两种 Canvas 都不要在循环里反复创建。

### 双 Canvas

适合复杂整帧动画或 LVGL Canvas。后缓冲先完成一帧，再切换隐藏标志或一次呈现；任何时候都不要展示尚未画完的 buffer。可参考 [hourglass LVGL sample](../../uiflow2-coder/assets/examples/m5ui/hourglass_320x240.py)。

### 控件 transition

按钮 pressed、selected、展开/收起等有限状态可使用 m5ui/LVGL transition。不要用控件 transition 驱动高频粒子或逐帧数据。

## 视觉效果配方

- **呼吸**：只改变状态点或高光的不透明度，周期 1.5 到 3 秒；错误和 EPD 禁用。
- **数值过渡**：在 150 到 400 ms 内平滑插值，保留最终值和单位位置；数据刷新频繁时合并更新。
- **进度弧**：背景弧固定，前景弧代表值；阈值同时改变颜色和文字。
- **扫描线/波形**：用于等待、音频或传感器可视化，限制线数和移动区域；不可遮挡读数。
- **粒子**：预分配固定粒子数组，限制粒子数、寿命和活动区域；不要每帧 append/remove 大量对象。
- **按压反馈**：轻微亮度、边框、阴影或 1 到 2 px 位移；控件尺寸和布局不改变。

## 传感器驱动

- 先滤波和限幅，再把传感器值映射到角度、位移或速度，避免抖动直接进入 UI。
- 传感器采样频率可以高于绘制频率；用最新样本而不是积压全部样本。
- 输入异常或读取失败时保留最后稳定画面，并显示 stale/error，而不是让图形跳到随机位置。

## EPD 与 Matrix 特例

- EPD：只做页面级、事件级或聚合后的刷新；使用文档确认的 `setEpdMode()`，不做连续过渡。
- Matrix：把动效拆成像素关键帧，优先轮廓、方向和节奏；避免亚像素、渐变阴影和长文本滚动。

## 主循环骨架

```python
def loop():
    M5.update()
    now = time.ticks_ms()
    if time.ticks_diff(now, last_frame_ms) < FRAME_INTERVAL_MS:
        time.sleep_ms(2)
        return
    last_frame_ms = now
    update_input_and_state()
    if render_requested:
        render_one_frame()
```

`M5.update()` 必须持续执行；循环需要短暂让出 CPU。网络、文件和传感器异常都要有超时或降级路径。
