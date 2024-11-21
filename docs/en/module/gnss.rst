
GNSSModule
==========

.. include:: ../refs/module.gnssmodule.ref

GNSS Module is a global positioning wireless communication module featuring the NEO-M9N-00B GPS module. It incorporates BMI270, BMM150 and a barometric pressure sensor.

Support the following products:

|GNSSModule|

Micropython Example:

    .. literalinclude:: ../../../examples/module/gnss/gnss_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |gnss_core2_example.m5f2|

class GNSSModule
----------------

Constructors
------------

.. class:: GNSSModule(id, rx, tx, address)

    initialize Function.

    :param int id: UART controllers id, the range is 0 to 2.
    :param int rx: UART rx pin.
    :param int tx: UART tx pin.
    :param int address: 

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: GNSSModule.set_accel_gyro_odr(accel_odr, gyro_odr)

    Set the accelerometer and gyroscope output data rate.

    :param  accel_odr: range of 0.78 Hz … 1.6 kHz.
        Options:
        - ``25``: 25
        - ``50``: 50
        - ``100``: 100
        - ``200``: 200
        - ``400``: 400
        - ``800``: 800
        - ``1600``: 1600
        - ``0.78``: 0.78
        - ``1.5``: 1.5
        - ``3.1``: 3.1
        - ``6.25``: 6.25
        - ``12.5``: 12.5
    :param  gyro_odr: range of 25 Hz … 6.4 kHz.
        Options:
        - ``25``: 25
        - ``50``: 50
        - ``100``: 100
        - ``200``: 200
        - ``400``: 400
        - ``800``: 800
        - ``1600``: 1600
        - ``3200``: 3200

    UIFLOW2:

        |set_accel_gyro_odr.png|

.. method:: GNSSModule.set_accel_range(accel_scale)

    Set the accelerometer scale range.

    :param  accel_scale: scale range of ±2g, ±4g, ±8g and ±16g.
        Options:
        - ``2``: 2
        - ``4``: 4
        - ``8``: 8
        - ``16``: 16

    UIFLOW2:

        |set_accel_range.png|

.. method:: GNSSModule.set_gyro_range(gyro_scale)

    Set the gyroscope scale range.

    :param  gyro_scale: 
        Options:
        - ``125``: 125
        - ``250``: 250
        - ``500``: 500
        - ``1000``: 1000
        - ``2000``: 2000

    UIFLOW2:

        |set_gyro_range.png|

.. method:: GNSSModule.set_magnet_odr(magnet_odr)


    :param  magnet_odr: 
        Options:
        - ``2``: 2
        - ``6``: 6
        - ``8``: 8
        - ``10``: 10
        - ``15``: 15
        - ``20``: 20
        - ``25``: 25
        - ``30``: 30

    UIFLOW2:

        |set_magnet_odr.png|

.. method:: GNSSModule.set_gyro_offsets(x, y, z)

    Set the manual gyro calibrations offsets value.

    :param  x: gyro calibrations offsets value of X-axis
    :param  y: gyro calibrations offsets value of Y-axis
    :param  z: gyro calibrations offsets value of Z-axis

    UIFLOW2:

        |set_gyro_offsets.png|

.. method:: GNSSModule.get_gyroscope()

    Get the tuple of x, y, and z values of the gyroscope and gyroscope vector in rad/sec.

    :return (tuple): gyroscope tuple (float, float, float)

    UIFLOW2:

        |get_gyroscope.png|

.. method:: GNSSModule.get_accelerometer()

    Get the tuple of x, y, and z values of the accelerometer and acceleration vector in gravity units (9.81m/s^2).

    :return (tuple): accelerometer tuple (float, float, float)

    UIFLOW2:

        |get_accelerometer.png|

.. method:: GNSSModule.get_magnetometer()

    Get the tuple of x, y, and z values of the magnetometer and magnetometer vector in uT.

    :return (tuple): magnetometer tuple (float, float, float)

    UIFLOW2:

        |get_magnetometer.png|

.. method:: GNSSModule.get_compass()

    Get the compass heading value is in range of 0º ~ 360º.

    :return (float): range is 0 to 360 degree

    UIFLOW2:

        |get_compass.png|

.. method:: GNSSModule.get_attitude()

    Get the attitude angles as yaw, pitch, and roll in degrees.

    :return (tuple): tuple of yaw, pitch, and roll (float, float, float)

    UIFLOW2:

        |get_attitude.png|

.. method:: GNSSModule.get_temperature()

    Get the temperature value in degrees celsius from the BMP280 sensor.

    :return (float): range is -40 ~ +85 °C.

    UIFLOW2:

        |get_temperature.png|

.. method:: GNSSModule.get_pressure()

    Get the pressure value in pascals from the BMP280 sensor.

    :return (float): range is 300 ~ 1100 hPa.

    UIFLOW2:

        |get_pressure.png|

.. method:: GNSSModule.set_time_zone(value)

    set timezone function.

    :param int value: timezone value

    UIFLOW2:

        |set_time_zone.png|

.. method:: GNSSModule.get_time_zone()

    get timezone function.

    :return (int): timezone value

    UIFLOW2:

        |get_time_zone.png|

.. method:: GNSSModule.get_satellite_num()

    get satellite numbers.

    :return (str): satellite numbers value.

    UIFLOW2:

        |get_satellite_num.png|

.. method:: GNSSModule.get_altitude()

    get altitude.

    :return (str): altitude unit is meter.

    UIFLOW2:

        |get_altitude.png|

.. method:: GNSSModule.get_time()

    get time.

    :return (str): time(hh:mm:ss)

    UIFLOW2:

        |get_time.png|

.. method:: GNSSModule.get_date()

    get date.

    :return (str): date(dd/mm/yy)

    UIFLOW2:

        |get_date.png|

.. method:: GNSSModule.get_latitude()

    get latitude.

    :return (str): latitude, using degrees minutes format (ddmm.mmmmmN/S).

    UIFLOW2:

        |get_latitude.png|

.. method:: GNSSModule.get_longitude()

    get longitude.

    :return (str): longitude, using degrees minutes format (ddmm.mmmmmE/W).

    UIFLOW2:

        |get_longitude.png|

.. method:: GNSSModule.get_latitude_decimal()

    get latitude decimal.

    :return (float): latitude decimal(dd.dddd).

    UIFLOW2:

        |get_latitude_decimal.png|

.. method:: GNSSModule.get_longitude_decimal()

    get longitude decimal.

    :return (float): longitude decimal(dd.dddd).

    UIFLOW2:

        |get_longitude_decimal.png|

.. method:: GNSSModule.get_speed(type)

    get speed.

    :return (str): speed.
    :param int type: speed type, 0 km/h, 1 knot/h
        Options:
        - ``km/h``: 0
        - ``knot/h``: 1

    UIFLOW2:

        |get_speed.png|

.. method:: GNSSModule.get_course()

    get course.

    :return (str): course unit is °.

    UIFLOW2:

        |get_course.png|

.. method:: GNSSModule.is_locate_valid()

    get locate status.

    :return (bool): locate status, true is locate, false is not locate.

    UIFLOW2:

        |is_locate_valid.png|



