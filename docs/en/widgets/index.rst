:mod:`Widgets` --- A basic UI library
=====================================

.. module:: Widgets
    :synopsis: A basic UI library

.. include:: ../refs/widgets.ref

Micropython Example:

    .. literalinclude:: ../../../examples/widgets/screen/cores3_widgets_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_widgets_example.m5f2|

Screen functions
----------------

.. function:: Widgets.setBrightness(brightness: int)

    Set the backlight of the monitor。``brightness`` ranges from 0 to 255.

    UIFLOW2:

        |setBrightness.png|

.. function:: Widgets.fillScreen(color: int)

    Set the background color of the monitor. ``color`` accepts the color code of RGB888.

    UIFLOW2:

        |fillScreen.png|

.. function:: Widgets.setRotation(rotation: int)

    Set the rotation Angle of the display.

    The ``rotation`` parameter only accepts the following values:

        - ``0``: Portrait (0°C)
        - ``1``: Landscape (90°C)
        - ``2``: Inverse Portrait (180°C)
        - ``3``: Inverse Landscape (270°C)

    UIFLOW2:

        |setRotation.png|

Classes
-------

.. toctree::
    :maxdepth: 1

    circle.rst
    image.rst
    image+.rst
    label.rst
