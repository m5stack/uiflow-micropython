
HeartHat
=========

.. include:: ../refs/hat.heart.ref

MAX30102 is a complete pulse oximetry and heart-rate sensor system solution designed for the demanding requirements of wearable devices.

Support the following products:

|HeartHat|

Micropython Example:

    .. literalinclude:: ../../../examples/hat/heart/stickc_heart_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_heart_example.m5f2|


class HeartHat
---------------

Constructors
------------

.. class:: HeartHat(i2c, address)

    Initialize the HeartHat.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the HeartHat.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: HeartHat.stop()

    Stop the HeartHat.


    UIFLOW2:

        |stop.png|

.. method:: HeartHat.start()

    Start the HeartHat.


    UIFLOW2:

        |start.png|

.. method:: HeartHat.deinit()

    Deinitialize the HeartHat.


    UIFLOW2:

        |deinit.png|

.. method:: HeartHat.get_heart_rate()

    Get the heart rate.


    UIFLOW2:

        |get_heart_rate.png|

.. method:: HeartHat.get_spo2()

    Get the SpO2.


    UIFLOW2:

        |get_spo2.png|

.. method:: HeartHat.get_ir()

    Get the IR value.


    UIFLOW2:

        |get_ir.png|

.. method:: HeartHat.get_red()

    Get the red value.


    UIFLOW2:

        |get_red.png|

.. method:: HeartHat.set_mode(mode)

    Set the mode of the HeartHat.

    :param int mode: The detect mode of the HeartHat.
        Options:
        - ``HeartHat.MODE_HR_ONLY``: Only heart rate
        - ``HeartHat.MODE_SPO2_HR``: Heart rate and SpO2

    UIFLOW2:

        |set_mode.png|

.. method:: HeartHat.set_led_current(led_current)

    Set the LED current of the HeartHat.

    :param int led_current: The LED current of the HeartHat.
        Options:
        - ``HeartHat.LED_CURRENT_0MA``: 0mA
        - ``HeartHat.LED_CURRENT_4_4MA``: 4.4mA
        - ``HeartHat.LED_CURRENT_7_6MA``: 7.6mA
        - ``HeartHat.LED_CURRENT_11MA``: 11mA
        - ``HeartHat.LED_CURRENT_14_2MA``: 14.2mA
        - ``HeartHat.LED_CURRENT_17_4MA``: 17.4mA
        - ``HeartHat.LED_CURRENT_20_8MA``: 20.8mA
        - ``HeartHat.LED_CURRENT_24MA``: 24mA
        - ``HeartHat.LED_CURRENT_27_1MA``: 27.1mA
        - ``HeartHat.LED_CURRENT_30_6MA``: 30.6mA
        - ``HeartHat.LED_CURRENT_33_8MA``: 33.8mA
        - ``HeartHat.LED_CURRENT_37MA``: 37mA
        - ``HeartHat.LED_CURRENT_40_2MA``: 40.2mA
        - ``HeartHat.LED_CURRENT_43_6MA``: 43.6mA
        - ``HeartHat.LED_CURRENT_46_8MA``: 46.8mA
        - ``HeartHat.LED_CURRENT_50MA``: 50mA

    UIFLOW2:

        |set_led_current.png|

.. method:: HeartHat.set_pulse_width(pulse_width)

    Set the pulse width of the HeartHat.

    :param int pulse_width: The pulse width of the HeartHat.
        Options:
        - ``HeartHat.PULSE_WIDTH_200US_ADC_13``: 200us
        - ``HeartHat.PULSE_WIDTH_400US_ADC_14``: 400us
        - ``HeartHat.PULSE_WIDTH_800US_ADC_15``: 800us
        - ``HeartHat.PULSE_WIDTH_1600US_ADC_16``: 1600us

    UIFLOW2:

        |set_pulse_width.png|

.. method:: HeartHat.set_sampling_rate(sampling_rate)

    Set the sampling rate of the HeartHat.

    :param int sampling_rate: The sampling rate of the HeartHat.
        Options:
        - ``HeartHat.SAMPLING_RATE_50HZ``: 50Hz
        - ``HeartHat.SAMPLING_RATE_100HZ``: 100Hz
        - ``HeartHat.SAMPLING_RATE_167HZ``: 167Hz
        - ``HeartHat.SAMPLING_RATE_200HZ``: 200Hz
        - ``HeartHat.SAMPLING_RATE_400HZ``: 400Hz
        - ``HeartHat.SAMPLING_RATE_600HZ``: 600Hz
        - ``HeartHat.SAMPLING_RATE_800HZ``: 800Hz
        - ``HeartHat.SAMPLING_RATE_1000HZ``: 1000Hz

    UIFLOW2:

        |set_sampling_rate.png|



Constants
---------

.. data:: HeartHat.MODE_HR_ONLY

    Detect heart rate only.

.. data:: HeartHat.MODE_SPO2_HR

    Detect heart rate and SpO2.



