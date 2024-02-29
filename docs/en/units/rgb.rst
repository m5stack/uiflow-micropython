RGB Unit
========

.. include:: ../refs/unit.rgb.ref

The following products are supported:

    |RGB|


Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()
    rgb_0 = RGB((36, 26), 3)
    Widgets.fillScreen(0x222222)

    rgb_0.set_brightness(80)
    rgb_0.fill_color(0xff0000)
    rgb_0.set_color(0, 0x33ff33)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |rgb_core_example.m5f2|


class RGB
---------

Constructors
------------

.. class:: RGB(port, number)

    Create an RGB object.

    parameter is:
        - ``port`` is the pins number of the port
        - ``number`` is the number of RGB lamp beads

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: RGB.set_brightness(br: int)

    This method is used to set the brightness of RGB lamp beads, and the setting range is 0-100.

    UIFLOW2:

        |set_brightness.svg|


.. method:: RGB.fill_color(c: int)

    This method is used to set the color of all RGB lamp beads, and the input value is 3-byte RGB888.

    UIFLOW2:

        |fill_color.svg|


.. method:: RGB.set_color(i, c: int)

    This method is used to set the specified RGB lamp bead color. The input value is the lamp bead index and 3-byte RGB888.

    UIFLOW2:

        |set_color.svg|
