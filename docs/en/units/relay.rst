RELAY Unit
==================

.. include:: ../refs/unit.relay.ref

Support the following products:

    |RELAY|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import *

    relay_0 = None

    def setup():
    global relay_0

    relay_0 = RelayUnit((8,9))
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(relay_0.get_status())
    relay_0.on()
    time.sleep(1)
    relay_0.off()
    time.sleep(1)
    relay_0.set_status(True)
    time.sleep(1)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |relay_core_example.m5f2|


class RelayUnit
---------------

Constructors
------------

.. class:: RelayUnit(io)

    Create a RelayUnit object.

    The parameters is:
        - ``io`` Define the control pin.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: RelayUnit.get_status()

    Gets the relay switch status.

    UIFLOW2:

        |get_status.svg|


.. method:: RealyUnit.on()

   turn on the relay.

    UIFLOW2:

        |on.svg|


.. method:: RealyUnit.off()

   Turn off the relay.

    UIFLOW2:

        |off.svg|


.. method:: RealyUnit.set_status()

   Set the relay status (True or false).

    UIFLOW2:

        |set_status.svg|
