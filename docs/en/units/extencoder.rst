ExtEncoder Unit
===============

.. include:: ../refs/unit.extencoder.ref

The following products are supported:

    |ExtEncoderUnit|


class ExtEncoderUnit
--------------------

Constructors
------------

.. class:: ExtEncoderUnit(i2c, address: int | list | tuple = 0x59)

    Creates a Rotary object.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ExtEncoderUnit.get_rotary_status() -> bool

    Gets the rotation status of the Rotary object.

    UIFLOW2:

        |get_rotary_status.svg|


.. method:: ExtEncoderUnit.get_rotary_value() -> int

    Gets the rotation value of the Rotary object.

    UIFLOW2:

        |get_rotary_value.svg|


.. method:: ExtEncoderUnit.get_rotary_increments() -> int

    Gets the rotation increment of the Rotary object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.svg|


.. method:: ExtEncoderUnit.reset_rotary_value() -> None

    Resets the rotation value of the Rotary object.

    UIFLOW2:

        |reset_rotary_value.svg|


.. method:: ExtEncoderUnit.set_rotary_value(new_value: int) -> None

    Sets the rotation value of the Rotary object.

    :param int new_value: adjust the current value.

    UIFLOW2:

        |set_rotary_value.svg|


.. method:: ExtEncoderUnit.get_perimeter() -> int

    Gets the perimeter of the Rotary object. The unit is millimeters.

    UIFLOW2:

        |get_perimeter.svg|


.. method:: ExtEncoderUnit.set_perimeter(perimeter: int) -> None

    Sets the perimeter of the Rotary object.

    :param int perimeter: the perimeter of the Rotary object. The unit is millimeters.

    UIFLOW2:

        |set_perimeter.svg|


.. method:: ExtEncoderUnit.get_pulse() -> int

    pluse per round.

    UIFLOW2:

        |get_pulse.svg|


.. method:: ExtEncoderUnit.set_pulse(pulse: int) -> None

    Sets the pulse per round.

    :param int pulse: the pulse per round.

    UIFLOW2:

        |set_pulse.svg|


.. method:: ExtEncoderUnit.get_zero_mode() -> int

    Gets the zero mode of the Rotary object.

    UIFLOW2:

        |get_zero_mode.svg|


.. method:: ExtEncoderUnit.set_zero_mode(mode: int) -> None

    Sets the zero mode of the Rotary object.

    :param int mode: the zero mode of the Rotary object.

    UIFLOW2:

        |set_zero_mode.svg|


.. method:: ExtEncoderUnit.get_meter_value() -> int

    Gets the meter value of the Rotary object. The unit is millimeters.

    UIFLOW2:

        |get_meter_value.svg|


.. method:: ExtEncoderUnit.get_zero_pulse_value() -> int

    Gets the zero pulse value of the Rotary object.

    UIFLOW2:

        |get_zero_pulse_value.svg|


.. method:: ExtEncoderUnit.set_zero_pulse_value(value: int) -> None

    Sets the zero pulse value of the Rotary object.

    :param int value: the zero pulse value of the Rotary object.

    UIFLOW2:

        |set_zero_pulse_value.svg|


.. method:: ExtEncoderUnit.get_firmware_version() -> int

    读版本号

    UIFLOW2:

        |get_firmware_version.svg|


.. method:: ExtEncoderUnit.set_address(address) -> int

    设置i2c地址

    UIFLOW2:

        |set_address.svg|
