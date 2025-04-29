Miniscale Unit
==============

.. include:: ../refs/unit.miniscale.ref

The ``Miniscale`` class is designed for interfacing with a mini scale weight sensor, which includes a HX711 22-bit ADC. This sensor is capable of measuring weight and also includes additional functionalities like LED control and various filters.

Support the following products:


|MINISCALE|



Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import MiniScaleUnit

    i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    scale = MiniScaleUnit(i2c)
    scale.setLed(255, 0, 0)
    print(miniscale.weight)


UIFLOW2 Example:

    |example.png|


.. only:: builder_html


class MiniScaleUnit
-------------------

Constructors
---------------------------

.. class:: MiniScaleUnit(i2c0)

    Create an MiniScaleUnit object.

    - ``I2C0`` is I2C Port.


    UIFLOW2:

        |init.png|


Methods
----------------------

.. method:: MiniScaleUnit.adc


    Gets the raw adc readout.

    UIFLOW2:

        |get_adc.png|

.. method:: MiniScaleUnit.weight


    Gets the weight readout in grams.

    UIFLOW2:

        |get_weight.png|


.. method:: MiniScaleUnit.button


    Gets the button state.

    UIFLOW2:

        |get_button.png|

.. method:: MiniScaleUnit.tare()


    Tare the scale.

    UIFLOW2:

        |tare.png|

.. method:: MiniScaleUnit.set_led(r, g, b)

    Sets the RGB LED color.

    - ``r``: Red value (0 - 255).
    - ``g``: Green value (0 - 255).
    - ``b``: Blue value (0 - 255).

    UIFLOW2:

        |setLed.png|

.. method:: MiniScaleUnit.reset

    Resets sensor.


    UIFLOW2:

        |reset.png|

.. method:: MiniScaleUnit.calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)


    Calibrates the MiniScale sensor.

    - ``weight1_g``: Weight1 in grams.
    - ``weight1_adc``: Weight1 in ADC value.
    - ``weight2_g``: Weight2 in grams.
    - ``weight2_adc``: Weight2 in ADC value.

    calibration steps:

    1. Reset sensor;
    2. Get adc, this is weight1_adc (should be zero). And weight1_g is also 0.
    3. Put some weight on it, then get adc, this is weight2_adc. And weight2_g is weight in gram you put on it.


    UIFLOW2:

        |calibration.png|

.. method:: MiniScaleUnit.set_low_pass_filter(enable)

    Enables or disables the low pass filter.


    UIFLOW2:

        |setLowPassFilter.png|


.. method:: MiniScaleUnit.get_low_pass_filter

    Returns the status of the low pass filter (enabled or not).


    UIFLOW2:

        |getLowPassFilter.png|

.. method:: MiniScaleUnit.set_average_filter_level(level)

    Sets the level of the average filter.

    - ``level``: Level of the average filter (0 - 50). Larger value for smoother result but more latency

    UIFLOW2:

        |setAverageFilterLevel.png|

.. method:: MiniScaleUnit.get_average_filter_level

    Returns the level of the average filter.

    UIFLOW2:

        |getAverageFilterLevel.png|

.. method:: MiniScaleUnit.set_ema_filter_alpha(alpha)

    Sets the alpha value for the EMA filter.

    The EMA (Exponential Moving Average) filter is more sensitive to changes in data compared to the average filter.

    - ``alpha``: Alpha value for the EMA filter (0 - 99). Smaller value for smoother result but more latency

    UIFLOW2:

        |setEMAFilterAlpha.png|

.. method:: MiniScaleUnit.get_ema_filter_alpha

    Returns the alpha value for the EMA filter.

    UIFLOW2:

        |getEMAFilterAlpha.png|

