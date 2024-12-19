:mod:`jpg`  
===============================

.. include:: ../refs/software.jpg.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: jpg
   :synopsis:  

``jpg`` 模块用于处理 JPG 格式图像的编码和解码操作

Micropython 案例 
--------------------------------

拍照
++++++++++++++++++++++++++++

点击屏幕开始倒计时拍照

    .. literalinclude:: ../../../examples/softwave/jpg/take_photo_example.py
        :language: python
        :linenos:
 

UIFlow2.0 Example 
--------------------------------

拍照
++++++++++++++++++++++++++++

点击屏幕开始倒计时拍照

    |take_photo_example.png|

.. only:: builder_html

    |take_photo_example.m5f2|


方法
--------------------------------

.. method:: encode(img: image.Image, quality=60) -> image.Image

    编码为 jpg 图像 

    - ``img`` 需要编码的图像，格式为 image.RGB565

    返回 ``image.Image`` 对象，图像格式为 image.JPEG 

    UIFlow2.0

        |encode.png|

.. method:: decode(img_jpg: image.Image) -> image.Image

    jpg 图像解码 

    - ``img`` 需要解码的图像，格式为 image.JPEG

    返回 ``image.Image`` 对象，图像格式为 image.RGB565 

    UIFlow2.0

        |decode.png|


