:mod:`code_scanner`  
===============================

.. include:: ../refs/software.code_scanner.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: code_scanner
   :synopsis:  

``code_scanner`` module for qrcode scanning recognition 

Micropython Example 
--------------------------------

qrcode detect 
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/softwave/code_scanner/qrcode_detect_example.py
        :language: python
        :linenos:
 

UIFlow2.0 Example 
--------------------------------

qrcode detect 
++++++++++++++++++++++++++++

    |qrcode_detect_example.png|

.. only:: builder_html

    |qrcode_detect_example.m5f2|

 

Methods
--------------------------------

.. method:: find_qrcodes(img: image.Image) -> image.qrcode

    QR code recognition 

    - ``img`` Image to be recognized 

    Returns ``image.qrcode`` instance 

    UIFlow2.0

        |find_qrcodes.png|


class image.QRCode  
------------------------------
``QRCode`` The QRCode object is returned by `code_scanner.find_qrcodes(img: image.Image)`.

.. method:: payload() -> str

    Return the payload string of the QR code

    UIFlow2.0

        |payload.png|

.. method:: type_name() -> str

    Return the type of the QR code  

    UIFlow2.0

        |type_name.png|



