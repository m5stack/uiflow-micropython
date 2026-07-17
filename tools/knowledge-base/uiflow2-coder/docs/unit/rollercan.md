
# RollerCAN Unit

Support the following products:

RollerCAN

RollerCAN I2C Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import RollerCANUnit

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
i2c1 = None
rollercan_0 = None

output = None
mode = None

def btnb__event(state):
    global title0, label0, label1, label2, label3, label4, i2c1, rollercan_0, output, mode
    output = output ^ (0x01 << 0)
    rollercan_0.set_motor_output_state(output)

def btna__event(state):
    global title0, label0, label1, label2, label3, label4, i2c1, rollercan_0, output, mode
    mode = mode + 1
    if mode > 4:
        mode = 1
    rollercan_0.set_motor_mode(mode)

def setup():
    global title0, label0, label1, label2, label3, label4, i2c1, rollercan_0, output, mode

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("RollerCAN I2C Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("mode:", 1, 63, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("motor state:", 2, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("speed:", 2, 152, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("mode", 40, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("on/off", 126, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb__event)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna__event)

    i2c1 = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000)
    rollercan_0 = RollerCANUnit(i2c1, address=0x64, mode=RollerCANUnit.I2C_MODE)
    rollercan_0.set_motor_output_state(0)
    output = 0
    mode = rollercan_0.get_motor_mode()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))

def loop():
    global title0, label0, label1, label2, label3, label4, i2c1, rollercan_0, output, mode
    M5.update()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))
    if mode == 1:
        rollercan_0.set_motor_speed(20000)
        rollercan_0.set_speed_max_current(400)
        label2.setText(str((str("speed:") + str((rollercan_0.get_motor_speed_readback())))))
    elif mode == 2:
        rollercan_0.set_motor_position(1000)
        rollercan_0.set_position_max_current(400)
        label2.setText(str((str("position:") + str((rollercan_0.get_motor_position_readback())))))
    elif mode == 3:
        rollercan_0.set_motor_max_current(400)
        label2.setText(str((str("current:") + str((rollercan_0.get_motor_current_readback())))))
    elif mode == 4:
        label2.setText(str((str("encoder:") + str((rollercan_0.get_encoder_value())))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

RollerCAN CAN Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import RollerCANUnit
from unit import CANUnit

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
can_0 = None
rollercan_0 = None

mode = None
output = None

def btna__event(state):
    global title0, label0, label1, label2, label3, label4, can_0, rollercan_0, mode, output
    mode = mode + 1
    if mode > 4:
        mode = 1
    rollercan_0.set_motor_mode(mode)

def btnb__event(state):
    global title0, label0, label1, label2, label3, label4, can_0, rollercan_0, mode, output
    output = output ^ (0x01 << 0)
    rollercan_0.set_motor_output_state(output)

def setup():
    global title0, label0, label1, label2, label3, label4, can_0, rollercan_0, mode, output

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("RollerCAN CAN Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("mode:", 1, 63, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("motor state:", 2, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("speed:", 2, 152, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("mode", 40, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("on/off", 126, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna__event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb__event)

    can_0 = CANUnit((13, 15), CANUnit.NORMAL, baudrate=1000000)
    rollercan_0 = RollerCANUnit(can_0, address=0xA8, mode=RollerCANUnit.CAN_MODE)
    rollercan_0.set_motor_output_state(0)
    output = 0
    mode = rollercan_0.get_motor_mode()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))

def loop():
    global title0, label0, label1, label2, label3, label4, can_0, rollercan_0, mode, output
    M5.update()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))
    if mode == 1:
        rollercan_0.set_motor_speed(20000)
        rollercan_0.set_speed_max_current(400)
        label2.setText(str((str("speed:") + str((rollercan_0.get_motor_speed_readback())))))
    elif mode == 2:
        rollercan_0.set_motor_position(1000)
        rollercan_0.set_position_max_current(400)
        label2.setText(str((str("position:") + str((rollercan_0.get_motor_position_readback())))))
    elif mode == 3:
        rollercan_0.set_motor_max_current(400)
        label2.setText(str((str("current:") + str((rollercan_0.get_motor_current_readback())))))
    elif mode == 4:
        label2.setText(str((str("encoder:") + str((rollercan_0.get_encoder_value())))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

RollerCAN CANToI2C Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import RollerCANUnit
from unit import CANUnit
from unit import ENVUnit

title0 = None
label5 = None
label7 = None
label0 = None
label6 = None
label1 = None
label2 = None
label3 = None
label4 = None
env3_0 = None
can_0 = None
rollercan_0 = None

output = None
mode = None

def btnb__event(state):
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    output = output ^ (0x01 << 0)
    rollercan_0.set_motor_output_state(output)

def btna__event(state):
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    mode = mode + 1
    if mode > 4:
        mode = 1
    rollercan_0.set_motor_mode(mode)

def btnc__event(state):
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    label5.setText(str((str("temp:") + str((env3_0.read_temperature())))))
    label6.setText(str((str("humi:") + str((env3_0.read_pressure())))))

def setup():
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "RollerCAN CANToI2C Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label5 = Widgets.Label("temp:", 182, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("update env", 199, 213, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("mode:", 1, 63, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("humi:", 182, 131, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("motor state:", 2, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("speed:", 2, 152, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("mode", 40, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("on/off", 126, 215, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb__event)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna__event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc__event)

    can_0 = CANUnit((13, 15), CANUnit.NORMAL, baudrate=1000000)
    rollercan_0 = RollerCANUnit(can_0, address=0xA8, mode=RollerCANUnit.CAN_TO_I2C_MODE)
    env3_0 = ENVUnit(i2c=rollercan_0, type=3)
    rollercan_0.set_motor_output_state(0)
    output = 0
    mode = rollercan_0.get_motor_mode()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))

def loop():
    global \
        title0, \
        label5, \
        label7, \
        label0, \
        label6, \
        label1, \
        label2, \
        label3, \
        label4, \
        env3_0, \
        can_0, \
        rollercan_0, \
        output, \
        mode
    M5.update()
    label0.setText(str((str("mode:") + str(mode))))
    label1.setText(str((str("motor state:") + str(output))))
    if mode == 1:
        rollercan_0.set_motor_speed(20000)
        rollercan_0.set_speed_max_current(400)
        label2.setText(str((str("speed:") + str((rollercan_0.get_motor_speed_readback())))))
    elif mode == 2:
        rollercan_0.set_motor_position(1000)
        rollercan_0.set_position_max_current(400)
        label2.setText(str((str("position:") + str((rollercan_0.get_motor_position_readback())))))
    elif mode == 3:
        rollercan_0.set_motor_max_current(400)
        label2.setText(str((str("current:") + str((rollercan_0.get_motor_current_readback())))))
    elif mode == 4:
        label2.setText(str((str("encoder:") + str((rollercan_0.get_encoder_value())))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## class RollerCANUnit

## Constructors

### `class RollerCANUnit(bus, address, mode)`

    Initialize the RollerCANUnit object based on communication mode.

    - Parameter `bus`: The I2C/CAN bus instance.
    - Parameter `address`: The motor's CAN address. Defaults to _ROLLERCAN_CAN_ADDR.
    - Parameter `mode`: The RollerCAN communication mode.

## class RollerBase

## Constructors

### `class RollerBase()`

## Methods

### `RollerBase.set_motor_output_state(ctrl) -> None`

    Set the motor output state.

    - Parameter `ctrl` (`int`): Control value for the motor output.

### `RollerBase.get_motor_output_state() -> bool`

    Get the motor output status.

    - Returns: True if the motor output is active, False otherwise.

### `RollerBase.set_motor_mode(mode) -> None`

    Set the motor mode.

    - Parameter `mode` (`int`): The mode to set for the motor.

### `RollerBase.get_motor_mode() -> int`

    Get the motor mode.

    - Returns: The current motor mode.

### `RollerBase.set_motor_over_range_protect_state(state) -> None`

    Set the motor over range protection state.

    - Parameter `state` (`int`): Protection state value (1 to enable, 0 to disable).

### `RollerBase.get_motor_over_range_protect_state() -> bool`

    Get the motor over range protection status.

    - Returns: True if protection is enabled, False otherwise.

### `RollerBase.remove_motor_jam_protect() -> None`

    Set the motor jam release protection.

### `RollerBase.get_motor_status() -> int`

    Get the motor status.

    - Returns: The current status of the motor.

### `RollerBase.get_motor_error_code() -> int`

    Get the motor error code.

    - Returns: The current error code of the motor.

### `RollerBase.set_button_change_mode(state) -> None`

    Set the button change mode.

    - Parameter `state` (`int`): Change mode state value (1 to enable, 0 to disable).

### `RollerBase.get_button_change_mode() -> int`

    Get the button change mode.

    - Returns: The current button change mode value.

### `RollerBase.set_motor_jam_protect_state(state) -> None`

    Set the motor jam protection enable/disable.

    - Parameter `state` (`int`): Protection state value (1 to enable, 0 to disable).

### `RollerBase.get_motor_jam_protect_state() -> bool`

    Get the motor jam protection status.

    - Returns: True if jam protection is enabled, False otherwise.

### `RollerBase.set_motor_id(id) -> None`

    Set the motor ID.

    - Parameter `id` (`int`): The ID to assign to the motor.

### `RollerBase.get_motor_id() -> int`

    Get the motor ID.

    - Returns: The current motor ID.

### `RollerBase.set_can_baudrate(bps) -> None`

    Set the can baudrate.

    - Parameter `bps` (`int`): Baud rate value.

### `RollerBase.get_can_baudrate() -> int`

    Get the can baudrate.

    - Returns: The current can baudrate.

### `RollerBase.set_rgb_brightness(bright) -> None`

    Set RGB brightness.

    - Parameter `bright` (`int`): Brightness value.

### `RollerBase.get_rgb_brightness() -> int`

    Get RGB brightness.

    - Returns: The current RGB brightness value.

### `RollerBase.set_motor_speed(speed) -> None`

    Set the motor speed and max current setting.

    - Parameter `speed` (`int`): The speed value to set.

### `RollerBase.get_motor_speed() -> int`

    Get the motor speed and max current setting.

    - Returns: The current motor speed.

### `RollerBase.set_speed_max_current(current) -> None`

    Set the motor speed and max current setting.

    - Parameter `current` (`int`): The max current value to set.

### `RollerBase.get_speed_max_current() -> int`

    Get the motor speed and max current setting.

    - Returns: The current max current setting.

### `RollerBase.get_motor_speed_readback() -> float`

    Get the motor speed readback.

    - Returns: The readback value of the motor speed.

### `RollerBase.set_motor_speed_pid(p, i, d) -> None`

    Set the motor speed PID.

    - Parameter `p` (`float`): Proportional gain.
    - Parameter `i` (`float`): Integral gain.
    - Parameter `d` (`float`): Derivative gain.

### `RollerBase.get_motor_speed_pid() -> tuple`

    Get the motor speed PID.

    - Returns: A tuple containing the PID values.

### `RollerBase.set_motor_position(position) -> None`

    Set the motor position and max current setting.

    - Parameter `position` (`int`): The position value to set.

### `RollerBase.get_motor_position() -> int`

    Get the motor position and max current setting.

    - Returns: The current motor position.

### `RollerBase.set_position_max_current(current) -> None`

    Set the motor position and max current setting.

    - Parameter `current` (`int`): The max current value to set.

### `RollerBase.get_position_max_current() -> int`

    Get the motor position and max current setting.

    - Returns: The current max current setting.

### `RollerBase.get_motor_position_readback() -> float`

    Get the motor position readback.

    - Returns: The readback value of the motor position.

### `RollerBase.get_motor_position_pid() -> tuple`

    Get the motor position PID.

    - Returns: A tuple containing the PID values for position.

### `RollerBase.set_motor_position_pid(p, i, d) -> None`

    Set the motor position PID.

    - Parameter `p` (`float`): Proportional gain.
    - Parameter `i` (`float`): Integral gain.
    - Parameter `d` (`float`): Derivative gain.

### `RollerBase.set_motor_max_current(current) -> None`

    Set the motor max current.

    - Parameter `current` (`int`): The maximum current for the motor, multiplied by 100 before sending.

### `RollerBase.get_motor_max_current() -> int`

    Get the motor max current.

    - Returns: The motor max current, divided by 100 after reading.

### `RollerBase.get_motor_current_readback() -> float`

    Get the motor current readback.

    - Returns: The motor current readback value, divided by 100 after reading.

### `RollerBase.set_rgb_color(rgb) -> None`

    Set the system RGB color.

    - Parameter `rgb` (`int`): The RGB color value, where the format is 0xRRGGBB.

### `RollerBase.get_rgb_color() -> tuple`

    Get the system RGB color.

    - Returns: The RGB color as a tuple (R, G, B).

### `RollerBase.set_rgb_mode(mode) -> None`

    Set the system RGB mode.

    - Parameter `mode` (`int`): The RGB mode value.

### `RollerBase.get_rgb_mode() -> int`

    Get the system RGB mode.

    - Returns: The current RGB mode value.

### `RollerBase.get_vin_voltage() -> int`

    Get the system VIN voltage.

    - Returns: The system VIN voltage value, multiplied by 10 after reading.

### `RollerBase.get_temperature_value() -> int`

    Get the system temperature.

    - Returns: The current system temperature value.

### `RollerBase.set_encoder_value(count) -> None`

    Set the system encoder value.

    - Parameter `count` (`int`): The encoder count value.

### `RollerBase.get_encoder_value() -> int`

    Get the system encoder value.

    - Returns: The current encoder value.

### `RollerBase.save_param_to_flash() -> None`

    Save the motor data to flash.

### `RollerBase.get_firmware_version() -> int`

    Get the device firmware version.

    - Returns: The current firmware version.

### `RollerBase.set_i2c_address(addr) -> None`

    Set the I2C address.

    - Parameter `addr` (`int`): The new I2C address. Must be between 0x08 and 0x77.

### `RollerBase.get_i2c_address() -> int`

    Get the current I2C address.

    - Returns: The current I2C address.

## class RollerI2C(RollerBase)

## Constructors

### `class RollerI2C(i2c, address)`

    Initialize the RollerI2C object.

    - Parameter `i2c` (`I2C|PAHUBUnit`): I2C bus instance or PAHUBUnit instance.
    - Parameter `address` (`int`): I2C address of the device. Defaults to _ROLLER485_I2C_ADDR.

## Methods

### `RollerI2C.read(register, length) -> bytes`

    Read data from a specified register on the I2C device.

    - Parameter `register`: The name of the register to read from.
    - Parameter `length`: The number of bytes to read.
    - Returns: The data read from the device as a bytes object.

### `RollerI2C.write(register, bytes) -> None`

    Write data to a specified register on the I2C device.

    - Parameter `register`: The name of the register to write to.
    - Parameter `bytes`: The data to write to the register as a bytes object.

## class RollerCAN(RollerBase)

## Constructors

### `class RollerCAN(bus, address, mode)`

    Initialize the RollerCAN object.

    - Parameter `bus`: The CAN bus instance.
    - Parameter `address`: The motor's CAN address. Defaults to _ROLLERCAN_CAN_ADDR.
    - Parameter `mode`: Optional mode for setting specific operational mode.

## Methods

### `RollerCAN.create_frame(register, option, data, is_read)`

    Create a CAN frame for sending commands.

    - Parameter `register`: The register for command identification.
    - Parameter `option`: Command option to specify the data.
    - Parameter `data`: Data payload for the frame.
    - Parameter `is_read`: Whether this frame is for a read command.

### `RollerCAN.read(register, length)`

    Send a read command to a specific register.

    - Parameter `register`: The register address to read from.
    - Parameter `length`: Length of data to read.

### `RollerCAN.i2c_read(register, length)`

    Read data from an I2C slave via CAN.

    - Parameter `register`: The I2C register address to read from.
    - Parameter `length`: Number of bytes to read.

### `RollerCAN.i2c_write(register, data, stop)`

    Write data to an I2C slave via CAN.

    - Parameter `register`: The I2C register address to write to.
    - Parameter `data`: The data to write.
    - Parameter `stop`: Whether to end the transaction with a stop condition.

### `RollerCAN.write(register, data)`

    Write data to a specific register.

    - Parameter `register`: The register address to write to.
    - Parameter `data`: Data payload to send to the register.

### `RollerCAN.read_response()`

    Read the response data from the CAN bus.

## class RollerCANToI2CBus(RollerBase)

## Constructors

### `class RollerCANToI2CBus(bus, address, mode)`

    Initialize RollerCANToI2CBus object with CAN bus and address.

    - Parameter `bus`: The CAN bus instance.
    - Parameter `address`: The I2C device address, default is _ROLLERCAN_I2C_ADDR.
    - Parameter `mode`: Optional mode for setting specific operational mode.

## Methods

### `RollerCANToI2CBus.readfrom_mem(addr, mem_addr, nbytes) -> bytes`

    Read data from an I2C memory register.

    - Parameter `addr` (`int`): I2C device address.
    - Parameter `mem_addr` (`int`): Memory register address.
    - Parameter `nbytes` (`int`): Number of bytes to read.

### `RollerCANToI2CBus.readfrom_mem_into(addr, mem_addr, buf) -> None`

    Read data from an I2C memory register and store it in the provided buffer.

    - Parameter `addr` (`int`): I2C device address.
    - Parameter `mem_addr` (`int`): Memory register address.
    - Parameter `buf` (`bytearray`): Buffer to store the data.

### `RollerCANToI2CBus.writeto_mem(addr, mem_addr, buf)`

    Write data to an I2C memory register.

    - Parameter `addr` (`int`): I2C device address.
    - Parameter `mem_addr` (`int`): Memory register address.
    - Parameter `buf` (`bytearray`): Data to write.

### `RollerCANToI2CBus.readfrom(addr, nbytes) -> bytes`

    Read data from an I2C device.

    - Parameter `addr` (`int`): I2C device address.
    - Parameter `nbytes` (`int`): Number of bytes to read.

### `RollerCANToI2CBus.readfrom_into(addr, buf) -> None`

    Read data from an I2C device and store it in the provided buffer.

    - Parameter `addr` (`int`): I2C device address.
    - Parameter `buf` (`bytearray`): Buffer to store the data.

### `RollerCANToI2CBus.writeto(addr, buf, stop)`

    Write data to an I2C device in chunks.

    - Parameter `addr` (`int`): I2C device address.
    - Parameter `buf` (`bytes|bytearray`): Data to write.
    - Parameter `stop` (`bool`): Whether to end the transaction with a stop condition.

### `RollerCANToI2CBus.scan() -> list`

    Scan for I2C devices on the bus.
