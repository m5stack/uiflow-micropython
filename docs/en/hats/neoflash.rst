NeoFlashHat
===========

.. include:: ../refs/hat.neoflash.ref


NeoFlash HAT is specifically designed for M5StickC, it is an RGB LED matrix.
Space on PCB board is 58x23.5mm and total include 126 RGB LEDs. Every single RGB
LED is programmable, which allows you setting the colors and brightness, plus on
the 7*18 matrix layout, you will have a nice experience on either display
digital numbers or colorful light effect.


Support the following products:

    |NeoFlashHat|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from hat import NeoFlashHat
    neoflash = NeoFlashHat((26, 0))
    neoflash.set_pixel(0, 0, 0xFF0000)
    neoflash.set_pixel(1, 0, 0x00FF00)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html


class NeoFlashHat
-----------------

Constructors
------------

.. class:: NeoFlashHat(port: tuple)

    Initialize the NeoFlashHat.

    :param tuple port: The port to which the NeoFlashHat is connected. port[0]: LEDs pin.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: NeoFlashHat.set_pixel(x: int, y: int, color: int) -> None

    Set the color of the pixel.

    :param int x: The x coordinate of the pixel.
    :param int y: The y coordinate of the pixel.
    :param int color: The color of the pixel.

    UIFLOW2:

        |set_pixel.svg|


.. method:: NeoFlashHat.set_pixels(data: list) -> None

    Set the color of the pixels.

    :param list data: The list of the pixel position and color, [x, y, color].

    UIFLOW2:

        |set_pixels.svg|


Constants
---------

.. data:: NeoFlashHat.WIDTH

    The width of the NeoFlashHat.

.. data:: NeoFlashHat.HEIGHT

    The height of the NeoFlashHat.
