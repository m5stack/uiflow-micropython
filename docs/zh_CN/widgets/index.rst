:mod:`Widgets` --- 一个基础的UI库
=================================

.. module:: Widgets
   :synopsis: 一个基础的UI库

.. include:: ../refs/widgets.ref

Micropython Example::

    import M5
    from M5 import Widgets

    M5.begin()
    Widgets.setBrightness(100)
    Widgets.fillScreen(0x6600cc)
    Widgets.setRotation(0)

UIFLOW2 Example:

    |example.svg|


Screen functions
----------------

.. function:: Widgets.setBrightness(brightness: int)

    设置显示器的背光。``brightness`` 的范围是 0 - 255。

    UIFLOW2:

        |setBrightness.svg|

.. function:: Widgets.fillScreen(color: int)

    设置显示器的背景颜色。``color`` 接受 RGB888 的颜色代码。

    UIFLOW2:

        |fillScreen.svg|

.. function:: Widgets.setRotation(rotation: int)

    设置显示器的旋转角度。

    ``rotation`` 参数只接受以下的值：

        - ``0``: Portrait (0°C)
        - ``1``: Landscape (90°C)
        - ``2``: Inverse Portrait (180°C)
        - ``3``: Inverse Landscape (270°C)

    UIFLOW2:

        |setRotation.svg|


Classes
-------

.. toctree::
    :maxdepth: 1

    label.rst
