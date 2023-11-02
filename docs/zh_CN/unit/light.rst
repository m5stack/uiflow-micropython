Light Unit
==================

.. include:: ../refs/unit.light.ref

Support the following products:


|Light|              


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import *


    light_0 = None


    def setup():
    global light_0

    light_0 = Light((8,9))
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(light_0.get_analog_value())




UIFLOW2 Example:

    |init.svg|

.. only:: builder_html

|light_core_example.m5f2|

class Light
-----------------

Constructors
--------------

.. class:: Light(IO1,IO2)

    创建一个Light对象.

    参数是:
        - ``IO1,IO2`` 定义数字和模拟输出引脚。

 
    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: Light.get_digital_value()


    获取数字量(0或者1)。   

    UIFLOW2:

        |get_digital_value.svg|

.. method:: Light.get_analog_value()

    获取模拟量(返回0-65535).

    UIFLOW2:

        |get_analog_value.svg|

.. method:: Light.get_ohm()

    获取阻值(返回整数)。

    UIFLOW2:

        |get_ohm.svg|

