Power
======

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.power.ref

class Power
------------

.. important::

    Power Class的方法依赖 ``M5.begin()`` |M5.begin.svg|。

    调用 Power 对象的所有方法，需要放在 ``M5.begin()`` |M5.begin.svg| 的后面。

Methods
-------

.. method:: Power.setExtOutput(enable: bool, port: int=0xFF) -> None

    设置外接端口的电源输出。

    ``enable`` 为 True 时，外接端口电源为输出模式。 ``enable`` 为 False 时，外接端口电源为输入模式。

    ``port`` 为端口号，可选值请参考 :ref:`class PORT`, 仅在 M5Stack Station 有效。

    UIFLOW2:

        |setExtOutput1.svg|
        |setExtOutput2.svg|


.. method:: Power.getExtOutput() -> bool

    获取外部端口的电源输出。

    返回值为 ``True``, 外接端口电源为输出模式。 返回值为 ``False``, 外接端口电源为输入模式。

    UIFLOW2:

        |getExtOutput.svg|


.. method:: Power.setUsbOutput(enable: bool) -> None

    设置主 USB 端口的电源输出。

    ``enable`` 为 True 时，主 USB 端口电源为输出模式。 ``enable`` 为 False 时，主 USB 端口电源为输入模式。

    UIFLOW2:

        |setUsbOutput.svg|


.. method:: Power.getUsbOutput() -> bool

    获取主USB端口的电源输出。

    返回值为 ``True``, 主 USB 端口电源为输出模式。 返回值为 ``False``, 主 USB 端口电源为输入模式。

    UIFLOW2:

        |getUsbOutput.svg|


.. method:: Power.setLed(brightness=255) -> None

    打开/关闭电源 LED。

    ``brightness`` 为亮度值，范围为 0-255。 0 为关闭，255 为最大亮度。

    UIFLOW2:

        |setLed.svg|


.. method:: Power.powerOff()

    所有电源关闭。

    UIFLOW2:

        |powerOff.svg|


.. method:: Power.timerSleep(seconds) -> None
            Power.timerSleep(minutes, hours) -> None
            Power.timerSleep(minutes, hours, date, weekDay) -> None

    睡眠和定时器启动。 启动条件可以通过参数指定。

    ``seconds``: 取值范围是 1 - 15300, 单位是秒。

    ``minutes``: 取值范围是 0 - 59, 单位是分钟。

    ``hours``: 取值范围是 0 - 23, 单位是小时。

    ``date``: 取值范围是 1 - 31, 单位是天。

    ``weekDay``: 取值范围是 0 - 6。

    UIFLOW2:

        |timerSleep1.svg|
        |timerSleep2.svg|
        |timerSleep3.svg|


.. method:: Power.deepSleep(micro_seconds: int=0, wakeup: bool=True)

    ESP32 深度睡眠。

    ``micro_seconds``: 唤醒的微秒数。

    ``wakeup``: 是否唤醒。

    UIFLOW2:

        |deepSleep.svg|


.. method:: Power.lightSleep(micro_seconds: int=0, wakeup: bool=True)

    ESP32 浅睡眠。

    ``micro_seconds``: 唤醒的微秒数。

    ``wakeup``: 是否唤醒。

    UIFLOW2:

        |lightSleep.svg|


.. method:: Power.getBatteryLevel() -> int

    获取剩余电池电量百分比。返回值范围是 0-100。

    UIFLOW2:

        |getBatteryLevel.svg|


.. method:: Power.setBatteryCharge(enable: bool) -> None

    设置电池充电使能.

    UIFLOW2:

        |setBatteryCharge.svg|


.. method:: Power.setChargeCurrent(max_mA: int) -> None

    设置电池充电电流。

    ``max_mA`` 取值范围是 0-2000, 单位是毫安。

    UIFLOW2:

        |setChargeCurrent.svg|


.. method:: Power.setChargeVoltage(max_mV: int) -> None

    设置电池充电电流。

    ``max_mV`` 取值范围是 4100-4600, 单位是毫伏。

    UIFLOW2:

        |setChargeVoltage.svg|


.. method:: Power.isCharging() -> bool

    获取电池当前是否正在充电。

    UIFLOW2:

        |isCharging.svg|


.. method:: Power.getBatteryVoltage() -> int

    获取电池电压。单位是毫伏。

    UIFLOW2:

        |getBatteryVoltage.svg|


.. method:: Power.getBatteryCurrent() -> int

    获取电池电流。单位是毫安。

    UIFLOW2:

        |getBatteryCurrent.svg|


.. method:: Power.getKeyState() -> int

    获取电源键按下情况。

    UIFLOW2:

        |getKeyState.svg|

.. method:: Power.setVibration(level: int) -> None

    操作振动电机。

    ``level``: 振动强度，取值范围是 0-255。

    UIFLOW2:

        |setVibration.svg|

.. _class PORT:

class PORT
----------

Constants
---------

.. data:: PORT.A

    端口 A

.. data:: PORT.B1

    端口 B1

.. data:: PORT.B2

    端口 B2

.. data:: PORT.C1

    端口 C1

.. data:: PORT.C2

    端口 C2

.. data:: PORT.USB

    USB 端口

.. data:: PORT.HAT

    HAT 端口

.. data:: PORT.ALL

    所有端口
