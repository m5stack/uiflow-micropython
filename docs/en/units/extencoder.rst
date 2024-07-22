ExtEncoder Unit
===============

.. include:: ../refs/unit.extencoder.ref

The following products are supported:

    |ExtEncoderUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/extencoder/cores3_extencoder_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_extencoder_example.m5f2|


class ExtEncoderUnit
--------------------

Constructors
------------

.. class:: ExtEncoderUnit(i2c, address: int | list | tuple = 0x59)

    Creates a ExtEncoderUnit object.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ExtEncoderUnit.get_rotary_status() -> bool

    Gets the rotation status of the ExtEncoderUnit object.

    UIFLOW2:

        |get_rotary_status.png|


.. method:: ExtEncoderUnit.get_rotary_value() -> int

    Gets the rotation value of the ExtEncoderUnit object.

    UIFLOW2:

        |get_rotary_value.png|


.. method:: ExtEncoderUnit.get_rotary_increments() -> int

    Gets the rotation increment of the ExtEncoderUnit object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.png|


.. method:: ExtEncoderUnit.reset_rotary_value() -> None

    Resets the rotation value of the ExtEncoderUnit object.

    UIFLOW2:

        |reset_rotary_value.png|


.. method:: ExtEncoderUnit.set_rotary_value(new_value: int) -> None

    Sets the rotation value of the ExtEncoderUnit object.

    :param int new_value: adjust the current value.

    UIFLOW2:

        |set_rotary_value.png|


.. method:: ExtEncoderUnit.get_perimeter() -> int

    Gets the perimeter of the ExtEncoderUnit object. The unit is millimeters.

    UIFLOW2:

        |get_perimeter.png|


.. method:: ExtEncoderUnit.set_perimeter(perimeter: int) -> None

    Sets the perimeter of the ExtEncoderUnit object.

    :param int perimeter: the perimeter of the ExtEncoderUnit object. The unit is millimeters.

    UIFLOW2:

        |set_perimeter.png|


.. method:: ExtEncoderUnit.get_pulse() -> int

    pluse per round.

    UIFLOW2:

        |get_pulse.png|


.. method:: ExtEncoderUnit.set_pulse(pulse: int) -> None

    Sets the pulse per round.

    :param int pulse: the pulse per round.

    UIFLOW2:

        |set_pulse.png|


.. method:: ExtEncoderUnit.get_zero_mode() -> int

    Gets the zero mode of the ExtEncoderUnit object.

    UIFLOW2:

        |get_zero_mode.png|


.. method:: ExtEncoderUnit.set_zero_mode(mode: int) -> None

    Sets the zero mode of the ExtEncoderUnit object.

    :param int mode: the zero mode of the ExtEncoderUnit object.

    UIFLOW2:

        |set_zero_mode.png|


.. method:: ExtEncoderUnit.get_meter_value() -> int

    Gets the meter value of the ExtEncoderUnit object. The unit is millimeters.

    UIFLOW2:

        |get_meter_value.png|


.. method:: ExtEncoderUnit.get_zero_pulse_value() -> int

    Gets the zero pulse value of the ExtEncoderUnit object.

    UIFLOW2:

        |get_zero_pulse_value.png|


.. method:: ExtEncoderUnit.set_zero_pulse_value(value: int) -> None

    Sets the zero pulse value of the ExtEncoderUnit object.

    :param int value: the zero pulse value of the ExtEncoderUnit object.

    UIFLOW2:

        |set_zero_pulse_value.png|


.. method:: ExtEncoderUnit.get_firmware_version() -> int

    Gets the firmware version of the ExtEncoderUnit object.

    UIFLOW2:

        |get_firmware_version.png|


.. method:: ExtEncoderUnit.set_address(address) -> int

    Sets the I2C address of the ExtEncoderUnit object.

    UIFLOW2:

        |set_address.png|
