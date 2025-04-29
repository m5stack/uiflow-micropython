Weight I2C Unit
===============

.. include:: ../refs/unit.weight_i2c.ref

The ``Weight I2C`` Unit is a weighing acquisition transmitter unit that adopts the "STM32+HX711 chip" solution to achieve 24-bit precision weight measurement through I2C communication and does not include a load cell sensor. This unit is capable of measuring weight and also includes various filters.

Support the following products:


|WEIGHT I2C|



Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import WEIGHT_I2CUnit
    import time

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    weight_i2c0 = WEIGHT_I2CUnit(i2c0)
    print(weight_i2c_0.get_adc_raw)
    print(weight_i2c_0.get_weight_float)
    time.sleep_ms(100)


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |weight-i2c-demo.m5f2|


class WEIGHT_I2CUnit
--------------------

Constructors
---------------------------

.. class:: WEIGHT_I2CUnit(i2c0, 0x26)

    Create an WEIGHT_I2CUnit object.

    - ``I2C0`` is I2C Port.
    - ``0x26`` is default I2C address


    UIFLOW2:

        |init_i2c_address.png|


Methods
----------------------

.. method:: WEIGHT_I2CUnit.get_adc_raw


    Gets the raw adc value.

    UIFLOW2:

        |get_adc_raw.png|

.. method:: WEIGHT_I2CUnit.get_weight_float


    Gets the weight in grams float value.

    UIFLOW2:

        |get_weight_float.png|

.. method:: WEIGHT_I2CUnit.get_weight_int


    Gets the weight in grams int value.

    UIFLOW2:

        |get_weight_int.png|

.. method:: WEIGHT_I2CUnit.get_weight_str


    Gets the weight in grams string value.

    UIFLOW2:

        |get_weight_str.png|

.. method:: WEIGHT_I2CUnit.set_reset_offset()

    Reset the offset value(Tare).


    UIFLOW2:

        |set_reset_offset.png|

.. method:: WEIGHT_I2CUnit.set_calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)


    Calibrates the Load sensor.

    - ``weight1_g``: Weight1 in grams.
    - ``weight1_adc``: Weight1 in ADC value.
    - ``weight2_g``: Weight2 in grams.
    - ``weight2_adc``: Weight2 in ADC value.

    calibration steps:

    1.Reset offset(Tare).
    2.Get the raw ADC value at no-load weight, this is the Raw ADC of zero weight in 0g.
    3.Put some weight on it, then get adc, this is the load weight adc value and the gram weight you put on it.


    UIFLOW2:

        |set_calibration.png|

.. method:: WEIGHT_I2CUnit.set_lowpass_filter(Enable)

    Enable or disable the low pass filter.


    UIFLOW2:

        |set_lowpass_filter.png|


.. method:: WEIGHT_I2CUnit.get_lowpass_filter

    Returns the status of the low pass filter (enable or disable).


    UIFLOW2:

        |get_lowpass_filter.png|

.. method:: WEIGHT_I2CUnit.set_average_filter_level(level)

    Sets the level of the average filter.

    - ``level``: Level of the average filter (0 - 50). Larger value for smoother result but more latency

    UIFLOW2:

        |set_average_filter_level.png|

.. method:: WEIGHT_I2CUnit.get_average_filter_level

    Returns the level of the average filter.

    UIFLOW2:

        |get_average_filter_level.png|

.. method:: WEIGHT_I2CUnit.set_ema_filter_alpha(alpha)

    Sets the alpha value for the EMA filter.

    The EMA (Exponential Moving Average) filter is more sensitive to changes in data compared to the average filter.

    - ``alpha``: Alpha value for the EMA filter (0 - 99). Smaller value for smoother result but more latency

    UIFLOW2:

        |set_ema_filter_alpha.png|

.. method:: WEIGHT_I2CUnit.get_ema_filter_alpha

    Returns the alpha value for the EMA filter.

    UIFLOW2:

        |get_ema_filter_alpha.png|

.. method:: WEIGHT_I2CUnit.set_i2c_address(address)

    The i2c address can be changed by the user and this address should be between 0x01 and 0x7F.

    - ``address``: range of address(0x01 - 0x7F).

    UIFLOW2:

        |set_i2c_address.png|

.. method:: WEIGHT_I2CUnit.get_device_spec(info)

    Get the firmware version details and I2c address of this device.

    - ``info``: (0xFE, 0xFF)

    UIFLOW2:

        |get_device_spec.png|
