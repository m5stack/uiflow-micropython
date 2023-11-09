Ultrasonic Unit
==================

.. include:: ../refs/unit.ultrasonic.ref

Support the following products:


|Ultrasonic|              


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    ultrasonic_0 = None

    def setup():
    global i2c0, ultrasonic_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ultrasonic_0 = ULTRASONIC_I2C(i2c0)
    M5.begin()
    Widgets.fillScreen(0x222222)





UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|ultrasonic_core_example.m5f2|

class ULTRASONIC_I2C
----------------------

Constructors
--------------

.. class:: ULTRASONIC_I2C(PORT)

    创建一个ULTRASONIC_I2C对象.

    参数是:
        - ``PORT`` 定义i2c端口。

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ULTRASONIC_I2C.get_target_distance()


    获取发射距离    

    UIFLOW2:

        |get_target_distance.svg|



