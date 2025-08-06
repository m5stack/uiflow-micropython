# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Canvas(lv.canvas):
    """Create a canvas widget for drawing.

    :param int x: The x-coordinate of the canvas.
    :param int y: The y-coordinate of the canvas.
    :param int w: The width of the canvas.
    :param int h: The height of the canvas.
    :param lv.COLOR_FORMAT color_format: The color format of the canvas (default is ARGB8888).
    :param int bg_c: The background color of the canvas in hexadecimal format (e.g., 0xRRGGBB).
    :param int bg_opa: The opacity of the background (0-255).
    :param lv.obj parent: The parent object of the canvas. If not specified, it will be
                   set to the active screen.
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=50,
        h=50,
        color_format=lv.COLOR_FORMAT.ARGB8888,
        bg_c=0xC9C9C9,
        bg_opa=255,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self._cbuf = lv.draw_buf_create(w, h, color_format, 0)
        self.set_draw_buf(self._cbuf)
        self.set_pos(x, y)

        self.fill_bg(bg_c, bg_opa)

        self._layer = lv.layer_t()
        self.init_layer(self._layer)

        self._area = lv.area_t()

    def fill_bg(self, color: int, opa: int):
        """Fill the canvas background with the specified color and opacity.

        :param int color: The background color in hexadecimal format (e.g., 0xRRGGBB).
        :param int opa: The opacity of the background (0-255).

        UiFlow2 Code Block:

            |set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.fill_bg(0x001122, 255)

        """
        if isinstance(color, int):
            color = lv.color_hex(color)
        super().fill_bg(color, opa)

    def set_px(self, x: int, y: int, color: lv.color_t, opa: int):
        """Set a pixel at (x, y) with the specified color and opacity.

        :param int x: The x-coordinate of the pixel.
        :param int y: The y-coordinate of the pixel.
        :param int color: The color of the pixel in hexadecimal format (e.g., 0xRRGGBB).
        :param int opa: The opacity of the pixel (0-255).

        UiFlow2 Code Block:

            |set_px.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.set_px(100, 100, 0xFF0000, 255)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)
        super().set_px(x, y, color, opa)

    def get_px_color(self, x: int, y: int) -> int:
        """Get the color of the pixel at (x, y).

        :param int x: The x-coordinate of the pixel.
        :param int y: The y-coordinate of the pixel.
        :return: The color of the pixel in hexadecimal format (e.g., 0xRRGGBB).
        :rtype: int

        UiFlow2 Code Block:

            |get_px_color.png|

        MicroPython Code Block:

            .. code-block:: python

                color = canvas_0.get_px_color(100, 100)
                print(hex(color))  # Prints the color in hexadecimal format
        """
        c = super().get_px(x, y)
        return c.red << 16 | c.green << 8 | c.blue

    def get_px_opa(self, x: int, y: int) -> int:
        """Get the opacity of the pixel at (x, y).

        :param int x: The x-coordinate of the pixel.
        :param int y: The y-coordinate of the pixel.
        :return: The opacity of the pixel (0-255).
        :rtype: int

        UiFlow2 Code Block:

            |get_px_opa.png|

        MicroPython Code Block:

            .. code-block:: python
        """
        c = super().get_px(x, y)
        return c.alpha

    def draw_arc(
        self,
        x: int,
        y: int,
        r: int,
        color: int = 0x000000,
        opa: int = lv.OPA.COVER,
        width: int = 1,
        start_angle: int = 0,
        end_angle: int = 90,
    ):
        """Draw an arc on the canvas.

        :param int x: The x-coordinate of the center of the arc.
        :param int y: The y-coordinate of the center of the arc.
        :param int r: The radius of the arc.
        :param int color: The color of the arc in hexadecimal format (e.g., 0xRRGGBB).
        :param int opa: The opacity of the arc (0-255).
        :param int width: The width of the arc line.
        :param int start_angle: The starting angle of the arc in degrees.
        :param int end_angle: The ending angle of the arc in degrees.

        UiFlow2 Code Block:

            |draw_arc.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.draw_arc(100, 100, 50, 0xFF0000, 255, 2, 0, 180)
        """
        if not hasattr(self, "_arc_dsc"):
            self._arc_dsc = lv.draw_arc_dsc_t()
        self._arc_dsc.init()

        self._arc_dsc.color = lv.color_hex(color)
        self._arc_dsc.opa = opa
        self._arc_dsc.width = width
        self._arc_dsc.center.x = x
        self._arc_dsc.center.y = y
        self._arc_dsc.radius = r
        self._arc_dsc.start_angle = start_angle
        self._arc_dsc.end_angle = end_angle

        lv.draw_arc(self._layer, self._arc_dsc)
        self.finish_layer(self._layer)

    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        radius: int = 0,
        bg_c: int = 0xFFFFFF,
        bg_opa: int = lv.OPA.COVER,
        border_c: int = 0xFFFFFF,
        border_opa: int = lv.OPA.COVER,
        border_w: int = 0,
        border_side: int = lv.BORDER_SIDE.FULL,
        outline_c: int = 0x000000,
        outline_opa: int = lv.OPA.COVER,
        outline_w: int = 0,
        outline_pad: int = 0,
        shadow_c: int = 0x000000,
        shadow_opa: int = lv.OPA.COVER,
        shadow_w: int = 0,
        shadow_offset_x: int = 0,
        shadow_offset_y: int = 0,
        shadow_spread: int = 0,
    ):
        """Draw a rectangle on the canvas.

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

            |draw_rect.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.draw_rect(10, 10, 100, 50, radius=5, bg_c=0xFF0000,
                                   bg_opa=255, border_c=0x00FF00, border_opa=255,
                                   border_w=2, outline_c=0x0000FF, outline_opa=255,
                                   outline_w=1, shadow_c=0x000000, shadow_opa=128,
                                   shadow_w=5, shadow_offset_x=2, shadow_offset_y= 2,
                                   shadow_spread=0)
        """
        if not hasattr(self, "_rect_dsc"):
            self._rect_dsc = lv.draw_rect_dsc_t()

        self._rect_dsc.init()
        self._rect_dsc.radius = radius
        self._rect_dsc.bg_color = lv.color_hex(bg_c)
        self._rect_dsc.bg_opa = bg_opa
        self._rect_dsc.border_color = lv.color_hex(border_c)
        self._rect_dsc.border_width = border_w
        self._rect_dsc.border_opa = border_opa
        self._rect_dsc.border_side = border_side
        self._rect_dsc.outline_color = lv.color_hex(outline_c)
        self._rect_dsc.outline_width = outline_w
        self._rect_dsc.outline_pad = outline_pad
        self._rect_dsc.outline_opa = outline_opa
        self._rect_dsc.shadow_color = lv.color_hex(shadow_c)
        self._rect_dsc.shadow_width = shadow_w
        self._rect_dsc.shadow_offset_x = shadow_offset_x
        self._rect_dsc.shadow_offset_y = shadow_offset_y
        self._rect_dsc.shadow_spread = shadow_spread
        self._rect_dsc.shadow_opa = shadow_opa

        self._area.x1 = x
        self._area.y1 = y
        self._area.x2 = x + w - 1
        self._area.y2 = y + h - 1
        lv.draw_rect(self._layer, self._rect_dsc, self._area)
        self.finish_layer(self._layer)

    def draw_image(
        self,
        img_src: str,
        x: int = 0,
        y: int = 0,
        rotation: int = 0,
        scale_x: float = 1.0,
        scale_y: float = 1.0,
        skew_x: int = 0,
        skew_y: int = 0,
    ):
        """Draw an image at the specified coordinates.

        :param str img_src: The source of the image (e.g., a file path or an image object).
        :param int x: The x-coordinate where the image will be drawn.
        :param int y: The y-coordinate where the image will be drawn.
        :param int rotation: The rotation angle of the image in degrees.
        :param float scale_x: The horizontal scaling factor of the image.
        :param float scale_y: The vertical scaling factor of the image.
        :param int skew_x: The horizontal skew angle of the image in degrees.
        :param int skew_y: The vertical skew angle of the image in degrees.

        UiFlow2 Code Block:

            |draw_image.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.draw_image("path/to/image.png", x=10, y=20, rotation=0,
                                    scale_x=1.0, scale_y=1.0, skew_x=0, skew_y=0)
        """
        if not hasattr(self, "_image_dsc"):
            self._image_dsc = lv.draw_image_dsc_t()
        if not hasattr(self, "_image_header"):
            self._image_header = lv.image_header_t()

        img_src = "S:" + img_src
        self._image_dsc.init()
        self._image_dsc.src = img_src
        self._image_dsc.rotation = rotation
        self._image_dsc.scale_x = int(scale_x * 256)
        self._image_dsc.scale_y = int(scale_y * 256)
        self._image_dsc.skew_x = skew_x
        self._image_dsc.skew_y = skew_y

        lv.image.decoder_get_info(img_src, self._image_header)
        self._area.x1 = x
        self._area.y1 = y
        self._area.x2 = x + self._image_header.w - 1
        self._area.y2 = y + self._image_header.h - 1
        lv.draw_image(self._layer, self._image_dsc, self._area)
        self.finish_layer(self._layer)

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: int = 0x000000,
        opa: int = lv.OPA.COVER,
        width: int = 1,
    ):
        """Draw a line from (x1, y1) to (x2, y2).

        :param int x1: The x-coordinate of the start point of the line.
        :param int y1: The y-coordinate of the start point of the line.
        :param int x2: The x-coordinate of the end point of the line.
        :param int y2: The y-coordinate of the end point of the line.
        :param int color: The color of the line in hexadecimal format (e.g., 0xRRGGBB).
        :param int opa: The opacity of the line (0-255).
        :param int width: The width of the line.

        UiFlow2 Code Block:

            |draw_line.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.draw_line(10, 10, 100, 100, color=0xFF0000, opa=255, width=2)
        """
        if not hasattr(self, "_line_dsc"):
            self._line_dsc = lv.draw_line_dsc_t()
        self._line_dsc.init()
        self._line_dsc.color = lv.color_hex(color)
        self._line_dsc.opa = opa
        self._line_dsc.width = width
        self._line_dsc.p1.x = x1
        self._line_dsc.p1.y = y1
        self._line_dsc.p2.x = x2
        self._line_dsc.p2.y = y2
        self._line_dsc.round_start = 1
        self._line_dsc.round_end = 1

        lv.draw_line(self._layer, self._line_dsc)
        self.finish_layer(self._layer)

    def draw_label(
        self,
        txt: str,
        x: int = 0,
        y: int = 0,
        font=lv.font_montserrat_14,
        color=0x000000,
        opa=lv.OPA.COVER,
    ):
        """Draw a label with the specified text at the given coordinates.

        :param str txt: The text to be displayed.
        :param int x: The x-coordinate where the label will be drawn.
        :param int y: The y-coordinate where the label will be drawn.
        :param font: The font to be used for the label (default is lv.font_montserrat_14).
        :param int color: The color of the text in hexadecimal format (e.g., 0xRRGGBB).
        :param int opa: The opacity of the text (0-255).

        UiFlow2 Code Block:

            |draw_label.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.draw_label("Hello, World!", x=10, y=20, font=lv.font_montserrat_14,
                                    color=0xFFFFFF, opa=255)
        """
        if not hasattr(self, "_label_dsc"):
            self._label_dsc = lv.draw_label_dsc_t()
        self._label_dsc.init()
        self._label_dsc.text = txt
        self._label_dsc.font = font
        self._label_dsc.color = lv.color_hex(color)
        self._label_dsc.opa = opa

        text_size = lv.point_t()
        lv.text_get_size(text_size, txt, font, 0, 0, lv.COORD.MAX, lv.TEXT_FLAG.NONE)
        self._area.x1 = x
        self._area.y1 = y
        self._area.x2 = x + text_size.x - 1
        self._area.y2 = y + text_size.y - 1

        lv.draw_label(self._layer, self._label_dsc, self._area)
        self.finish_layer(self._layer)

    def draw_triangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
        bg_c: int = 0xFFFFFF,
        bg_opa: int = lv.OPA.COVER,
    ):
        """Draw a triangle with the specified vertices.

        :param int x1: The x-coordinate of the first vertex.
        :param int y1: The y-coordinate of the first vertex.
        :param int x2: The x-coordinate of the second vertex.
        :param int y2: The y-coordinate of the second vertex.
        :param int x3: The x-coordinate of the third vertex.
        :param int y3: The y-coordinate of the third vertex.
        :param int bg_c: The background color of the triangle in hexadecimal format (e.g., 0xRRGGBB).
        :param int bg_opa: The opacity of the triangle (0-255).

        UiFlow2 Code Block:

            |draw_triangle.png|

        MicroPython Code Block:

            .. code-block:: python

                canvas_0.draw_triangle(10, 10, 50, 10, 30, 40, bg_c=0xFF0000, bg_opa=255)
        """
        if not hasattr(self, "_triangle_dsc"):
            self._triangle_dsc = lv.draw_triangle_dsc_t()
        self._triangle_dsc.init()

        self._triangle_dsc.bg_color = lv.color_hex(bg_c)
        self._triangle_dsc.bg_opa = bg_opa
        self._triangle_dsc.p[0].x = x1
        self._triangle_dsc.p[0].y = y1
        self._triangle_dsc.p[1].x = x2
        self._triangle_dsc.p[1].y = y2
        self._triangle_dsc.p[2].x = x3
        self._triangle_dsc.p[2].y = y3

        lv.draw_triangle(self._layer, self._triangle_dsc)
        self.finish_layer(self._layer)

    def set_style_radius(self, radius: int, part: int) -> None:
        if radius < 0:
            raise ValueError("Radius must be a non-negative integer.")
        super().set_style_radius(radius, part)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
