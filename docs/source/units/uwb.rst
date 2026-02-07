
UWB Unit
========

.. include:: ../refs/unit.uwb.ref

UWB is a Unit which integrates the UWB(Ultra Wide Band) communication protocol which uses nanosecond pulses to locate objects and define position and orientation. The design uses the Ai-ThinkerBU01 Transceiver module which is based on Decawave's DW1000 design. The internal STM32 chip with its integrated ranging algorithm,is capable of 10cm positioning accuracy and also supports AT command control. Applications include: Indoor wireless tracking/range finding of assets,which works by triangulating the position of the base station/s and tag (the base station resolves the position information and outputs it to the tag).
The firmware currently carried by this Unit only supports the transmission of ranging information, and does not currently support the transmission of custom information. When in use, it supports the configuration of 4 base station devices (using different IDs), and only a single tag device is allowed to operate at the same time.


Support the following products:

|UWBUnit|

Micropython Anchor Example:

    .. literalinclude:: ../../../examples/unit/uwb/core2_uwb_anchor_example.py
        :language: python
        :linenos:

Micropython Tag Example:

    .. literalinclude:: ../../../examples/unit/uwb/stickc_plus2_uwb_tag_example.py
        :language: python
        :linenos:


UIFLOW2 Anchor Example:

    |example_anchor.png|

UIFLOW2 Tag Example:

    |example_tag.png|

.. only:: builder_html

    |core2_uwb_anchor_example.m5f2|

    |stickc_plus2_uwb_tag_example.m5f2|

class UWBUnit
-------------

Constructors
------------

.. class:: UWBUnit(id, port, device_mode, device_id, verbose)

    Create a UWB unit object.

    :param  id: UART ID.
    :param  port: The port that the unit is connected to.
    :param  device_mode: device mode.
    :param  device_id: device ID.
    :param bool verbose: verbose output.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: UWBUnit.get_distance(index)

    Get the distance to the anchor ID (0 ~ 3).

    :return (float): distance in meters.
    :param int index: anchor ID (0 ~ 3).

    UIFLOW2:

        |get_distance.png|

.. method:: UWBUnit.get_device_id()

    Get the device ID.

    :return (int): device ID.

    UIFLOW2:

        |get_device_id.png|

.. method:: UWBUnit.get_device_mode()

    Get the device mode.

    :return (int): device mode.

    UIFLOW2:

        |get_device_mode.png|

.. method:: UWBUnit.set_device_mode(mode, id)

    Set the device mode and ID.

    :param int mode: device mode.
        Options:
        - ``Anchor``: UWBUnit.ANCHOR
        - ``Tag``: UWBUnit.TAG
    :param int id: device ID.

    UIFLOW2:

        |set_device_mode.png|

.. method:: UWBUnit.isconnected()

    Check if the UWB unit is connected.

    :return: True if connected, False otherwise.

    UIFLOW2:

        |isconnected.png|

.. method:: UWBUnit.get_version()

    Get the UWB unit firmware version.

    :return: firmware version.

    UIFLOW2:

        |get_version.png|

.. method:: UWBUnit.reset()

    Reset the UWB unit.

.. method:: UWBUnit.set_measurement_interval(interval)

    Set the measurement interval.

    :param int interval: measurement interval.

    UIFLOW2:

        |set_measurement_interval.png|

.. method:: UWBUnit.set_measurement(enable)

    Set the measurement output.

    :param bool enable: enable or disable measurement output.

    UIFLOW2:

        |set_measurement.png|

.. method:: UWBUnit.set_callback(anchor, event, callback)

    Set the callback function for the anchor status.

    :param int anchor: anchor ID (0 ~ 3).
    :param int event: anchor status.
        Options:
        - ``ONLINE``: UWBUnit.ONLINE
        - ``OFFLINE``: UWBUnit.OFFLINE
    :param  callback: callback function.

    UIFLOW2:

        |set_callback.png|

.. method:: UWBUnit.update()

    Update the distances and anchor status.

    UIFLOW2:

        |update.png|



Constants
---------

.. data:: UWBUnit.UNKNOWN
.. data:: UWBUnit.ANCHOR
.. data:: UWBUnit.TAG

    device role

    
.. data:: UWBUnit.OFFLINE
.. data:: UWBUnit.ONLINE
.. data:: UWBUnit._mode_map

    device status

    
