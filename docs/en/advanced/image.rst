image
===============================

.. include:: ../refs/advanced.image.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: image
   :synopsis: machine vision

Micropython Example 
--------------------------------

draw test
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/advanced/image/cores3_example_draw_test.py
        :language: python
        :linenos:

UIFlow2.0 Example 
--------------------------------

draw test
++++++++++++++++++++++++++++

    |image_draw_example.png|

.. only:: builder_html

    |cores3_example_draw_test.m5f2|

class image.Image
--------------------------------
The line object is returned by `camera.snapshot()`.

Basic Methods
--------------------------------

.. method:: width() -> int

    Returns the image width in pixels.
    
    UIFlow2.0

        |width.png|

.. method:: height() -> int

    Returns the image height in pixels.

    UIFlow2.0

        |height.png|

.. method:: format() -> int

    Returns the image format

    UIFlow2.0

        |format.png|

.. method:: size() -> int

    Returns the image size in bytes.

    UIFlow2.0

        |size.png|

.. method:: bytearray() -> bytearray

    Returns a bytearray object that points to the image data for byte-level read/write access.

    UIFlow2.0

        |bytearray.png|


Drawing Methods
--------------------------------
 
.. method:: draw_line(x0:int, y0:int, x1:int, y1:int, color:Optional[int,Tuple[int,int,int]]=None, thickness=1) -> Image

    Draws a line from (x0, y0) to (x1, y1) on the image. You may either
    pass x0, y0, x1, y1 separately or as a tuple (x0, y0, x1, y1).

    - ``color`` is an RGB888 tuple for Grayscale or RGB565 images. Defaults to 
      white. However, you may also pass the underlying pixel value (0-255) for 
      grayscale images or a RGB565 value for RGB565 images.

    - ``thickness`` controls how thick the line is in pixels.

    Returns the image object so you can call another method using ``.`` notation.

    UIFlow2.0

        |draw_line.png|

.. method:: draw_rectangle(x:int, y:int, w:int, h:int, color:Optional[int,Tuple[int,int,int]]=None, thickness=1, fill=False) -> Image

    Draws a rectangle on the image. You may either pass x, y, w, h separately
    or as a tuple (x, y, w, h).

    - ``color`` is an RGB888 tuple for Grayscale or RGB565 images. Defaults to
      white. However, you may also pass the underlying pixel value (0-255) for
      grayscale images or a RGB565 value for RGB565 images.

    - ``thickness`` controls how thick the lines are in pixels.

    - ``fill`` set to True to fill the rectangle.

    Returns the image object so you can call another method using ``.`` notation.

    UIFlow2.0

        |draw_rectangle.png|

.. method:: draw_circle(x:int, y:int, radius:int, color:Optional[int,Tuple[int,int,int]]=None, thickness=1, fill=False) -> Image

    Draws a circle on the image. You may either pass x, y, radius separately or
    as a tuple (x, y, radius).

    - ``color`` is an RGB888 tuple for Grayscale or RGB565 images. Defaults to
      white. However, you may also pass the underlying pixel value (0-255) for
      grayscale images or a RGB565 value for RGB565 images.

    - ``thickness`` controls how thick the edges are in pixels.

    - ``fill`` set to True to fill the circle.

    Returns the image object so you can call another method using ``.`` notation.

    UIFlow2.0

        |draw_circle.png|
        
        
.. method:: draw_string(x:int, y:int, text:str, color:Optional[int,Tuple[int,int,int]]=None, scale=1) -> Image

    Draws 8x16 text starting at location (x, y) in the image. You may either pass
    x, y separately or as a tuple (x, y).

    - ``text`` is a string to write to the image. ``\n``, ``\r``, and ``\r\n``
      line endings move the cursor to the next line.

    - ``color`` is an RGB888 tuple for Grayscale or RGB565 images. Defaults to
      white. However, you may also pass the underlying pixel value (0-255) for
      grayscale images or a RGB565 value for RGB565 images.

    - ``scale`` may be increased to increase/decrease the size of the text on the
      image. You can pass greater than 0 integer or floating point values.

    Returns the image object so you can call another method using ``.`` notation.


    UIFlow2.0

        |draw_string.png|

Constants
--------------------------------

.. data:: RGB565
   :type: int

   RGB565 pixel format. Each pixel is 16-bits, 2-bytes. 5-bits are used for red,
   6-bits are used for green, and 5-bits are used for blue.

.. data:: GRAYSCALE
   :type: int

   GRAYSCALE pixel format. Each pixel is 8-bits, 1-byte.
 
.. data:: JPEG
   :type: int

   A JPEG image.
 
.. data:: YUV422
   :type: int
 
   A pixel format that is very easy to jpeg compress. Each pixel is stored as a grayscale
   8-bit Y value followed by alternating 8-bit U/V color values that are shared between two
   Y values (8-bits Y1, 8-bits U, 8-bits Y2, 8-bits V, etc.). Only some image processing
   methods work with YUV422.

    UIFlow2.0

        |format_option.png|
  
