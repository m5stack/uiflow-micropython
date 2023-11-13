NCIR Unit
==================

.. include:: ../refs/unit.ncir.ref

Support the following products:


|NCIR|              


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    ncir_0 = None

    def setup():
    global i2c0, ncir_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ncir_0 = NCIRUnit(i2c0)
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(ncir_0.get_ambient_temperature())
    print(ncir_0.get_object_temperature())



UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|ncir_core_example.m5f2|

class NCIRUnit
-----------------

Constructors
--------------

.. class:: NCIRUnit(i2c)

    创建一个NCIRUnit对象.

    The parameters is:
        - ``i2c`` 定义i2c引脚。

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ncir.get_ambient_temperature()


    获取环境温度。 

    UIFLOW2:

        |get_ambient_temperature.svg|

.. method:: ncir.get_object_temperature()

   获取测量物体温度。

    UIFLOW2:

        |get_object_temperature.svg|


