# `Widgets` --- A basic UI library

## M5 Series Display Libraries

#### 1. Display

- A low-level graphics library providing basic screen drawing, text, lines, and color management.
- Can be used independently, suitable for scenarios that only require drawing graphics or text.

#### 2. M5Widgets

- A basic UI widget library providing labels, image displays, and other UI controls.
- Built on top of M5GFX.
- Suitable for simple interactive UI elements.

#### 3. M5UI

- A high-level UI framework based on LVGL.
- Provides page management, multi-widget layouts, and unified event handling.

#### Usage Tips

- ⚠️ Do not mix M5GFX, M5Widgets, and M5UI simultaneously, as it may cause rendering issues or event conflicts.
- For graphics-only drawing → use M5GFX.
- For simple interactive widgets → use M5Widgets.
- For multi-page UI → use M5UI.

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *

def setup():
    M5.begin()
    Widgets.fillScreen(0x222222)

    Widgets.setBrightness(100)
    Widgets.fillScreen(0x6600CC)
    Widgets.setRotation(0)

def loop():
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## Screen functions

### `Widgets.setBrightness(brightness: int)`

    Set the backlight of the monitor。`brightness` ranges from 0 to 255.

### `Widgets.fillScreen(color: int)`

    Set the background color of the monitor. `color` accepts the color code of RGB888.

### `Widgets.setRotation(rotation: int)`

    Set the rotation Angle of the display.

    The `rotation` parameter only accepts the following values:

        - `0`: Portrait (0°C)
        - `1`: Landscape (90°C)
        - `2`: Inverse Portrait (180°C)
        - `3`: Inverse Landscape (270°C)

## Classes
