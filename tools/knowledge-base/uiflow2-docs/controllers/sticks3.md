#######
###### StickS3

<!-- .. include:: ../refs/controllers.sticks3.ref -->

Support the following products:

    |StickS3|

## UiFlow2 Example

#### Button Control

Open the |sticks3_button_example.m5f2| project in UiFlow2.

This example demonstrates button callback functions. When button A (BtnA) is clicked, it increments a counter and updates the display. When button B (BtnB) is clicked, it also increments a counter and updates the display.

UiFlow2 Code Block:

Example output:

    None

#### IMU Sensor

Open the |sticks3_imu_example.m5f2| project in UiFlow2.

This example demonstrates the built-in IMU (Inertial Measurement Unit) sensor functionality. It reads and displays accelerometer and gyroscope data in real-time, showing acceleration values in m/s² and gyroscope values in degrees per second (dps).

UiFlow2 Code Block:

Example output:

    None

#### Power Management

Open the |sticks3_power_example.m5f2| project in UiFlow2.

This example demonstrates power management features including battery voltage monitoring, VBUS voltage reading, charging status detection, and control of battery charging and external output. Press BtnA to toggle external output (5V OUT), and press BtnB to toggle battery charging.

UiFlow2 Code Block:

Example output:

    None

#### IR Transmission

Open the |sticks3_ir_tx_example.m5f2| project in UiFlow2.

This example demonstrates infrared (IR) transmission functionality. When button A is pressed, it sends IR data with a specified address and data value. The example displays the address and data being transmitted.

<!-- .. NOTE:: -->
   When using IR transmission, the external output mode should be enabled.

UiFlow2 Code Block:

Example output:

    None

#### IR Reception

Open the |sticks3_ir_rx_example.m5f2| project in UiFlow2.

This example demonstrates infrared (IR) reception functionality using NEC decode protocol. When IR data is received, it displays the address and data values on the screen.

<!-- .. NOTE:: -->
   When using IR reception, the PA (Power Amplifier) should be turned off and the external output mode should be enabled.

UiFlow2 Code Block:

Example output:

    None

#### Audio Recording and Playback

Open the |sticks3_audio_example.m5f2| project in UiFlow2.

This example demonstrates audio recording and playback functionality. Press button A to start recording for 5 seconds. After recording completes, the audio will automatically play back. The example displays the recording status and countdown timer.

UiFlow2 Code Block:

Example output:

    None

#### HAT ToF Sensor

Open the |sticks3_hat_tof_example.m5f2| project in UiFlow2.

This example demonstrates how to use the ToF (Time of Flight) HAT sensor to measure distance. The example reads distance values from the sensor and displays them on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Button Control

This example demonstrates button callback functions. When button A (BtnA) is clicked, it increments a counter and updates the display. When button B (BtnB) is clicked, it also increments a counter and updates the display.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *

label_title = None
label_btna_cnt = None
label_btnb_cnt = None
label_tip = None
btna_cnt = None
btnb_cnt = None

def btna_click_event_cb(state):
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    btna_cnt = (btna_cnt if isinstance(btna_cnt, (int, float)) else 0) + 1
    label_btna_cnt.setText(str((str("BtnA: ") + str(btna_cnt))))
    print("button a press")

def btnb_click_event_cb(state):
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    btnb_cnt = (btnb_cnt if isinstance(btnb_cnt, (int, float)) else 0) + 1
    label_btnb_cnt.setText(str((str("BtnB: ") + str(btnb_cnt))))
    print("button b press")

def setup():
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Button", 35, 5, 1.0, 0x1A94DD, 0x000000, Widgets.FONTS.DejaVu18)
    label_btna_cnt = Widgets.Label(
        "BtnA: ", 5, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_btnb_cnt = Widgets.Label("BtnB:", 5, 80, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "Press button", 7, 200, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_click_event_cb)
    btna_cnt = 0
    btnb_cnt = 0

def loop():
    global label_title, label_btna_cnt, label_btnb_cnt, label_tip, btna_cnt, btnb_cnt
    M5.update()

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

Example output:

    None

#### IMU Sensor

This example demonstrates the built-in IMU (Inertial Measurement Unit) sensor functionality. It reads and displays accelerometer and gyroscope data in real-time, showing acceleration values in m/s² and gyroscope values in degrees per second (dps).

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import time

label_imu = None
label_accel = None
label_gyro = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_y = None
label_gyro_z = None
label_gyro_x = None
last_time = None
accel = None
gyro = None

def setup():
    global \
        label_imu, \
        label_accel, \
        label_gyro, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_x, \
        last_time, \
        accel, \
        gyro
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_imu = Widgets.Label("IMU", 46, 4, 1.0, 0x1BCDCD, 0x000000, Widgets.FONTS.DejaVu18)
    label_accel = Widgets.Label(
        "Accel(m/^2)", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_gyro = Widgets.Label(
        "Gyro(dps)", 17, 138, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_acc_x = Widgets.Label("X:", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_acc_y = Widgets.Label("Y:", 5, 85, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_acc_z = Widgets.Label("Z:", 5, 110, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_gyro_y = Widgets.Label("Y:", 5, 187, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_gyro_z = Widgets.Label("Z:", 5, 213, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_gyro_x = Widgets.Label("X:", 5, 163, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

def loop():
    global \
        label_imu, \
        label_accel, \
        label_gyro, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_x, \
        last_time, \
        accel, \
        gyro
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        accel = Imu.getAccel()
        gyro = Imu.getGyro()
        label_acc_x.setText(str((str("X: ") + str((accel[0] * 9.8)))))
        label_acc_y.setText(str((str("Y: ") + str((accel[1] * 9.8)))))
        label_acc_z.setText(str((str("Z: ") + str((accel[2] * 9.8)))))
        label_gyro_x.setText(str((str("X: ") + str((gyro[0])))))
        label_gyro_y.setText(str((str("Y: ") + str((gyro[1])))))
        label_gyro_z.setText(str((str("Z: ") + str((gyro[2])))))

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

Example output:

    None

#### Power Management

This example demonstrates power management features including battery voltage monitoring, VBUS voltage reading, charging status detection, and control of battery charging and external output. Press BtnA to toggle external output (5V OUT), and press BtnB to toggle battery charging.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time

label_title = None
label_5vout = None
label_usb = None
label_bat = None
label_tip = None
label_state = None
label_vout = None
vout_flag = None
charge = None
last_time = None
usb_vol = None
bat_vol = None
vout_vol = None
vout_state = None

def btna_click_event_cb(state):
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    vout_flag = not vout_flag
    if vout_flag:
        Power.setExtOutput(True)
        print("turn on the output")
    else:
        Power.setExtOutput(False)
        print("turn off the output")

def btnb_click_event_cb(state):
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    charge = not charge
    if charge:
        print("set charge")
        Power.setBatteryCharge(True)
    else:
        print("no charge")
        Power.setBatteryCharge(False)

def setup():
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Power", 36, 5, 1.0, 0x13BDDE, 0x000000, Widgets.FONTS.DejaVu18)
    label_5vout = Widgets.Label(
        "OUT:----mV", 5, 85, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_usb = Widgets.Label("USB:----mV", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_bat = Widgets.Label("Bat:----mV", 5, 60, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "BtnA Control", 5, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_state = Widgets.Label("ON", 31, 152, 1.0, 0x00FF00, 0x000000, Widgets.FONTS.DejaVu40)
    label_vout = Widgets.Label("5V OUT", 28, 125, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_click_event_cb)

    Power.setBatteryCharge(True)
    Power.setExtOutput(False)
    charge = True
    label_bat.setColor(0x33CC00, 0x000000)

def loop():
    global \
        label_title, \
        label_5vout, \
        label_usb, \
        label_bat, \
        label_tip, \
        label_state, \
        label_vout, \
        vout_flag, \
        charge, \
        last_time, \
        usb_vol, \
        bat_vol, \
        vout_vol, \
        vout_state
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        usb_vol = Power.getVBUSVoltage()
        bat_vol = Power.getBatteryVoltage()
        vout_vol = Power.getExtVoltage(M5.Power.PORT.A)
        vout_state = Power.getExtOutput()
        if Power.isCharging():
            label_bat.setColor(0x33CC00, 0x000000)
        else:
            label_bat.setColor(0xFFFFFF, 0x000000)
        if vout_state:
            label_state.setCursor(x=32, y=152)
            label_state.setText(str("ON"))
            label_state.setColor(0x33CC00, 0x000000)
        else:
            label_state.setCursor(x=24, y=152)
            label_state.setText(str("OFF"))
            label_state.setColor(0x666666, 0x000000)
        label_usb.setText(str((str("USB:") + str((str(usb_vol) + str("mV"))))))
        label_bat.setText(str((str("Bat:") + str((str(bat_vol) + str("mV"))))))
        label_5vout.setText(str((str("Out:") + str((str((int(vout_vol))) + str("mV"))))))

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

Example output:

    None

#### IR Transmission

This example demonstrates infrared (IR) transmission functionality. When button A is pressed, it sends IR data with a specified address and data value. The example displays the address and data being transmitted.

<!-- .. NOTE:: -->
   When using IR transmission, the external output mode should be enabled.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR

label_title = None
label_addr = None
label_data = None
label_tip = None
ir = None
data = None
addr = None

def btna_click_event_cb(state):
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    data = (data if isinstance(data, (int, float)) else 0) + 1
    ir.tx(addr, data)
    print((str("IR: Send addr: ") + str((str(addr) + str((str(" data: ") + str(data)))))))
    label_data.setText(str((str("data: ") + str(data))))

def setup():
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("IR", 58, 5, 1.0, 0x1AEAEB, 0x000000, Widgets.FONTS.DejaVu18)
    label_addr = Widgets.Label("addr:", 5, 45, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data:", 5, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "BtnA Send", 18, 200, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)
    ir = IR()
    ir.rx_cb(ir_rx_event)
    addr = 56
    data = 0
    Power.setExtOutput(True)
    label_addr.setText(str((str("addr: ") + str(addr))))

def loop():
    global label_title, label_addr, label_data, label_tip, ir, data, addr
    M5.update()

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

Example output:

    None

#### IR Reception

This example demonstrates infrared (IR) reception functionality using NEC decode protocol. When IR data is received, it displays the address and data values on the screen in real-time.

<!-- .. NOTE:: -->
   When using IR reception, the PA (Power Amplifier) should be turned off and the external output mode should be enabled.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR

label_title = None
label0 = None
label_addr = None
label_data = None
ir = None
data = None
addr = None

def ir_rx_event(_data, _addr, _ctrl):
    global label_title, label0, label_addr, label_data, ir, data, addr
    data = _data
    addr = _addr
    label_addr.setText(str((str("addr: ") + str(addr))))
    label_data.setText(str((str("data: ") + str(data))))

def setup():
    global label_title, label0, label_addr, label_data, ir, data, addr

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("IR RX", 41, 5, 1.0, 0x0FBAE1, 0x000000, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("NEC Decode", 8, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_addr = Widgets.Label("addr:", 5, 115, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_data = Widgets.Label("data:", 5, 145, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    Speaker.setPA(False)
    ir = IR()
    ir.rx_cb(ir_rx_event)

def loop():
    global label_title, label0, label_addr, label_data, ir, data, addr
    M5.update()

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

Example output:

    None

#### Audio Recording and Playback

This example demonstrates audio recording and playback functionality. Press button A to start recording for 5 seconds.
After recording completes, the audio will automatically play back. The example displays the recording status and countdown timer.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from audio import Recorder
import time
from audio import Player

label_title = None
label_tip = None
label_cnt = None
label_conut = None
label_status = None
recorder = None
player = None
flag_record = None
record_start_time = None
remaining = None
RECORD_DURATION = None
record_file_path = None

def btna_click_event_cb(state):
    global \
        label_title, \
        label_tip, \
        label_cnt, \
        label_conut, \
        label_status, \
        recorder, \
        player, \
        flag_record, \
        record_start_time, \
        remaining, \
        RECORD_DURATION, \
        record_file_path
    if not flag_record and not (recorder.is_recording()):
        print("start record")
        flag_record = True
        record_start_time = time.ticks_ms()
        label_status.setCursor(x=9, y=50)
        label_status.setText(str("Recording..."))
        label_status.setColor(0xFF0000, 0x000000)
        recorder.record("file://flash/res/audio/" + str(record_file_path), RECORD_DURATION, False)

def setup():
    global \
        label_title, \
        label_tip, \
        label_cnt, \
        label_conut, \
        label_status, \
        recorder, \
        player, \
        flag_record, \
        record_start_time, \
        remaining, \
        RECORD_DURATION, \
        record_file_path

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Audio", 39, 5, 1.0, 0x19B1D7, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip = Widgets.Label(
        "BtnA Record", 8, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_cnt = Widgets.Label(
        "count down", 11, 88, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_conut = Widgets.Label("5", 48, 118, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu56)
    label_status = Widgets.Label("Stop", 45, 50, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)

    Mic.end()
    Speaker.end()
    Speaker.setPA(True)
    recorder = Recorder(8000, 16, True)
    player = Player(None)
    RECORD_DURATION = 5
    record_file_path = "test.amr"
    player.set_vol(90)

def loop():
    global \
        label_title, \
        label_tip, \
        label_cnt, \
        label_conut, \
        label_status, \
        recorder, \
        player, \
        flag_record, \
        record_start_time, \
        remaining, \
        RECORD_DURATION, \
        record_file_path
    M5.update()
    if flag_record:
        if recorder.is_recording():
            remaining = (
                RECORD_DURATION - (time.ticks_diff((time.ticks_ms()), record_start_time)) / 1000
            )
            if remaining > 0:
                label_conut.setText(str(int(remaining)))
            else:
                label_conut.setText(str(0))
        else:
            flag_record = False
            label_conut.setText(str(""))
            label_cnt.setText(str(""))
            label_status.setColor(0x33CC00, 0x000000)
            label_status.setCursor(x=22, y=50)
            label_status.setText(str("Playing..."))
            player.play(
                "file://flash/res/audio/" + str(record_file_path), pos=0, volume=-1, sync=True
            )
            label_status.setColor(0xFFFFFF, 0x000000)
            label_status.setCursor(x=45, y=50)
            label_status.setText(str("Stop"))
            label_cnt.setText(str("count down"))
            label_conut.setText(str(5))

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

Example output:

    None

#### HAT ToF Sensor

This example demonstrates how to use the ToF (Time of Flight) HAT sensor to measure distance. The example reads distance values from the sensor and displays them on the screen in real-time.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from hat import ToFHat
import time

label_title = None
label_distance = None
label_dis = None
label_cm = None
i2c0 = None
hat_tof_0 = None
last_time = None
dis = None

def setup():
    global label_title, label_distance, label_dis, label_cm, i2c0, hat_tof_0, last_time, dis

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("HAT ToF", 27, 5, 1.0, 0x1F70D7, 0x000000, Widgets.FONTS.DejaVu18)
    label_distance = Widgets.Label(
        "Distance", 27, 55, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_dis = Widgets.Label("---", 35, 90, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu56)
    label_cm = Widgets.Label("cm", 53, 155, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    i2c0 = I2C(0, scl=Pin(0), sda=Pin(8), freq=100000)
    hat_tof_0 = ToFHat(i2c0)
    dis = 0
    Power.setBatteryCharge(True)
    Power.setExtOutput(True)

def loop():
    global label_title, label_distance, label_dis, label_cm, i2c0, hat_tof_0, last_time, dis
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 200:
        last_time = time.ticks_ms()
        dis = int(hat_tof_0.get_distance())
        if dis < 10:
            label_dis.setCursor(x=48, y=90)
        elif dis < 100:
            label_dis.setCursor(x=33, y=90)
        else:
            label_dis.setCursor(x=12, y=90)
        label_dis.setText(str(dis))
        print((str("Distance: ") + str((str(dis) + str(" cm")))))

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

Example output:

    None
