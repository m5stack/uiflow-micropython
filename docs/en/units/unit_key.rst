
KeyUnit
=======

.. include:: ../refs/unit.key.ref

Unit Key is a single mechanical key input unit with built-in RGB LED. The key shaft adopts Blue switch with tactile bump and audible click features. Embedded with one programable RGB LED - SK6812, supports 256 level brightness. Two digital IOs are available for key status and LED control key status and lighting control. Suitable for multiple HMI applications.

Support the following products:

|KeyUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import KeyUnit
    key = KeyUnit((33,32)) # for core2
    key.set_color(0x00FF00)
    key.set_brightness(10)
    key.get_key_state()


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class KeyUnit
-------------

Constructors
------------

.. method:: KeyUnit(port)

    Initialize the KeyUnit.

    - ``port``: The port to which the KeyUnit is connected. port[0]: key pin, port[1]: LEDs pin.

    UIFLOW2:

        |__init__.svg|



Methods
-------

.. method:: KeyUnit.get_key_state()

    Get the state of the key.


    UIFLOW2:

        |get_key_state.svg|

.. method:: KeyUnit.set_color(color)

    Set the color of the LED.

    - ``color``: The color of the LED.

    UIFLOW2:

        |set_color.svg|

.. method:: KeyUnit.set_brightness(br)

    Set the brightness of the LED.

    - ``br``: The brightness of the LED, range from 0 to 100.

    UIFLOW2:

        |set_brightness.svg|


