
ENVPRO Unit
===========
.. sku:U169
.. include:: ../refs/unit.envpro.ref

ENV Pro Unit is an environmental sensor that utilizes the BME688 sensor solution, supporting the measurement of various environmental parameters such as volatile organic compounds (VOCs), indoor air quality (IAQ), temperature, humidity, and atmospheric pressure. It features a compact size, wide operating range, simple communication interface (I2C), excellent performance, and low power consumption, making it suitable for weather stations, indoor environmental monitoring, and air quality detection applications.

Support the following products:

|ENVPROUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/envpro/envpro_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |envpro_cores3_example.m5f2|

class ENVPROUnit
----------------

Constructors
------------

.. class:: ENVPROUnit(i2c, address)

    Initialize the ENVPROUnit with an I2C object and an optional address.

    :param  i2c: The I2C interface or PAHUBUnit instance to communicate with the ENV PRO sensor.
    :param int address: The I2C address of the ENV PRO sensor. Defaults to 0x77.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ENVPROUnit.get_over_sampling_rate(env)

    Retrieve the oversampling rate for the specified environment parameter.

    :param  env: The environment parameter (TEMPERATURE, PRESSURE, HUMIDITY).

    UIFLOW2:

        |get_over_sampling_rate.png|

.. method:: ENVPROUnit.set_over_sampling_rate(env, rate)

    Set the oversampling rate for the specified environment parameter.

    :param  env: The environment parameter (TEMPERATURE, PRESSURE, HUMIDITY).
    :param  rate: The oversampling rate to be set.

    UIFLOW2:

        |set_over_sampling_rate.png|

.. method:: ENVPROUnit.get_iir_filter_coefficient()

    Retrieve the IIR filter coefficient.


    UIFLOW2:

        |get_iir_filter_coefficient.png|

.. method:: ENVPROUnit.set_iir_filter_coefficient(value)

    Set the IIR filter coefficient.

    :param  value: The IIR filter coefficient to be set.

    UIFLOW2:

        |set_iir_filter_coefficient.png|

.. method:: ENVPROUnit.get_temperature()

    Retrieve the measured temperature.


    UIFLOW2:

        |get_temperature.png|

.. method:: ENVPROUnit.get_humidity()

    Retrieve the measured humidity.


    UIFLOW2:

        |get_humidity.png|

.. method:: ENVPROUnit.get_pressure()

    Retrieve the measured pressure.


    UIFLOW2:

        |get_pressure.png|

.. method:: ENVPROUnit.get_gas_resistance()

    Retrieve the measured gas resistance.


    UIFLOW2:

        |get_gas_resistance.png|

.. method:: ENVPROUnit.get_altitude()

    Retrieve the calculated altitude based on pressure readings.

    ``Note``: Altitude is calculated based on the difference between barometric pressure and sea level pressure


    UIFLOW2:

        |get_altitude.png|



Constants
---------

    .. data:: ENVPROUnit.TEMPERATURE
    .. data:: ENVPROUnit.PRESSURE
    .. data:: ENVPROUnit.HUMIDITY