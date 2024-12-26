
Scales Unit
===========
.. sku:U108
.. include:: ../refs/unit.scales.ref

UNIT Scales is a high precision low-cost I2C port weighing sensor, with a total weighing range of 20kgs. Adopt STM32F030 as the controller, HX711 as sampling chip and 20 kgs weighing sensor. With tare button and programable RGB LED. This Unit offers the customer with a highly integrated weighing solution, suitable for the applications of weighing, item counting, item movement Checking and so on.

Support the following products:

|ScalesUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/scales/scales_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |scales_cores3_example.m5f2|

class ScalesUnit
----------------

Constructors
------------

.. class:: ScalesUnit(i2c, address)

    Initialize the ScalesUnit with I2C communication and an optional I2C address.

    :param  i2c: The I2C or PAHUBUnit instance for communication.
    :param  address: The I2C address or a list/tuple of addresses for the scales unit.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ScalesUnit.get_button_status(status)

    Retrieve the status of a button on the scales unit.

    :param  status: The button status identifier.

    :returns: The current status of the specified button.

    UIFLOW2:

        |get_button_status.png|

.. method:: ScalesUnit.set_button_offset(enable)

    Enable or disable the button offset for the scales unit.

    :param  enable: The offset enable value (1 to enable, 0 to disable).

    UIFLOW2:

        |set_button_offset.png|

.. method:: ScalesUnit.set_rgbled_sync(control)

    Set synchronization mode for the RGB LED.

    :param  control: The control value for synchronization.

    UIFLOW2:

        |set_rgbled_sync.png|

.. method:: ScalesUnit.get_rgbled_sync()

    Retrieve the synchronization mode of the RGB LED.

    :returns: The synchronization mode value.

.. method:: ScalesUnit.set_rgb_led(rgb)

    Set the RGB values for the LED.

    :param  rgb: The RGB value as a 24-bit integer.

    UIFLOW2:

        |set_rgb_led.png|

.. method:: ScalesUnit.get_rgb_led()

    Retrieve the current RGB values of the LED.

    :returns: A list containing the RGB values.

    UIFLOW2:

        |get_rgb_led.png|

.. method:: ScalesUnit.get_scale_value(scale)

    Get the scale value for the specified scale type.

    :param  scale: The scale type identifier.

    :returns: The scale value as an integer.

    UIFLOW2:

        |get_scale_value.png|

.. method:: ScalesUnit.set_raw_offset(value)

    Set the raw offset for the scales unit.

    :param  value: The raw offset value as an integer.

    UIFLOW2:

        |set_raw_offset.png|

.. method:: ScalesUnit.set_current_raw_offset()

    Set the current raw offset value for the scales unit.


    UIFLOW2:

        |set_current_raw_offset.png|

.. method:: ScalesUnit.set_calibration_zero()

    Calibrate the scales unit for zero weight.


    UIFLOW2:

        |set_calibration_zero.png|

.. method:: ScalesUnit.set_calibration_load(gram)

    Calibrate the scales unit with a specified weight.

    :param  gram: The weight value in grams for calibration.

    UIFLOW2:

        |set_calibration_load.png|

.. method:: ScalesUnit.get_device_inform(mode)

    Get the device information for a specified mode.

    :param  mode: The mode identifier for the requested information.

    :returns: The device information value.

    UIFLOW2:

        |get_device_inform.png|

.. method:: ScalesUnit.set_i2c_address(addr)

    Change the I2C address of the scales unit.

    :param  addr: The new I2C address value.

    UIFLOW2:

        |set_i2c_address.png|



