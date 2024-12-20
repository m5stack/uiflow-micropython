:mod:`jpg`  
===============================

.. include:: ../refs/software.jpg.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: jpg
   :synopsis:  

``jpg`` module for encoding and decoding operations of JPG format images

Micropython Example 
--------------------------------

take photo 
++++++++++++++++++++++++++++

Click the screen to start the countdown and take a photo

    .. literalinclude:: ../../../examples/softwave/jpg/take_photo_example.py
        :language: python
        :linenos:
 

UIFlow2.0 Example 
--------------------------------

take photo 
++++++++++++++++++++++++++++

Click the screen to start the countdown and take a photo

    |take_photo_example.png|

.. only:: builder_html

    |take_photo_example.m5f2|


Methods
--------------------------------

.. method:: encode(img: image.Image, quality=60) -> image.Image

    encode to jog photo

    - ``img`` Image to be encoded, in the format of image.RGB565

    Return ``image.Image`` instance, image format image.JPEG 

    UIFlow2.0

        |encode.png|

.. method:: decode(img_jpg: image.Image) -> image.Image

    jpg photo decode  

    - ``img`` Image to be decoded, in the format of image.JPEG

    Return ``image.Image`` instance, image format image.RGB565 

    UIFlow2.0

        |decode.png|


 
