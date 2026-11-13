
# Display

A lcd display library

StopWatch includes a built-in round AMOLED display accessed through
`M5.Lcd` / `M5.Display` after `M5.begin()`.
Read [Text Layout](../quick-reference/text-layout.md) for measured
width, overflow and vertical bounds, and
[Resource Files and Paths](../quick-reference/resource-files.md) before
loading an image or font file.

## M5 Series Display Libraries

#### 1. Display (M5.Lcd)

- A low-level graphics library providing basic screen drawing, text, lines, and color management.
- Can be used independently, suitable for scenarios that only require drawing graphics or text.
- **Access via**: `M5.Lcd.fillRect()`, `M5.Lcd.drawRect()`, `M5.Lcd.drawString()`, etc.

#### 2. M5Widgets

- A basic UI widget library providing labels, image displays, and other UI controls.
- Built on top of M5GFX.
- Suitable for simple interactive UI elements.
- **Access via**: `M5.Widgets.Label()`, `M5.Widgets.Image()`, `M5.Widgets.Rectangle()`, etc.
- **Important**: `M5.Widgets` provides UI component **classes**, not drawing methods.
- **Recommendation**: For new interactive UI projects, prefer M5UI/LVGL. Use M5.Widgets for simple or legacy UI components.

#### 3. M5UI

- A high-level UI framework based on LVGL.
- Provides page management, multi-widget layouts, and unified event handling.
- **Recommendation**: Prefer M5UI/LVGL for new interactive UI projects.

#### Usage Tips

- ⚠️ Do not mix M5GFX, M5Widgets, and M5UI simultaneously, as it may cause rendering issues or event conflicts.
- For graphics-only drawing → use M5GFX.
- For simple interactive widgets → use M5Widgets.
- For multi-page UI → use M5UI/LVGL (recommended for new projects).

#### Common Mistakes to Avoid

- ❌ **WRONG**: `M5.Lcd.fill_rect()` / `draw_string()` / `set_text_color()` - `M5.Lcd` methods are camelCase only; snake_case raises AttributeError
- ℹ️ **NOT the same rule**: `m5ui` `Label.set_text_color()` and `Image.draw_string()` are real snake_case methods of *those* classes - check the object type, do not "fix" them by habit
- ❌ **WRONG**: `Widgets.fillRect()` or `Widgets.drawRect()` - These methods do not exist in Widgets module
- ✅ **CORRECT**: `M5.Lcd.fillRect()` or `M5.Lcd.drawRect()` - Use M5.Lcd for drawing methods
- ❌ **WRONG**: `from M5 import Widgets; Widgets.fillRect(...)` - Widgets is for UI components, not drawing
- ✅ **CORRECT**: `import M5; M5.Lcd.fillRect(...)` - M5.Lcd provides all drawing methods

**Key Distinction**:
- `M5.Lcd` = Drawing methods (fillRect, drawRect, drawCircle, drawString, etc.)
- `M5.Widgets` = UI component classes (Label, Image, Rectangle, Circle, etc.)

## Screen Rotation

The rotation value is relative to the board's normal viewing direction.
The values `0`, `1`, `2` and `3` select 0°, 90°, 180° and 270°,
respectively. A value does not universally mean portrait or landscape;
the physical direction depends on the board and the M5GFX version.

#### Normal Orientation

- Core/Basic/Fire, Core2, CoreS3, StackChan: rotation `0`, logical size `320 × 240`.
- Cardputer, Cardputer Adv, DinMeter, Station: rotation `0`, logical size `240 × 135`.
- CoreP4X: rotation `0`, logical size `480 × 480`.

These values apply to the firmware documented on this site. Older firmware
may use a different rotation mapping. For the 320 × 240 controllers listed
above, rotations `1` and `3` use a logical size of 240 × 320, while
`0` and `2` use 320 × 240.

On a square display such as CoreP4X, all four rotations have the same
dimensions. Use readable text or corner markers to identify the direction.

#### Migrating Existing Examples

For Core/Basic/Fire, Core2, CoreS3 and StackChan, older examples that used
`Widgets.setRotation(1)` for normal landscape should now use
`Widgets.setRotation(0)`. The same applies to `M5.Lcd.setRotation()`.

For M5UI/LVGL, set the desired rotation before calling `m5ui.init()` so
the UI is initialized with the intended screen dimensions.

For other controllers or deliberately rotated layouts, select the rotation
that matches the intended result rather than replacing every `1` with
`0`.

After changing rotation, read `M5.Lcd.width()` and `M5.Lcd.height()`
to check the logical dimensions. The origin is the top-left corner;
X increases to the right and Y increases downward. On touch devices,
also check that touches at all four corners match the displayed positions.

```python
import M5
from M5 import Widgets

M5.begin()
Widgets.setRotation(0)
width = M5.Lcd.width()
height = M5.Lcd.height()
```
## MicroPython Example

#### Basic Drawing

This example demonstrates basic drawing functions of Display, including text, images, QR code, and various shapes.

```python
import os, sys, io
import M5
from M5 import *

def setup():
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)

    print((str("rotation: ") + str((M5.Display.getRotation()))))
    print(
        (
            str((str("w: ") + str((M5.Display.width()))))
            + str((str("h:") + str((M5.Display.height()))))
        )
    )
    M5.Display.setRotation(0)
    M5.Display.clear(0x000000)
    M5.Display.setTextColor(0x0000FF, 0x000000)
    M5.Display.setCursor(200, 3)
    M5.Display.printf("hello M5")
    M5.Display.print("hello M5", 0x6600CC)
    M5.Display.drawImage("/flash/res/img/default.png", 0, 0)
    M5.Display.drawQR("Hello", 220, 40, 100, 1)
    M5.Display.drawCircle(30, 80, 20, 0x3333FF)
    M5.Display.fillCircle(80, 80, 20, 0x009900)
    M5.Display.drawEllipse(60, 140, 50, 30, 0x00FF00)
    M5.Display.fillEllipse(60, 140, 30, 20, 0xFFFF00)
    M5.Display.drawLine(115, 10, 115, 60, 0xFF0000)
    M5.Display.drawRect(125, 10, 40, 30, 0xFF0000)
    M5.Display.fillRect(125, 50, 40, 30, 0x00FF00)
    M5.Display.drawTriangle(135, 150, 110, 190, 160, 190, 0x00FF00)
    M5.Display.fillTriangle(145, 150, 170, 190, 190, 150, 0x0000FF)
    M5.Display.drawArc(10, 180, 40, 45, 0, 90, 0xFFFF00)
    M5.Display.fillArc(20, 190, 40, 45, 0, 90, 0x00FFFF)

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

#### Canvas Drawing

This example demonstrates how to create and use a canvas for drawing. It creates a canvas with 2-bit color depth, draws circles on it, and then pushes the canvas to the display.

```python
import os, sys, io
import M5
from M5 import *

title0 = None
canvas_rmy = None

def setup():
    global title0, canvas_rmy

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Display canvas example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )

    canvas_rmy = M5.Display.newCanvas(100, 100, 2, True)
    canvas_rmy.drawCircle(30, 30, 20, 0xFFFFFF)
    canvas_rmy.drawCircle(30, 50, 20, 0xFFFFFF)
    canvas_rmy.drawCircle(50, 40, 20, 0xFFFFFF)
    canvas_rmy.push(50, 30)
    print((str("color depth: ") + str((canvas_rmy.getColorDepth()))))

def loop():
    global title0, canvas_rmy
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

#### Flicker-free Animation with Canvas

When an animation frame contains several drawing operations, do not erase and redraw
the elements directly on `M5.Lcd`. The display can expose the intermediate cleared
or partially drawn state, which appears as flicker. Create an off-screen canvas once,
draw the complete frame on the canvas, and call `push()` once after the frame is ready.

The API name is `M5.Lcd` (case-sensitive). Create the canvas during setup and reuse it;
creating a new canvas for every frame wastes memory and can cause allocation failures.

```python
import time
import M5
from M5 import *

canvas = None
ball_x = 12
direction = 2

def setup():
    global canvas
    M5.begin()
    # Only the animated region needs a canvas. PSRAM must be available when psram=True.
    canvas = M5.Lcd.newCanvas(w=200, h=80, bpp=16, psram=True)

def loop():
    global ball_x, direction
    M5.update()

    # Build the whole frame off-screen. Nothing below is visible yet.
    canvas.fillRect(0, 0, 200, 80, 0x000000)
    canvas.fillCircle(ball_x, 40, 12, 0x00FF00)
    canvas.setTextColor(0xFFFFFF, 0x000000)
    canvas.drawString("Canvas animation", 8, 8)

    # Present the completed frame in one operation.
    canvas.push(60, 80)

    ball_x += direction
    if ball_x <= 12 or ball_x >= 188:
        direction = -direction
    time.sleep_ms(16)

if __name__ == "__main__":
    setup()
    while True:
        loop()
```
Use a canvas sized only for the changing region when the rest of the screen is static.
If memory is limited, reduce the canvas dimensions or color depth, or set `psram=False`
when the target device has no PSRAM. Direct drawing remains appropriate for a single
small update that does not expose intermediate frame states. For multi-step graphics,
sprites, gauges, or animation frames, prefer the canvas-and-single-`push()` pattern.

## **API**

The examples below use `M5.Lcd`, the built-in display object. Initialize it
before running an example:

```python
import M5

M5.begin()
```
`M5.Display` is an alias for `M5.Lcd`. `from M5 import *` also exports
the same object as `Display` and `Lcd`. The off-screen `canvas` objects
in the Canvas examples are separate drawing targets.

### `class M5.Display`

    Parameters marked required must be supplied. Optional values are shown in the method
    signatures. Shape drawing methods and `fillScreen()` reuse the current drawing
    color when `color` is omitted or set to `-1`. The `clear()` method uses the
    current base color.

### `width()`

        Get the horizontal resolution of the display.

```python
M5.Lcd.width()
```
### `height()`

        Get the vertical resolution of the display.

```python
M5.Lcd.height()
```
### `getRotation()`

        Get the current rotation of the display.

        Rotation values:

        - 0: 0° rotation
        - 1: 90° rotation
        - 2: 180° rotation
        - 3: 270° rotation

        The value can also be 4~7 for M5GFX mirrored orientations; see
        `setRotation()` below. Display dimensions alone do not identify
        whether an orientation is mirrored.

```python
M5.Lcd.getRotation()
```
### `getColorDepth()`

        Get the color depth of the display.

```python
M5.Lcd.getColorDepth()
```
### `getCursor()`

        Get the current cursor position on the display.

```python
M5.Lcd.getCursor()
```
### `setRotation(r)`

        Set the rotation of the display.

        - Parameter `r` (`int`): rotation value (0~3)
            - 0: 0° rotation
            - 1: 90° rotation
            - 2: 180° rotation
            - 3: 270° rotation

> Note: The Python binding does not reject values outside 0~3.
> Current M5GFX LCD/framebuffer drivers use the low three bits:
> 4~7 select mirrored orientations, and other integers wrap to
> 0~7 (for example, 8 becomes 0). A value of 4 can be returned by
> `getRotation()` while width and height match rotation 0.
> Use 0~3 for ordinary rotation and validate application input
> before calling this method.
>
> See `display-rotation` for board-specific dimensions and migration from older examples. Set the desired rotation before initializing M5UI/LVGL.

```python
M5.Lcd.setRotation(2)
```
### `setColorDepth(bpp)`

        Set the color depth of the canvas.

        - Parameter `bpp` (`int`): desired color depth in bits per pixel.

        Notes: This method only applies to canvas objects, not the display itself. For CoreS3 devices, the display color depth is fixed at 16 bits.

```python
M5.Lcd.setColorDepth(16)
```
### `setEpdMode(epd_mode)`

        Set the EPD mode for the display.

        - Parameter `epd_mode` (`int`): desired EPD mode
            - 1: M5.Lcd.EPDMode.EPD_QUALITY
            - 2: M5.Lcd.EPDMode.EPD_TEXT
            - 3: M5.Lcd.EPDMode.EPD_FAST
            - 4: M5.Lcd.EPDMode.EPD_FASTEST

        Notes: Only applicable to devices with EPD capabilities.

```python
M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FAST)
```
### `getEpdMode()`

        Return the current EPD refresh mode as an integer.

        - Returns: 0 for a non-EPD display, or the current EPD mode:
            1 (EPD_QUALITY), 2 (EPD_TEXT), 3 (EPD_FAST), or 4 (EPD_FASTEST).
        - Return type: int

        This is the refresh mode, not a Boolean flag. Use `isEPD()` to
        check display capabilities and `setEpdMode()` to select a mode
        on an EPD display.

```python
print(M5.Lcd.getEpdMode())
```
### `isEPD()`

        Check if the display is an EPD (Electronic Paper Display).

```python
M5.Lcd.isEPD()
```
### `setFont(font)`

        Set the font for the display.

        - Parameter `support built-in font and font file(e.g., .bin(lvgl binary font format) or .vlw(Processing font format)). The following built-in fonts are available` (`font:`):

             Font Name                            Status           Alternatives                         Unsupported Devices                                          |
             M5.Lcd.FONTS.ASCII7                  N Deprecated   M5.Lcd.FONTS.Montserrat12                                                                         |
             M5.Lcd.FONTS.DejaVu9                 N Deprecated   M5.Lcd.FONTS.Montserrat12                                                                         |
             M5.Lcd.FONTS.DejaVu12                N Deprecated   M5.Lcd.FONTS.Montserrat14                                                                         |
             M5.Lcd.FONTS.DejaVu18                N Deprecated   M5.Lcd.FONTS.Montserrat18                                                                         |
             M5.Lcd.FONTS.DejaVu24                N Deprecated   M5.Lcd.FONTS.Montserrat24                                                                         |
             M5.Lcd.FONTS.DejaVu40                N Deprecated   M5.Lcd.FONTS.Montserrat40                                                                         |
             M5.Lcd.FONTS.DejaVu56                N Deprecated   M5.Lcd.FONTS.Montserrat44                                                                         |
             M5.Lcd.FONTS.DejaVu72                N Deprecated   M5.Lcd.FONTS.Montserrat48                                                                         |
             M5.Lcd.FONTS.EFontCN24               N Deprecated   M5.Lcd.FONTS.AlibabaPuHuiTiCN24                                                                   |
             M5.Lcd.FONTS.EFontJA24               N Deprecated   M5.Lcd.FONTS.AlibabaSansJA24                                                                      |
             M5.Lcd.FONTS.EFontKR24               N Deprecated   M5.Lcd.FONTS.AlibabaSansKR24                                                                      |
             M5.Lcd.FONTS.Montserrat12            S Recommended                                                                                                    |
             M5.Lcd.FONTS.Montserrat14            S Recommended                                                                                                    |
             M5.Lcd.FONTS.Montserrat16            S Recommended                                                                                                    |
             M5.Lcd.FONTS.Montserrat18            S Recommended                                                                                                    |
             M5.Lcd.FONTS.Montserrat24            S Recommended                                                                                                    |
             M5.Lcd.FONTS.Montserrat40            S Recommended                                                                                                    |
             M5.Lcd.FONTS.Montserrat48            S Recommended                                                                                                    |
             M5.Lcd.FONTS.AlibabaPuHuiTiCN24      S Recommended                                       M5STACK_StickC_PLUS, M5STACK_CoreInk, M5STACK_StickC,        |
             M5.Lcd.FONTS.AlibabaSansJA24         S Recommended                                       M5STACK_Atom_Lite, M5STACK_Stamp_PICO, M5STACK_Atom_Matrix,  |
             M5.Lcd.FONTS.AlibabaSansKR24         S Recommended                                       M5STACK_AtomU, M5STACK_Atom_Echo, M5STACK_NanoC6             |

```python
M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu18)
```
### `drawString(text, x, y, font=None)`

        Draw a string at the specified pixel coordinates using the current
        text color, text size, and the current or supplied font.

        - Parameter `text` (`str`): text to draw (required).
        - Parameter `x` (`int`): horizontal coordinate (required).
        - Parameter `y` (`int`): vertical coordinate (required).
        - Parameter `font`: optional built-in font object from `M5.Lcd.FONTS`.
            `None` uses the current font. A supplied font becomes the
            current font for subsequent drawing operations.
        - Returns: `None`. The Python wrapper does not return the drawn width.

        To use a font file, load it with `setFont()` first and omit the
        `font` argument. To measure a string, use `textWidth()`.

```python
M5.Lcd.drawString("Hello", 10, 20)
M5.Lcd.drawString("World", 10, 50, M5.Lcd.FONTS.Montserrat18)
```
### `textWidth(text, font=None)`

        Return the width of a string in pixels at the current text size.

        - Parameter `text` (`str`): text to measure (required).
        - Parameter `font`: optional built-in font object from `M5.Lcd.FONTS`.
            `None` uses the current font. In the current Python wrapper,
            supplying this argument also changes the current drawing font.
        - Returns: string width in pixels.
        - Return type: int

        To measure text with a font file, load it with `setFont()` first
        and omit the `font` argument.

```python
width = M5.Lcd.textWidth("Hello")
print(width)
```
### `fontHeight(font=None)`

        Return the font height in pixels at the current text size.

        - Parameter `font`: optional built-in font object from `M5.Lcd.FONTS`.
            `None` measures the current font. Supplying a font here does
            not change the current drawing font.
        - Returns: font height in pixels.
        - Return type: int

        To measure a font file, load it with `setFont()` first and omit
        the `font` argument.

```python
height = M5.Lcd.fontHeight()
print(height)
```
### `setTextColor(fgcolor, bgcolor=0x000000)`

        Set the text color and background color.

        - Parameter `fgcolor` (`int`): text color in RGB888 format (required)
        - Parameter `bgcolor` (`int`): background color in RGB888 format (default 0, black)

```python
M5.Lcd.setTextColor(0xFF0000, 0x000000)
```
### `setTextScroll(scroll)`

        Enable or disable text scrolling.

        - Parameter `scroll` (`bool`): True to enable text scrolling, False to disable (required)

```python
M5.Lcd.setTextScroll(True)
```
### `setTextSize(size)`

        Set the size of the text.

        - Parameter `size` (`int`): desired text size

```python
M5.Lcd.setTextSize(2)
```
### `setCursor(x, y)`

        Set the cursor position.

        - Parameter `x` (`int`): horizontal position of the cursor (required)
        - Parameter `y` (`int`): vertical position of the cursor (required)

```python
M5.Lcd.setCursor(10, 20)
```
### `clear(color=-1)`

        Clear the display with a specific color.

        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current base color when omitted or set to -1)

> Warning: Avoid calling `clear()` inside a loop or event handler — it
> redraws every pixel and causes visible flickering. For dynamic
> content, use `fillRect()` to erase only the changed region,
> then draw the new content on top.

```python
M5.Lcd.clear(0xFFFFFF)
```
### `fillScreen(color=-1)`

        Fill the entire screen with a specified color.

        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

> Warning: Avoid calling `fillScreen()` inside a loop or event handler —
> it redraws every pixel and causes visible flickering. Draw static
> backgrounds once during setup. For dynamic updates, use
> `fillRect()` to clear only the changed area.

```python
M5.Lcd.fillScreen(0xFF0000)
```
### `drawPixel(x, y, color=-1)`

        Draw a single pixel on the screen.

        - Parameter `x` (`int`): horizontal coordinate of the pixel (required)
        - Parameter `y` (`int`): vertical coordinate of the pixel (required)
        - Parameter `color` (`int`): pixel color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawPixel(50, 50, 0x00FF00)
```
### `drawCircle(x, y, r, color=-1)`

        Draw an outline of a circle.

        - Parameter `x` (`int`): x-coordinate of circle center (required)
        - Parameter `y` (`int`): y-coordinate of circle center (required)
        - Parameter `r` (`int`): radius of the circle (required)
        - Parameter `color` (`int`): circle color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawCircle(60, 60, 20, 0x0000FF)
```
### `fillCircle(x, y, r, color=-1)`

        Draw a filled circle.

        - Parameter `x` (`int`): x-coordinate of circle center (required)
        - Parameter `y` (`int`): y-coordinate of circle center (required)
        - Parameter `r` (`int`): radius of the circle (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillCircle(60, 60, 20, 0x00FFFF)
```
### `drawEllipse(x, y, rx, ry, color=-1)`

        Draw an outline of an ellipse.

        - Parameter `x` (`int`): x-coordinate of ellipse center (required)
        - Parameter `y` (`int`): y-coordinate of ellipse center (required)
        - Parameter `rx` (`int`): horizontal radius (required)
        - Parameter `ry` (`int`): vertical radius (required)
        - Parameter `color` (`int`): ellipse color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawEllipse(80, 40, 30, 20, 0xFF00FF)
```
### `fillEllipse(x, y, rx, ry, color=-1)`

        Draw a filled ellipse.

        - Parameter `x` (`int`): x-coordinate of ellipse center (required)
        - Parameter `y` (`int`): y-coordinate of ellipse center (required)
        - Parameter `rx` (`int`): horizontal radius (required)
        - Parameter `ry` (`int`): vertical radius (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillEllipse(80, 40, 30, 20, 0x00FF00)
```
### `drawLine(x0, y0, x1, y1, color=-1)`

        Draw a line.

        - Parameter `x0` (`int`): starting x-coordinate (required)
        - Parameter `y0` (`int`): starting y-coordinate (required)
        - Parameter `x1` (`int`): ending x-coordinate (required)
        - Parameter `y1` (`int`): ending y-coordinate (required)
        - Parameter `color` (`int`): line color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawLine(10, 10, 100, 100, 0xFF0000)
```
### `drawRect(x, y, w, h, color=-1)`

        Draw a rectangle.

        - Parameter `x` (`int`): top-left x-coordinate (required)
        - Parameter `y` (`int`): top-left y-coordinate (required)
        - Parameter `w` (`int`): width of rectangle (required)
        - Parameter `h` (`int`): height of rectangle (required)
        - Parameter `color` (`int`): rectangle color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawRect(20, 20, 80, 50, 0x00FF00)
```
### `fillRect(x, y, w, h, color=-1)`

        Draw a filled rectangle.

        - Parameter `x` (`int`): top-left x-coordinate (required)
        - Parameter `y` (`int`): top-left y-coordinate (required)
        - Parameter `w` (`int`): width of rectangle (required)
        - Parameter `h` (`int`): height of rectangle (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillRect(20, 20, 80, 50, 0x0000FF)
```
### `drawRoundRect(x, y, w, h, r, color=-1)`

        Draw a rounded rectangle.

        - Parameter `x` (`int`): top-left x-coordinate (required)
        - Parameter `y` (`int`): top-left y-coordinate (required)
        - Parameter `w` (`int`): width of rectangle (required)
        - Parameter `h` (`int`): height of rectangle (required)
        - Parameter `r` (`int`): corner radius (required)
        - Parameter `color` (`int`): rectangle color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawRoundRect(30, 30, 60, 40, 10, 0xFF00FF)
```
### `fillRoundRect(x, y, w, h, r, color=-1)`

        Draw a filled rounded rectangle.

        - Parameter `x` (`int`): top-left x-coordinate (required)
        - Parameter `y` (`int`): top-left y-coordinate (required)
        - Parameter `w` (`int`): width of rectangle (required)
        - Parameter `h` (`int`): height of rectangle (required)
        - Parameter `r` (`int`): corner radius (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillRoundRect(30, 30, 60, 40, 10, 0x00FFFF)
```
### `drawTriangle(x0, y0, x1, y1, x2, y2, color=-1)`

        Draw a triangle.

        - Parameter `x0` (`int`): first vertex x-coordinate (required)
        - Parameter `y0` (`int`): first vertex y-coordinate (required)
        - Parameter `x1` (`int`): second vertex x-coordinate (required)
        - Parameter `y1` (`int`): second vertex y-coordinate (required)
        - Parameter `x2` (`int`): third vertex x-coordinate (required)
        - Parameter `y2` (`int`): third vertex y-coordinate (required)
        - Parameter `color` (`int`): triangle color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawTriangle(10, 10, 50, 80, 90, 10, 0xFF0000)
```
### `fillTriangle(x0, y0, x1, y1, x2, y2, color=-1)`

        Draw a filled triangle.

        - Parameter `x0` (`int`): first vertex x-coordinate (required)
        - Parameter `y0` (`int`): first vertex y-coordinate (required)
        - Parameter `x1` (`int`): second vertex x-coordinate (required)
        - Parameter `y1` (`int`): second vertex y-coordinate (required)
        - Parameter `x2` (`int`): third vertex x-coordinate (required)
        - Parameter `y2` (`int`): third vertex y-coordinate (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillTriangle(10, 10, 50, 80, 90, 10, 0x00FF00)
```
### `drawArc(x, y, r0, r1, angle0, angle1, color=-1)`

        Draw an arc.

        - Parameter `x` (`int`): center x-coordinate (required)
        - Parameter `y` (`int`): center y-coordinate (required)
        - Parameter `r0` (`int`): first radius (required)
        - Parameter `r1` (`int`): second radius (required)
        - Parameter `angle0` (`int`): starting angle in degrees (required)
        - Parameter `angle1` (`int`): ending angle in degrees (required)
        - Parameter `color` (`int`): arc color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawArc(50, 50, 20, 30, 0, 180, 0xFF0000)
```
### `fillArc(x, y, r0, r1, angle0, angle1, color=-1)`

        Draw a filled arc.

        - Parameter `x` (`int`): center x-coordinate (required)
        - Parameter `y` (`int`): center y-coordinate (required)
        - Parameter `r0` (`int`): first radius (required)
        - Parameter `r1` (`int`): second radius (required)
        - Parameter `angle0` (`int`): starting angle in degrees (required)
        - Parameter `angle1` (`int`): ending angle in degrees (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillArc(50, 50, 20, 30, 0, 180, 0x00FF00)
```
### `drawEllipseArc(x, y, r0x, r1x, r0y, r1y, angle0, angle1, color=-1)`

        Draw an elliptical arc.

        - Parameter `x` (`int`): center x-coordinate (required)
        - Parameter `y` (`int`): center y-coordinate (required)
        - Parameter `r0x` (`int`): first horizontal radius (required)
        - Parameter `r1x` (`int`): second horizontal radius (required)
        - Parameter `r0y` (`int`): first vertical radius (required)
        - Parameter `r1y` (`int`): second vertical radius (required)
        - Parameter `angle0` (`int`): starting angle in degrees (required)
        - Parameter `angle1` (`int`): ending angle in degrees (required)
        - Parameter `color` (`int`): arc color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.drawEllipseArc(50, 50, 20, 40, 10, 30, 0, 180, 0xFF00FF)
```
### `fillEllipseArc(x, y, r0x, r1x, r0y, r1y, angle0, angle1, color=-1)`

        Draw a filled elliptical arc.

        - Parameter `x` (`int`): center x-coordinate (required)
        - Parameter `y` (`int`): center y-coordinate (required)
        - Parameter `r0x` (`int`): first horizontal radius (required)
        - Parameter `r1x` (`int`): second horizontal radius (required)
        - Parameter `r0y` (`int`): first vertical radius (required)
        - Parameter `r1y` (`int`): second vertical radius (required)
        - Parameter `angle0` (`int`): starting angle in degrees (required)
        - Parameter `angle1` (`int`): ending angle in degrees (required)
        - Parameter `color` (`int`): fill color in RGB888 format (optional, reuses the current color when omitted or set to -1)

```python
M5.Lcd.fillEllipseArc(50, 50, 20, 40, 10, 30, 0, 180, 0x00FFFF)
```
### `drawQR(text, x, y, w, version=1)`

        Draw a QR code.

        - Parameter `text` (`str`): QR code content
        - Parameter `x` (`int`): x-coordinate to display (required)
        - Parameter `y` (`int`): y-coordinate to display (required)
        - Parameter `w` (`int`): QR code width (required)
        - Parameter `version` (`int`): QR code version (default 1, range: 0~38)

```python
M5.Lcd.drawQR("Hello", 0, 0, 200)
```
### `drawPng(img, x=0, y=0, maxW=0, maxH=0, offX=0, offY=0, scaleX=1.0, scaleY=0.0)`

        Draw a PNG image.

        - Parameter `img` (`str`): image path or data
        - Parameter `x` (`int`): display x-coordinate (default 0)
        - Parameter `y` (`int`): display y-coordinate (default 0)
        - Parameter `maxW` (`int`): max width to draw (default 0)
        - Parameter `maxH` (`int`): max height to draw (default 0)
        - Parameter `offX` (`int`): x-offset in image (default 0)
        - Parameter `offY` (`int`): y-offset in image (default 0)
        - Parameter `scaleX` (`float`): horizontal scale factor (default 1.0)
        - Parameter `scaleY` (`float`): vertical scale factor (default 0.0)

```python
M5.Lcd.drawPng("res/img/uiflow.png", 0, 0)
```
        Example:

```python
M5.Lcd.drawPng("res/img/uiflow.png", 0, 0)
img = open("res/img/uiflow.png", "b")
img.seek(0)
M5.Lcd.drawPng(img.read(), 0, 100)
img.close()
```
### `drawJpg(img, x=0, y=0, maxW=0, maxH=0, offX=0, offY=0, scaleX=1.0, scaleY=0.0)`

        Draw a JPG image.

        - Parameter `img`: image path or data
        - Parameter `x` (`int`): display x-coordinate (default 0)
        - Parameter `y` (`int`): display y-coordinate (default 0)
        - Parameter `maxW` (`int`): max width to draw (default 0)
        - Parameter `maxH` (`int`): max height to draw (default 0)
        - Parameter `offX` (`int`): x-offset in image (default 0)
        - Parameter `offY` (`int`): y-offset in image (default 0)
        - Parameter `scaleX` (`float`): horizontal scale factor (default 1.0)
        - Parameter `scaleY` (`float`): vertical scale factor (default 0.0)

```python
M5.Lcd.drawJpg("res/img/uiflow.jpg", 0, 0)
```
        Example:

```python
M5.Lcd.drawJpg("res/img/uiflow.jpg", 0, 0)
img = open("res/img/uiflow.jpg", "b")
img.seek(0)
M5.Lcd.drawJpg(img.read(), 0, 100)
img.close()
```
### `drawBmp(img, x=0, y=0, maxW=0, maxH=0, offX=0, offY=0, scaleX=1.0, scaleY=0.0)`

        Draw a BMP image.

        - Parameter `img`: image path or data
        - Parameter `x` (`int`): display x-coordinate (default 0)
        - Parameter `y` (`int`): display y-coordinate (default 0)
        - Parameter `maxW` (`int`): max width to draw (default 0)
        - Parameter `maxH` (`int`): max height to draw (default 0)
        - Parameter `offX` (`int`): x-offset in image (default 0)
        - Parameter `offY` (`int`): y-offset in image (default 0)
        - Parameter `scaleX` (`float`): horizontal scale factor (default 1.0)
        - Parameter `scaleY` (`float`): vertical scale factor (default 0.0)

```python
M5.Lcd.drawBmp("res/img/uiflow.bmp", 0, 0)
```
        Example:

```python
M5.Lcd.drawBmp("res/img/uiflow.bmp", 0, 0)
img = open("res/img/uiflow.bmp", "b")
img.seek(0)
M5.Lcd.drawBmp(img.read(), 0, 100)
img.close()
```
### `drawImage(img, x=0, y=0, maxW=0, maxH=0, offX=0, offY=0, scaleX=1.0, scaleY=0.0)`

        Draw an image.

        - Parameter `img`: image path or data
        - Parameter `x` (`int`): display x-coordinate (default 0)
        - Parameter `y` (`int`): display y-coordinate (default 0)
        - Parameter `maxW` (`int`): max width to draw (default 0)
        - Parameter `maxH` (`int`): max height to draw (default 0)
        - Parameter `offX` (`int`): x-offset in image (default 0)
        - Parameter `offY` (`int`): y-offset in image (default 0)
        - Parameter `scaleX` (`float`): horizontal scale factor (default 1.0)
        - Parameter `scaleY` (`float`): vertical scale factor (default 0.0)

```python
img = open("res/img/uiflow.jpg", "b")
```
        Example:

```python
img = open("res/img/uiflow.jpg", "b")
img.seek(0)
M5.Lcd.drawImage(img.read(), 0, 0)
img.close()
```
### `drawRawBuf(buf, x, y, w, h, len, swap=False)`

        Draw an image from raw buffer data.

        - Parameter `buf`: image buffer
        - Parameter `x` (`int`): display x-coordinate (required)
        - Parameter `y` (`int`): display y-coordinate (required)
        - Parameter `w` (`int`): image width (required)
        - Parameter `h` (`int`): image height (required)
        - Parameter `len` (`int`): length of image data (required)
        - Parameter `swap` (`bool`): inverted display (default False)

```python
M5.Lcd.drawRawBuf(raw_buf, 0, 0, 100, 100, len(raw_buf), swap=False)
```
        Example:

```python
width, height = 40, 30
green565 = 0x07E0
raw_buf = bytearray(width * height * 2)
for i in range(width * height):
    raw_buf[2*i]   = (green565 >> 8) & 0xFF
    raw_buf[2*i+1] = green565 & 0xFF
M5.Lcd.drawRawBuf(raw_buf, 100, 100, width, height, len(raw_buf), swap=False)
```
### `print(text, color=-1)`

        Display a string (no formatting support).

        - Parameter `text` (`str`): text to display
        - Parameter `color` (`int`): color in RGB888 format (optional, keeps the current text color when omitted or set to -1)

```python
M5.Lcd.print("Hello World", color=0xFF0000)
```
### `printf(text)`

        Display a formatted string.

        - Parameter `text` (`str`): text to display with formatting

```python
M5.Lcd.printf("Value: %d" % 100)
```
### `newCanvas(w, h, bpp=-1, psram=False)`

        Create an off-screen canvas. Use it to compose a complete animation frame before
        presenting the frame with a single `push(x, y)` call. Reuse the returned object
        instead of creating it repeatedly in the main loop.

        - Parameter `w` (`int`): canvas width
        - Parameter `h` (`int`): canvas height
        - Parameter `bpp` (`int`): color depth (default -1)
        - Parameter `psram` (`bool`): use PSRAM (default False)
        - Returns: created canvas object

```python
w1 = M5.Lcd.newCanvas(w=100, h=100, bpp=16)
```
        Example:

```python
w1 = M5.Lcd.newCanvas(w=100, h=100, bpp=16)
w1.drawImage("res/img/uiflow.jpg", 80, 0)
w1.push(30, 0)
```
### `startWrite()`

        Start writing to the display.

```python
M5.Lcd.startWrite()
```
        Example:

```python
M5.Lcd.startWrite()
M5.Lcd.drawPixel(10, 10, 0xFF0000)
M5.Lcd.endWrite()
```
### `endWrite()`

        End writing to the display.

```python
M5.Lcd.endWrite()
```
