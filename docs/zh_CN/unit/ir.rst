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

    |init.svg|

.. only:: builder_html

|ir_core_example.m5f2|

class IR
--------------

Constructors
--------------

.. class:: IR(IO1,IO2)

    创建一个IR对象.

    参数是:
        - ``IO1,IO2`` 接收和发射引脚定义.

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ir.tx()


    向某个地址发送ir信号值。    

    UIFLOW2:

        |tx.svg|

.. method:: ir.rx_event()

    判断读取到红外信号的时候，开始做某些处理程序。

    UIFLOW2:

        |rx_event.svg|

