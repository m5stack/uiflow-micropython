image
=====

.. include:: ../refs/advanced.image.ref

.. note:: This module is only applicable to the CoreS3 Controller


UiFlow2 Example 
---------------

draw test
+++++++++

Open the |cores3_example_draw_test.m5f2| project in UiFlow2.

This example captures an image from the camera and demonstrates how to draw text and basic shapes on it.

UiFlow2 Code Block:

    |image_draw_example.png|

Example output:

    None

find qrcode
+++++++++++

Open the |cores3_image_find_qrcode_example.m5f2| project in UiFlow2.

This example captures images from the camera, detects QR codes, and draws their bounding boxes and decoded payload text on the LCD.

UiFlow2 Code Block:

    |cores3_image_find_qrcode_example.png|

Example output:

    None

MicroPython Example 
-------------------

draw test
+++++++++

    .. literalinclude:: ../../../examples/advanced/image/cores3_example_draw_test.py
        :language: python
        :linenos:

find qrcode
+++++++++++

    .. literalinclude:: ../../../examples/advanced/image/cores3_image_find_qrcode_example.py
        :language: python
        :linenos:

**API**
-------

.. class:: image.Image
 
    The image.Image object is returned by `camera.snapshot()`.

    .. method:: width()

        Returns the image width in pixels.

        :returns width: image width.
        :return type: int

        UiFlow2 Code Block:

            |width.png|

        MicroPython Code Block:

            .. code-block:: python

                width()

    .. method:: height()

        Returns the image height in pixels.

        :returns height: image height.
        :return type: int

        UiFlow2 Code Block:

            |height.png|

        MicroPython Code Block:

            .. code-block:: python

                height()

    .. method:: format()

        Returns the image format.

        Returns image.GRAYSCALE for grayscale images, image.RGB565 for RGB565 images, image.BAYER for bayer pattern images, and image.JPEG for JPEG images.

        :returns format: image format.
        :return type: int

        UiFlow2 Code Block:

            |format.png|

        MicroPython Code Block:

            .. code-block:: python

                format()

    .. method:: size()

        Returns the image size in bytes.

        :returns size: image size in bytes.
        :return type: int

        UiFlow2 Code Block:

            |size.png|

        MicroPython Code Block:

            .. code-block:: python

                size()

    .. method:: bytearray()

        Returns a bytearray object that points to the image data for byte-level read/write access.

        :returns data: image data buffer.
        :return type: bytearray

        UiFlow2 Code Block:

            |bytearray.png|

        MicroPython Code Block:

            .. code-block:: python

                bytearray()

    .. method:: draw_line(x0, y0, x1, y1, color, thickness)

        Draws a line from (x0, y0) to (x1, y1) on the image. You may either
        pass x0, y0, x1, y1 separately or as a tuple (x0, y0, x1, y1).

        :param int x0: start x coordinate.
        :param int y0: start y coordinate.
        :param int x1: end x coordinate.
        :param int y1: end y coordinate.
        :param color: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        :param int thickness: line thickness in pixels. Defaults to 1.

        :returns self: the image object for method chaining.
        :return type: Image

        UiFlow2 Code Block:

            |draw_line.png|

        MicroPython Code Block:

            .. code-block:: python

                img.draw_line(10, 10, 100, 100, color=(255,0,0), thickness=2)

    .. method:: draw_rectangle(x, y, w, h, color, thickness, fill)

        Draws a rectangle on the image. You may either pass x, y, w, h separately
        or as a tuple (x, y, w, h).

        :param int x: top-left x coordinate.
        :param int y: top-left y coordinate.
        :param int w: rectangle width.
        :param int h: rectangle height.
        :param color: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        :param int thickness: border thickness in pixels. Defaults to 1.
        :param bool fill: set True to fill the rectangle. Defaults to False.

        :returns self: the image object for method chaining.
        :return type: Image

        UiFlow2 Code Block:

            |draw_rectangle.png|

        MicroPython Code Block:

            .. code-block:: python

                img.draw_rectangle(20, 20, 80, 60, color=(0,255,0), thickness=2, fill=True)

    .. method:: draw_circle(x, y, radius, color, thickness, fill)

        Draws a circle on the image. You may either pass x, y, radius separately or
        as a tuple (x, y, radius).

        :param int x: circle center x coordinate.
        :param int y: circle center y coordinate.
        :param int radius: circle radius.
        :param color: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        :param int thickness: border thickness in pixels. Defaults to 1.
        :param bool fill: set True to fill the circle. Defaults to False.

        :returns self: the image object for method chaining.
        :return type: Image

        UiFlow2 Code Block:

            |draw_circle.png|

        MicroPython Code Block:

            .. code-block:: python

                img.draw_circle(50, 50, 30, color=(0,0,255), thickness=3, fill=False)

    .. method:: draw_string(x, y, text, color, scale)

        Draws 8x16 text starting at location (x, y) in the image. You may either pass
        x, y separately or as a tuple (x, y).

        :param int x: text start x coordinate.
        :param int y: text start y coordinate.
        :param str text: text to draw. Supports ``\n``, ``\r``, ``\r\n`` line breaks.
        :param color: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        :param scale: scale factor to resize text. Integer or float > 0. Defaults to 1.

        :returns self: the image object for method chaining.
        :return type: Image

        UiFlow2 Code Block:

            |draw_string.png|

        MicroPython Code Block:

            .. code-block:: python

                img.draw_string(10, 10, "Hello", color=(255,255,0), scale=2)

    .. method:: find_qrcodes()

        Finds all QR codes returns a list of ``image.qrcode`` objects.  
        Please see the image.qrcode object for more details.

        :returns qrcodes: list of detected QR codes.
        :return type: List[image.qrcode]

        UiFlow2 Code Block:

            |find_qrcodes.png|

        MicroPython Code Block:

            .. code-block:: python

                qrcodes = img.find_qrcodes()

.. class:: image.qrcode

    Please call ``Image.find_qrcodes()`` to create this object.

    .. method:: corners()

        Get the 4 corners of the QR code in clockwise order starting from the top-left.

        :returns corners: list of 4 (x, y) tuples.
        :return type: List[Tuple[int, int]]

        UiFlow2 Code Block:

            |corners.png|

        MicroPython Code Block:

            .. code-block:: python

                q.corners()

    .. method:: rect()

        Get the bounding box of the QR code.

        :returns rect: (x, y, w, h) tuple.
        :return type: Tuple[int, int, int, int]

        UiFlow2 Code Block:

            |rect.png|

        MicroPython Code Block:

            .. code-block:: python

                q.rect()

    .. method:: x()

        Get the bounding box x coordinate.

        :returns x: the x coordinate.
        :return type: int

        UiFlow2 Code Block:

            |x.png|

        MicroPython Code Block:

            .. code-block:: python

                q.x()

    .. method:: y()

        Get the bounding box y coordinate.

        :returns y: the y coordinate.
        :return type: int

        UiFlow2 Code Block:

            |y.png|

        MicroPython Code Block:

            .. code-block:: python

                q.y()

    .. method:: w()

        Get the bounding box width.

        :returns w: the width of the QR code.
        :return type: int

        UiFlow2 Code Block:

            |w.png|

        MicroPython Code Block:

            .. code-block:: python

                q.w()

    .. method:: h()

        Get the bounding box height.

        :returns h: the height of the QR code.
        :return type: int

        UiFlow2 Code Block:

            |h.png|

        MicroPython Code Block:

            .. code-block:: python

                q.h()

    .. method:: payload()

        Get the decoded payload string (e.g. URL) from the QR code.

        :returns payload: decoded string.
        :return type: str

        UiFlow2 Code Block:

            |payload.png|

        MicroPython Code Block:

            .. code-block:: python

                q.payload()

    .. method:: version()

        Get the QR code version number.

        :returns version: QR code version.
        :return type: int

        UiFlow2 Code Block:

            |version.png|

        MicroPython Code Block:

            .. code-block:: python

                q.version()

    .. method:: ecc_level()

        Get the QR code ECC (error correction) level.

        ECC levels: L, M, Q, H. Higher levels allow more damage tolerance but reduce data capacity.

        :returns ecc: ECC level (0~3).
        :return type: int

        UiFlow2 Code Block:

            |ecc_level.png|

        MicroPython Code Block:

            .. code-block:: python

                q.ecc_level()

    .. method:: mask()

        Get the QR code mask pattern (0~7).

        Mask is used to improve QR readability.

        :returns mask: mask pattern ID.
        :return type: int

        UiFlow2 Code Block:

            |mask.png|

        MicroPython Code Block:

            .. code-block:: python

                q.mask()

    .. method:: eci()

        Get the QR code ECI (Extended Channel Interpretation) value.

        ECI indicates the text encoding (e.g. UTF-8, Shift-JIS). ``0`` means ECI not used.

        :returns eci: ECI value.
        :return type: int

        UiFlow2 Code Block:

            |eci.png|

        MicroPython Code Block:

            .. code-block:: python

                q.eci()

Constants
---------

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

    UiFlow2 Code Block:

        |format_option.png|

