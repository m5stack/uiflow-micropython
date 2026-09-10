# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
from M5 import *
from chain import ChainBus
from chain import Servos8V2Chain
import time


title = None
label_angle = None
label_timer = None
label_power = None
label_state = None
bus2 = None
servos8v2_0 = None
last_move = 0
position = 0

ANGLES = (45, 135)


def require_ok(result, action):
    if not result:
        raise RuntimeError(action + " failed")


def setup():
    global title, label_angle, label_timer, label_power, label_state
    global bus2, servos8v2_0, last_move

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title("Chain 8Servos2 Servo", 3, 0xFFFFFF, 0x0055AA, Widgets.FONTS.DejaVu18)
    label_angle = Widgets.Label(
        "All channels: 90 deg", 10, 58, 1.0, 0x17E6CF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_timer = Widgets.Label(
        "Servo PWM: 50 Hz", 10, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_power = Widgets.Label(
        "Use external servo power", 10, 138, 1.0, 0xFFD166, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_state = Widgets.Label(
        "Sweeps 45 <-> 135 deg", 10, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    servos8v2_0 = Servos8V2Chain(bus2, 1)
    for channel in range(8):
        require_ok(
            servos8v2_0.set_channel_mode(channel, Servos8V2Chain.MODE_SERVO),
            "set IO%d servo mode" % channel,
        )
    for channel in range(8):
        require_ok(servos8v2_0.set_servo_angle(channel, 90), "center servo %d" % channel)
    modes = tuple(servos8v2_0.get_channel_mode(channel) for channel in range(8))
    freqs = (
        servos8v2_0.get_pwm_freq(0),
        servos8v2_0.get_pwm_freq(4),
    )
    label_timer.setText("PWM groups: %d / %d Hz" % freqs)
    label_state.setText("Mode: %s" % ("OK" if modes == (3,) * 8 else str(modes)))
    last_move = time.ticks_ms()
    print("Chain 8Servos2: modes =", modes, "PWM groups =", freqs)
    print("Chain 8Servos2: all channels centered at 90 degrees")


def loop():
    global last_move, position

    M5.update()
    if time.ticks_diff(time.ticks_ms(), last_move) < 1500:
        return
    last_move = time.ticks_ms()
    angle = ANGLES[position]
    position = (position + 1) % len(ANGLES)
    for channel in range(8):
        require_ok(servos8v2_0.set_servo_angle(channel, angle), "set servo %d angle" % channel)
    label_angle.setText("All channels: %d deg" % angle)
    print("Servo angle:", angle)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            if bus2 is not None:
                bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
