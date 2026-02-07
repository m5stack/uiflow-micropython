Miniscale Unit
==============

.. include:: ../refs/unit.miniscale.ref

The ``Miniscale`` class is designed for interfacing with a mini scale weight sensor, which includes a HX711 22-bit ADC. This sensor is capable of measuring weight and also includes additional functionalities like LED control and various filters.

Support the following products:


|MINISCALE|



UiFlow2 Example
---------------

Basic Example
^^^^^^^^^^^^^

Open the |m5cores3_miniscales_base_example.m5f2| project in UiFlow2.

This example demonstrates how to read and display weight values from the MiniScale unit. It sets up an average filter level of 10 for smoother readings and updates the weight display every second.

UiFlow2 Code Block:

    |m5cores3_miniscales_base_example.png|

Example output:

    None

Calibration Example
^^^^^^^^^^^^^^^^^^^

Open the |m5cores3_miniscales_calibrate_example.m5f2| project in UiFlow2.

This example demonstrates the complete calibration process for the MiniScale unit. It guides users through a three-step calibration: first removing all items and recording the zero-point ADC value, then placing a 100g weight and recording that ADC value, and finally performing tare operation to set the zero point. After calibration, the weight is displayed with an average filter level of 5.

UiFlow2 Code Block:

    |m5cores3_miniscales_calibrate_example.png|

Example output:

    None

MicroPython Example
-------------------

Basic Example
^^^^^^^^^^^^^

This example demonstrates how to read and display weight values from the MiniScale unit. It sets up an average filter level of 10 for smoother readings and updates the weight display every second.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/miniscales/m5cores3_miniscales_base_example.py
        :language: python
        :linenos:

Example output:

    None

Calibration Example
^^^^^^^^^^^^^^^^^^^

This example demonstrates the complete calibration process for the MiniScale unit. It guides users through a three-step calibration: first removing all items and recording the zero-point ADC value, then placing a 100g weight and recording that ADC value, and finally performing tare operation to set the zero point. After calibration, the weight is displayed with an average filter level of 5.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/miniscales/m5cores3_miniscales_calibrate_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class MiniScaleUnit  
^^^^^^^^^^^^^^^^^^^
 
.. class:: unit.miniscale.MiniScaleUnit(i2c, address=0x26)

    Create a MiniScaleUnit object.

    :param I2C | PAHUBUnit i2c: The I2C or PAHUBUnit instance for communication.
    :param int address: The I2C address of the MiniScale unit, default is 0x26.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import MiniScaleUnit
            from hardware import I2C, Pin

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            miniscale_0 = MiniScaleUnit(i2c0)

    .. method:: adc

        Read raw ADC value (unprocessed).

        :returns: Raw ADC value (integer).
        :rtype: int

        UiFlow2 Code Block:

            |get_adc.png|

        MicroPython Code Block:

            .. code-block:: python

                adc_value = miniscale_0.adc

    .. method:: weight

        Read current weight (grams).

        :returns: Actual weight (float after subtracting tare value).
        :rtype: float

        UiFlow2 Code Block:

            |get_weight.png|

        MicroPython Code Block:

            .. code-block:: python

                weight_value = miniscale_0.weight

    .. method:: button

        Read button state.

        :returns: True if pressed, False if not pressed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_button.png|

        MicroPython Code Block:

            .. code-block:: python

                button_state = miniscale_0.button

    .. method:: tare()

        Tare operation. Record current weight as offset value, so subsequent weight readings use current as zero point.

        UiFlow2 Code Block:

            |tare.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.tare()

    .. method:: set_led(r, g, b)

        Set RGB indicator color.

        :param int r: Red component (0~255).
        :param int g: Green component (0~255).
        :param int b: Blue component (0~255).

        UiFlow2 Code Block:

            |set_led.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.set_led(255, 0, 0)

    .. method:: reset()

        Reset module internal weight register (clear to zero).

        UiFlow2 Code Block:

            |reset.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.reset()

    .. method:: calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)

        Calibrate module gain (GAP value).

        Calibration process example:
        1. Reset offset
        2. Read no-load ADC (RawADC_0g)
        3. Place known weight (e.g., 100g) and read ADC (RawADC_100g)
        4. Calculate GAP = (RawADC_100g - RawADC_0g) / 100
        5. Write to module to save calibration coefficient

        :param float weight1_g: Weight at first point (unit: g).
        :param int weight1_adc: ADC value at first point.
        :param float weight2_g: Weight at second point (unit: g).
        :param int weight2_adc: ADC value at second point.
        :raises ValueError: If two weights are equal.

        UiFlow2 Code Block:

            |calibration.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.calibration(0, adc_0, 100, adc_100)

    .. method:: set_low_pass_filter(enabled)

        Enable or disable low-pass filter.

        :param bool enabled: True to enable filter, False to disable filter.

        UiFlow2 Code Block:

            |set_low_pass_filter.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.set_low_pass_filter(True)

    .. method:: get_low_pass_filter()

        Get low-pass filter status.

        :returns: True if filter is enabled.
        :rtype: bool

        UiFlow2 Code Block:

            |get_low_pass_filter.png|

        MicroPython Code Block:

            .. code-block:: python

                filter_enabled = miniscale_0.get_low_pass_filter()

    .. method:: set_average_filter_level(level)

        Set average filter level.

        :param int level: Average count level (0~50), higher value means smoother but more delay.
        :raises ValueError: If out of range.

        UiFlow2 Code Block:

            |set_average_filter_level.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.set_average_filter_level(10)

    .. method:: get_average_filter_level()

        Get average filter level.

        :returns: Current average filter level (integer).
        :rtype: int

        UiFlow2 Code Block:

            |get_average_filter_level.png|

        MicroPython Code Block:

            .. code-block:: python

                filter_level = miniscale_0.get_average_filter_level()

    .. method:: set_ema_filter_alpha(alpha)

        Set exponential moving average (EMA) filter parameter.

        The EMA (Exponential Moving Average) filter is more sensitive to changes in data compared to the average filter.

        :param int alpha: EMA filter coefficient (0~99), smaller value means smoother but more response delay.
        :raises ValueError: If out of range.

        UiFlow2 Code Block:

            |set_ema_filter_alpha.png|

        MicroPython Code Block:

            .. code-block:: python

                miniscale_0.set_ema_filter_alpha(50)

    .. method:: get_ema_filter_alpha()

        Get EMA filter coefficient.

        :returns: Current EMA alpha value (integer).
        :rtype: int

        UiFlow2 Code Block:

            |get_ema_filter_alpha.png|

        MicroPython Code Block:

            .. code-block:: python

                ema_alpha = miniscale_0.get_ema_filter_alpha()


