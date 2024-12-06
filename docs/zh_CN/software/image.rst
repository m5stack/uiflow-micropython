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
 
