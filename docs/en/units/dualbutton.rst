Dual_Button Unit
==================

.. include:: ../refs/unit.dual_button.ref

Support the following products:


|Dual_Button|              


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import *


    dual_button_0_blue = None
    dual_button_0_red = None

    def setup():
    global dual_button_0_blue, dual_button_0_red

    dual_button_0_blue, dual_button_0_red = DualButton((36, 26))
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(dual_button_0_blue.isHolding())




UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|dual_button_core_example.m5f2|

class DualButton
-----------------

Constructors
--------------

.. class:: DualButton(IO1,IO2)

    Create a DualButton object.

    The parameters are:
        - ``IO1,IO2`` 定义两个按键引脚。

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: Dual_Button.isHolding()


    The parameters are:

    UIFLOW2:

        |get_status.svg|

.. method:: Dual_Button.setCallback()

    Execute the program when the key is pressed.

    UIFLOW2:

        |setCallback.svg|

.. method:: Dual_Button.tick()

    The polling method, placed in the loop function, constantly detects the state of the key.

    UIFLOW2:

        |tick.svg|

