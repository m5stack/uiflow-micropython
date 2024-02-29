RELAY Unit
==================

.. include:: ../refs/unit.relay.ref

支持以下产品:

    |RELAY|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import *

    relay_0 = None

    def setup():
    global relay_0

    relay_0 = RelayUnit((8,9))
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(relay_0.get_status())
    relay_0.on()
    time.sleep(1)
    relay_0.off()
    time.sleep(1)
    relay_0.set_status(True)
    time.sleep(1)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |relay_core_example.m5f2|


class RelayUnit
---------------

Constructors
--------------

.. class:: RelayUnit(io)

    创建一个RelayUnit对象.

    参数如下：
        - ``io`` 定义控制引脚。

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: RelayUnit.get_status()

    获取继电器开关状态。

    UIFLOW2:

        |get_status.svg|


.. method:: RealyUnit.on()

   闭合继电器。

    UIFLOW2:

        |on.svg|


.. method:: RealyUnit.off()

   打开继电器。

    UIFLOW2:

        |off.svg|


.. method:: RealyUnit.set_status()

   设置继电器状态（ True 或者 false ）。

    UIFLOW2:

        |set_status.svg|
