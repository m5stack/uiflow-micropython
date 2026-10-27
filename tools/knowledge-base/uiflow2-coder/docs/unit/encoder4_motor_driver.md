# 4EncoderMotor Driver Unit

This library controls Unit 4EncoderMotor Driver over I2C, including four motor
channels, open-loop PWM, position and speed control, and encoder feedback.

Support the following products:

    Unit 4EncoderMotor Driver

## MicroPython Example

#### Four-Motor PWM Control

Run the same example on CoreS3 with the connection described above.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Encoder4MotorDriverUnit
from hardware import Pin
from hardware import I2C

page0 = None
button_stop = None
label_title = None
label_m1 = None
slider_m1 = None
slider_m2 = None
slider_m3 = None
slider_m4 = None
label_m4 = None
label_m3 = None
label_m2 = None
label_v1 = None
label_v4 = None
label_v3 = None
label_v2 = None
i2c0 = None
encoder4motordriver_0 = None
speed1 = None
speed2 = None
speed3 = None
speed4 = None
speed = None

def button_stop_short_clicked_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    encoder4motordriver_0.stop_motor(Encoder4MotorDriverUnit.MOTOR_ALL)
    encoder4motordriver_0.set_rgb_color(0xCC0000)
    speed1 = 0
    speed2 = 0
    speed3 = 0
    speed4 = 0
    label_v1.set_text(str(speed1))
    label_v2.set_text(str(speed2))
    label_v3.set_text(str(speed3))
    label_v4.set_text(str(speed4))

def slider_m1_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed1 = slider_m1.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_1, speed1)
    label_v1.set_text(str(speed1))
    encoder4motordriver_0.set_rgb_color(0x009900)

def slider_m2_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed2 = slider_m2.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_2, speed2)
    label_v2.set_text(str(speed2))
    encoder4motordriver_0.set_rgb_color(0x009900)

def slider_m3_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed3 = slider_m3.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_3, speed3)
    label_v3.set_text(str(speed3))
    encoder4motordriver_0.set_rgb_color(0x009900)

def slider_m4_value_changed_event(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    speed4 = slider_m4.get_value()
    encoder4motordriver_0.set_motor_pwm_duty(Encoder4MotorDriverUnit.MOTOR_4, speed4)
    label_v4.set_text(str(speed4))
    encoder4motordriver_0.set_rgb_color(0x009900)

def button_stop_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_stop_short_clicked_event(event_struct)
    return

def slider_m1_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m1_value_changed_event(event_struct)
    return

def slider_m2_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m2_value_changed_event(event_struct)
    return

def slider_m3_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m3_value_changed_event(event_struct)
    return

def slider_m4_event_handler(event_struct):
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider_m4_value_changed_event(event_struct)
    return

def setup():
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
        speed

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    button_stop = m5ui.M5Button(
        text="STOP",
        x=112,
        y=185,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_title = m5ui.M5Label(
        "4Encoder Motor Control",
        x=12,
        y=5,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_m1 = m5ui.M5Label(
        "M1",
        x=4,
        y=42,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    slider_m1 = m5ui.M5Slider(
        x=55,
        y=45,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    slider_m2 = m5ui.M5Slider(
        x=55,
        y=76,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    slider_m3 = m5ui.M5Slider(
        x=56,
        y=107,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    slider_m4 = m5ui.M5Slider(
        x=55,
        y=139,
        w=205,
        h=11,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=0,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label_m4 = m5ui.M5Label(
        "M4",
        x=4,
        y=136,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_m3 = m5ui.M5Label(
        "M3",
        x=3,
        y=104,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_m2 = m5ui.M5Label(
        "M2",
        x=4,
        y=73,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v1 = m5ui.M5Label(
        "00",
        x=267,
        y=42,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v4 = m5ui.M5Label(
        "00",
        x=267,
        y=136,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v3 = m5ui.M5Label(
        "00",
        x=267,
        y=104,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_v2 = m5ui.M5Label(
        "00",
        x=267,
        y=73,
        text_c=0x079EE1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    button_stop.add_event_cb(button_stop_event_handler, lv.EVENT.ALL, None)
    slider_m1.add_event_cb(slider_m1_event_handler, lv.EVENT.ALL, None)
    slider_m2.add_event_cb(slider_m2_event_handler, lv.EVENT.ALL, None)
    slider_m3.add_event_cb(slider_m3_event_handler, lv.EVENT.ALL, None)
    slider_m4.add_event_cb(slider_m4_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    encoder4motordriver_0 = Encoder4MotorDriverUnit(i2c0, 0x24)
    page0.screen_load()
    speed = 0
    encoder4motordriver_0.set_motor_mode(
        Encoder4MotorDriverUnit.MOTOR_ALL, Encoder4MotorDriverUnit.MODE_OPEN_LOOP
    )
    encoder4motordriver_0.set_rgb_color(0x009900)
    speed1 = 0
    speed2 = 0
    speed3 = 0
    speed4 = 0

def loop():
    global \
        page0, \
        button_stop, \
        label_title, \
        label_m1, \
        slider_m1, \
        slider_m2, \
        slider_m3, \
        slider_m4, \
        label_m4, \
        label_m3, \
        label_m2, \
        label_v1, \
        label_v4, \
        label_v3, \
        label_v2, \
        i2c0, \
        encoder4motordriver_0, \
        speed1, \
        speed2, \
        speed3, \
        speed4, \
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

    Four sliders control the motor PWM targets independently; **STOP** stops
    all four motors. If the Unit is not detected, a connection-check prompt is shown.

## **API**

#### Encoder4MotorDriverUnit

## `Encoder4MotorDriverUnit`
Control the Unit 4EncoderMotor Driver over I2C.

The Unit supports four motor channels with open-loop PWM, position and speed
control, encoder feedback, soft start and stop, RGB LED control, and input
power monitoring. The object borrows the supplied I2C bus and does not
deinitialize it. If the configured address is not found, check the Unit's
Grove connection, power supply, and I2C address.

- Parameter `| PAHUBUnit i2c` (`I2C`): Initialized I2C bus or compatible PAHUB port.
- Parameter `address` (`int`): 7-bit I2C address in the range 0x08~0x77. Defaults to 0x24.

```python
from hardware import I2C, Pin
from unit import Encoder4MotorDriverUnit

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
unit_4enc_motor_driver = Encoder4MotorDriverUnit(i2c0, 0x24)
```
Motor channel constants:

- `MOTOR_ALL = -1`: apply a setter or action to all four motors in order.
- `MOTOR_1 = 0`, `MOTOR_2 = 1`, `MOTOR_3 = 2`, `MOTOR_4 = 3`:
  select one motor. Reading methods accept one channel in the range 0~3.

Control mode constants:

- `MODE_OPEN_LOOP = 0`: open-loop PWM control.
- `MODE_POSITION = 1`: position control.
- `MODE_SPEED = 2`: speed control.

Encoder phase constants:

- `ENCODER_MODE_AB = 0`: AB phase order.
- `ENCODER_MODE_BA = 1`: BA phase order.

Speed samples and closed-loop speed targets use the device's native values
in the range -127~127, without a documented RPM conversion. Position speed
limits use the native range 0~127. Soft start and stop gradually changes PWM
output to reduce mechanical shock when starting, stopping, or changing speed.

### `set_motor_mode`
Set one motor control mode.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    mode (int): One of `MODE_OPEN_LOOP`, `MODE_POSITION`, or
        `MODE_SPEED`.

Returns:
    None.

### `get_motor_mode`
Get one motor control mode.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Current mode. Range: 0~2.

### `set_motor_pwm_duty`
Set open-loop PWM duty and direction for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    percent (int or float): Signed PWM duty. Unit: percent. Range:
        -100~100. The sign selects direction and 0 stops output.

Returns:
    None.

### `get_motor_pwm_duty`
Get the commanded open-loop PWM duty for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Signed commanded PWM duty. Unit: percent. Range: -100~100.

### `read_motor_speed`
Read the live native speed sample for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Signed device-native speed sample. Range: -127~127. The
    firmware updates this value every 20 ms. It is not RPM and has no
    verified physical-unit conversion.

### `stop_motor`
Stop one motor and leave it in open-loop mode.

PWM is cleared before the mode changes so a previous position or speed
target cannot resume when open-loop mode becomes active.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.

Returns:
    None.

### `enable_soft_start`
Enable soft start and stop for one motor in open-loop mode.

The shared setting is retained in the Unit's flash. Repeating the call
with the channel already enabled does not change the stored value.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.

Returns:
    None.

### `disable_soft_start`
Disable soft start and stop for one motor in open-loop mode.

The shared setting is retained in the Unit's flash. Repeating the call
with the channel already disabled does not change the stored value.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.

Returns:
    None.

### `is_soft_start_enabled`
Return whether soft start and stop is enabled for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    bool: `True` when soft start and stop is enabled.

### `read_encoder_count`
Read one motor encoder count without clearing it.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Signed encoder count. Range: -2147483648~2147483647.

### `set_encoder_count`
Set one motor encoder count.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    count (int): Signed encoder count. Range:
        -2147483648~2147483647.

Returns:
    None.

### `clear_encoder_count`
Clear one motor encoder count to zero.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    None.

### `set_encoder_mode`
Set the global encoder phase order.

A changed value is retained in the Unit's flash and immediately
restarts the Unit. The call waits for the current I2C address to become
available again. Avoid unnecessary calls to limit flash writes.

Args:
    mode (int): `ENCODER_MODE_AB` or `ENCODER_MODE_BA`.

Returns:
    None.

### `get_encoder_mode`
Get the global encoder phase order.

Returns:
    int: `ENCODER_MODE_AB` or `ENCODER_MODE_BA`.

### `set_position_pid`
Set position-loop PID coefficients for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    kp (int): Native proportional coefficient. Range: 0~255.
    ki (int): Native integral coefficient. Range: 0~255.
    kd (int): Native derivative coefficient. Range: 0~255.

Returns:
    None.

### `get_position_pid`
Get position-loop PID coefficients for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    tuple: `(kp, ki, kd)`. Each native coefficient is 0~255.

### `set_position_target_count`
Set the position-loop target in encoder counts.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    count (int): Signed target. Unit: encoder counts. Range:
        -2147483648~2147483647.

Returns:
    None.

### `get_position_target_count`
Get the configured position-loop target in encoder counts.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Signed target. Unit: encoder counts. Range:
    -2147483648~2147483647.

### `set_position_speed_limit`
Set the native position-loop speed limit.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    speed_limit (int): Unsigned device-native speed limit. Range: 0~127.

Returns:
    None.

### `get_position_speed_limit`
Get the native position-loop speed limit.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Unsigned, dimensionless device level. Range: 0~127. This
    value is not RPM.

### `set_speed_pid`
Set speed-loop PID coefficients for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    kp (int): Native proportional coefficient. Range: 0~255.
    ki (int): Native integral coefficient. Range: 0~255.
    kd (int): Native derivative coefficient. Range: 0~255.

Returns:
    None.

### `get_speed_pid`
Get speed-loop PID coefficients for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    tuple: `(kp, ki, kd)`. Each native coefficient is 0~255.

### `set_speed_target`
Set the native closed-loop speed target for one motor.

Args:
    channel (int): Motor channel index. Range: 0~3, or `MOTOR_ALL` for all motors.
    speed (int): Signed device-native speed target. Range: -127~127.

Returns:
    None.

### `get_speed_target`
Get the configured closed-loop speed target.

Args:
    channel (int): Motor channel index. Range: 0~3.

Returns:
    int: Signed device-native speed target. Range: -127~127.

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
Read the motor supply input voltage.

Returns:
    float: Input voltage. Unit: V. Range depends on the hardware supply.

### `read_input_voltage_adc`
Read the raw 12-bit motor-supply voltage ADC sample.

Returns:
    int: Raw ADC sample. Range: 0~4095. This is not a voltage unit;
    use `read_input_voltage()` for volts.

### `read_input_current`
Read the total motor supply input current.

Returns:
    float: Input current. Unit: A. Range depends on the connected load.

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
    int: 7-bit I2C address. Range: 0x08~0x77 for public API use.

### `set_i2c_address`
Set the Unit I2C address and switch this object to it.

A changed address is retained in the Unit's flash and immediately
restarts the Unit. The call waits at least 300 ms, then polls the new
address before updating this object. Avoid unnecessary calls to limit
flash writes.

Args:
    address (int): New 7-bit I2C address. Range: 0x08~0x77.

Returns:
    None.
