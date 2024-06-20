WateringUnit
============

.. include:: ../refs/unit.watering.ref

Watering is a capacitive soil moisture detection and adjustment unit.
The product integrates water pump and measuring plates for soil moisture
detection and pump water control. It can be used for intelligent plant breeding
scenarios and can easily achieve humidity detection and Irrigation control.
The measurement electrode plate uses the capacitive design, which can
effectively avoid the corrosion problem of the electrode plate in actual use
compared with the resistive electrode plate.


Support the following products:

    |WateringUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import WateringUnit
    water = WateringUnit((33,32)) # for core2
    water.on()
    time.sleep(1)
    water.off()
    print(water.get_voltage())
    print(water.get_raw())


class WateringUnit
------------------

Constructors
------------

.. class:: WateringUnit(port: tuple) -> None

    Initialize the Fader.

    :param port: The port to which the Fader is connected. port[0]: adc pin, port[1]: pump pin.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: WateringUnit.get_voltage() -> float

    Get the voltage of the sensor.

    :return: The voltage of the sensor.

    UIFLOW2:

        |get_voltage.svg|


.. method:: WateringUnit.get_raw() -> int

    Read the raw value of the ADC.

    :return: The raw value of the ADC.

    UIFLOW2:

        |get_raw.svg|


.. method:: WateringUnit.on() -> None

    Turn on the pump.

    UIFLOW2:

        |on.svg|


.. method:: WateringUnit.off() -> None

    Turn off the pump.

    UIFLOW2:

        |off.svg|


.. method:: WateringUnit.set_pump(state: int) -> None

    Set the state of the pump.

    :param int state: The state of the pump.

    UIFLOW2:

        |set_pump.svg|
