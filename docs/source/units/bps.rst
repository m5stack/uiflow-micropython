BPS Unit
========

.. include:: ../refs/unit.bps.ref

The Barometric Pressure Sensor(BPS) ``BPS Unit`` is a barometer unit that uses Bosch BMP280 pressure sensor(BPS) or QMP6988 barometric pressure sensor(BPS V1.1) to measure atmospheric pressure, temperature and altitude estimation.

Support the following products:

    ========= ============= 
    |BPSUnit| |BPSUnit_V11|           
    ========= =============

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import BPSUnit
    import time

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    bps_0 = BPSUnit(i2c0)

    while True:
        print((str('Temperature: ') + str((bps_0.get_temperature()))))
        print((str('Pressure: ') + str((bps_0.get_pressure()))))
        print((str('Altitude: ') + str((bps_0.get_altitude()))))
        time.sleep(0.5)

UIFLOW2 Example:

    |unit-bps-demo.png|

.. only:: builder_html

    |unit-bps-demo.m5f2|


class BPSUnit
-------------

Constructors
------------

.. class:: BPSUnit(i2c)

    Create a BPSUnit object

    :param i2c: the I2C object.
    
    UIFLOW2:

        |init.png|


Methods
-------


.. method:: BPSUnit.get_temperature()

    Get the temperature value in degrees celsius from the BMP280 or QMP6988 sensor. 

    - Return: ``float``:  -40 ~ +85 °C

    UIFLOW2:

        |get_temperature.png|


.. method:: BPSUnit.get_pressure()

    Get the pressure value in pascals from the BMP280 or QMP6988 sensor. 

    - Return: ``float``:  300 ~ 1100 hPa

    UIFLOW2:

        |get_pressure.png|


.. method:: BPSUnit.get_altitude()

    Get the altitude can be estimated using the pressure. 
    which approximates the altitude relative to the pressure difference. 
    The standard sea-level pressure is 1013.25 hPa.

    - Return: ``float``:  altitude in meters

    UIFLOW2:

        |get_altitude.png|
