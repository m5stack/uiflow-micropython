RGB Unit
==========

.. include:: ../refs/unit.rgb.ref

支持以下产品：

|RGB| 

Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()
    rgb_0 = RGB((36, 26), 3)
    Widgets.fillScreen(0x222222)

    rgb_0.set_brightness(80)
    rgb_0.fill_color(0xff0000)
    rgb_0.set_color(0, 0x33ff33)

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|rgb_core_example.m5f2|

class RGB
-----------

Constructors
------------

.. class:: RGB(port, number)

    创建一个RGB对象。

    参数是：
        - ``port`` 是端口的引脚号
        - ``number`` 是灯珠数量

    UIFLOW2:

        |init.svg|



Methods
-------

.. method:: RGB.set_brightness(br: int)

    此方法用于设置RGB灯珠亮度, 设置范围为0-100。

    UIFLOW2:

        |set_brightness.svg|

.. method:: RGB.fill_color(c: int)

    此方法用于设置全部RGB灯珠颜色, 传入值为3字节的RGB888。

    UIFLOW2:

        |fill_color.svg|

.. method:: RGB.set_color(i, c: int)

    此方法用于设置指定RGB灯珠颜色, 传入值为灯珠索引和3字节的RGB888。

    UIFLOW2:

        |set_color.svg|

