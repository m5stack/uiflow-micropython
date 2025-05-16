.. _hardware.Display:

Display
=======

A lcd display library

.. module:: Display
    :synopsis: A lcd display library


Micropython Example
-------------------

draw test
+++++++++

::

    import M5
    from M5 import Display
    import random
    import time

    M5.begin()

    print("rotation: ", Display.getRotation())
    print("color depth: ", Display.getColorDepth())
    print("w: %d, h: %d"%(Display.width(), Display.height()))

    Display.setRotation(1)
    Display.clear(0)
    Display.setTextColor(fgcolor=0x0000FF, bgcolor=0)
    Display.setFont(M5.Lcd.FONTS.EFontCN24)
    Display.setCursor(220, 3)
    Display.print("你好",color=0xFF0000)

    Display.drawImage("res/img/uiflow.jpg", 0, 0)
    Display.drawJpg("res/img/default.jpg", 60, 0)

    Display.drawQR("Hello", 220, 40, 100)

    Display.drawCircle(30, 80, 20, 0x0000FF)
    Display.fillCircle(80, 80, 20, 0x0000FF)

    Display.drawEllipse(60, 140, 50, 30, 0x00FF00)
    Display.fillEllipse(60, 140, 30, 20, 0xFFFF00)

    Display.drawLine(x0=115, y0=10, x1=115, y1=60, color=0xFF0000)

    Display.drawRect(125, 10, 40, 30, 0xFF0000)
    Display.fillRect(125, 50, 40, 30, 0x00FF00)

    Display.drawRoundRect(120, 90, 50, 40, 10, 0xFF0000)
    Display.fillRoundRect(125, 95, 40, 30, 10, 0x00FF00)

    Display.drawTriangle(135, 150, 110, 190, 160, 190, 0x00FF00)
    Display.fillTriangle(145, 150, 170, 190, 190, 150, 0x0000FF)

    Display.drawArc(10, 180, 40, 45, 0, 90, 0xFFFF00)
    Display.fillArc(20, 190, 40, 45, 0, 90, 0x00FFFF)

    Display.drawEllipseArc(200, 150, 30, 35, 20, 25, 0, 90, 0x00FF0F)
    Display.fillEllipseArc(200, 170, 30, 35, 20, 25, 0, 90, 0x00FFF0)


Functions
---------

.. method:: Display.width() -> int

    Get the horizontal resolution of the display.

    Returns An integer representing the horizontal resolution (width) in pixels.

.. method:: Display.height() -> int

    Get the vertical resolution of the display.

    Returns An integer representing the vertical resolution (height) in pixels.

.. method:: Display.getRotation() -> int

    Get the current rotation of the display.

    Returns An integer representing the display's rotation:

    - ``1``: 0° rotation
    - ``2``: 90° rotation
    - ``3``: 180° rotation
    - ``4``: 270° rotation

.. method:: Display.getColorDepth() -> int

    Get the color depth of the display.

    Returns An integer representing the display's color depth in bits.

.. method::Display.getCursor() -> Tuple[int, int]

    Get the current cursor position on the display.

    Returns A tuple (x, y) where:

    - ``x`` is the horizontal position of the cursor.
    - ``y`` is the vertical position of the cursor.

.. method:: Display.setRotation(r: int = -1)

    Set the rotation of the display.

    The ``r`` parameter only accepts the following values:

    - ``1``: 0° rotation
    - ``2``: 90° rotation
    - ``3``: 180° rotation
    - ``4``: 270° rotation

.. method:: Display.setColorDepth(bpp: int = 1)

    Set the color depth of the display.

    - ``bpp`` The desired color depth in bits per pixel.

    Notes: For CoreS3 devices, the color depth is fixed at 16 bits, and this method has no effect.

.. method:: Display.setEpdMode(epd_mode)

    Set the EPD mode for the display.

    - ``epd_mode`` The desired EPD mode.
        - 0: M5.Lcd.EPDMode.EPD_QUALITY 
        - 1: M5.Lcd.EPDMode.EPD_TEXT
        - 2: M5.Lcd.EPDMode.EPD_FAST
        - 3: M5.Lcd.EPDMode.EPD_FASTEST

    Notes: This method is only applicable to devices with EPD (Electronic Paper Display) capabilities.

.. method:: Display.isEPD() -> bool

    Check if the display is an EPD (Electronic Paper Display).

    Returns A boolean indicating whether the display is an EPD.

.. method:: Display.setFont(font)

    Set the font for the display.

    The ``font`` parameter only accepts the following values:

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

.. method:: Display.setTextColor(fgcolor: int = 0, bgcolor: int = 0)

    Set the text color and background color.

    - ``fgcolor`` The text color in RGB888 format. Default is 0 (black).
    - ``bgcolor`` The background color in RGB888 format. Default is 0 (black).

.. method:: Display.setTextScroll(scroll: bool = False)

    Enable or disable text scrolling.

    - ``scroll`` Set to True to enable text scrolling, or False to disable it. Default is False.\

.. method:: Display.setTextSize(size)

    Set the size of the text.

    - ``size`` The desired text size.

.. method:: Display.setCursor(x: int = 0, y: int = 0)

    Set the cursor position.

    - ``x`` The horizontal position of the cursor. Default is 0.
    - ``y`` The vertical position of the cursor. Default is 0.

.. method:: Display.clear(color: int = 0)

    Clear the display with a specific color.

    - ``color`` The fill color in RGB888 format. Default is 0.

.. method:: Display.fillScreen(color: int = 0)

    Fill the entire screen with a specified color.

    - ``color`` The fill color in RGB888 format. Default is 0.


.. method:: Display.drawPixel(x: int = -1, y: int = -1, color: int = 0)

    Draw a single pixel on the screen.

    - ``x`` The horizontal coordinate of the pixel. Default is -1.
    - ``y`` The vertical coordinate of the pixel. Default is -1.
    - ``color`` The color of the pixel in RGB888 format. Default is 0.

.. method:: Display.drawCircle(x: int = -1, y: int = -1, r: int = -1, color: int = 0)

    Draw an outline of a circle.

    - ``x`` The x-coordinate of the circle center. Default is -1.
    - ``y`` The y-coordinate of the circle center. Default is -1.
    - ``r`` The radius of the circle. Default is -1.
    - ``color`` The color of the circle in RGB888 format. Default is 0.

.. method:: Display.fillCircle(x: int = -1, y: int = -1, r: int = -1, color: int = 0)

    Draw a filled circle.

    - ``x`` The x-coordinate of the circle center. Default is -1.
    - ``y`` The y-coordinate of the circle center. Default is -1.
    - ``r`` The radius of the circle. Default is -1.
    - ``color`` The fill color in RGB888 format. Default is 0.

.. method:: Display.drawEllipse(x: int = -1, y: int = -1, rx: int = -1, ry: int = -1, color: int = 0)

    Draw an outline of an ellipse.

    - ``x`` The x-coordinate of the ellipse center. Default is -1.
    - ``y`` The y-coordinate of the ellipse center. Default is -1.
    - ``rx`` The horizontal radius of the ellipse. Default is -1.
    - ``ry`` The vertical radius of the ellipse. Default is -1.
    - ``color`` The color of the ellipse in RGB888 format. Default is 0.

.. method:: Display.fillEllipse(x: int = -1, y: int = -1, rx: int = -1, ry: int = -1, color: int = 0)

    Draw a filled ellipse.

    - ``x`` The x-coordinate of the ellipse center. Default is -1.
    - ``y`` The y-coordinate of the ellipse center. Default is -1.
    - ``rx`` The horizontal radius of the ellipse. Default is -1.
    - ``ry`` The vertical radius of the ellipse. Default is -1.
    - ``color`` The fill color in RGB888 format. Default is 0.

.. method:: Display.drawLine(x0: int = -1, y0: int = -1, x1: int = -1, y1: int = -1, color: int = 0)

    Draw a line.

    - ``x0, y0`` Starting point coordinates of the line. Default is -1.
    - ``x1, y1`` Ending point coordinates of the line. Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.drawRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, color: int = 0)

    Draw a rectangle.

    - ``x, y`` Top-left corner coordinates of the rectangle. Default is -1.
    - ``w, h`` Width and height of the rectangle. Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.fillRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, color: int = 0)

    Draw a filled rectangle.

    - ``x, y`` Top-left corner coordinates of the rectangle. Default is -1.
    - ``w, h`` Width and height of the rectangle. Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.drawRoundRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, r: int = -1, color: int = 0)

    Draw a rounded rectangle.

    - ``x, y`` Top-left corner coordinates of the rectangle. Default is -1.
    - ``w, h`` Width and height of the rectangle. Default is -1.
    - ``r`` Radius of the corners. Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.fillRoundRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, r: int = -1, color: int = 0)

    Draw a filled rounded rectangle.

    - ``x, y`` Top-left corner coordinates of the rectangle. Default is -1.
    - ``w, h`` Width and height of the rectangle. Default is -1.
    - ``r`` Radius of the corners. Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.


.. method:: Display.drawTriangle(x0: int = -1, y0: int = -1, x1: int = -1, y1: int = -1, x2: int = -1, y2: int = -1, color: int = 0)

    Draw a triangle.

    - ``x0, y0`` Coordinates of the first vertex. Default is -1.
    - ``x1, y1`` Coordinates of the second vertex. Default is -1.
    - ``x2, y2`` Coordinates of the third vertex. Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.fillTriangle(x0: int = -1, y0: int = -1, x1: int = -1, y1: int = -1, x2: int = -1, y2: int = -1, color: int = 0)

    Draw a filled triangle.

    - ``x0, y0`` Coordinates of the first vertex. Default is -1.
    - ``x1, y1`` Coordinates of the second vertex. Default is -1.
    - ``x2, y2`` Coordinates of the third vertex. Default is -1.
    - ``color:`` Color in RGB888 format. Default is 0.

.. method:: Display.drawArc(x: int = -1, y: int = -1, r0: int = -1, r1: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    Draw an arc.

    - ``x, y`` Center coordinates of the arc. Default is -1.
    - ``r0`` Inner radius of the arc. Default is -1.
    - ``r1`` Outer radius of the arc. Default is -1.
    - ``angle0`` Starting angle of the arc (in degrees). Default is -1.
    - ``angle1`` Ending angle of the arc (in degrees). Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.fillArc(x: int = -1, y: int = -1, r0: int = -1, r1: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    Draw a filled arc.

    - ``x, y`` Center coordinates of the arc. Default is -1.
    - ``r0`` Inner radius of the arc. Default is -1.
    - ``r1`` Outer radius of the arc. Default is -1.
    - ``angle0`` Starting angle of the arc (in degrees). Default is -1.
    - ``angle1`` Ending angle of the arc (in degrees). Default is -1.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.drawEllipseArc(x: int = -1, y: int = -1, r0x: int = -1, r0y: int = -1, r1x: int = -1, r1y: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    Draw an elliptical arc.

    - ``x, y`` Center coordinates of the elliptical arc. Default is -1.
    - ``r0x, r0y`` Radii of the inner ellipse (horizontal and vertical). Default is -1.
    - ``r1x, r1y`` Radii of the outer ellipse (horizontal and vertical). Default is -1.
    - ``angle0`` Starting angle of the arc (in degrees). Default is -1.
    - ``angle1`` Ending angle of the arc (in degrees). Default is 0.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.fillEllipseArc(x: int = -1, y: int = -1, r0x: int = -1, r0y: int = -1, r1x: int = -1, r1y: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    Draw a filled elliptical arc.

    - ``x, y`` Center coordinates of the elliptical arc. Default is -1.
    - ``r0x, r0y`` Radii of the inner ellipse (horizontal and vertical). Default is -1.
    - ``r1x, r1y`` Radii of the outer ellipse (horizontal and vertical). Default is -1.
    - ``angle0`` Starting angle of the arc (in degrees). Default is -1.
    - ``angle1`` Ending angle of the arc (in degrees). Default is -1.
    - ``color:`` Color in RGB888 format. Default is 0.

.. method:: Display.drawQR(text: str = None, x: int = 0, y: int = 0, w: int = 0, version: int = 1)

    Draw a QR code.

    - ``text`` QR code content.
    - ``x, y`` Starting coordinates for displaying the QR code.
    - ``w:`` Width of the QR code. Default is 0.
    - ``version`` QR code version. Default is 1.

    **Example**:

    Generate and display a QR code with the content "hello":

    .. code-block:: python

        Display.drawQR("Hello", 0, 0, 200)

.. method:: Display.drawPng(img: str, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0, scaleX=True, scaleY=False)

    Draw a PNG image.

    - ``img`` Image file path or opened image data.
    - ``x, y`` Starting coordinates on the display screen.
    - ``maxW, maxH`` Width and height to be drawn. Draws the full image if ≤0.
    - ``offX, offY`` Offset in the image to start from.
    - ``scaleX, scaleY`` Whether to scale the image horizontally or vertically.

    **Examples**:

    Display a PNG image from a specified path:

    .. code-block:: python

        Display.drawPng("res/img/uiflow.png", 0, 0)

    Display a PNG image from read data:

    .. code-block:: python

        img = open("res/img/uiflow.png", "b")
        img.seek(0)
        Display.drawPng(img.read(), 0, 100)
        img.close()

.. method:: Display.drawJpg(img, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0)

    Draw a JPG image.

    - ``img`` Image file path or opened image data.
    - ``x, y`` Starting coordinates on the display screen.
    - ``maxW, maxH`` Width and height to be drawn. Draws the full image if ≤0.
    - ``offX, offY`` Offset in the image to start from.

.. method:: Display.drawBmp(img: str, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0)

    Draw a BMP image.

    - ``img`` Image file path or opened image data.
    - ``x, y`` Starting coordinates on the display screen.
    - ``maxW, maxH`` Width and height to be drawn. Draws the full image if ≤0.
    - ``offX, offY`` Offset in the image to start from.

.. method:: Display.drawImage(img: str, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0)

    Draw an image.

    - ``img`` Image file path or opened image data.
    - ``x, y`` Starting coordinates on the display screen.
    - ``maxW, maxH`` Width and height to be drawn. Draws the full image if ≤0.
    - ``offX, offY`` Offset in the image to start from.

    **Example**:

    Draw an image from the buffer:

    .. code-block:: python

        img = open(img_path)
        img.seek(0)
        drawImage(img.read())

.. method:: Display.drawRawBuf(buf, x: int = 0, y: int = 0, w: int = 0, h: int = 0, len: int = 0, swap: bool = False)

    Draw an image from raw buffer data.

    - ``buf`` Image buffer.
    - ``x, y`` Starting coordinates on the display screen.
    - ``w, h`` Width and height of the image.
    - ``len`` Length of the image data.
    - ``swap`` Whether to enable inverted display.

.. method:: Display.print(text: str = None, color: int = 0)

    Display a string (no formatting support).

    - ``text`` Text to display.
    - ``color`` Color in RGB888 format. Default is 0.

.. method:: Display.printf(text: str = None)

    Display a formatted string.

    - ``text`` Text to display with formatting.

.. method:: Display.newCanvas(w: int = 0, h: int = 0, bpp: int = -1, psram: bool = False)

    Create a canvas.

    - ``w, h`` Width and height of the canvas.
    - ``bpp`` Color depth. Default is -1.
    - ``psram`` Whether to use PSRAM. Default is False.

    Returns Created canvas object.

    **Example**:

    .. code-block:: python

        w1 = Display.newCanvas(w=100, h=100, bpp=16)
        w1.drawImage("res/img/uiflow.jpg", 80, 0)
        w1.push(30, 0)

.. method:: Display.startWrite()

    Start writing to the display.

.. method:: Display.endWrite()

    End writing to the display.
