
ADCV11Unit
==========
.. sku:U013-V11
.. include:: ../refs/unit.adc_v11.ref

ADC V1.1 Unit is an A/D conversion module that utilizes the ADS1110 chip, a 16-bit self-calibrating analog-to-digital converter. It is designed with an I2C interface, offering convenient connectivity. The module offers conversion speeds of 8, 16, 32, and 128 samples per second (SPS), providing varying levels of accuracy at 16, 15, 14, and 12 bits of resolution respectively.

Support the following products:

|ADCV11Unit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/adc_v11/adcv11_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |adcv11_core2_example.m5f2|

class ADCV11Unit
----------------

Constructors
------------

.. class:: ADCV11Unit(i2c)

    Initialize the ADCV11Unit with an I2C or PAHUBUnit interface.

    :param  i2c: The I2C or PAHUBUnit instance used for communication.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ADCV11Unit.get_voltage()

    Get the measured voltage from the ADC V1.1 Unit.

    :return: The measured voltage value, rounded to two decimal places.

    UIFLOW2:

        |get_voltage.png|

.. method:: ADCV11Unit.set_gain(gain)

    Set the gain configuration for the ADC.

    :param  gain: The gain value to configure.

    UIFLOW2:

        |set_gain.png|

.. method:: ADCV11Unit.set_sample_rate(rate)

    Configure the ADC's sampling rate.


    :param  rate: The sample rate to set.

    UIFLOW2:

        |set_sample_rate.png|

.. method:: ADCV11Unit.set_mode(mode)

    Set the ADC's operating mode.

    :param  mode: The mode to configure, e.g., continuous or single conversion.

    UIFLOW2:

        |set_mode.png|

.. method:: ADCV11Unit.set_config()

    Update the ADC configuration register with the current settings.

.. method:: ADCV11Unit.get_adc_raw_value()

    Read the raw ADC value.

    UIFLOW2:

        |get_adc_raw_value.png|


