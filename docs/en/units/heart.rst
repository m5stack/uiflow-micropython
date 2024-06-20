
HeartUnit
=========

.. include:: ../refs/unit.heart.ref

MAX30100 is a complete pulse oximetry and heart-rate sensor system solution designed for the demanding requirements of wearable devices.

Support the following products:

|HeartUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/heart/core_heart_unit_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |core_heart_unit_example.m5f2|

class HeartUnit
---------------

Constructors
------------

.. class:: HeartUnit(i2c, address)

    Initialize the HeartUnit.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the HeartUnit.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: HeartUnit.stop()

    Stop the HeartUnit.


    UIFLOW2:

        |stop.png|

.. method:: HeartUnit.start()

    Start the HeartUnit.


    UIFLOW2:

        |start.png|

.. method:: HeartUnit.deinit()

    Deinitialize the HeartUnit.


    UIFLOW2:

        |deinit.png|

.. method:: HeartUnit.get_heart_rate()

    Get the heart rate.


    UIFLOW2:

        |get_heart_rate.png|

.. method:: HeartUnit.get_spo2()

    Get the SpO2.


    UIFLOW2:

        |get_spo2.png|

.. method:: HeartUnit.get_ir()

    Get the IR value.


    UIFLOW2:

        |get_ir.png|

.. method:: HeartUnit.get_red()

    Get the red value.


    UIFLOW2:

        |get_red.png|

.. method:: HeartUnit.set_mode(mode)

    Set the mode of the HeartUnit.

    :param int mode: The detect mode of the HeartUnit.
        Options:
        - ``HeartUnit.MODE_HR_ONLY``: Only heart rate
        - ``HeartUnit.MODE_SPO2_HR``: Heart rate and SpO2

    UIFLOW2:

        |set_mode.png|

.. method:: HeartUnit.set_led_current(led_current)

    Set the LED current of the HeartUnit.

    :param int led_current: The LED current of the HeartUnit.
        Options:
        - ``HeartUnit.LED_CURRENT_0MA``: 0mA
        - ``HeartUnit.LED_CURRENT_4_4MA``: 4.4mA
        - ``HeartUnit.LED_CURRENT_7_6MA``: 7.6mA
        - ``HeartUnit.LED_CURRENT_11MA``: 11mA
        - ``HeartUnit.LED_CURRENT_14_2MA``: 14.2mA
        - ``HeartUnit.LED_CURRENT_17_4MA``: 17.4mA
        - ``HeartUnit.LED_CURRENT_20_8MA``: 20.8mA
        - ``HeartUnit.LED_CURRENT_24MA``: 24mA
        - ``HeartUnit.LED_CURRENT_27_1MA``: 27.1mA
        - ``HeartUnit.LED_CURRENT_30_6MA``: 30.6mA
        - ``HeartUnit.LED_CURRENT_33_8MA``: 33.8mA
        - ``HeartUnit.LED_CURRENT_37MA``: 37mA
        - ``HeartUnit.LED_CURRENT_40_2MA``: 40.2mA
        - ``HeartUnit.LED_CURRENT_43_6MA``: 43.6mA
        - ``HeartUnit.LED_CURRENT_46_8MA``: 46.8mA
        - ``HeartUnit.LED_CURRENT_50MA``: 50mA

    UIFLOW2:

        |set_led_current.png|

.. method:: HeartUnit.set_pulse_width(pulse_width)

    Set the pulse width of the HeartUnit.

    :param int pulse_width: The pulse width of the HeartUnit.
        Options:
        - ``HeartUnit.PULSE_WIDTH_200US_ADC_13``: 200us
        - ``HeartUnit.PULSE_WIDTH_400US_ADC_14``: 400us
        - ``HeartUnit.PULSE_WIDTH_800US_ADC_15``: 800us
        - ``HeartUnit.PULSE_WIDTH_1600US_ADC_16``: 1600us

    UIFLOW2:

        |set_pulse_width.png|

.. method:: HeartUnit.set_sampling_rate(sampling_rate)

    Set the sampling rate of the HeartUnit.

    :param int sampling_rate: The sampling rate of the HeartUnit.
        Options:
        - ``HeartUnit.SAMPLING_RATE_50HZ``: 50Hz
        - ``HeartUnit.SAMPLING_RATE_100HZ``: 100Hz
        - ``HeartUnit.SAMPLING_RATE_167HZ``: 167Hz
        - ``HeartUnit.SAMPLING_RATE_200HZ``: 200Hz
        - ``HeartUnit.SAMPLING_RATE_400HZ``: 400Hz
        - ``HeartUnit.SAMPLING_RATE_600HZ``: 600Hz
        - ``HeartUnit.SAMPLING_RATE_800HZ``: 800Hz
        - ``HeartUnit.SAMPLING_RATE_1000HZ``: 1000Hz

    UIFLOW2:

        |set_sampling_rate.png|



Constants
---------

.. data:: HeartUnit.MODE_HR_ONLY

    Detect heart rate only.

.. data:: HeartUnit.MODE_SPO2_HR

    Detect heart rate and SpO2.



