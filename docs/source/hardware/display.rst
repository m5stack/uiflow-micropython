.. _hardware.Display:

Display
=======

.. include:: ../refs/hardware.display.ref

A lcd display library

.. module:: Display
    :synopsis: A lcd display library


M5 Series Display Libraries
---------------------------

1. Display
^^^^^^^^^^^
- A low-level graphics library providing basic screen drawing, text, lines, and color management.
- Can be used independently, suitable for scenarios that only require drawing graphics or text.

2. M5Widgets
^^^^^^^^^^^^^
- A basic UI widget library providing labels, image displays, and other UI controls.
- Built on top of M5GFX.
- Suitable for simple interactive UI elements.

3. M5UI
^^^^^^^^
- A high-level UI framework based on LVGL.
- Provides page management, multi-widget layouts, and unified event handling.

Usage Tips
^^^^^^^^^^
- ⚠️ Do not mix M5GFX, M5Widgets, and M5UI simultaneously, as it may cause rendering issues or event conflicts.
- For graphics-only drawing → use M5GFX.
- For simple interactive widgets → use M5Widgets.
- For multi-page UI → use M5UI.


UiFlow2 Example
---------------

Basic Drawing
^^^^^^^^^^^^^

Open the |cores3_draw_test_example.m5f2| project in UiFlow2.

This example demonstrates basic drawing functions of Display, including text, images, QR code, and various shapes.

UiFlow2 Code Block:

    |cores3_draw_test_example.png|

Example output:

    None

Canvas Drawing
^^^^^^^^^^^^^^

Open the |cores3_display_canvas_example.m5f2| project in UiFlow2.

This example demonstrates how to create and use a canvas for drawing. It creates a canvas with 2-bit color depth, draws circles on it, and then pushes the canvas to the display.

UiFlow2 Code Block:

    |cores3_display_canvas_example.png|

Example output:

    None

MicroPython Example
-------------------

Basic Drawing
^^^^^^^^^^^^^

This example demonstrates basic drawing functions of Display, including text, images, QR code, and various shapes.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/display/cores3_draw_test_example.py
        :language: python
        :linenos:

Example output:

    None

Canvas Drawing
^^^^^^^^^^^^^^

This example demonstrates how to create and use a canvas for drawing. It creates a canvas with 2-bit color depth, draws circles on it, and then pushes the canvas to the display.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/display/cores3_display_canvas_example.m5f2.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

.. class:: M5.Display

    .. method:: width()

        Get the horizontal resolution of the display.

        :returns width: horizontal resolution in pixels.
        :return type: int

        UiFlow2 Code Block:

            |width.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.width()

    .. method:: height()

        Get the vertical resolution of the display.

        :returns height: vertical resolution in pixels.
        :return type: int

        UiFlow2 Code Block:

            |height.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.height()

    .. method:: getRotation()

        Get the current rotation of the display.

        :returns rotation: display rotation value.
        :return type: int

        Rotation values:

        - 1: 0° rotation
        - 2: 90° rotation
        - 3: 180° rotation
        - 4: 270° rotation

        UiFlow2 Code Block:

            |getrotation.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.getRotation()

    .. method:: getColorDepth()

        Get the color depth of the display.

        :returns depth: color depth in bits per pixel.
        :return type: int

        UiFlow2 Code Block:

            |getcolordepth.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.getColorDepth()

    .. method:: getCursor()

        Get the current cursor position on the display.

        :returns pos: tuple (x, y) of cursor position.
        :return type: tuple

        UiFlow2 Code Block:

            |getcursor.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.getCursor()

    .. method:: setRotation(r)

        Set the rotation of the display.

        :param int r: rotation value (1~4)
            - 1: 0° rotation
            - 2: 90° rotation
            - 3: 180° rotation
            - 4: 270° rotation

        UiFlow2 Code Block:

            |setrotation.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setRotation(2)

    .. method:: setColorDepth(bpp)

        Set the color depth of the canvas.

        :param int bpp: desired color depth in bits per pixel.

        Notes: This method only applies to canvas objects, not the display itself. For CoreS3 devices, the display color depth is fixed at 16 bits.

        UiFlow2 Code Block:

            |setcolordepth.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setColorDepth(16)

    .. method:: setEpdMode(epd_mode)

        Set the EPD mode for the display.

        :param int epd_mode: desired EPD mode
            - 0: M5.Lcd.EPDMode.EPD_QUALITY
            - 1: M5.Lcd.EPDMode.EPD_TEXT
            - 2: M5.Lcd.EPDMode.EPD_FAST
            - 3: M5.Lcd.EPDMode.EPD_FASTEST

        Notes: Only applicable to devices with EPD capabilities.

        UiFlow2 Code Block:

            |setepdmode.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setEpdMode(2)

    .. method:: isEPD()

        Check if the display is an EPD (Electronic Paper Display).

        :returns is_epd: True if the display is EPD, False otherwise.
        :return type: bool

        UiFlow2 Code Block:

            |isepd.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.isEPD()

    .. method:: setFont(font)

        Set the font for the display.

        :param font: font type. Available options:

            - M5.Lcd.FONTS.ASCII7
            - M5.Lcd.FONTS.DejaVu9
            - M5.Lcd.FONTS.DejaVu12
            - M5.Lcd.FONTS.DejaVu18
            - M5.Lcd.FONTS.DejaVu24
            - M5.Lcd.FONTS.DejaVu40
            - M5.Lcd.FONTS.DejaVu56
            - M5.Lcd.FONTS.DejaVu72
            - M5.Lcd.FONTS.EFontCN24
            - M5.Lcd.FONTS.EFontJA24
            - M5.Lcd.FONTS.EFontKR24

        UiFlow2 Code Block:

            |setfont.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setFont(M5.Lcd.FONTS.DejaVu18)

    .. method:: setTextColor(fgcolor, bgcolor)

        Set the text color and background color.

        :param int fgcolor: text color in RGB888 format (default 0, black)
        :param int bgcolor: background color in RGB888 format (default 0, black)

        UiFlow2 Code Block:

            |settextcolor.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setTextColor(0xFF0000, 0x000000)

    .. method:: setTextScroll(scroll)

        Enable or disable text scrolling.

        :param bool scroll: True to enable text scrolling, False to disable (default False)

        UiFlow2 Code Block:

            |settextscroll.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setTextScroll(True)

    .. method:: setTextSize(size)

        Set the size of the text.

        :param int size: desired text size

        UiFlow2 Code Block:

            |settextsize.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setTextSize(2)

    .. method:: setCursor(x, y)

        Set the cursor position.

        :param int x: horizontal position of the cursor (default 0)
        :param int y: vertical position of the cursor (default 0)

        UiFlow2 Code Block:

            |setcursor.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.setCursor(10, 20)

    .. method:: clear(color)

        Clear the display with a specific color.

        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |clear.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.clear(0xFFFFFF)

    .. method:: fillScreen(color)

        Fill the entire screen with a specified color.

        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillscreen.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillScreen(0xFF0000)

    .. method:: drawPixel(x, y, color)

        Draw a single pixel on the screen.

        :param int x: horizontal coordinate of the pixel (default -1)
        :param int y: vertical coordinate of the pixel (default -1)
        :param int color: pixel color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawpixel.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawPixel(50, 50, 0x00FF00)

    .. method:: drawCircle(x, y, r, color)

        Draw an outline of a circle.

        :param int x: x-coordinate of circle center (default -1)
        :param int y: y-coordinate of circle center (default -1)
        :param int r: radius of the circle (default -1)
        :param int color: circle color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawcircle.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawCircle(60, 60, 20, 0x0000FF)

    .. method:: fillCircle(x, y, r, color)

        Draw a filled circle.

        :param int x: x-coordinate of circle center (default -1)
        :param int y: y-coordinate of circle center (default -1)
        :param int r: radius of the circle (default -1)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillcircle.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillCircle(60, 60, 20, 0x00FFFF)

    .. method:: drawEllipse(x, y, rx, ry, color)

        Draw an outline of an ellipse.

        :param int x: x-coordinate of ellipse center (default -1)
        :param int y: y-coordinate of ellipse center (default -1)
        :param int rx: horizontal radius (default -1)
        :param int ry: vertical radius (default -1)
        :param int color: ellipse color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawellipse.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawEllipse(80, 40, 30, 20, 0xFF00FF)

    .. method:: fillEllipse(x, y, rx, ry, color)

        Draw a filled ellipse.

        :param int x: x-coordinate of ellipse center (default -1)
        :param int y: y-coordinate of ellipse center (default -1)
        :param int rx: horizontal radius (default -1)
        :param int ry: vertical radius (default -1)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillellipse.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillEllipse(80, 40, 30, 20, 0x00FF00)

    .. method:: drawLine(x0, y0, x1, y1, color)

        Draw a line.

        :param int x0: starting x-coordinate (default -1)
        :param int y0: starting y-coordinate (default -1)
        :param int x1: ending x-coordinate (default -1)
        :param int y1: ending y-coordinate (default -1)
        :param int color: line color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawline.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawLine(10, 10, 100, 100, 0xFF0000)

    .. method:: drawRect(x, y, w, h, color)

        Draw a rectangle.

        :param int x: top-left x-coordinate (default -1)
        :param int y: top-left y-coordinate (default -1)
        :param int w: width of rectangle (default -1)
        :param int h: height of rectangle (default -1)
        :param int color: rectangle color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawrect.png|

        MicroPython Code Block:

            .. code-block:: python

                display.drawRect(20, 20, 80, 50, 0x00FF00)

    .. method:: fillRect(x, y, w, h, color)

        Draw a filled rectangle.

        :param int x: top-left x-coordinate (default -1)
        :param int y: top-left y-coordinate (default -1)
        :param int w: width of rectangle (default -1)
        :param int h: height of rectangle (default -1)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillrect.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillRect(20, 20, 80, 50, 0x0000FF)

    .. method:: drawRoundRect(x, y, w, h, r, color)

        Draw a rounded rectangle.

        :param int x: top-left x-coordinate (default -1)
        :param int y: top-left y-coordinate (default -1)
        :param int w: width of rectangle (default -1)
        :param int h: height of rectangle (default -1)
        :param int r: corner radius (default -1)
        :param int color: rectangle color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawroundrect.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawRoundRect(30, 30, 60, 40, 10, 0xFF00FF)

    .. method:: fillRoundRect(x, y, w, h, r, color)

        Draw a filled rounded rectangle.

        :param int x: top-left x-coordinate (default -1)
        :param int y: top-left y-coordinate (default -1)
        :param int w: width of rectangle (default -1)
        :param int h: height of rectangle (default -1)
        :param int r: corner radius (default -1)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillroundrect.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillRoundRect(30, 30, 60, 40, 10, 0x00FFFF)

    .. method:: drawTriangle(x0, y0, x1, y1, x2, y2, color)

        Draw a triangle.

        :param int x0: first vertex x-coordinate (default -1)
        :param int y0: first vertex y-coordinate (default -1)
        :param int x1: second vertex x-coordinate (default -1)
        :param int y1: second vertex y-coordinate (default -1)
        :param int x2: third vertex x-coordinate (default -1)
        :param int y2: third vertex y-coordinate (default -1)
        :param int color: triangle color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawtriangle.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawTriangle(10, 10, 50, 80, 90, 10, 0xFF0000)

    .. method:: fillTriangle(x0, y0, x1, y1, x2, y2, color)

        Draw a filled triangle.

        :param int x0: first vertex x-coordinate (default -1)
        :param int y0: first vertex y-coordinate (default -1)
        :param int x1: second vertex x-coordinate (default -1)
        :param int y1: second vertex y-coordinate (default -1)
        :param int x2: third vertex x-coordinate (default -1)
        :param int y2: third vertex y-coordinate (default -1)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |filltriangle.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillTriangle(10, 10, 50, 80, 90, 10, 0x00FF00)

    .. method:: drawArc(x, y, r0, r1, angle0, angle1, color)

        Draw an arc.

        :param int x: center x-coordinate (default -1)
        :param int y: center y-coordinate (default -1)
        :param int r0: first radius (default -1)
        :param int r1: second radius (default -1)
        :param int angle0: starting angle in degrees (default -1)
        :param int angle1: ending angle in degrees (default -1)
        :param int color: arc color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawarc.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawArc(50, 50, 20, 30, 0, 180, 0xFF0000)

    .. method:: fillArc(x, y, r0, r1, angle0, angle1, color)

        Draw a filled arc.

        :param int x: center x-coordinate (default -1)
        :param int y: center y-coordinate (default -1)
        :param int r0: first radius (default -1)
        :param int r1: second radius (default -1)
        :param int angle0: starting angle in degrees (default -1)
        :param int angle1: ending angle in degrees (default -1)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillarc.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillArc(50, 50, 20, 30, 0, 180, 0x00FF00)

    .. method:: drawEllipseArc(x, y, r0x, r1x, r0y, r1y, angle0, angle1, color)

        Draw an elliptical arc.

        :param int x: center x-coordinate (default -1)
        :param int y: center y-coordinate (default -1)
        :param int r0x: first horizontal radius (default -1)
        :param int r1x: second horizontal radius (default -1)
        :param int r0y: first vertical radius (default -1)
        :param int r1y: second vertical radius (default -1)
        :param int angle0: starting angle in degrees (default -1)
        :param int angle1: ending angle in degrees (default 0)
        :param int color: arc color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |drawellipsearc.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawEllipseArc(50, 50, 20, 40, 10, 30, 0, 180, 0xFF00FF)

    .. method:: fillEllipseArc(x, y, r0x, r1x, r0y, r1y, angle0, angle1, color)

        Draw a filled elliptical arc.

        :param int x: center x-coordinate (default -1)
        :param int y: center y-coordinate (default -1)
        :param int r0x: first horizontal radius (default -1)
        :param int r1x: second horizontal radius (default -1)
        :param int r0y: first vertical radius (default -1)
        :param int r1y: second vertical radius (default -1)
        :param int angle0: starting angle in degrees (default -1)
        :param int angle1: ending angle in degrees (default 0)
        :param int color: fill color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |fillellipsearc.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.fillEllipseArc(50, 50, 20, 40, 10, 30, 0, 180, 0x00FFFF)

    .. method:: drawQR(text, x, y, w, version)

        Draw a QR code.

        :param str text: QR code content
        :param int x: x-coordinate to display (default 0)
        :param int y: y-coordinate to display (default 0)
        :param int w: QR code width (default 0)
        :param int version: QR code version (default 1, range: 0~38)

        UiFlow2 Code Block:

            |drawqr.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawQR("Hello", 0, 0, 200)

    .. method:: drawPng(img, x, y, maxW, maxH, offX, offY, scaleX, scaleY)

        Draw a PNG image.

        :param str img: image path or data
        :param int x: display x-coordinate (default 0)
        :param int y: display y-coordinate (default 0)
        :param int maxW: max width to draw (default 0)
        :param int maxH: max height to draw (default 0)
        :param int offX: x-offset in image (default 0)
        :param int offY: y-offset in image (default 0)
        :param bool scaleX: scale horizontally (default True)
        :param bool scaleY: scale vertically (default False)

        UiFlow2 Code Block:

            |drawpng.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawPng("res/img/uiflow.png", 0, 0)

        Example:

            .. code-block:: python

                Display.drawPng("res/img/uiflow.png", 0, 0)
                img = open("res/img/uiflow.png", "b")
                img.seek(0)
                Display.drawPng(img.read(), 0, 100)
                img.close()

    .. method:: drawJpg(img, x, y, maxW, maxH, offX, offY)

        Draw a JPG image.

        :param img: image path or data
        :param int x: display x-coordinate (default 0)
        :param int y: display y-coordinate (default 0)
        :param int maxW: max width to draw (default 0)
        :param int maxH: max height to draw (default 0)
        :param int offX: x-offset in image (default 0)
        :param int offY: y-offset in image (default 0)

        UiFlow2 Code Block:

            |drawjpg.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawJpg("res/img/uiflow.jpg", 0, 0)

        Example:

            .. code-block:: python

                Display.drawJpg("res/img/uiflow.jpg", 0, 0)
                img = open("res/img/uiflow.jpg", "b")
                img.seek(0)
                Display.drawJpg(img.read(), 0, 100)
                img.close()

    .. method:: drawBmp(img, x, y, maxW, maxH, offX, offY)

        Draw a BMP image.

        :param img: image path or data
        :param int x: display x-coordinate (default 0)
        :param int y: display y-coordinate (default 0)
        :param int maxW: max width to draw (default 0)
        :param int maxH: max height to draw (default 0)
        :param int offX: x-offset in image (default 0)
        :param int offY: y-offset in image (default 0)

        UiFlow2 Code Block:

            |drawbmp.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawBmp("res/img/uiflow.bmp", 0, 0)

        Example:

            .. code-block:: python

                Display.drawBmp("res/img/uiflow.bmp", 0, 0)
                img = open("res/img/uiflow.bmp", "b")
                img.seek(0)
                Display.drawBmp(img.read(), 0, 100)
                img.close()

    .. method:: drawImage(img, x, y, maxW, maxH, offX, offY)

        Draw an image.

        :param img: image path or data
        :param int x: display x-coordinate (default 0)
        :param int y: display y-coordinate (default 0)
        :param int maxW: max width to draw (default 0)
        :param int maxH: max height to draw (default 0)
        :param int offX: x-offset in image (default 0)
        :param int offY: y-offset in image (default 0)

        UiFlow2 Code Block:

            |drawimage.png|

        MicroPython Code Block:

            .. code-block:: python

                img = open("res/img/uiflow.jpg", "b")

        Example:

            .. code-block:: python

                img = open("res/img/uiflow.jpg", "b")
                img.seek(0)
                Display.drawImage(img.read(), 0, 0)
                img.close()

    .. method:: drawRawBuf(buf, x, y, w, h, len, swap)

        Draw an image from raw buffer data.

        :param buf: image buffer
        :param int x: display x-coordinate (default 0)
        :param int y: display y-coordinate (default 0)
        :param int w: image width (default 0)
        :param int h: image height (default 0)
        :param int len: length of image data (default 0)
        :param bool swap: inverted display (default False)

        UiFlow2 Code Block:

            |drawrawbuf.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.drawRawBuf(raw_buf, 0, 0, 100, 100, len(raw_buf), swap=False)

        Example:

            .. code-block:: python

                width, height = 40, 30
                green565 = 0x07E0
                raw_buf = bytearray(width * height * 2)
                for i in range(width * height):
                    raw_buf[2*i]   = (green565 >> 8) & 0xFF
                    raw_buf[2*i+1] = green565 & 0xFF
                Display.drawRawBuf(raw_buf, 100, 100, width, height, len(raw_buf), swap=False)

    .. method:: print(text, color)

        Display a string (no formatting support).

        :param str text: text to display
        :param int color: color in RGB888 format (default 0)

        UiFlow2 Code Block:

            |print.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.print("Hello World", color=0xFF0000)

    .. method:: printf(text)

        Display a formatted string.

        :param str text: text to display with formatting

        UiFlow2 Code Block:

            |printf.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.printf("Value: %d" % 100)

    .. method:: newCanvas(w, h, bpp, psram)

        Create a canvas.

        :param int w: canvas width
        :param int h: canvas height
        :param int bpp: color depth (default -1)
        :param bool psram: use PSRAM (default False)
        :returns: created canvas object

        UiFlow2 Code Block:

            |newcanvas.png|

        MicroPython Code Block:

            .. code-block:: python

                w1 = Display.newCanvas(w=100, h=100, bpp=16)

        Example:

            .. code-block:: python

                w1 = Display.newCanvas(w=100, h=100, bpp=16)
                w1.drawImage("res/img/uiflow.jpg", 80, 0)
                w1.push(30, 0)

    .. method:: startWrite()

        Start writing to the display.

        UiFlow2 Code Block:

            |startwrite.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.startWrite()

        Example:

            .. code-block:: python

                Display.startWrite()
                Display.drawPixel(10, 10, 0xFF0000)
                Display.endWrite()

    .. method:: endWrite()

        End writing to the display.

        UiFlow2 Code Block:

            |endwrite.png|

        MicroPython Code Block:

            .. code-block:: python

                Display.endWrite()

