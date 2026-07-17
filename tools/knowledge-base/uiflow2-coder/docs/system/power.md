# Power

## class Power

> Important: Methods of the Power Class depend on `M5.begin()` .
>
> All methods calling the Power object need to be placed after `M5.begin()` .
> Note: The Power class manages the **built-in** power monitoring chip (INA226,
> INA3221, AXP192, etc.) on the host device's internal I2C bus. If your
> device has a built-in power monitor, use the Power API below to read
> battery voltage/current — do **not** initialize I2C manually or
> instantiate an external `INA226Unit`, as this will conflict with the
> system driver and may cause crashes.
>
> External (Grove-connected) power monitor units should still be
> initialized via `from unit import INA226Unit` with user-created I2C.
## Methods

### `Power.setExtOutput(enable: bool, port: int=0xFF) -> None`

    Set power output of the external ports.

    When `enable` is True, the power output of the external ports is in output
    mode. When `enable` is False, the power output of the external ports is
    in input mode.

    `port` is the port number, optional values are available in `class PORT`,
    only valid for M5Stack Station.

### `Power.getExtOutput() -> bool`

    Get power output of the external ports.

    Returns `True` if the power output of the external ports is in output
    mode. Returns `False` if the power output of the external ports is in
    input mode.

### `Power.setUsbOutput(enable: bool) -> None`

    Set power output of the main USB port.

    When `enable` is True, the power output of the main USB port is in output
    mode. When `enable` is False, the power output of the main USB port is in
    input mode.

### `Power.getUsbOutput() -> bool`

    Get power output of the main USB port.

    Returns `True` if the power output of the main USB port is in output mode.
    Returns `False` if the power output of the main USB port is in input mode.

### `Power.setLed(brightness=255) -> None`

    Turn on/off the power LED.

    `brightness` is the brightness value, ranging from 0 to 255. 0 is off,
    255 is the maximum brightness.

### `Power.powerOff()`

    Turn off all power.

### `Power.timerSleep(seconds) -> None`
            Power.timerSleep(minutes, hours) -> None
            Power.timerSleep(minutes, hours, date, weekDay) -> None

    sleep and timer boot. The boot condition can be specified by the argument.

    `seconds`: Range is 1 - 15300, in seconds.

    `minutes`: Range is 0 - 59, in minutes.

    `hours`: Range is 0 - 23, in hours.

    `date`: Range is 1 - 31, in days.

    `weekDay`: Range is 0 - 6.

### `Power.deepSleep(micro_seconds: int=0, wakeup: bool=True)`

    ESP32 deepsleep.

    `micro_seconds`: Number of micro seconds to wakeup.

    `wakeup`: Whether to wake up.

### `Power.lightSleep(micro_seconds: int=0, wakeup: bool=True)`

    ESP32 lightsleep.

    `micro_seconds`: Number of micro seconds to wakeup.

    `wakeup`: Whether to wake up.

### `Power.getBatteryLevel() -> int`

    Get the remaining battery power percentage. Returns a value between 0-100.

### `Power.setBatteryCharge(enable: bool) -> None`

    Set battery charging enable.

### `Power.setChargeCurrent(max_mA: int) -> None`

    Set battery charge current.

    `max_mA`: Range is 0-2000, in milliamps.

### `Power.setChargeVoltage(max_mV: int) -> None`

    Set battery charge voltage.

    `max_mV`: Range is 4100-4600, in millivolts.

### `Power.isCharging() -> bool`

    Get whether the battery is currently charging or not.

### `Power.getBatteryVoltage() -> int`

    Get battery voltage. Unit is millivolts.

### `Power.getBatteryCurrent() -> int`

    Get battery current. Unit is milliamps.

### `Power.getKeyState() -> int`

    Get Power Key Press condition.

### `Power.setVibration(level: int) -> None`

    Operate the vibration motor.

    `level`: Vibration intensity, ranging from 0-255.

## class PORT

## Constants

### `PORT.A`

    Port A.

### `PORT.B1`

    Port B1.

### `PORT.B2`

    Port B2.

### `PORT.C1`

    Port C1.

### `PORT.C2`

    Port C2.

### `PORT.USB`

    USB Port.

### `PORT.HAT`

    HAT Port.

### `PORT.ALL`

    All Ports.
