Rotary
======

.. include:: ../refs/hardware.rotary.ref


Rotary 用于控制主机内部集成的旋转编码器。以下是主机的 Rotary 支持详细：

.. table::
    :widths: auto
    :align: center

    +-----------------+--------+
    | Controller      | Rotary |
    +=================+========+
    | Dial            | |S|    |
    +-----------------+--------+
    | DinMeter        | |S|    |
    +-----------------+--------+

.. |S| unicode:: U+2714


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *

    label0 = None
    rotary = None

    def btnA_wasClicked_event(state):
        global label0, rotary
        rotary.reset_rotary_value()
        label0.setText(str(rotary.get_rotary_value()))

    def setup():
        global label0, rotary

        M5.begin()
        Widgets.fillScreen(0x222222)
        label0 = Widgets.Label("0", 96, 80, 1.0, 0xffa000, 0x222222, Widgets.FONTS.DejaVu72)

        BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

        rotary = Rotary()

    def loop():
        global label0, rotary
        M5.update()
        if rotary.get_rotary_status():
            label0.setText(str(rotary.get_rotary_value()))

    if __name__ == '__main__':
        try:
            setup()
            while True:
            loop()
        except (Exception, KeyboardInterrupt) as e:
            try:
            from utility import print_error_msg
            print_error_msg(e)
            except ImportError:
            print("please update to latest firmware")


UIFLOW2 Example:

    |example.svg|


class Rotary
------------

Constructors
------------

.. class:: Rotary()

    创建一个 Rotary 对象.

    UIFLOW2:

        |init.svg|

Methods
-------

.. method:: Rotary.get_rotary_status() -> bool

    获取 Rotary 对象的旋转状态。

    UIFLOW2:

        |get_rotary_status.svg|


.. method:: Rotary.get_rotary_value() -> int

    .. note:: 不能和 :meth:`Rotary.get_rotary_increments()` 同时使用

    获取 Rotary 对象的旋转值。

    UIFLOW2:

        |get_rotary_value.svg|


.. method:: Rotary.get_rotary_increments() -> int

    .. note:: 不能和 :meth:`Rotary.get_rotary_status()` 同时使用

    获取 Rotary 对象的旋转增量。可用于判断旋转方向。

    UIFLOW2:

        |get_rotary_increments.svg|


.. method:: Rotary.reset_rotary_value() -> None

    重置 Rotary 对象的旋转值。

    UIFLOW2:

        |reset_rotary_value.svg|


.. method:: Rotary.set_rotary_value() -> None

    设置 Rotary 对象的旋转值。

    UIFLOW2:

        |set_rotary_value.svg|
