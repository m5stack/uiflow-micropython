IMU Pro Unit
============

.. include:: ../refs/unit.imupro.ref

The ``IMU Pro Unit`` is a versatile and integrated inertial motion unit. It incorporates advanced six-axis attitude sensors (BMI270), a three-axis geomagnetic sensor (BMM150), and an atmospheric pressure sensor (BMP280) to provide comprehensive measurement and detection capabilities for users. Whether it is measuring acceleration and angular velocity, detecting the direction and intensity of the geomagnetic field, or measuring atmospheric pressure.

Support the following products:

    |IMUProUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import IMUProUnit
    import time

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    imupro_0 = IMUProUnit(i2c0)

    while True:
        print((str('Acc:') + str((imupro_0.get_accelerometer()))))
        print((str('Gryo:') + str((imupro_0.get_gyroscope()))))
        print((str('Magneto:') + str((imupro_0.get_magnetometer()))))
        print((str('Compass:') + str((imupro_0.get_compass()))))
        print((str('Attitude') + str((imupro_0.get_attitude()))))
        print((str('Temperature') + str((imupro_0.get_temperature()))))
        print((str('Pressure:') + str((imupro_0.get_pressure()))))
        time.sleep_ms(100)

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |unit-imu-pro-demo.m5f2|


class IMUProUnit
----------------

Constructors
------------

.. class:: IMUProUnit(i2c)

    Create a IMUProUnit object

    :param i2c: the I2C object.
    
    UIFLOW2:

        |init.png|


Methods
-------

.. method:: IMUProUnit.get_accelerometer()

    Get the tuple of x, y, and z values of the accelerometer and acceleration vector in gravity units (9.81m/s^2). 

    - Return: ``tuple``:  (float, float, float)

    UIFLOW2:

        |get_accelerometer.png|


.. method:: IMUProUnit.get_gyroscope()

    Get the tuple of x, y, and z values of the gyroscope and gyroscope vector in rad/sec.

    - Return: ``tuple``:  (float, float, float)   

    UIFLOW2:

        |get_gyroscope.png|


.. method:: IMUProUnit.get_magnetometer()

    Get the tuple of x, y, and z values of the magnetometer and magnetometer vector in uT.

    - Return: ``tuple``:  (float, float, float)   

    UIFLOW2:

        |get_magnetometer.png|


.. method:: IMUProUnit.get_compass()

    Get the compass heading value is in range of 0º ~ 360º.

    - Return: ``float``:  0 ~ 360  

    UIFLOW2:

        |get_compass.png|


.. method:: IMUProUnit.get_attitude()

    Get the attitude angles as yaw, pitch, and roll in degrees. 

    - Return: ``tuple``:  (float, float, float)

    UIFLOW2:

        |get_attitude.png|


.. method:: IMUProUnit.get_temperature()

    Get the temperature value in degrees celsius from the BMP280 sensor. 

    - Return: ``float``:  -40 ~ +85 °C

    UIFLOW2:

        |get_temperature.png|


.. method:: IMUProUnit.get_pressure()

    Get the pressure value in pascals from the BMP280 sensor. 

    - Return: ``float``:  300 ~ 1100 hPa

    UIFLOW2:

        |get_pressure.png|


.. method:: IMUProUnit.set_accel_gyro_odr(accel_odr, gyro_odr)

    Set the accelerometer and gyroscope output data rate(ODR): 0.78 Hz … 1.6 kHz (accelerometer) and 25 Hz … 6.4 kHz (gyroscope). 

    :param accel_odr: range of 0.78 Hz … 1.6 kHz.
    :type unit: float
    :param gyro_odr: range of 25 Hz … 6.4 kHz.
    :type unit: float

    UIFLOW2:

        |set_accel_gyro_odr.png|


.. method:: IMUProUnit.set_magnet_odr(magnet_odr)

    Set the magnetometer output data rate(ODR): 2, 6, 8, 10(default), 15, 20, 25, 30Hz.

    :param magnet_odr: range of 2Hz … 30Hz.
    :type unit: int

    UIFLOW2:

        |set_magnet_odr.png|


.. method:: IMUProUnit.set_accel_range(accel_scale)

    Set the accelerometer scale range. 

    :param accel_scale: scale range of ±2g, ±4g, ±8g and ±16g.
    :type unit: int

    UIFLOW2:

        |set_accel_range.png|


.. method:: IMUProUnit.set_gyro_range(gyro_scale)

    Set the gyroscope scale range. 

    :param gyro_scale: scale range of ±125 dps, ±250 dps, ±500 dps, ±1000 dps, and ±2000 dps. 
    :type unit: int

    UIFLOW2:

        |set_gyro_range.png|


.. method:: IMUProUnit.set_gyro_offsets(x, y, z)

    Set the manual gyro calibrations offsets value
    
    :param x: 0.0
    :type unit: float
    :param y: 0.0
    :type unit: float
    :param z: 0.0
    :type unit: float
    
    UIFLOW2:

        |set_gyro_offsets.png|

