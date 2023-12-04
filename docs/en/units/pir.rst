PIR Unit
==================

.. include:: ../refs/unit.pir.ref

Support the following products:


|PIR|              


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    pir_0 = None

    def setup():
    global i2c0, pir_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    pir_0 = PIR((8, 9))
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(pir_0.get_status())



UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|pir_core_example.m5f2|

class PIR
-----------------

Constructors
--------------

.. class:: PIR(IO1,IO2)

    Create a PIR object.

    The parameters are:
        - ``IO1,IO2`` I2C pin.

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: PIR.get_status()


    Get detection status.  

    UIFLOW2:

        |get_status.svg|

.. method:: PIR.enable_irq()

   Enable Human detection function.

    UIFLOW2:

        |enable_irq.svg|

.. method:: PIR.disable_irq()

    Disable Human detection function.

    UIFLOW2:

        |disable_irq.svg|

.. method:: PIR.set_callback()

    Polling method, placed in the loop function, constantly check.

    UIFLOW2:

        |set_callback.svg|
