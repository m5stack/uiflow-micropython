:mod:`Widgets` --- A basic UI library
=====================================

.. module:: Widgets
    :synopsis: A basic UI library

.. include:: ../refs/widgets.ref

Micropython Example::

    import M5
    from M5 import Widgets

    M5.begin()
    Widgets.setBrightness(100)
    Widgets.fillScreen(0x6600cc)
    Widgets.setRotation(0)

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    :download:`example.m5f2 <../../_static/widgets/example.m5f2>`

Screen functions
----------------

.. function:: Widgets.setBrightness(brightness: int)

    Set the backlight of the monitor。``brightness`` ranges from 0 to 255.

    UIFLOW2:

        |setBrightness.svg|

.. function:: Widgets.fillScreen(color: int)

    Set the background color of the monitor. ``color`` accepts the color code of RGB888.

    UIFLOW2:

        |fillScreen.svg|

.. function:: Widgets.setRotation(rotation: int)

    Set the rotation Angle of the display.

    The ``rotation`` parameter only accepts the following values:

        - ``0``: Portrait (0°C)
        - ``1``: Landscape (90°C)
        - ``2``: Inverse Portrait (180°C)
        - ``3``: Inverse Landscape (270°C)

    UIFLOW2:

        |setRotation.svg|

Classes
-------

.. toctree::
    :maxdepth: 1

    circle.rst
    image.rst
    image+.rst
    label.rst
