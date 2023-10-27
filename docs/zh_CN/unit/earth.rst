EARTH Unit
==========

.. include:: ../refs/unit.earth.ref

支持以下产品：


|EARTH|              


Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()

    earth_0 = Earth((36, 26))
    print(earth_0.humidity())


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|earth_core_example.m5f2|

class Earth
------------

Constructors
------------

.. class:: Earth(port)

    创建一个Earth对象。

    参数是：
        - ``port`` 是端口的引脚号

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: EARTH.get_analog_value()

    此方法允许读取EARTH采集的模拟量并返回一个整数型数值。范围为0-65535。

    UIFLOW2:

        |get_analog_value.svg|

.. method:: EARTH.get_digital_value()

    此方法允许读取EARTH采集的数字量并返回一个整数型数值。范围为0或者1。

    UIFLOW2:

        |get_digital_value.svg|

.. method:: EARTH.get_voltage_mv()

    此方法允许读取EARTH采集的电压值并返回一个整数型数值。范围0-3300。

    UIFLOW2:

        |get_voltage_mv.svg|

.. method:: EARTH.humidity()

    此方法允许读取EARTH采集的电压值并返回一个浮点型数值。范围0.0-1.0。

    UIFLOW2:

        |humidity.svg|

.. method:: EARTH.set_calibrate()

    此方法允许设置校准EARTH传感器的最大（0-3300）和最小值（0-3300）。

    UIFLOW2:

        |set_calibrate.svg|        
