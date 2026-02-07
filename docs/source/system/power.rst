Power
======

.. include:: ../refs/system.ref
.. include:: ../refs/system.power.ref

class Power
------------

.. important::

    Methods of the Power Class depend on ``M5.begin()`` |M5.begin.png|.

    All methods calling the Power object need to be placed after ``M5.begin()`` |M5.begin.png|.


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

        |setExtOutput1.png|
        |setExtOutput2.png|


.. method:: Power.getExtOutput() -> bool

    Get power output of the external ports.

    Returns ``True`` if the power output of the external ports is in output
    mode. Returns ``False`` if the power output of the external ports is in
    input mode.

    UIFLOW2:

        |getExtOutput.png|


.. method:: Power.setUsbOutput(enable: bool) -> None

    Set power output of the main USB port.

    When ``enable`` is True, the power output of the main USB port is in output
    mode. When ``enable`` is False, the power output of the main USB port is in
    input mode.

    UIFLOW2:

        |setUsbOutput.png|


.. method:: Power.getUsbOutput() -> bool

    Get power output of the main USB port.

    Returns ``True`` if the power output of the main USB port is in output mode.
    Returns ``False`` if the power output of the main USB port is in input mode.

    UIFLOW2:

        |getUsbOutput.png|


.. method:: Power.setLed(brightness=255) -> None

    Turn on/off the power LED.

    ``brightness`` is the brightness value, ranging from 0 to 255. 0 is off,
    255 is the maximum brightness.

    UIFLOW2:

        |setLed.png|


.. method:: Power.powerOff()

    Turn off all power.

    UIFLOW2:

        |powerOff.png|


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

        |timerSleep1.png|
        |timerSleep2.png|
        |timerSleep3.png|


.. method:: Power.deepSleep(micro_seconds: int=0, wakeup: bool=True)

    ESP32 deepsleep.

    ``micro_seconds``: Number of micro seconds to wakeup.

    ``wakeup``: Whether to wake up.

    UIFLOW2:

        |deepSleep.png|


.. method:: Power.lightSleep(micro_seconds: int=0, wakeup: bool=True)

    ESP32 lightsleep.

    ``micro_seconds``: Number of micro seconds to wakeup.

    ``wakeup``: Whether to wake up.

    UIFLOW2:

        |lightSleep.png|


.. method:: Power.getBatteryLevel() -> int

    Get the remaining battery power percentage. Returns a value between 0-100.

    UIFLOW2:

        |getBatteryLevel.png|


.. method:: Power.setBatteryCharge(enable: bool) -> None

    Set battery charging enable.

    UIFLOW2:

        |setBatteryCharge.png|


.. method:: Power.setChargeCurrent(max_mA: int) -> None

    Set battery charge current.

    ``max_mA``: Range is 0-2000, in milliamps.

    UIFLOW2:

        |setChargeCurrent.png|


.. method:: Power.setChargeVoltage(max_mV: int) -> None

    Set battery charge voltage.

    ``max_mV``: Range is 4100-4600, in millivolts.

    UIFLOW2:

        |setChargeVoltage.png|


.. method:: Power.isCharging() -> bool

    Get whether the battery is currently charging or not.

    UIFLOW2:

        |isCharging.png|


.. method:: Power.getBatteryVoltage() -> int

    Get battery voltage. Unit is millivolts.

    UIFLOW2:

        |getBatteryVoltage.png|


.. method:: Power.getBatteryCurrent() -> int

    Get battery current. Unit is milliamps.

    UIFLOW2:

        |getBatteryCurrent.png|


.. method:: Power.getKeyState() -> int

    Get Power Key Press condition.

    UIFLOW2:

        |getKeyState.png|

.. method:: Power.setVibration(level: int) -> None

    Operate the vibration motor.

    ``level``: Vibration intensity, ranging from 0-255.

    UIFLOW2:

        |setVibration.png|


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
