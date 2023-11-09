IR Unit
==================

.. include:: ../refs/unit.ir.ref

Support the following products:


|IR|              


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import *

    ir_0 = None

    def setup():
    global ir_0

    ir_0 = IR((36, 26))
    ir_0.tx(0, 0)
    M5.begin()
    Widgets.fillScreen(0x222222)





UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|ir_core_example.m5f2|

class IR
--------------

Constructors
--------------

.. class:: IR(IO1,IO2)

    Create an IR object.

    The parameters is:
        - ``IO1,IO2`` Receive and transmit pin definitions.

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ir.tx()


    Sends an ir signal value to an address.  

    UIFLOW2:

        |tx.svg|

.. method:: ir.rx_event()

    Determine when the infrared signal is read and start to do some processing procedures.

    UIFLOW2:

        |rx_event.svg|

