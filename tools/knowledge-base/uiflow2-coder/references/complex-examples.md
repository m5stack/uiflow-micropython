# Curated Complex Examples

这些示例是人工精选的复杂 UIFlow2 程序，用于复用整体结构、状态管理和性能策略。
示例按 UI 体系和屏幕分辨率组织，不以某一款主机作为唯一适用范围。
每个条目单独记录验证状态；未标明硬件验证时，不要声称已经过真机测试。
API 名称、参数和兼容性仍以 `docs/` 为准；不要仅凭示例推断未记录的 API。

## Hourglass (Widgets, 135 x 240)

- 仓库源路径：`examples/widgets/hourglass_135x240.py`
- Skill 镜像：[assets/examples/widgets/hourglass_135x240.py](../assets/examples/widgets/hourglass_135x240.py)
- 能力点：IMU gravity mapping and filtering、button-driven state changes、off-screen Canvas rendering、grid-based particle simulation、allocation-conscious animation loop
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 135 x 240 Widgets animation, sensor-driven simulation, or frame-timed Canvas application.

## Weather (Widgets, 135 x 240)

- 仓库源路径：`examples/widgets/weather_135x240.py`
- Skill 镜像：[assets/examples/widgets/weather_135x240.py](../assets/examples/widgets/weather_135x240.py)
- 能力点：reuse of the existing UIFlow2 Wi-Fi connection、optional Wi-Fi fallback only when offline、HTTPS weather API requests and JSON parsing、cached offline display and refresh scheduling、off-screen Canvas dashboard rendering
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 135 x 240 Widgets dashboard, periodic API client, cached offline view, or weather application.

## Weather (M5UI/LVGL, 320 x 240)

- 仓库源路径：`examples/m5ui/weather_320x240.py`
- Skill 镜像：[assets/examples/m5ui/weather_320x240.py](../assets/examples/m5ui/weather_320x240.py)
- 能力点：M5UI page, Canvas, label, and button composition、reuse of the existing UIFlow2 Wi-Fi connection、optional Wi-Fi fallback only when offline、IP-based location with Shenzhen fallback、HTTPS weather requests, caching, and offline display
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 320 x 240 M5UI/LVGL network dashboard, weather client, or cached offline view.

## Hourglass (M5UI/LVGL, 320 x 240)

- 仓库源路径：`examples/m5ui/hourglass_320x240.py`
- Skill 镜像：[assets/examples/m5ui/hourglass_320x240.py](../assets/examples/m5ui/hourglass_320x240.py)
- 能力点：M5UI page and touch button composition、IMU gravity mapping and filtering、double-buffered LVGL Canvas rendering、grid-based particle simulation、frame-timed allocation-conscious animation
- 验证状态：开发者提供的参考实现；未记录真机验证
- 适用场景：Building a 320 x 240 M5UI/LVGL animation, IMU-driven simulation, or custom LVGL Canvas renderer.
