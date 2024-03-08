Power
======

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.power.ref

class Power
------------

.. important::

    Methods of the Power Class depend on ``M5.begin()`` |M5.begin.svg|.

    All methods calling the Power object need to be placed after ``M5.begin()`` |M5.begin.svg|.

Methods
-------

.. method:: Power.setExtOutput(enable: bool, port: int=0xFF) -> None

    Set power output of the external ports.

    When ``enable`` is True, the power output of the external ports is in output
    mode. When ``enable`` is False, the power output of the external ports is
    in input mode.

    ``port`` is the port number, optional values are available in :ref:`class PORT`,
    only valid for M5Stack Station.

    UIFLOW2:

        |setExtOutput1.svg|
        |setExtOutput2.svg|


.. method:: Power.getExtOutput() -> bool

    Get power output of the external ports.

    Returns ``True`` if the power output of the external ports is in output
    mode. Returns ``False`` if the power output of the external ports is in
    input mode.

    UIFLOW2:

        |getExtOutput.svg|


.. method:: Power.setUsbOutput(enable: bool) -> None

    Set power output of the main USB port.

    When ``enable`` is True, the power output of the main USB port is in output
    mode. When ``enable`` is False, the power output of the main USB port is in
    input mode.

    UIFLOW2:

        |setUsbOutput.svg|


.. method:: Power.getUsbOutput() -> bool

    Get power output of the main USB port.

    Returns ``True`` if the power output of the main USB port is in output mode.
    Returns ``False`` if the power output of the main USB port is in input mode.

    UIFLOW2:

        |getUsbOutput.svg|


.. method:: Power.setLed(brightness=255) -> None

    Turn on/off the power LED.

    ``brightness`` is the brightness value, ranging from 0 to 255. 0 is off,
    255 is the maximum brightness.

    UIFLOW2:

        |setLed.svg|


.. method:: Power.powerOff()

    Turn off all power.

    UIFLOW2:

        |powerOff.svg|


.. method:: Power.timerSleep(seconds) -> None
            Power.timerSleep(minutes, hours) -> None
            Power.timerSleep(minutes, hours, date, weekDay) -> None

    sleep and timer boot. The boot condition can be specified by the argument.

    ``seconds``: Range is 1 - 15300, in seconds.

    ``minutes``: Range is 0 - 59, in minutes.

    ``hours``: Range is 0 - 23, in hours.

    ``date``: Range is 1 - 31, in days.

    ``weekDay``: Range is 0 - 6.

    UIFLOW2:

        |timerSleep1.svg|
        |timerSleep2.svg|
        |timerSleep3.svg|


.. method:: Power.deepSleep(micro_seconds: int=0, wakeup: bool=True)

    ESP32 deepsleep.

    ``micro_seconds``: Number of micro seconds to wakeup.

    ``wakeup``: Whether to wake up.

    UIFLOW2:

        |deepSleep.svg|


.. method:: Power.lightSleep(micro_seconds: int=0, wakeup: bool=True)

    ESP32 lightsleep.

    ``micro_seconds``: Number of micro seconds to wakeup.

    ``wakeup``: Whether to wake up.

    UIFLOW2:

        |lightSleep.svg|


.. method:: Power.getBatteryLevel() -> int

    Get the remaining battery power percentage. Returns a value between 0-100.

    UIFLOW2:

        |getBatteryLevel.svg|


.. method:: Power.setBatteryCharge(enable: bool) -> None

    Set battery charging enable.

    UIFLOW2:

        |setBatteryCharge.svg|


.. method:: Power.setChargeCurrent(max_mA: int) -> None

    Set battery charge current.

    ``max_mA``: Range is 0-2000, in milliamps.

    UIFLOW2:

        |setChargeCurrent.svg|


.. method:: Power.setChargeVoltage(max_mV: int) -> None

    Set battery charge voltage.

    ``max_mV``: Range is 4100-4600, in millivolts.

    UIFLOW2:

        |setChargeVoltage.svg|


.. method:: Power.isCharging() -> bool

    Get whether the battery is currently charging or not.

    UIFLOW2:

        |isCharging.svg|


.. method:: Power.getBatteryVoltage() -> int

    Get battery voltage. Unit is millivolts.

    UIFLOW2:

        |getBatteryVoltage.svg|


.. method:: Power.getBatteryCurrent() -> int

    Get battery current. Unit is milliamps.

    UIFLOW2:

        |getBatteryCurrent.svg|


.. method:: Power.getKeyState() -> int

    Get Power Key Press condition.

    UIFLOW2:

        |getKeyState.svg|

.. method:: Power.setVibration(level: int) -> None

    Operate the vibration motor.

    ``level``: Vibration intensity, ranging from 0-255.

    UIFLOW2:

        |setVibration.svg|

.. _class PORT:

class PORT
----------

Constants
---------

.. data:: PORT.A

    Port A.

.. data:: PORT.B1

    Port B1.

.. data:: PORT.B2

    Port B2.

.. data:: PORT.C1

    Port C1.

.. data:: PORT.C2

    Port C2.

.. data:: PORT.USB

    USB Port.

.. data:: PORT.HAT

    HAT Port.

.. data:: PORT.ALL

    All Ports.
