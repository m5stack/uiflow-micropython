
# M5Canvas

M5Canvas is a powerful graphics widget that provides a drawable surface for creating custom graphics, animations, and visual effects in the user interface. It supports drawing operations, sprite management, and advanced graphics rendering.

## MicroPython Example

#### draw basic shapes

This example demonstrates how to create a canvas and draw basic shapes programmatically.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
canvas0 = None

y = None
x = None

def setup():
    global page0, canvas0, x, y

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    canvas0 = m5ui.M5Canvas(
        x=120,
        y=100,
        w=80,
        h=40,
        color_format=lv.COLOR_FORMAT.ARGB8888,
        bg_c=0x4994EC,
        bg_opa=255,
        parent=page0,
    )

    page0.set_bg_color(0xFFCCCC, 255, 0)
    page0.screen_load()
    for y in range(10, 21):
        for x in range(5, 76):
            canvas0.set_px(x, y, 0x4994EC, 50)
    for y in range(20, 31):
        for x in range(5, 76):
            canvas0.set_px(x, y, 0x4994EC, 20)
    for y in range(30, 41):
        for x in range(5, 76):
            canvas0.set_px(x, y, 0x4994EC, 0)

def loop():
    global page0, canvas0, x, y
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Example output:

    A canvas displaying various geometric shapes with different colors.

#### batch drawing

Use `begin_draw()` and `end_draw()` to combine multiple canvas drawing operations into a single layer commit. This avoids visible intermediate redraws when a complex shape or animation frame needs several draw calls.

```python
canvas_0.fill_bg(0xFFFFFF, 255)
canvas_0.begin_draw()
canvas_0.draw_rect(50, 50, 200, 200, radius=20, bg_c=0xFFD54F)
canvas_0.draw_arc(120, 100, 10, 0x333333, 255, 3, 200, 340)
canvas_0.draw_triangle(140, 130, 160, 130, 150, 145, bg_c=0xFF8A65)
canvas_0.end_draw()
```
## **API**

#### M5Canvas

## `M5Canvas`
Create a canvas widget for drawing.

- Parameter `x` (`int`): The x-coordinate of the canvas.
- Parameter `y` (`int`): The y-coordinate of the canvas.
- Parameter `w` (`int`): The width of the canvas.
- Parameter `h` (`int`): The height of the canvas.
- Parameter `color_format` (`lv.COLOR_FORMAT`): The color format of the canvas (default is ARGB8888).
- Parameter `bg_c` (`int`): The background color of the canvas in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `bg_opa` (`int`): The opacity of the background (0-255).
- Parameter `parent` (`lv.obj`): The parent object of the canvas. If not specified, it will be
               set to the active screen.

### `begin_draw`
Start batch drawing and defer layer commit until `end_draw()`.

Draw methods keep their default behavior when batch drawing is not active.
Call this before multiple draw operations to avoid refreshing the canvas
after each individual operation.

### `end_draw`
Finish batch drawing and commit all pending draw operations once.

### `fill_bg`
Fill the canvas background with the specified color and opacity.

- Parameter `color` (`int`): The background color in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `opa` (`int`): The opacity of the background (0-255).

```python
canvas_0.fill_bg(0x001122, 255)
```

### `set_px`
Set a pixel at (x, y) with the specified color and opacity.

- Parameter `x` (`int`): The x-coordinate of the pixel.
- Parameter `y` (`int`): The y-coordinate of the pixel.
- Parameter `color` (`int`): The color of the pixel in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `opa` (`int`): The opacity of the pixel (0-255).

```python
canvas_0.set_px(100, 100, 0xFF0000, 255)
```

### `get_px_color`
Get the color of the pixel at (x, y).

- Parameter `x` (`int`): The x-coordinate of the pixel.
- Parameter `y` (`int`): The y-coordinate of the pixel.
- Returns: The color of the pixel in hexadecimal format (e.g., 0xRRGGBB).
- Return type: int

```python
color = canvas_0.get_px_color(100, 100)
print(hex(color))  # Prints the color in hexadecimal format
```

### `get_px_opa`
Get the opacity of the pixel at (x, y).

- Parameter `x` (`int`): The x-coordinate of the pixel.
- Parameter `y` (`int`): The y-coordinate of the pixel.
- Returns: The opacity of the pixel (0-255).
- Return type: int

### `draw_arc`
Draw an arc on the canvas.

- Parameter `x` (`int`): The x-coordinate of the center of the arc.
- Parameter `y` (`int`): The y-coordinate of the center of the arc.
- Parameter `r` (`int`): The radius of the arc.
- Parameter `color` (`int`): The color of the arc in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `opa` (`int`): The opacity of the arc (0-255).
- Parameter `width` (`int`): The width of the arc line.
- Parameter `start_angle` (`int`): The starting angle of the arc in degrees.
- Parameter `end_angle` (`int`): The ending angle of the arc in degrees.

```python
canvas_0.draw_arc(100, 100, 50, 0xFF0000, 255, 2, 0, 180)
```

### `draw_rect`
Draw a rectangle on the canvas.

- Parameter `x` (`int`): The x-coordinate of the rectangle.
- Parameter `y` (`int`): The y-coordinate of the rectangle.
- Parameter `w` (`int`): The width of the rectangle.
- Parameter `h` (`int`): The height of the rectangle.
- Parameter `radius` (`int`): The corner radius of the rectangle.
- Parameter `bg_c` (`int`): The background color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `bg_opa` (`int`): The opacity of the background (0-255).
- Parameter `border_c` (`int`): The border color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `border_opa` (`int`): The opacity of the border (0-255).
- Parameter `border_w` (`int`): The width of the border.
- Parameter `border_side` (`int`): The side of the border to draw (e.g., lv.BORDER_SIDE.FULL).
- Parameter `outline_c` (`int`): The outline color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `outline_opa` (`int`): The opacity of the outline (0-255).
- Parameter `outline_w` (`int`): The width of the outline.
- Parameter `outline_pad` (`int`): The padding of the outline.
- Parameter `shadow_c` (`int`): The shadow color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `shadow_opa` (`int`): The opacity of the shadow (0-255).
- Parameter `shadow_w` (`int`): The width of the shadow.
- Parameter `shadow_offset_x` (`int`): The horizontal offset of the shadow.
- Parameter `shadow_offset_y` (`int`): The vertical offset of the shadow.
- Parameter `shadow_spread` (`int`): The spread of the shadow.

```python
canvas_0.draw_rect(10, 10, 100, 50, radius=5, bg_c=0xFF0000,
                   bg_opa=255, border_c=0x00FF00, border_opa=255,
                   border_w=2, outline_c=0x0000FF, outline_opa=255,
                   outline_w=1, shadow_c=0x000000, shadow_opa=128,
                   shadow_w=5, shadow_offset_x=2, shadow_offset_y= 2,
                   shadow_spread=0)
```

### `draw_image`
Draw an image at the specified coordinates.

- Parameter `img_src` (`str`): The source of the image (e.g., a file path or an image object).
- Parameter `x` (`int`): The x-coordinate where the image will be drawn.
- Parameter `y` (`int`): The y-coordinate where the image will be drawn.
- Parameter `rotation` (`int`): The rotation angle of the image in degrees.
- Parameter `scale_x` (`float`): The horizontal scaling factor of the image.
- Parameter `scale_y` (`float`): The vertical scaling factor of the image.
- Parameter `skew_x` (`int`): The horizontal skew angle of the image in degrees.
- Parameter `skew_y` (`int`): The vertical skew angle of the image in degrees.

```python
canvas_0.draw_image("path/to/image.png", x=10, y=20, rotation=0,
                    scale_x=1.0, scale_y=1.0, skew_x=0, skew_y=0)
```

### `draw_line`
Draw a line from (x1, y1) to (x2, y2).

- Parameter `x1` (`int`): The x-coordinate of the start point of the line.
- Parameter `y1` (`int`): The y-coordinate of the start point of the line.
- Parameter `x2` (`int`): The x-coordinate of the end point of the line.
- Parameter `y2` (`int`): The y-coordinate of the end point of the line.
- Parameter `color` (`int`): The color of the line in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `opa` (`int`): The opacity of the line (0-255).
- Parameter `width` (`int`): The width of the line.

```python
canvas_0.draw_line(10, 10, 100, 100, color=0xFF0000, opa=255, width=2)
```

### `draw_label`
Draw a label with the specified text at the given coordinates.

- Parameter `txt` (`str`): The text to be displayed.
- Parameter `x` (`int`): The x-coordinate where the label will be drawn.
- Parameter `y` (`int`): The y-coordinate where the label will be drawn.
- Parameter `font`: The font to be used for the label (default is lv.font_montserrat_14).
- Parameter `color` (`int`): The color of the text in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `opa` (`int`): The opacity of the text (0-255).

```python
canvas_0.draw_label("Hello, World!", x=10, y=20, font=lv.font_montserrat_14,
                    color=0xFFFFFF, opa=255)
```

### `draw_triangle`
Draw a triangle with the specified vertices.

- Parameter `x1` (`int`): The x-coordinate of the first vertex.
- Parameter `y1` (`int`): The y-coordinate of the first vertex.
- Parameter `x2` (`int`): The x-coordinate of the second vertex.
- Parameter `y2` (`int`): The y-coordinate of the second vertex.
- Parameter `x3` (`int`): The x-coordinate of the third vertex.
- Parameter `y3` (`int`): The y-coordinate of the third vertex.
- Parameter `bg_c` (`int`): The background color of the triangle in hexadecimal format (e.g., 0xRRGGBB).
- Parameter `bg_opa` (`int`): The opacity of the triangle (0-255).

```python
canvas_0.draw_triangle(10, 10, 50, 10, 30, 40, bg_c=0xFF0000, bg_opa=255)
```

### `set_style_radius`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
canvas_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
canvas_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_pos(x, y)`

        Set the position of the canvas.

        - Parameter `x` (`int`): The x-coordinate of the canvas.
        - Parameter `y` (`int`): The y-coordinate of the canvas.
        - Returns: None

```python
canvas_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the canvas.

        - Parameter `x` (`int`): The x-coordinate of the canvas.
        - Returns: None

```python
canvas_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the canvas.

        - Parameter `y` (`int`): The y-coordinate of the canvas.
        - Returns: None

```python
canvas_0.set_y(100)
```
### `align_to(obj, align, x, y)`

        Align the canvas to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
canvas_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
### `set_size(width, height)`

        Set the size of the canvas.

        - Parameter `width` (`int`): The width of the canvas.
        - Parameter `height` (`int`): The height of the canvas.
        - Returns: None

```python
canvas_0.set_size(200, 100)
```
### `set_width(width)`

        Set the width of the canvas.

        - Parameter `width` (`int`): The width of the canvas.
        - Returns: None

```python
canvas_0.set_width(200)
```
### `set_height(height)`

        Set the height of the canvas.

        - Parameter `height` (`int`): The height of the canvas.
        - Returns: None

```python
canvas_0.set_height(100)
```
### `get_width()`

        Get the width of the canvas.

        - Returns: The width of the canvas.
        - Return type: int

```python
width = canvas_0.get_width()
```
### `get_height()`

        Get the height of the canvas.

        - Returns: The height of the canvas.
        - Return type: int

```python
height = canvas_0.get_height()
```
