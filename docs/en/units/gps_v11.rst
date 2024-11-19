
GPSV1.1(SMA) Unit
=================

.. include:: ../refs/unit.gps_v11.ref

GPS Unit v1.1 is a GNSS global positioning navigation unit, integrating the high-performance CASIC navigation chip AT6668 and signal amplifier chip MAX2659, with a built-in ceramic antenna, providing more precise and reliable satellite positioning services.

GPS SMA Unit is a GNSS global positioning navigation unit that integrates the high-performance CASIC navigation chip AT6668 and the signal amplifier chip MAX2659. It uses an external antenna to provide more accurate and reliable satellite positioning services.

Support the following products:

    |GPSV11Unit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/gps_v11/gpsv11_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |gpsv11_core2_example.m5f2|

class GPSV11Unit
----------------

Constructors
------------

.. class:: GPSV11Unit(id, port)

    Initialize the GPSV11Unit with a specific UART id and port for communication.

    :param int id: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
    :param  port: A list or tuple containing the TX and RX pins for UART communication.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: GPSV11Unit.set_work_mode(mode)

    Set the working mode of the GPS module.

    :param int mode: The mode to set, defined by the GPS module.

    UIFLOW2:

        |set_work_mode.png|

.. method:: GPSV11Unit.get_work_mode()

    Get the current working mode of the GPS module.

    :return: The current working mode of the GPS module.

    UIFLOW2:

        |get_work_mode.png|

.. method:: GPSV11Unit.get_antenna_state()

    Get the state of the antenna.

    :return: The antenna state.

    UIFLOW2:

        |get_antenna_state.png|

.. method:: GPSV11Unit.get_gps_time()

    Get the current GPS time.

    :return: The GPS time as a list of strings [hour, minute, second].

    UIFLOW2:

        |get_gps_time.png|

.. method:: GPSV11Unit.get_gps_date()

    Get the current GPS date.

    :return: The GPS date as a list of strings [day, month, year].

    UIFLOW2:

        |get_gps_date.png|

.. method:: GPSV11Unit.get_gps_date_time()

    Get the current GPS date and time combined.

    :return: The GPS date and time as a list of strings [year, month, day, hour, minute, second].

    UIFLOW2:

        |get_gps_date_time.png|

.. method:: GPSV11Unit.get_timestamp()

    Get the timestamp of the current GPS time.

    :return: The timestamp representing the current GPS time.

    UIFLOW2:

        |get_timestamp.png|

.. method:: GPSV11Unit.get_latitude()

    Get the current latitude.

    :return: The current latitude in string format.

    UIFLOW2:

        |get_latitude.png|

.. method:: GPSV11Unit.get_longitude()

    Get the current longitude.

    :return: The current longitude in string format.

    UIFLOW2:

        |get_longitude.png|

.. method:: GPSV11Unit.get_altitude()

    Get the current altitude.

    :return: The current altitude in string format.

    UIFLOW2:

        |get_altitude.png|

.. method:: GPSV11Unit.get_satellite_num()

    Get the number of satellites used for positioning.

    :return: The number of satellites.

    UIFLOW2:

        |get_satellite_num.png|

.. method:: GPSV11Unit.get_pos_quality()

    Get the quality of the GPS position.

    :return: The position quality indicator.

    UIFLOW2:

        |get_pos_quality.png|

.. method:: GPSV11Unit.get_corse_over_ground()

    Get the course over ground (COG).

    :return: The course over ground in degrees.

    UIFLOW2:

        |get_corse_over_ground.png|

.. method:: GPSV11Unit.get_speed_over_ground()

    Get the speed over ground (SOG).

    :return: The speed over ground in knots.

    UIFLOW2:

        |get_speed_over_ground.png|

.. method:: GPSV11Unit.set_time_zone(value)

    Set the time zone offset for the GPS time.

    :param value: The time zone offset value to set.

    UIFLOW2:

        |set_time_zone.png|

.. method:: GPSV11Unit.get_time_zone()

    Get the current time zone offset.

    :return: The current time zone offset.

    UIFLOW2:

        |get_time_zone.png|

.. method:: GPSV11Unit.deinit()

    Deinitialize the GPS unit, stopping any running tasks and releasing resources.

    UIFLOW2:

        |deinit.png|


.. method:: GPSV11Unit._add_checksum(message)

    Add checksum to the message for communication with the GPS module.

    :param str message: The message to which the checksum will be added.

    :return: The message with added checksum.


.. method:: GPSV11Unit._decode_gga(data)

    Decode the GGA sentence to extract GPS quality, number of satellites, and altitude.

    :param str data: The GGA sentence to decode.


.. method:: GPSV11Unit._decode_rmc(data)

    Decode the RMC sentence to extract GPS time, latitude, longitude, speed, course, and date.

    :param str data: The RMC sentence to decode.


.. method:: GPSV11Unit._decode_txt(data)

    Decode the TXT sentence to extract antenna state.

    :param str data: The TXT sentence to decode.


.. method:: GPSV11Unit._monitor()

    Monitor the GPS data and decode incoming sentences.
