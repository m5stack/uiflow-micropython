# EncoderMotor Driver Unit

The `EncoderMotorDriverUnit` class controls Unit EncoderMotor Driver over I2C.
It supports signed open-loop PWM, position and speed control, encoder feedback,
motor sleep, soft start and stop, RGB LED control, and input power monitoring.

Support the following products:

    Unit EncoderMotor Driver

## MicroPython Example

#### Basic Motor Control

Run the following example on CoreS3 with the same connection and Unit runtime
settings described above. The `+`, `-` and `STOP` controls have the same
behavior as the UiFlow2 project.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import EncoderMotorDriverUnit
from hardware import Pin
from hardware import I2C

page0 = None
label_title = None
button_speed_up = None
button_speed_down = None
label_speed = None
button_stop = None
i2c0 = None
encodermotordriver_0 = None
speed = None

def button_stop_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    label_speed.set_text(str(speed))

def button_speed_up_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    if speed < 80:
        speed = speed + 20
    else:
        speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    label_speed.set_text(str(speed))

def button_speed_down_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    if speed > -80:
        speed = speed - 20
    else:
        speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    label_speed.set_text(str(speed))

def button_stop_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_stop_short_clicked_event(event_struct)
    return

def button_speed_up_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_speed_up_short_clicked_event(event_struct)
    return

def button_speed_down_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_speed_down_short_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Encoder Motor Control",
        x=20,
        y=5,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button_speed_up = m5ui.M5Button(
        text="+",
        x=50,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button_speed_down = m5ui.M5Button(
        text="-",
        x=230,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_speed = m5ui.M5Label(
        "00",
        x=132,
        y=75,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    button_stop = m5ui.M5Button(
        text="STOP",
        x=112,
        y=165,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    button_stop.add_event_cb(button_stop_event_handler, lv.EVENT.ALL, None)
    button_speed_up.add_event_cb(button_speed_up_event_handler, lv.EVENT.ALL, None)
    button_speed_down.add_event_cb(button_speed_down_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    encodermotordriver_0 = EncoderMotorDriverUnit(i2c0, 0x2F)
    speed = 0
    encodermotordriver_0.set_motor_pwm_duty(speed)
    page0.screen_load()

def loop():
    global \
        page0, \
        label_title, \
        button_speed_up, \
        button_speed_down, \
        label_speed, \
        button_stop, \
        i2c0, \
        encodermotordriver_0, \
        speed
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Example output:

    The center label shows the PWM target. If the Unit is not detected,
    the screen shows a connection-check prompt.

## **API**

#### EncoderMotorDriverUnit

## `EncoderMotorDriverUnit`
Control the Unit EncoderMotor Driver over I2C.

The Unit supports signed open-loop PWM, position and speed control, encoder
feedback, motor sleep, soft start and stop, RGB LED control, and input power
monitoring. The object borrows the supplied I2C bus and does not deinitialize
it. If the configured address is not found, check the Unit's Grove connection,
power supply, and I2C address.

- Parameter `| PAHUBUnit i2c` (`I2C`): Initialized I2C bus or compatible PAHUB port.
- Parameter `address` (`int`): 7-bit I2C address in the range 0x08~0x77. Defaults to 0x2F.

```python
from hardware import I2C, Pin
from unit import EncoderMotorDriverUnit

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
encodermotordriver_0 = EncoderMotorDriverUnit(i2c0, 0x2F)
```
Control mode constants:

- `MODE_OPEN_LOOP = 0`: open-loop PWM control.
- `MODE_POSITION = 1`: position control.
- `MODE_SPEED = 2`: speed control.

Encoder phase constants:

- `ENCODER_MODE_AB = 0`: AB phase order.
- `ENCODER_MODE_BA = 1`: BA phase order.

### `set_motor_mode`
Set the motor control mode.

Args:
    mode (int): One of `MODE_OPEN_LOOP`, `MODE_POSITION`, or
        `MODE_SPEED`.

Returns:
    None.

### `get_motor_mode`
Get the current motor control mode.

Returns:
    int: Current mode. Range: 0~2.

### `set_motor_pwm_duty`
Set the signed open-loop motor PWM duty.

Args:
    percent (int or float): Signed duty. Unit: percent. Range:
        -100~100. The sign selects the direction.

Returns:
    None.

### `get_motor_pwm_duty`
Get the motor PWM value as a signed percentage.

In open-loop mode this is the commanded PWM duty. In a closed-loop
mode the firmware may update the register with its live motor output.

Returns:
    int: Signed PWM duty. Unit: percent. Range: -100~100.

### `read_motor_speed`
Read the live device-native motor speed sample.

Returns:
    int: Signed native speed sample. Range: -127~127. The firmware
    updates this value every 20 ms. It is not RPM and has no verified
    physical-unit conversion.

### `stop_motor`
Stop the motor and leave it in open-loop mode.

The method clears PWM before and after changing the mode so a previous
closed-loop output cannot remain active after the mode transition.

Returns:
    None.

### `read_encoder_count`
Read the current encoder count without clearing it.

Returns:
    int: Signed encoder count. Range: -2147483648~2147483647.

### `set_encoder_count`
Set the current encoder count.

Args:
    count (int): Signed encoder count. Range:
        -2147483648~2147483647.

Returns:
    None.

### `clear_encoder_count`
Clear the encoder count to zero.

Returns:
    None.

### `set_encoder_mode`
Set the encoder AB or BA phase order.

A changed value is retained in the Unit's flash and immediately
restarts the Unit. The call waits for the current I2C address to become
available again. Avoid unnecessary calls to limit flash writes.

Args:
    mode (int): `ENCODER_MODE_AB` or `ENCODER_MODE_BA`.

Returns:
    None.

### `get_encoder_mode`
Get the encoder phase order.

Returns:
    int: `ENCODER_MODE_AB` or `ENCODER_MODE_BA`.

### `set_position_pid`
Set the position-loop PID coefficients.

Args:
    kp (int): Native proportional coefficient. Range: 0~255.
    ki (int): Native integral coefficient. Range: 0~255.
    kd (int): Native derivative coefficient. Range: 0~255.

Returns:
    None.

### `get_position_pid`
Get the position-loop PID coefficients.

Returns:
    tuple: `(kp, ki, kd)`. Each native coefficient is 0~255.

### `set_position_target_count`
Set the position-loop target in encoder counts.

Args:
    count (int): Signed target. Unit: encoder counts. Range:
        -2147483648~2147483647.

Returns:
    None.

### `get_position_target_count`
Get the configured position-loop target in encoder counts.

Returns:
    int: Signed target. Unit: encoder counts. Range:
    -2147483648~2147483647.

### `set_position_speed_limit`
Set the native position-loop maximum speed.

The position controller uses the absolute value of this speed limit.
The value is a device-native setting without a documented RPM conversion.

Args:
    speed_limit (int): Signed device-native speed limit. Range:
        -127~127.

Returns:
    None.

### `get_position_speed_limit`
Get the native position-loop maximum speed.

Returns:
    int: Signed, dimensionless device value. Range: -127~127. This
    value is not RPM.

### `set_speed_pid`
Set the speed-loop PID coefficients.

Args:
    kp (int): Native proportional coefficient. Range: 0~255.
    ki (int): Native integral coefficient. Range: 0~255.
    kd (int): Native derivative coefficient. Range: 0~255.

Returns:
    None.

### `get_speed_pid`
Get the speed-loop PID coefficients.

Returns:
    tuple: `(kp, ki, kd)`. Each native coefficient is 0~255.

### `set_speed_target`
Set the native closed-loop speed target.

Args:
    speed (int): Signed, dimensionless target. Range: -127~127. The
        value is not RPM.

Returns:
    None.

### `get_speed_target`
Get the configured closed-loop speed target.

Returns:
    int: Signed, dimensionless target. Range: -127~127. This value is
    not RPM.

### `enable_soft_start`
Enable soft start and stop in open-loop mode.

The setting is retained in the Unit's flash. Repeating the call while
already enabled avoids another write.

Returns:
    None.

### `disable_soft_start`
Disable soft start and stop in open-loop mode.

The setting is retained in the Unit's flash. Repeating the call while
already disabled avoids another write.

Returns:
    None.

### `is_soft_start_enabled`
Return whether soft start and stop is enabled.

Returns:
    bool: `True` when soft start and stop is enabled.

### `enable_motor`
Set Motor nSleep to run and enable the motor driver.

Returns:
    None.

### `disable_motor`
Set Motor nSleep to sleep and disable the motor driver.

Returns:
    None.

### `is_motor_enabled`
Return whether Motor nSleep is in the run state.

Returns:
    bool: `True` when the motor driver is enabled.

### `set_rgb_color`
Set the onboard RGB LED color.

Args:
    color (int): RGB888 color in `0xRRGGBB` format. Range:
        0x000000~0xFFFFFF.

Returns:
    None.

### `get_rgb_color`
Get the onboard RGB LED color.

Returns:
    int: RGB888 color in `0xRRGGBB` format. Range:
    0x000000~0xFFFFFF.

### `set_rgb_brightness`
Set the onboard RGB LED brightness.

Args:
    percent (int or float): Brightness. Unit: percent. Range: 0~100.

Returns:
    None.

### `get_rgb_brightness`
Get the onboard RGB LED brightness.

Returns:
    int: Brightness. Unit: percent. Range: 0~100.

### `read_input_voltage`
Read the motor-supply input voltage.

Returns:
    float: Input voltage. Unit: V. Range depends on the supply.

### `read_input_voltage_adc`
Read the raw 12-bit motor-supply voltage ADC sample.

Returns:
    int: Raw ADC sample. Range: 0~4095. Use
    `read_input_voltage()` for volts.

### `read_input_current`
Read the motor-supply input current.

Returns:
    float: Input current. Unit: A. Range depends on the load.

### `get_firmware_version`
Get the Unit firmware version register value.

Returns:
    int: Firmware version value. Range: 0~255.

### `get_uid`
Get the device's 12-byte STM32 unique identifier.

Returns:
    bytes: Device UID with exactly 12 bytes in protocol order.

### `get_i2c_address`
Get the Unit I2C address from the device.

Returns:
    int: 7-bit I2C address. Range: 0x08~0x77.

### `set_i2c_address`
Set the Unit I2C address and switch this object to it.

A changed address is retained in the Unit's flash. The protocol states
that the Unit restarts and requires about 300 ms before responding at
the new address. This method waits and polls before updating the
object's address. Avoid unnecessary calls to limit flash writes.

Args:
    address (int): New 7-bit I2C address. Range: 0x08~0x77.

Returns:
    None.
