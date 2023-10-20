Angle Unit
==========

.. include:: ../refs/unit.angle.ref

支持以下产品：

|Angle| 

Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()

    angle_0 = Angle((8,9))

    while True:
        print(angle_0.get_voltage())
        print(angle_0.get_value())

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|angle_core_example.m5f2|

class Angle
-----------

Constructors
------------

.. class:: Angle(port)

    创建一个Angle对象。

    参数是：
        - ``port`` 是端口的引脚号

    UIFLOW2:

        |init.svg|



Methods
-------

.. method:: Angle.get_value()

    此方法允许读取Angle的旋转值并返回一个整型数值。范围为0-65535.。

    UIFLOW2:

        |get_value.svg|

.. method:: Angle.get_voltage()

    此方法允许读取Angle的电压值, 返回值为一个浮点型数值。

    UIFLOW2:

        |get_voltage.svg|

