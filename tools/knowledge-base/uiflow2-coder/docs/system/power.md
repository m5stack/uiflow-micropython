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

### `Power.setExtOutput(enable: bool, port_mask: int=0xFF) -> None`

    Set power output of the external ports.

    When `enable` is True, the power output of the external ports is in output
    mode. When `enable` is False, the power output of the external ports is
    in input mode.

    `port_mask` selects external outputs using `class PORT` masks.
    Individual port selection depends on the controller.

### `Power.getType() -> int`

    Return the power-management type as an integer.

| Value | Type |
| --- | --- |
| 0 | Unknown |
| 1 | ADC |
| 2 | AXP192 |
| 3 | IP5306 |
| 4 | AXP2101 |
| 5 | AW32001 |
| 6 | M5PM1 |

### `Power.getVBUSVoltage() -> int`

    Return the USB VBUS voltage in millivolts, or `-1` when unsupported.

### `Power.getExtVoltage(ext_port: int) -> float`

    Return the external-port voltage in millivolts. `ext_port` is a
    `class PORT` mask. Unsupported measurements return `0.0`.

### `Power.getExtCurrent(ext_port: int) -> float`

    Return the external-port current in milliamps. `ext_port` is a
    `class PORT` mask. Unsupported measurements return `0.0`.
    StopWatch, StickS3 and StampS3Bat have no external-current measurement;
    their `0.0` result does not indicate a measured zero current.

### `Power.getPortVbus(port: int)`

    Return an INA3221 channel voltage in volts on M5Station.
    `port` is a channel index from 0 to 5, independent of `class PORT`
    masks. ESP32-S3 and other non-ESP32 targets return `None`.

### `Power.getPortCurrent(port: int)`

    Return an INA3221 channel current in amperes on M5Station.
    `port` is a channel index from 0 to 5, independent of `class PORT`
    masks. ESP32-S3 and other non-ESP32 targets return `None`.

### `Power.setExtPortBusConfig(direction: int, output_enable: int=1, voltage: int=3000, current_limit: int=232) -> None`

    Configure the M5PowerHub external CAN power bus.

    `direction`: `0` for input, `1` for output.

    `output_enable`: `0` to disable output, `1` to enable output.

    `voltage`: Output voltage in millivolts, from 3000 to 20000 in steps of 20.

    `current_limit`: Output current limit in milliamps, from 0 to 232.

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

### `Power.setLed(br=255) -> None`

    Turn on/off the power LED.

    `br` is the brightness value, ranging from 0 to 255. 0 is off,
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

### `Power.deepSleep(micro_seconds: int=0, touch_wakeup: bool=True)`

    ESP32 deepsleep.

    `micro_seconds`: Number of micro seconds to wakeup.

    `touch_wakeup`: Whether to enable touch wake-up on supported controllers.

### `Power.lightSleep(micro_seconds: int=0, touch_wakeup: bool=True)`

    ESP32 lightsleep.

    `micro_seconds`: Number of micro seconds to wakeup.

    `touch_wakeup`: Whether to enable touch wake-up on supported controllers.

### `Power.getBatteryLevel() -> int`

    Get the remaining battery power percentage. Returns a value between 0-100.

### `Power.setBatteryCharge(enable: bool) -> None`

    Set battery charging enable.

### `Power.setChargeCurrent(ma: int) -> None`

    Set battery charge current.

    `ma`: Requested charge current in milliamps. Supported values depend on the controller.

### `Power.setChargeVoltage(max_mv: int) -> None`

    Set battery charge voltage.

    `max_mv`: Requested charge voltage in millivolts. Supported values depend on the controller.

### `Power.isCharging() -> bool`

    Get whether the battery is currently charging or not.

### `Power.getBatteryVoltage() -> int`

    Get battery voltage. Unit is millivolts.

### `Power.getBatteryCurrent() -> int`

    Get battery current in milliamps. Positive values indicate charging and
    negative values indicate discharging. Controllers without a current
    measurement return `0`.

### `Power.getKeyState() -> int`

    Get Power Key Press condition.

### `Power.setVibration(level: int) -> None`

    Operate the vibration motor.

    `level`: Vibration intensity, ranging from 0-255.

## class PORT

## Constants

Access these masks through `M5.Power.PORT`. Physical port support depends
on the controller. `PORT.HAT` and `PORT.ALL` are not exported by UiFlow2;
do not use them as masks.

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

### `PORT.PWR485`

    External RS485 power on M5PowerHub.

### `PORT.PWRCAN`

    External CAN power on M5PowerHub.

### `PORT.EXT`

    External power port on supported controllers.

### `PORT.MAIN`

    Main power port on supported controllers.
