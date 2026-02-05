:mod:`Display`   
==============
显示屏显示库

.. include:: ../refs/hardware.display.ref

.. module:: Display
    :synopsis: A lcd display library

UiFlow2 示例
------------

基本绘图
^^^^^^^

在 UiFlow2 中打开 |cores3_draw_test_example.m5f2| 项目。

此示例演示了 Display 的基本绘图功能，包括文本、图片、二维码以及各种形状。

UiFlow2 代码块：

    |cores3_draw_test_example.png|

示例输出：

    无

画布使用
^^^^^^^

在 UiFlow2 中打开 |cores3_display_canvas_example.m5f2| 项目。

此示例演示了如何创建和使用画布进行绘图。它创建一个 2 位颜色深度的画布，在上面绘制圆形，然后将画布推送到显示屏。

UiFlow2 代码块：

    |cores3_display_canvas_example.png|

示例输出：

    无

MicroPython 示例
----------------

基本绘图
^^^^^^^^

此示例演示了 Display 的基本绘图功能，包括文本、图片、二维码以及各种形状。

MicroPython 代码块：

    .. literalinclude:: ../../../examples/hardware/display/cores3_draw_test_example.py
        :language: python
        :linenos:

示例输出：

    无

画布绘图
^^^^^^^^

此示例演示了如何创建和使用画布进行绘图。它创建一个 2 位颜色深度的画布，在上面绘制圆形，然后将画布推送到显示屏。

MicroPython 代码块：

    .. literalinclude:: ../../../examples/hardware/display/cores3_display_canvas_example.m5f2.py
        :language: python
        :linenos:

示例输出：

    无


API 应用
^^^^^^^^

.. function:: Display.width() -> int

    获取显示屏水平分辨率。

    返回一个整数，表示显示屏的水平分辨率（宽度）以像素为单位。

.. function:: Display.height() -> int
    
    获取显示屏垂直分辨率。

    返回一个整数，表示显示屏的垂直分辨率（高度）以像素为单位。

.. function:: Display.getRotation() -> int

    获取显示屏旋转方向。 

    返回一个整数，表示显示屏的旋转方向，对应角度如下:

    - ``1``: 0° rotation
    - ``2``: 90° rotation
    - ``3``: 180° rotation
    - ``4``: 270° rotation

.. function:: Display.getColorDepth() -> int

    获取显示屏颜色深度。

    返回一个整数，表示显示屏的颜色深度（位数）。 

.. function::Display.getCursor() -> Tuple[int, int]

    获取显示屏绘图光标位置。 

    返回一个元组 (x, y)，其中：

    - ``x``表示光标的水平位置  
    - ``y``表示光标的垂直位置  


.. function:: Display.setRotation(r: int = -1)

    设置显示屏旋转。 

    参数 ``r`` 仅接受以下值：  

    - ``0``: 0° rotation
    - ``1``: 90° rotation
    - ``2``: 180° rotation
    - ``3``: 270° rotation

.. function:: Display.setColorDepth(bpp: int = 1)

    设置画布的颜色深度。

    - ``bpp`` 期望的颜色深度，单位为每像素的位数。  
    
    注意：此方法仅对画布（canvas）对象有效，不对显示屏本身生效。对于 CoreS3 设备，显示屏的颜色深度固定为 16 位。 

.. function:: Display.setFont(font)

    设置显示字体。 

    参数 ``font`` 仅接受以下值：  

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

.. function:: Display.setTextColor(fgcolor: int = 0, bgcolor: int = 0)

    设置文本颜色和背景颜色。

    - ``fgcolor`` 文本颜色，RGB888 格式。默认值为 0（黑色）。
    - ``bgcolor`` 背景颜色，RGB888 格式。默认值为 0（黑色）。  

.. function:: Display.setTextScroll(scroll: bool = False)

    - ``scroll`` 设置为 True 启用文本滚动，设置为 False 禁用文本滚动。默认值为 False。

.. function:: Display.setTextSize(size)

    设置文本的大小。 

.. function:: Display.setCursor(x: int = 0, y: int = 0)

    设置光标位置。

    - ``x`` 光标的水平位置。默认值为 0。  
    - ``y`` 光标的垂直位置。默认值为 0。  

.. function:: Display.clear(color: int = 0)

    使用指定颜色 ``color`` 清空显示屏，RGB888 格式。默认值为 0。  

.. function:: Display.fillScreen(color: int = 0)

    使用指定颜色 ``color`` 填充整个屏幕，RGB888 格式。默认值为 0。  

.. function:: Display.drawPixel(x: int = -1, y: int = -1, color: int = 0)

    在屏幕上绘制单个像素。

    - ``x`` 像素的水平坐标。默认值为 -1。  
    - ``y``  像素的垂直坐标。默认值为 -1。  
    - ``color`` 像素的颜色，RGB888 格式。默认值为 0。  

.. function:: Display.drawCircle(x: int = -1, y: int = -1, r: int = -1, color: int = 0)

    绘制一个圆。

    - ``x`` 圆心的 x 坐标。默认值为 -1。  
    - ``y`` 圆心的 y 坐标。默认值为 -1。  
    - ``r`` 圆的半径。默认值为 -1。  
    - ``color`` 圆的颜色，RGB888 格式。默认值为 0。  

.. function:: Display.fillCircle(x: int = -1, y: int = -1, r: int = -1, color: int = 0)

    绘制一个实心圆。  

    - ``x`` 圆心的 x 坐标。默认值为 -1。  
    - ``y`` 圆心的 y 坐标。默认值为 -1。  
    - ``r`` 圆的半径。默认值为 -1。  
    - ``color`` 填充颜色，RGB888 格式。默认值为 0。  

.. function:: Display.drawEllipse(x: int = -1, y: int = -1, rx: int = -1, ry: int = -1, color: int = 0)

    绘制一个椭圆。

    - ``x`` 椭圆中心的 x 坐标。默认值为 -1。  
    - ``y`` 椭圆中心的 y 坐标。默认值为 -1。  
    - ``rx`` 椭圆的水平半径。默认值为 -1。  
    - ``ry`` 椭圆的垂直半径。默认值为 -1。  
    - ``color`` 椭圆的颜色，RGB888 格式。默认值为 0。  

.. function:: Display.fillEllipse(x: int = -1, y: int = -1, rx: int = -1, ry: int = -1, color: int = 0)

    绘制一个实心椭圆。  

    - ``x`` 椭圆中心的 x 坐标。默认值为 -1。  
    - ``y`` 椭圆中心的 y 坐标。默认值为 -1。  
    - ``rx`` 椭圆的水平半径。默认值为 -1。  
    - ``ry`` 椭圆的垂直半径。默认值为 -1。  
    - ``color`` 填充颜色，RGB888 格式。默认值为 0。 

.. function:: Display.drawLine(x0: int = -1, y0: int = -1, x1: int = -1, y1: int = -1, color: int = 0)

    绘制一条直线。  

    - ``x0, y0`` 直线起点坐标，默认值为 -1。  
    - ``x1, y1`` 直线终点坐标，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.drawRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, color: int = 0)

    绘制一个矩形。  

    - ``x, y`` 矩形左上角坐标，默认值为 -1。  
    - ``w, h`` 矩形的宽度和高度，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.fillRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, color: int = 0)

    绘制一个填充矩形。  

    - ``x, y`` 矩形左上角坐标，默认值为 -1。  
    - ``w, h`` 矩形的宽度和高度，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.drawRoundRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, r: int = -1, color: int = 0)

    绘制一个圆角矩形。  

    - ``x, y`` 矩形左上角坐标，默认值为 -1。  
    - ``w, h`` 矩形的宽度和高度，默认值为 -1。  
    - ``r`` 圆角半径，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.fillRoundRect(x: int = -1, y: int = -1, w: int = -1, h: int = -1, r: int = -1, color: int = 0)

    绘制一个填充圆角矩形。  

    - ``x, y`` 矩形左上角坐标，默认值为 -1。  
    - ``w, h`` 矩形的宽度和高度，默认值为 -1。  
    - ``r`` 圆角半径，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.drawTriangle(x0: int = -1, y0: int = -1, x1: int = -1, y1: int = -1, x2: int = -1, y2: int = -1, color: int = 0)

    绘制一个三角形。  

    - ``x0, y0`` 第一个顶点的坐标，默认值为 -1。  
    - ``x1, y1`` 第二个顶点的坐标，默认值为 -1。  
    - ``x2, y2`` 第三个顶点的坐标，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.fillTriangle(x0: int = -1, y0: int = -1, x1: int = -1, y1: int = -1, x2: int = -1, y2: int = -1, color: int = 0)

    绘制一个填充三角形。  

    - ``x0, y0`` 第一个顶点的坐标，默认值为 -1。  
    - ``x1, y1`` 第二个顶点的坐标，默认值为 -1。  
    - ``x2, y2`` 第三个顶点的坐标，默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.drawArc(x: int = -1, y: int = -1, r0: int = -1, r1: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    绘制一个弧线。  

    - ``x, y`` 弧线的中心坐标，默认值为 -1。  
    - ``r0`` 弧线的内半径，默认值为 -1。  
    - ``r1`` 弧线的外半径，默认值为 -1。  
    - ``angle0`` 弧线的起始角度（单位：度），默认值为 -1。  
    - ``angle1`` 弧线的终止角度（单位：度），默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.fillArc(x: int = -1, y: int = -1, r0: int = -1, r1: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    绘制一个填充弧线。  

    - ``x, y`` 弧线的中心坐标，默认值为 -1。  
    - ``r0`` 弧线的内半径，默认值为 -1。  
    - ``r1`` 弧线的外半径，默认值为 -1。  
    - ``angle0`` 弧线的起始角度（单位：度），默认值为 -1。  
    - ``angle1`` 弧线的终止角度（单位：度），默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.drawEllipseArc(x: int = -1, y: int = -1, r0x: int = -1, r0y: int = -1, r1x: int = -1, r1y: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    绘制一个椭圆弧线。  

    - ``x, y`` 椭圆弧线的中心坐标，默认值为 -1。  
    - ``r0x, r0y`` 内椭圆的水平半径和垂直半径，默认值为 -1。  
    - ``r1x, r1y`` 外椭圆的水平半径和垂直半径，默认值为 -1。  
    - ``angle0`` 椭圆弧线的起始角度（单位：度），默认值为 -1。  
    - ``angle1`` 椭圆弧线的终止角度（单位：度），默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。  

.. function:: Display.fillEllipseArc(x: int = -1, y: int = -1, r0x: int = -1, r0y: int = -1, r1x: int = -1, r1y: int = -1, angle0: int = -1, angle1: int = -1, color: int = 0)

    绘制一个填充椭圆弧线。  

    - ``x, y`` 椭圆弧线的中心坐标，默认值为 -1。  
    - ``r0x, r0y`` 内椭圆的水平半径和垂直半径，默认值为 -1。  
    - ``r1x, r1y`` 外椭圆的水平半径和垂直半径，默认值为 -1。  
    - ``angle0`` 椭圆弧线的起始角度（单位：度），默认值为 -1。  
    - ``angle1`` 椭圆弧线的终止角度（单位：度），默认值为 -1。  
    - ``color`` 颜色，RGB888 格式，默认值为 0。

.. function:: Display.drawQR(text: str = None, x: int = 0, y: int = 0, w: int = 0, version: int = 1)

    绘制二维码。

    - ``text`` 二维码内容，默认值为 None。
    - ``x, y`` 二维码显示的起始坐标，默认值为 0。
    - ``w`` 二维码的宽度，默认值为 0。
    - ``version`` 二维码版本，默认值为 1，范围: 0~38。

    **Example**:

    生成一个内容为“hello”的二维码:

    .. code-block:: python

        Display.drawQR("Hello", 0, 0, 200)

.. function:: Display.drawPng(img: str, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0, scaleX=True, scaleY=False)

    绘制 PNG 图片。

    - ``img`` 图片文件路径或已打开的图片数据。
    - ``x, y`` 图片显示的起始坐标，默认值为 0。
    - ``maxW, maxH`` 要绘制的宽度和高度，若值 ≤0 则绘制整个图片，默认值为 0。
    - ``offX, offY`` 图片中起始的偏移量，默认值为 0。
    - ``scaleX, scaleY`` 是否水平或垂直缩放图片，默认值分别为 True 和 False。

    **Examples**:

    显示 PNG 图片文件:

    .. code-block:: python

        Display.drawPng("res/img/uiflow.png", 0, 0)

    显示从数据读取的 PNG 图片:

    .. code-block:: python

        img = open("res/img/uiflow.png", "b")
        img.seek(0)
        Display.drawPng(img.read(), 0, 100)
        img.close()

.. function:: Display.drawJpg(img, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0)

    绘制 JPG 图片。

    - ``img`` 图片文件路径或已打开的图片数据。
    - ``x, y`` 图片显示的起始坐标，默认值为 0。
    - ``maxW, maxH`` 要绘制的宽度和高度，若值 ≤0 则绘制整个图片，默认值为 0。
    - ``offX, offY`` 图片中起始的偏移量，默认值为 0。

.. function:: Display.drawBmp(img: str, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0)

    绘制 BMP 图片。

    - ``img`` 图片文件路径或已打开的图片数据。
    - ``x, y`` 图片显示的起始坐标，默认值为 0。
    - ``maxW, maxH`` 要绘制的宽度和高度，若值 ≤0 则绘制整个图片，默认值为 0。
    - ``offX, offY`` 图片中起始的偏移量，默认值为 0。

.. function:: Display.drawImage(img: str, x: int = 0, y: int = 0, maxW: int = 0, maxH: int = 0, offX: int = 0, offY: int = 0)

    绘制任意格式图片。

    - ``img`` 图片文件路径或已打开的图片数据。
    - ``x, y`` 图片显示的起始坐标，默认值为 0。
    - ``maxW, maxH`` 要绘制的宽度和高度，若值 ≤0 则绘制整个图片，默认值为 0。
    - ``offX, offY`` 图片中起始的偏移量，默认值为 0。

    **Example**:

    绘制缓冲区中的图片:

    .. code-block:: python

        img = open(img_path)
        img.seek(0)
        drawImage(img.read())

.. function:: Display.drawRawBuf(buf, x: int = 0, y: int = 0, w: int = 0, h: int = 0, len: int = 0, swap: bool = False)

    使用原始缓冲区数据绘制图片。

    - ``buf`` 图片缓冲数据。
    - ``x, y`` 图片显示的起始坐标，默认值为 0。
    - ``w, h`` 图片的宽度和高度。
    - ``len`` 图片数据长度。
    - ``swap`` 是否启用反色显示，默认值为 False。

.. function:: Display.print(text: str = None, color: int = 0)

    显示字符串 (不支持格式化输入)。

    - ``text`` 要显示的文本，默认值为 None。
    - ``color`` 颜色 (RGB888 格式)，默认值为 0。

.. function:: Display.printf(text: str = None)

    显示格式化字符串。

    - ``text`` 要显示的格式化文本。

.. function:: Display.newCanvas(w: int = 0, h: int = 0, bpp: int = -1, psram: bool = False)

    创建画布。

    - ``w, h`` 画布的宽度和高度，默认值为 0。
    - ``bpp`` 色深，默认值为 -1。
    - ``psram``是否使用 PSRAM，默认值为 False。
    
    返回创建的画布对象。

    **Example**: 

    .. code-block:: python

        w1 = Display.newCanvas(w=100, h=100, bpp=16)
        w1.drawImage("res/img/uiflow.jpg", 80, 0)
        w1.push(30, 0)

.. function:: Display.startWrite()

    开始对显示屏写入操作。

.. function:: Display.endWrite()

    结束对显示屏写入操作。

