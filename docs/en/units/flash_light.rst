
FlashLightUnit
==============

.. include:: ../refs/unit.flash_light.ref

FlashLight UNIT is an I/O Unit with built-in flash, including AW3641 driver and a white LED, with a color temperature of 5000-5700K. There is a mode selection switch on the board, which can set the flash mode and the constant lighting mode. The communication interface is GPIO. This Unit can be used as a flash or lighting applications.

Support the following products:

|FlashLightUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import FlashLightUnit
    flash = FlashLightUnit((33,32))
    flash.flash(FlashLightUnit.BRIGHTNESS_100, FlashLightUnit.TIME_220MS, True)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class FlashLightUnit
--------------------

Constructors
------------

.. class:: FlashLightUnit(port)

    Initialize the FlashLightUnit.

    - ``port``: The port to which the FlashLightUnit is connected. port[0]: adc pin, port[1]: pump pin.

    UIFLOW2:

        |__init__.svg|


Methods
-------

.. method:: FlashLightUnit.flash(brightness, time, turn_off)

    Flash the light.

    - ``brightness``: The brightness of the light.
        Options:
        - ``FlashLightUnit.BRIGHTNESS_100``: 100%
        - ``FlashLightUnit.BRIGHTNESS_90``: 90%
        - ``FlashLightUnit.BRIGHTNESS_80``: 80%
        - ``FlashLightUnit.BRIGHTNESS_70``: 70%
        - ``FlashLightUnit.BRIGHTNESS_60``: 60%
        - ``FlashLightUnit.BRIGHTNESS_50``: 50%
        - ``FlashLightUnit.BRIGHTNESS_40``: 40%
        - ``FlashLightUnit.BRIGHTNESS_30``: 30%
    - ``time``: The time of the light.
        Options:
        - ``FlashLightUnit.TIME_220MS``: 220ms
        - ``FlashLightUnit.TIME_1300MS``: 1300ms
    - ``turn_off``: Turn off the light after flash.

    UIFLOW2:

        |flash.svg|





