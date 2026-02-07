IMU Unit
=========

.. include:: ../refs/unit.imu.ref

6-Axis IMU Unit is a 6-axis attitude sensor with 3-axis gravity accelerometer and 3-axis gyroscope, which can calculate tilt angle and acceleration in real time. The chip adopts mpu6886

Support the following products:

    |IMUUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import IMUUnit
    import time

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    imu_0 = IMUUnit(i2c0)
    imu_0.set_accel_unit(1)
    imu_0.set_gyro_unit(1)

    while True:
        print((str('Acc:') + str((imu_0.get_accelerometer()))))
        print((str('Gryo:') + str((imu_0.get_gyroscope()))))
        print((str('Attitude') + str((imu_0.get_attitude()))))
        time.sleep_ms(100)

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |unit-imu-demo.m5f2|


class IMUUnit
-------------

Constructors
------------

.. class:: IMUUnit(i2c)

    Create a IMUUnit object

    :param i2c: the I2C object.
    
    UIFLOW2:

        |init.png|


Methods
-------

.. method:: IMUUnit.get_accelerometer()

    Get the tuple of x, y, and z values of the accelerometer and acceleration vector in gravity units (9.81m/s^2). 

    - Return: ``tuple``:  (float, float, float)

    UIFLOW2:

        |get_accelerometer.png|


.. method:: IMUUnit.get_gyroscope()

    Get the tuple of x, y, and z values of the gyroscope and gyroscope vector in rad/sec.

    - Return: ``tuple``:  (float, float, float)   

    UIFLOW2:

        |get_gyroscope.png|


.. method:: IMUUnit.get_attitude()

    Get the attitude angles as yaw, pitch, and roll in degrees.. 

    - Return: ``tuple``:  (float, float, float)

    UIFLOW2:

        |get_attitude.png|


.. method:: IMUUnit.set_accel_range(accel_scale)

    Set the accelerometer scale range. 

    :param accel_scale: scale range of ±2g, ±4g, ±8g and ±16g.
    :type unit: int

    UIFLOW2:

        |set_accel_range.png|


.. method:: IMUUnit.set_gyro_range(gyro_scale)

    Set the gyroscope scale range. 

    :param gyro_scale: scale range of ±250 dps, ±500 dps, ±1000 dps, and ±2000 dps. 
    :type unit: int

    UIFLOW2:

        |set_gyro_range.png|


.. method:: IMUUnit.set_accel_unit(unit)

    Set the accelerometer unit g or m/s^2. 
    
    :param unit: 0: g,  1: m/s^2.
    :type unit: int
    
    UIFLOW2:

        |set_accel_unit.png|


.. method:: IMUUnit.set_gyro_unit(unit)

    Set the gyroscope unit rad/sec or degrees/sec. 

    :param unit: 0: degrees/sec, 1: rad/sec.
    :type unit: int

    UIFLOW2:

        |set_gyro_unit.png|


.. method:: IMUUnit.set_gyro_calibrate(samples, delay)

    Set the gyro calibrations with the number of samples and delay of each samples 
    
    :param samples: number of samples.
    :type samples: int.
    :param delay: delay in milliseconds for each samples.
    :type delay: int
    
    UIFLOW2:

        |set_gyro_calibrate.png|


.. method:: IMUUnit.set_gyro_offsets(x, y, z)

    Set the manual gyro calibrations offsets value
    
    :param x: 0.0
    :type unit: float
    :param y: 0.0
    :type unit: float
    :param z: 0.0
    :type unit: float
    
    UIFLOW2:

        |set_gyro_offsets.png|

