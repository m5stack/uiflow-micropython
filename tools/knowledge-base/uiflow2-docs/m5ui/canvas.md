<!-- .. currentmodule:: m5ui -->

# M5Canvas

<!-- .. include:: ../refs/m5ui.canvas.ref -->

M5Canvas is a powerful graphics widget that provides a drawable surface for creating custom graphics, animations, and visual effects in the user interface. It supports drawing operations, sprite management, and advanced graphics rendering.

## UiFlow2 Example

#### draw basic shapes

Open the |cores3_canvas_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to create a canvas and draw basic shapes like rectangles, circles, and lines.

UiFlow2 Code Block:

Example output:

    A canvas with various colored shapes including rectangles, circles, and lines.

## MicroPython Example

#### draw basic shapes

This example demonstrates how to create a canvas and draw basic shapes programmatically.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

## **API**

#### M5Canvas

## M5Canvas
Create a canvas widget for drawing.

:param int x: The x-coordinate of the canvas.
:param int y: The y-coordinate of the canvas.
:param int w: The width of the canvas.
:param int h: The height of the canvas.
:param lv.COLOR_FORMAT color_format: The color format of the canvas (default is ARGB8888).
:param int bg_c: The background color of the canvas in hexadecimal format (e.g., 0xRRGGBB).
:param int bg_opa: The opacity of the background (0-255).
:param lv.obj parent: The parent object of the canvas. If not specified, it will be
               set to the active screen.

### `fill_bg`
Fill the canvas background with the specified color and opacity.

:param int color: The background color in hexadecimal format (e.g., 0xRRGGBB).
:param int opa: The opacity of the background (0-255).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.fill_bg(0x001122, 255)

### `set_px`
Set a pixel at (x, y) with the specified color and opacity.

:param int x: The x-coordinate of the pixel.
:param int y: The y-coordinate of the pixel.
:param int color: The color of the pixel in hexadecimal format (e.g., 0xRRGGBB).
:param int opa: The opacity of the pixel (0-255).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.set_px(100, 100, 0xFF0000, 255)

### `get_px_color`
Get the color of the pixel at (x, y).

:param int x: The x-coordinate of the pixel.
:param int y: The y-coordinate of the pixel.
:return: The color of the pixel in hexadecimal format (e.g., 0xRRGGBB).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = canvas_0.get_px_color(100, 100)
        print(hex(color))  # Prints the color in hexadecimal format

### `get_px_opa`
Get the opacity of the pixel at (x, y).

:param int x: The x-coordinate of the pixel.
:param int y: The y-coordinate of the pixel.
:return: The opacity of the pixel (0-255).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

### `draw_arc`
Draw an arc on the canvas.

:param int x: The x-coordinate of the center of the arc.
:param int y: The y-coordinate of the center of the arc.
:param int r: The radius of the arc.
:param int color: The color of the arc in hexadecimal format (e.g., 0xRRGGBB).
:param int opa: The opacity of the arc (0-255).
:param int width: The width of the arc line.
:param int start_angle: The starting angle of the arc in degrees.
:param int end_angle: The ending angle of the arc in degrees.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.draw_arc(100, 100, 50, 0xFF0000, 255, 2, 0, 180)

### `draw_rect`
Draw a rectangle on the canvas.

:param int x: The x-coordinate of the rectangle.
:param int y: The y-coordinate of the rectangle.
:param int w: The width of the rectangle.
:param int h: The height of the rectangle.
:param int radius: The corner radius of the rectangle.
:param int bg_c: The background color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
:param int bg_opa: The opacity of the background (0-255).
:param int border_c: The border color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
:param int border_opa: The opacity of the border (0-255).
:param int border_w: The width of the border.
:param int border_side: The side of the border to draw (e.g., lv.BORDER_SIDE.FULL).
:param int outline_c: The outline color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
:param int outline_opa: The opacity of the outline (0-255).
:param int outline_w: The width of the outline.
:param int outline_pad: The padding of the outline.
:param int shadow_c: The shadow color of the rectangle in hexadecimal format (e.g., 0xRRGGBB).
:param int shadow_opa: The opacity of the shadow (0-255).
:param int shadow_w: The width of the shadow.
:param int shadow_offset_x: The horizontal offset of the shadow.
:param int shadow_offset_y: The vertical offset of the shadow.
:param int shadow_spread: The spread of the shadow.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.draw_rect(10, 10, 100, 50, radius=5, bg_c=0xFF0000,
                           bg_opa=255, border_c=0x00FF00, border_opa=255,
                           border_w=2, outline_c=0x0000FF, outline_opa=255,
                           outline_w=1, shadow_c=0x000000, shadow_opa=128,
                           shadow_w=5, shadow_offset_x=2, shadow_offset_y= 2,
                           shadow_spread=0)

### `draw_image`
Draw an image at the specified coordinates.

:param str img_src: The source of the image (e.g., a file path or an image object).
:param int x: The x-coordinate where the image will be drawn.
:param int y: The y-coordinate where the image will be drawn.
:param int rotation: The rotation angle of the image in degrees.
:param float scale_x: The horizontal scaling factor of the image.
:param float scale_y: The vertical scaling factor of the image.
:param int skew_x: The horizontal skew angle of the image in degrees.
:param int skew_y: The vertical skew angle of the image in degrees.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.draw_image("path/to/image.png", x=10, y=20, rotation=0,
                            scale_x=1.0, scale_y=1.0, skew_x=0, skew_y=0)

### `draw_line`
Draw a line from (x1, y1) to (x2, y2).

:param int x1: The x-coordinate of the start point of the line.
:param int y1: The y-coordinate of the start point of the line.
:param int x2: The x-coordinate of the end point of the line.
:param int y2: The y-coordinate of the end point of the line.
:param int color: The color of the line in hexadecimal format (e.g., 0xRRGGBB).
:param int opa: The opacity of the line (0-255).
:param int width: The width of the line.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.draw_line(10, 10, 100, 100, color=0xFF0000, opa=255, width=2)

### `draw_label`
Draw a label with the specified text at the given coordinates.

:param str txt: The text to be displayed.
:param int x: The x-coordinate where the label will be drawn.
:param int y: The y-coordinate where the label will be drawn.
:param font: The font to be used for the label (default is lv.font_montserrat_14).
:param int color: The color of the text in hexadecimal format (e.g., 0xRRGGBB).
:param int opa: The opacity of the text (0-255).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.draw_label("Hello, World!", x=10, y=20, font=lv.font_montserrat_14,
                            color=0xFFFFFF, opa=255)

### `draw_triangle`
Draw a triangle with the specified vertices.

:param int x1: The x-coordinate of the first vertex.
:param int y1: The y-coordinate of the first vertex.
:param int x2: The x-coordinate of the second vertex.
:param int y2: The y-coordinate of the second vertex.
:param int x3: The x-coordinate of the third vertex.
:param int y3: The y-coordinate of the third vertex.
:param int bg_c: The background color of the triangle in hexadecimal format (e.g., 0xRRGGBB).
:param int bg_opa: The opacity of the triangle (0-255).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        canvas_0.draw_triangle(10, 10, 50, 10, 30, 40, bg_c=0xFF0000, bg_opa=255)

### `set_style_radius`

<!-- .. py:method:: set_flag(flag, value) -->

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_flag(lv.obj.FLAG.HIDDEN, True)

<!-- .. py:method:: toggle_flag(flag) -->

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        :param int flag: The flag to toggle.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.toggle_flag(lv.obj.FLAG.HIDDEN)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the canvas.

        :param int x: The x-coordinate of the canvas.
        :param int y: The y-coordinate of the canvas.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_pos(100, 100)

<!-- .. py:method:: set_x(x) -->

        Set the x-coordinate of the canvas.

        :param int x: The x-coordinate of the canvas.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_x(100)

<!-- .. py:method:: set_y(y) -->

        Set the y-coordinate of the canvas.

        :param int y: The y-coordinate of the canvas.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_y(100)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the canvas to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the canvas.

        :param int width: The width of the canvas.
        :param int height: The height of the canvas.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_size(200, 100)

<!-- .. py:method:: set_width(width) -->

        Set the width of the canvas.

        :param int width: The width of the canvas.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_width(200)

<!-- .. py:method:: set_height(height) -->

        Set the height of the canvas.

        :param int height: The height of the canvas.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                canvas_0.set_height(100)

<!-- .. py:method:: get_width() -->

        Get the width of the canvas.

        :return: The width of the canvas.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = canvas_0.get_width()

<!-- .. py:method:: get_height() -->

        Get the height of the canvas.

        :return: The height of the canvas.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = canvas_0.get_height()
