Button
======

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.button.ref

Button用于控制主机内部集成的按键。以下是主机的Button支持详细：

.. table::
    :widths: auto
    :align: center

    +-----------------+------+------+------+--------+--------+
    |                 | BtnA | BtnB | BtnC | BtnPWR | BtnEXT |
    +=================+======+======+======+========+========+
    | AtomS3          | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | AtomS3 Lite     | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | AtomS3U         | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | StampS3         | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | CoreS3          |      |      |      | |S|    |        |
    +-----------------+------+------+------+--------+--------+
    | Core2           | |S|  | |S|  | |S|  |        |        |
    +-----------------+------+------+------+--------+--------+
    | TOUGH           |      |      |      |        |        |
    +-----------------+------+------+------+--------+--------+

.. |S| unicode:: U+2714

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *

    def btnPWR_wasClicked_event(state):
        global label0
        label0.setText('clicked')

    def btnPWR_wasHold_event(state):
        global label0
        label0.setText('hold')

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 58, 43, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_HOLD, cb=btnPWR_wasHold_event)

    while True:
        M5.update()

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    :download:`example.m5f2 <../../_static/hardware/button/example.m5f2>`

class Button
------------

.. important::

    Button Class的方法重度依赖 ``M5.begin()`` |begin.svg| 和 ``M5.update()`` |update.svg|。

    调用 Button 对象的所有方法，需要放在 ``M5.begin()`` |begin.svg| 的后面，并在 主循环中调用 ``M5.update()`` |update.svg|。

Methods
-------

.. method:: Button.isHolding()

    返回 Button 对象是否处于长按状态。

    UIFLOW2:

        |isHolding.svg|

.. method:: Button.isPressed()

    返回 Button 对象是否处于按下状态。

    UIFLOW2:

        |isPressed.svg|

.. method:: Button.isReleased()

    返回 Button 对象是否处于松开状态。

    UIFLOW2:

        |isReleased.svg|

.. method:: Button.wasClicked()

    当 Button 对象被短暂按下并释放时返回 True。

    UIFLOW2:

        |wasClicked.svg|

.. method:: Button.wasDoubleClicked()

    当 Button 对象被双击后经过一段时间后返回 True。

    UIFLOW2:

        |wasDoubleClicked.svg|

.. method:: Button.wasHold()

    当 Button 对象被按住一段时间时返回 True。

    UIFLOW2:

        |wasHold.svg|

.. method:: Button.wasPressed()

    当 Button 对象被按下时返回 True。

    UIFLOW2:

        |wasPressed.svg|

.. method:: Button.wasReleased()

    当 Button 对象被松开时返回 True。

    UIFLOW2:

        |wasReleased.svg|

.. method:: Button.wasSingleClicked()

    当 Button 对象被单击后经过一段时间后返回 True。

    UIFLOW2:

        |wasSingleClicked.svg|

Event Handling
--------------

.. method:: Button.setCallback(type:Callback_Type, cb)

    设置事件回调函数

    UIFLOW2:

        |setCallback.svg|

Constants
---------

.. data:: Button.CB_TYPE

    一个 Callback_Type 对象。

class Callback_Type
-------------------

Constants
---------

.. data:: Callback_Type.WAS_CLICKED

    单击事件类型

.. data:: Callback_Type.WAS_DOUBLECLICKED

    双击事件类型

.. data:: Callback_Type.WAS_HOLD

    长按事件类型

.. data:: Callback_Type.WAS_PRESSED

    按下事件类型

.. data:: Callback_Type.WAS_RELEASED

    松开事件类型
