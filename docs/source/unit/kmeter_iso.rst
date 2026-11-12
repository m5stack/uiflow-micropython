Kmeter ISO Unit
===============

.. include:: ../refs/unit.kmeter_iso.ref


Supported Products:


    |KmeterISOUnit| 


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import KMeterISOUnit
    import time
    

    M5.begin()
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    kmeter_iso_0 = KMeterISOUnit(i2c0, 0x66)
    while True:
        if kmeter_iso_0.is_ready():
            print(kmeter_iso_0.get_thermocouple_temperature(0))
            print(kmeter_iso_0.get_internal_temperature(0))
        time.sleep_ms(250)


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_kmeteriso_example.m5f2|


class KMeterISOUnit
-------------------

Constructors
------------

Import with ``from unit import KMeterISOUnit``.

.. class:: KMeterISOUnit(i2c, address=0x66)

    :param object i2c: the I2C object.
    :param int address: 0x08 ~ 0x77.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: KMeterISOUnit.get_thermocouple_temperature(scale=0) -> float

    Get the temperature of the thermocouple in the KmeterISO Unit. Returns a float value.

    ``scale`` accepts values of :py:data:`KMeterISOUnit.CELSIUS` or :py:data:`KMeterISOUnit.FAHRENHEIT`.

    UIFLOW2:

        |get_thermocouple_temperature.png|


.. method:: KMeterISOUnit.get_internal_temperature(scale=0) -> float

    Get the internal temperature of the KmeterISO Unit. Returns a float value.

    ``scale`` accepts values of :py:data:`KMeterISOUnit.CELSIUS` or :py:data:`KMeterISOUnit.FAHRENHEIT`.

    UIFLOW2:

        |get_internal_temperature.png|


.. method:: KMeterISOUnit.is_ready() -> bool

    Check if the measurement result is ready.

    UIFLOW2:

        |is_ready.png|


.. method:: KMeterISOUnit.get_thermocouple_temperature_string(scale=0) -> str

    Get the temperature of the thermocouple in the KmeterISO Unit as a string with a sign.

    ``scale`` accepts values of :py:data:`KMeterISOUnit.CELSIUS` or :py:data:`KMeterISOUnit.FAHRENHEIT`.

    UIFLOW2:

        |get_thermocouple_temperature_string.png|


.. method:: KMeterISOUnit.get_internal_temperature_string(scale=0) -> str

    Get the internal temperature of the KmeterISO Unit as a string with a sign.

    ``scale`` accepts values of :py:data:`KMeterISOUnit.CELSIUS` or :py:data:`KMeterISOUnit.FAHRENHEIT`.

    UIFLOW2:

        |get_internal_temperature_string.png|


.. method:: KMeterISOUnit.get_device_info(mode) -> int

    Get the firmware version of the KmeterISO Unit. Returns an integer version number.

    :param int mode: 

    ====    ==========
    int     mode
    0xFE    firmware version
    0xFF    i2c address
    ====    ==========

    UIFLOW2:

        |get_device_spec.png|


.. method:: KMeterISOUnit.set_i2c_address(address) -> int

    Set the i2c address can be changed by the user and this address should be between 0x08 and 0x77.

    UIFLOW2:

        |set_i2c_address.png|


Constants
---------

.. data:: KMeterISOUnit.CELSIUS
    :type: int

    Celsius scale.


.. data:: KMeterISOUnit.FAHRENHEIT
    :type: int

    Fahrenheit scale.
