
FaderUnit
=========

.. include:: ../refs/unit.fader.ref

UNIT FADER is a Slide Potentiometer with color indicator, employ a 35mm slide potentiometer + 14x SK6812 programmable RGB lights. The fader has its own center point positioning, and excellent slide appliances for stable, reliable performance and precise control. The integrated beads support digital addressing, which means you can adjust the brightness and color of each LED light. The product is suitable for lighting, music control, and other applications.

Support the following products:

    |FaderUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import FaderUnit
    fader = FaderUnit((33,32)) # for core2
    fader.update_color()


class FaderUnit
---------------

Constructors
------------

.. method:: FaderUnit(port: tuple)

    Initialize the Fader.

    :param tuple port: The port to which the Fader is connected. port[0]: adc pin, port[1]: LEDs pin.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: FaderUnit.get_voltage() -> float

    Get the voltage of the Fader.

    :return: The voltage of the Fader.

    UIFLOW2:

        |get_voltage.svg|


.. method:: FaderUnit.get_raw() -> int

    Read the raw value of the ADC.

    :return: int from 0 to 65535.

    UIFLOW2:

        |get_raw.svg|

.. method:: FaderUnit.update_color() -> None

    Update the color based on adc value.

    UIFLOW2:

        |update_color.svg|


.. method:: FaderUnit.update_brightness() -> None

    Update the brightness based on adc value.

    UIFLOW2:

        |update_brightness.svg|

.. method:: FaderUnit.set_brightness(br: int)

    This method is used to set the brightness of RGB lamp beads, and the setting range is 0-100.

    UIFLOW2:

        |set_brightness.svg|


.. method:: FaderUnit.fill_color(c: int)

    This method is used to set the color of all RGB lamp beads, and the input value is 3-byte RGB888.

    UIFLOW2:

        |fill_color.svg|


.. method:: FaderUnit.set_color(i, c: int)

    This method is used to set the specified RGB lamp bead color. The input value is the lamp bead index and 3-byte RGB888.

    UIFLOW2:

        |set_color.svg|
