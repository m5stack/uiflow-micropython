:mod:`code_scanner`  
===============================

.. include:: ../refs/software.code_scanner.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: code_scanner
   :synopsis:  

``code_scanner`` 模块用于扫码识别 

Micropython 案例 
--------------------------------

二维码识别 
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/softwave/code_scanner/qrcode_detect_example.py
        :language: python
        :linenos:
 
UIFlow2.0 Example 
--------------------------------

二维码识别
++++++++++++++++++++++++++++

    |qrcode_detect_example.png|

.. only:: builder_html

    |qrcode_detect_example.m5f2|

 

方法
--------------------------------

.. method:: find_qrcodes(img: image.Image) -> image.qrcode

    二维码识别 

    - ``img`` 需要识别的图像 

    返回 ``image.qrcode`` 对象 

    UIFlow2.0

        |find_qrcodes.png|


class image.QRCode  
------------------------------
``QRCode`` 对象由 code_scanner.find_qrcodes() 返回

.. method:: payload() -> str

    返回二维码的有效载荷字符串 

    UIFlow2.0

        |payload.png|

.. method:: type_name() -> str

    返回二维码的类型  

    UIFlow2.0

        |type_name.png|
