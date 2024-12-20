:mod:`image`  
===============================

.. include:: ../refs/software.image.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: image
   :synopsis: machine vision

``image`` 模块用于机器视觉

Micropython 案例 
--------------------------------

绘图测试
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/softwave/image/cores3_example_draw_test.py
        :language: python
        :linenos:
 

UIFlow2.0 Example 
--------------------------------

绘图测试
++++++++++++++++++++++++++++

    |image_draw_example.png|

.. only:: builder_html

    |cores3_example_draw_test.m5f2|


class image.Image
--------------------------------
``image.Image`` 对象由 `camera.snapshot()` 返回.

基础方法
--------------------------------

.. method:: width() -> int

    返回图像的宽度（以像素为单位）。

    UIFlow2.0

        |width.png|
        
.. method:: height() -> int

    返回图像的高度（以像素为单位）。

    UIFlow2.0

        |height.png|

.. method:: format() -> int

    返回图像的格式 

    UIFlow2.0

        |format.png|

.. method:: size() -> int

    返回图像的大小（以字节为单位）。

    UIFlow2.0

        |size.png|

.. method:: bytearray() -> bytearray

    返回一个 bytearray 对象，该对象指向图像数据，允许进行字节级别的读写访问。

    UIFlow2.0

        |bytearray.png|


绘图方法
--------------------------------

.. method:: draw_line(x0:int, y0:int, x1:int, y1:int, color:Optional[int,Tuple[int,int,int]]=None, thickness=1) -> Image

    在图像上绘制一条从 (x0, y0) 到 (x1, y1) 的线段。你可以分别传递 x0, y0, x1, y1，或者将它们作为元组 (x0, y0, x1, y1) 一起传递。

    - ``color`` 颜色值 RGB888 格式，可以是 (r, g, b) 元组或整数。 
    - ``thickness`` 控制线条的粗细（以像素为单位）。

    返回 ``image.Image`` 对象，以便你可以使用 . 表示法调用其他方法。

    UIFlow2.0

        |draw_line.png|

.. method:: draw_rectangle(x:int, y:int, w:int, h:int, color:Optional[int,Tuple[int,int,int]]=None, thickness=1, fill=False) -> Image

    在图像上绘制一个矩形。你可以分别传递 x, y, w, h，或者将它们作为元组 (x, y, w, h) 一起传递。

    - ``color`` 颜色值 RGB888 格式，可以是 (r, g, b) 元组或整数。 
    - ``thickness`` 控制线条的粗细（以像素为单位）。
    - ``fill`` 是否填充。

    返回 ``image.Image`` 对象，以便你可以使用 . 表示法调用其他方法。

    UIFlow2.0

        |draw_rectangle.png|

.. method:: draw_circle(x:int, y:int, radius:int, color:Optional[int,Tuple[int,int,int]]=None, thickness=1, fill=False) -> Image

    在图像上绘制一个圆形。你可以分别传递 x, y, radius，或者将它们作为元组 (x, y, radius) 一起传递。

    - ``color`` 颜色值 RGB888 格式，可以是 (r, g, b) 元组或整数。 
    - ``thickness`` 控制线条的粗细（以像素为单位）。
    - ``fill`` 是否填充。

    返回 ``image.Image`` 对象，以便你可以使用 . 表示法调用其他方法。

    UIFlow2.0

        |draw_circle.png|
        
.. method:: draw_string(x:int, y:int, text:str, color:Optional[int,Tuple[int,int,int]]=None, scale=1) -> Image

    在图像上绘制从位置 (x, y) 开始的 8x16 文本。你可以分别传递 x, y，或者将它们作为元组 (x, y) 一起传递。

    - ``text`` 是要写入图像的字符串。``\n``、``\r`` 和 ``\r\n`` 换行符将光标移动到下一行。
    - ``color`` 颜色值 RGB888 格式，可以是 (r, g, b) 元组或整数。  (0-255) for
    grayscale images or a RGB565 value for RGB565 images.
    - ``scale`` 可增加或减少图像中文本的大小。你可以传递大于 0 的整数或浮动值。

    返回 ``image.Image`` 对象，以便你可以使用 . 表示法调用其他方法。

    UIFlow2.0

        |draw_string.png|

常量
--------------------------------

.. data:: RGB565
   :type: int

   RGB565 像素格式。每个像素为 16 位，2 字节。5 位用于红色，6 位用于绿色，5 位用于蓝色。

.. data:: GRAYSCALE
   :type: int

   灰度图像像素格式。每个像素为 8 位，1 字节。
 
.. data:: JPEG
   :type: int

   JPEG 图像。
 
.. data:: YUV422
   :type: int
 
   一种非常适合 JPEG 压缩的像素格式。每个像素存储为一个灰度 8 位 Y 值，后跟交替的 8 位 U/V 色彩值，这些值在两个 Y 值之间共享（8 位 Y1，8 位 U，8 位 Y2，8 位 V，依此类推）。只有一些图像处理方法可以与 YUV422 格式兼容。

    UIFlow2.0

        |format_option.png|
  
