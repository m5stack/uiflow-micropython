
GPS Module
===========

.. include:: ../refs/module.gps.ref

COM.GPS is a satellite positioning module in the M5Stack stacking module series. It is developed based on the NEO-M8N module.

Support the following products:

    +-------------------------+-------------------------+
    | |GPSModule|             | |COM.GPSModule|         |
    +-------------------------+-------------------------+


Micropython Example:

    .. literalinclude:: ../../../examples/module/gps/gps_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |gps_core2_example.m5f2|


class GPSModule
---------------

Constructors
------------

.. class:: GPSModule(id, rx, tx)

    initialize Function.

    :param int id: UART controllers id, the range is 0 to 2.
    :param int rx: UART rx pin.
    :param int tx: UART tx pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: GPSModule.set_time_zone(value)

    set timezone function.

    :param int value: timezone value

    UIFLOW2:

        |set_time_zone.png|

.. method:: GPSModule.get_time_zone()

    get timezone function.

    :return (int): timezone value

    UIFLOW2:

        |get_time_zone.png|

.. method:: GPSModule.get_satellite_num()

    get satellite numbers.

    :return (str): satellite numbers value.

    UIFLOW2:

        |get_satellite_num.png|

.. method:: GPSModule.get_altitude()

    get altitude.

    :return (str): altitude unit is meter.

    UIFLOW2:

        |get_altitude.png|

.. method:: GPSModule.get_time()

    get time.

    :return (str): time(hh:mm:ss)

    UIFLOW2:

        |get_time.png|

.. method:: GPSModule.get_date()

    get date.

    :return (str): date(dd/mm/yy)

    UIFLOW2:

        |get_date.png|

.. method:: GPSModule.get_latitude()

    get latitude.

    :return (str): latitude, using degrees minutes format (ddmm.mmmmmN/S).

    UIFLOW2:

        |get_latitude.png|

.. method:: GPSModule.get_longitude()

    get longitude.

    :return (str): longitude, using degrees minutes format (ddmm.mmmmmE/W).

    UIFLOW2:

        |get_longitude.png|

.. method:: GPSModule.get_latitude_decimal()

    get latitude decimal.

    :return (float): latitude decimal(dd.dddd).

    UIFLOW2:

        |get_latitude_decimal.png|

.. method:: GPSModule.get_longitude_decimal()

    get longitude decimal.

    :return (float): longitude decimal(dd.dddd).

    UIFLOW2:

        |get_longitude_decimal.png|

.. method:: GPSModule.get_speed(type)

    get speed.

    :return (str): speed.
    :param int type: speed type, 0 km/h, 1 knot/h
        Options:
        - ``km/h``: 0
        - ``knot/h``: 1

    UIFLOW2:

        |get_speed.png|

.. method:: GPSModule.get_course()

    get course.

    :return (str): course unit is °.

    UIFLOW2:

        |get_course.png|

.. method:: GPSModule.is_locate_valid()

    get locate status.

    :return (bool): locate status, true is locate, false is not locate.

    UIFLOW2:

        |is_locate_valid.png|
