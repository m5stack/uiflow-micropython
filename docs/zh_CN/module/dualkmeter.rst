DualKmeter Module
=================

.. include:: ../refs/module.dualkmeter.ref

支持以下产品：

+-------------------------+
| |DualKmeter Module13.2| |
+-------------------------+

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import DualKmeterModule

    M5.begin()
    km_0 = DualKmeterModule(address=0x11)
    while True:
        if km_0.is_ready():
            print(km_0.get_thermocouple_temperature(scale=km_0.CELSIUS))

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    :download:`example.m5f2 <../../_static/module/dualkmeter/example.m5f2>`

class DualKmeterModule
----------------------

Constructors
------------

.. class:: DualKmeterModule(address=0x11)

    创建 DualKmeterModule 对象，``address`` 接受 0x11 ~ 0x20 的值。

    UIFLOW2:

        |init.svg|

Methods
-------

.. method:: DualKmeterModule.get_thermocouple_temperature(scale=0) -> float

    获取 DualKmeter Module 热电偶的温度，返回 float 类型的值。

    ``scale`` 允许接受的值是 :py:data:`DualKmeter.CELSIUS` 或者 :py:data:`DualKmeter.FAHRENHEIT` 。

    UIFLOW2:

        |get_thermocouple_temperature.svg|

.. method:: DualKmeterModule.get_kmeter_temperature(scale=0) -> float

    获取 DualKmeter Module 内部的温度，返回 float 类型的值。

    ``scale`` 允许接受的值是 :py:data:`DualKmeter.CELSIUS` 或者 :py:data:`DualKmeter.FAHRENHEIT` 。

    UIFLOW2:

        |get_kmeter_temperature.svg|

.. method:: DualKmeterModule.get_kmeter_channel() -> int

    获取 DualKmeter Module 当前使用的热电偶通道。``0`` 是通道1, ``1`` 是通道2。

    UIFLOW2:

        |get_kmeter_channel.svg|

.. method:: DualKmeterModule.set_kmeter_channel(channel) -> None

    设置 DualKmeter Module 使用的热电偶通道。``0`` 是通道1, ``1`` 是通道2。

    UIFLOW2:

        |set_kmeter_channel.svg|

.. method:: DualKmeterModule.is_ready() -> bool

    获取测量结果是否存于就绪状态。

    UIFLOW2:

        |is_ready.svg|

.. method:: DualKmeterModule.get_thermocouple_temperature_string(scale=0) -> str

    获取 DualKmeter Module 热电偶的温度，返回带正负符号的温度字符串。

    ``scale`` 允许接受的值是 :py:data:`DualKmeter.CELSIUS` 或者 :py:data:`DualKmeter.FAHRENHEIT` 。

    UIFLOW2:

        |get_thermocouple_temperature_string.svg|

.. method:: DualKmeterModule.get_kmeter_temperature_string(scale=0) -> str

    获取 DualKmeter Module 内部的温度，返回带正负符号的温度字符串。

    ``scale`` 允许接受的值是 :py:data:`DualKmeter.CELSIUS` 或者 :py:data:`DualKmeter.FAHRENHEIT` 。

    UIFLOW2:

        |get_kmeter_temperature_string.svg|

.. method:: DualKmeterModule.get_fw_ver() -> int

    获取 DualKmeter Module 的固件版本。返回 int 类型的版本号。

    UIFLOW2:

        |get_fw_ver.svg|

Constants
---------

.. data:: DualKmeterModule.CELSIUS
    :type: int

    摄氏温标

.. data:: DualKmeterModule.FAHRENHEIT
    :type: int

    华氏温标
