Watering Unit
=============

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

Micropython Example:

    .. literalinclude:: ../../../examples/unit/watering/cores3_watering_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_watering_example.m5f2|

class WateringUnit
------------------

Constructors
------------

.. class:: WateringUnit(port: tuple) -> None

    Initialize the Fader.

    :param port: The port to which the Fader is connected. port[0]: adc pin, port[1]: pump pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: WateringUnit.get_voltage() -> float

    Get the voltage of the sensor.

    :return: The voltage of the sensor.

    UIFLOW2:

        |get_voltage.png|


.. method:: WateringUnit.get_raw() -> int

    Read the raw value of the ADC.

    :return: The raw value of the ADC.

    UIFLOW2:

        |get_raw.png|


.. method:: WateringUnit.on() -> None

    Turn on the pump.

    UIFLOW2:

        |on.png|


.. method:: WateringUnit.off() -> None

    Turn off the pump.

    UIFLOW2:

        |off.png|


.. method:: WateringUnit.set_pump(state: int) -> None

    Set the state of the pump.

    :param int state: The state of the pump.

    UIFLOW2:

        |set_pump.png|
