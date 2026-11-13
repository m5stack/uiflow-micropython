Power
======

.. include:: ../refs/system.ref
.. include:: ../refs/system.power.ref

class Power
------------

.. important::

    Methods of the Power Class depend on ``M5.begin()`` |M5.begin.png|.

    All methods calling the Power object need to be placed after ``M5.begin()`` |M5.begin.png|.

.. note::

    The Power class manages the **built-in** power monitoring chip (INA226,
    INA3221, AXP192, etc.) on the host device's internal I2C bus. If your
    device has a built-in power monitor, use the Power API below to read
    battery voltage/current — do **not** initialize I2C manually or
    instantiate an external ``INA226Unit``, as this will conflict with the
    system driver and may cause crashes.

    External (Grove-connected) power monitor units should still be
    initialized via ``from unit import INA226Unit`` with user-created I2C.


Methods
-------

.. method:: Power.setExtOutput(enable: bool, port_mask: int=0xFF) -> None

    Set power output of the external ports.

    When ``enable`` is True, the power output of the external ports is in output
    mode. When ``enable`` is False, the power output of the external ports is
    in input mode.

    ``port_mask`` selects external outputs using :ref:`class PORT` masks.
    Individual port selection depends on the controller.

    UIFLOW2:

        |setExtOutput1.png|
        |setExtOutput2.png|


.. method:: Power.getType() -> int

    Return the power-management type as an integer.

    .. list-table::
        :header-rows: 1

        * - Value
          - Type
        * - 0
          - Unknown
        * - 1
          - ADC
        * - 2
          - AXP192
        * - 3
          - IP5306
        * - 4
          - AXP2101
        * - 5
          - AW32001
        * - 6
          - M5PM1


.. method:: Power.getVBUSVoltage() -> int

    Return the USB VBUS voltage in millivolts, or ``-1`` when unsupported.


.. method:: Power.getExtVoltage(ext_port: int) -> float

    Return the external-port voltage in millivolts. ``ext_port`` is a
    :ref:`class PORT` mask. Unsupported measurements return ``0.0``.


.. method:: Power.getExtCurrent(ext_port: int) -> float

    Return the external-port current in milliamps. ``ext_port`` is a
    :ref:`class PORT` mask. Unsupported measurements return ``0.0``.
    StopWatch, StickS3 and StampS3Bat have no external-current measurement;
    their ``0.0`` result does not indicate a measured zero current.


.. method:: Power.getPortVbus(port: int)

    Return an INA3221 channel voltage in volts on M5Station.
    ``port`` is a channel index from 0 to 5, independent of :ref:`class PORT`
    masks. ESP32-S3 and other non-ESP32 targets return ``None``.


.. method:: Power.getPortCurrent(port: int)

    Return an INA3221 channel current in amperes on M5Station.
    ``port`` is a channel index from 0 to 5, independent of :ref:`class PORT`
    masks. ESP32-S3 and other non-ESP32 targets return ``None``.


.. method:: Power.setExtPortBusConfig(direction: int, output_enable: int=1, voltage: int=3000, current_limit: int=232) -> None

    Configure the M5PowerHub external CAN power bus.

    ``direction``: ``0`` for input, ``1`` for output.

    ``output_enable``: ``0`` to disable output, ``1`` to enable output.

    ``voltage``: Output voltage in millivolts, from 3000 to 20000 in steps of 20.

    ``current_limit``: Output current limit in milliamps, from 0 to 232.


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


.. method:: Power.setLed(br=255) -> None

    Turn on/off the power LED.

    ``br`` is the brightness value, ranging from 0 to 255. 0 is off,
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


.. method:: Power.deepSleep(micro_seconds: int=0, touch_wakeup: bool=True)

    ESP32 deepsleep.

    ``micro_seconds``: Number of micro seconds to wakeup.

    ``touch_wakeup``: Whether to enable touch wake-up on supported controllers.

    UIFLOW2:

        |deepSleep.png|


.. method:: Power.lightSleep(micro_seconds: int=0, touch_wakeup: bool=True)

    ESP32 lightsleep.

    ``micro_seconds``: Number of micro seconds to wakeup.

    ``touch_wakeup``: Whether to enable touch wake-up on supported controllers.

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


.. method:: Power.setChargeCurrent(ma: int) -> None

    Set battery charge current.

    ``ma``: Requested charge current in milliamps. Supported values depend on the controller.

    UIFLOW2:

        |setChargeCurrent.png|


.. method:: Power.setChargeVoltage(max_mv: int) -> None

    Set battery charge voltage.

    ``max_mv``: Requested charge voltage in millivolts. Supported values depend on the controller.

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

    Get battery current in milliamps. Positive values indicate charging and
    negative values indicate discharging. Controllers without a current
    measurement return ``0``.

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

Access these masks through ``M5.Power.PORT``. Physical port support depends
on the controller. ``PORT.HAT`` and ``PORT.ALL`` are not exported by UiFlow2;
do not use them as masks.

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


.. data:: PORT.PWR485

    External RS485 power on M5PowerHub.


.. data:: PORT.PWRCAN

    External CAN power on M5PowerHub.


.. data:: PORT.EXT

    External power port on supported controllers.


.. data:: PORT.MAIN

    Main power port on supported controllers.
