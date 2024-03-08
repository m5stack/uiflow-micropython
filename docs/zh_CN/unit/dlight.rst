DLight Unit
===========

.. include:: ../refs/unit.dlight.ref

支持以下产品：

    |Dlight|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import *

    i2c0 = None
    dlight_0 = None

    def setup():
    global i2c0, dlight_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    dlight_0 = DLight(i2c0)
    print(dlight_0.get_lux())
    M5.begin()
    Widgets.fillScreen(0x222222)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |dlight_core_example.m5f2|


class DLight
------------

Constructors
------------

.. class:: DLight(port)

    创建一个DLight对象.

    参数是:
        - ``PORT`` 定义i2c端口。

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: dlight.get_lux()

   获取光照强度。

    UIFLOW2:

        |get_lux.svg|


.. method:: dlight.configure()

    配置测量模式（持续测量/单次测量）和分辨率。

    UIFLOW2:

        |configure.svg|
