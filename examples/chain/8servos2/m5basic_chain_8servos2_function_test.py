# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from chain import ChainBus
from chain import Servos8V2Chain


BG = 0x222222
HEADER = 0x0055AA
WHITE = 0xFFFFFF
GRAY = 0x666666
RED = 0xFF3030
YELLOW = 0xFFD166
CYAN = 0x17E6CF

PAGE_GPIO_INPUT = 0
PAGE_GPIO_OUTPUT = 1
PAGE_ADC = 2
PAGE_PWM = 3
PAGE_RGB = 4
PAGE_SERVO = 5
PAGE_POWER = 6
PAGE_COUNT = 7

PWM_FREQS = (1, 16384, 32768, 49152, 65535)
PULL_NAMES = ("NONE", "UP", "DOWN")
RGB_COLORS = (0xFF0000, 0x00FF00, 0x0000FF, 0xFFFFFF, 0x000000)
RGB_NAMES = ("RED", "GREEN", "BLUE", "WHITE", "OFF")

bus2 = None
device = None
page = PAGE_GPIO_INPUT
input_pull_index = 0
output_channel = 0
output_levels = [False] * 8
pwm_freq_index = 0
pwm_duty = 0
rgb_channel = 0
rgb_color_index = 0
servo_channel = 0
servo_angle = 0
servo_direction = 1
last_refresh = 0
last_servo_move = 0

title_label = None
method_label = None
info_left_label = None
info_right_label = None
keys_label = None
channel_rects = []
channel_labels = []
channel_states = [None] * 8
adc_name_labels = []
adc_value_labels = []
pwm_labels = []
rgb_status_label = None
servo_status_label = None
power_name_labels = []
power_value_labels = []


def require_ok(result, action):
    if not result:
        raise RuntimeError(action + " failed")


def require_value(value, action):
    if value is None:
        raise RuntimeError(action + " failed")
    return value


def set_mode(channel, mode):
    require_ok(device.set_channel_mode(channel, mode), "set IO%d mode" % channel)


def set_output(channel, value):
    require_ok(device.set_gpio_output_value(channel, value), "set IO%d output" % channel)


def set_pwm_frequency(channel, freq):
    require_ok(device.set_pwm_freq(channel, freq), "set IO%d PWM frequency" % channel)


def set_pwm_output(channel, duty):
    require_ok(device.set_pwm_duty(channel, duty), "set IO%d PWM duty" % channel)


def set_rgb_config(channel, count, refresh=False):
    require_ok(device.set_rgb_config(channel, count, refresh), "set IO%d RGB config" % channel)


def set_rgb_color(index, color):
    require_ok(device.set_rgb_buffer(index, color), "set RGB%d color" % index)


def set_servo(channel, angle):
    require_ok(device.set_servo_angle(channel, angle), "set IO%d servo angle" % channel)


def create_ui():
    global title_label, method_label, info_left_label, info_right_label, keys_label
    global channel_rects, channel_labels, adc_name_labels, adc_value_labels
    global pwm_labels, rgb_status_label, servo_status_label
    global power_name_labels, power_value_labels

    Widgets.Rectangle(0, 0, 320, 28, HEADER, HEADER)
    Widgets.Rectangle(0, 214, 320, 26, HEADER, HEADER)
    title_label = Widgets.Label("", 8, 4, 1.0, WHITE, HEADER, Widgets.FONTS.DejaVu18)
    method_label = Widgets.Label("", 8, 34, 1.0, CYAN, BG, Widgets.FONTS.DejaVu12)
    info_left_label = Widgets.Label("", 8, 54, 1.0, YELLOW, BG, Widgets.FONTS.DejaVu12)
    info_right_label = Widgets.Label("", 122, 54, 1.0, YELLOW, BG, Widgets.FONTS.DejaVu12)
    keys_label = Widgets.Label("", 8, 220, 1.0, WHITE, HEADER, Widgets.FONTS.DejaVu12)

    channel_rects = []
    channel_labels = []
    for channel in range(8):
        x = 8 + (channel % 4) * 78
        y = 76 + (channel // 4) * 62
        channel_rects.append(Widgets.Rectangle(x, y, 70, 52, WHITE, GRAY))
        channel_labels.append(
            Widgets.Label(str(channel), x + 29, y + 15, 1.0, WHITE, GRAY, Widgets.FONTS.DejaVu18)
        )

    adc_name_labels = []
    adc_value_labels = []
    for channel in range(8):
        x = 14 + (channel // 4) * 158
        y = 76 + (channel % 4) * 32
        adc_name_labels.append(
            Widgets.Label("IO%d" % channel, x, y, 1.0, CYAN, BG, Widgets.FONTS.DejaVu18)
        )
        adc_value_labels.append(
            Widgets.Label("   0", x + 55, y, 1.0, WHITE, BG, Widgets.FONTS.DejaVu18)
        )

    pwm_labels = (
        Widgets.Label("Frequency", 26, 82, 1.0, CYAN, BG, Widgets.FONTS.DejaVu18),
        Widgets.Label("    1 Hz", 170, 82, 1.0, WHITE, BG, Widgets.FONTS.DejaVu18),
        Widgets.Label("Duty", 26, 122, 1.0, CYAN, BG, Widgets.FONTS.DejaVu18),
        Widgets.Label("  0 %", 170, 122, 1.0, WHITE, BG, Widgets.FONTS.DejaVu18),
        Widgets.Label(
            "IO0-3 and IO4-7 share frequency", 26, 166, 1.0, YELLOW, BG, Widgets.FONTS.DejaVu12
        ),
        Widgets.Label(
            "Measure PWM output on any channel", 26, 188, 1.0, WHITE, BG, Widgets.FONTS.DejaVu12
        ),
    )
    rgb_status_label = Widgets.Label(
        "Selected IO0  Color: RED", 62, 198, 1.0, YELLOW, BG, Widgets.FONTS.DejaVu12
    )
    servo_status_label = Widgets.Label(
        "Selected IO0  Angle:  0", 70, 198, 1.0, YELLOW, BG, Widgets.FONTS.DejaVu12
    )
    power_names = ("Reference", "Grove", "DC input", "Current")
    power_name_labels = []
    power_value_labels = []
    for index, name in enumerate(power_names):
        y = 80 + index * 32
        power_name_labels.append(Widgets.Label(name, 28, y, 1.0, CYAN, BG, Widgets.FONTS.DejaVu18))
        power_value_labels.append(
            Widgets.Label("0", 180, y, 1.0, WHITE, BG, Widgets.FONTS.DejaVu18)
        )
    hide_content()


def hide_content():
    for widget in channel_labels:
        widget.setVisible(False)
    for widget in channel_rects:
        widget.setVisible(False)
    for widget in adc_name_labels:
        widget.setVisible(False)
    for widget in adc_value_labels:
        widget.setVisible(False)
    for widget in pwm_labels:
        widget.setVisible(False)
    rgb_status_label.setVisible(False)
    servo_status_label.setVisible(False)
    for widget in power_name_labels:
        widget.setVisible(False)
    for widget in power_value_labels:
        widget.setVisible(False)


def show_header(title, method, keys, info_left="", info_right=""):
    title_label.setText(title)
    method_label.setText("Test: " + method)
    keys_label.setText(keys)
    info_left_label.setText(info_left)
    info_right_label.setText(info_right)
    info_left_label.setVisible(bool(info_left))
    info_right_label.setVisible(bool(info_right))


def show_channel_boxes():
    global channel_states

    channel_states = [None] * 8
    for channel in range(8):
        channel_rects[channel].setVisible(True)
        channel_labels[channel].setVisible(True)


def update_channel_box(channel, value, selected=False):
    state = (bool(value), bool(selected))
    if channel_states[channel] == state:
        return
    channel_states[channel] = state
    fill = RED if value else GRAY
    border = YELLOW if selected else WHITE
    channel_rects[channel].setColor(color=border, fill_c=fill)
    channel_labels[channel].setColor(WHITE, fill)


def update_gpio_input():
    for channel in range(8):
        value = require_value(device.get_gpio_input_value(channel), "read IO%d input" % channel)
        update_channel_box(channel, value)


def update_gpio_output():
    for channel in range(8):
        update_channel_box(channel, output_levels[channel], channel == output_channel)


def show_adc():
    for widget in adc_name_labels:
        widget.setVisible(True)
    for widget in adc_value_labels:
        widget.setVisible(True)
    update_adc()


def update_adc():
    for channel in range(8):
        value = require_value(device.get_adc_input(channel), "read IO%d ADC" % channel)
        adc_value_labels[channel].setText("%4d" % value)


def show_pwm():
    for widget in pwm_labels:
        widget.setVisible(True)
    update_pwm()


def update_pwm():
    pwm_labels[1].setText("%5d Hz" % PWM_FREQS[pwm_freq_index])
    pwm_labels[3].setText("%3d %%" % pwm_duty)


def show_rgb():
    show_channel_boxes()
    rgb_status_label.setVisible(True)
    update_rgb()


def update_rgb():
    color = RGB_COLORS[rgb_color_index]
    for channel in range(8):
        selected = channel == rgb_channel
        fill = color if selected else GRAY
        border = YELLOW if selected else WHITE
        text_color = 0x000000 if fill == WHITE else WHITE
        state = ("rgb", fill, selected)
        if channel_states[channel] == state:
            continue
        channel_states[channel] = state
        channel_rects[channel].setColor(color=border, fill_c=fill)
        channel_labels[channel].setColor(text_color, fill)
    rgb_status_label.setText(
        "Selected IO%d  Color: %s" % (rgb_channel, RGB_NAMES[rgb_color_index])
    )


def show_servo():
    show_channel_boxes()
    servo_status_label.setVisible(True)
    for channel in range(8):
        update_channel_box(channel, channel == servo_channel, channel == servo_channel)
    update_servo_status()


def update_servo_status():
    servo_status_label.setText("Selected IO%d  Angle:%3d" % (servo_channel, servo_angle))


def show_power():
    for widget in power_name_labels:
        widget.setVisible(True)
    for widget in power_value_labels:
        widget.setVisible(True)
    update_power()


def update_power():
    values = (
        require_value(device.get_reference_voltage(), "read reference voltage"),
        require_value(device.get_grove_voltage(), "read Grove voltage"),
        require_value(device.get_dc_voltage(), "read DC voltage"),
        require_value(device.get_current(), "read current"),
    )
    units = ("mV", "mV", "mV", "mA")
    for index, value in enumerate(values):
        power_value_labels[index].setText("%5d %s" % (value, units[index]))


def reset_channels():
    for channel in range(8):
        set_mode(channel, device.MODE_INPUT)
        require_ok(device.set_input_pull(channel, device.PULL_NONE), "clear IO%d pull" % channel)


def apply_input_pull():
    pulls = (device.PULL_NONE, device.PULL_UP, device.PULL_DOWN)
    for channel in range(8):
        require_ok(
            device.set_input_pull(channel, pulls[input_pull_index]), "set IO%d pull" % channel
        )
    keys_label.setText("A NEXT     B PULL: " + PULL_NAMES[input_pull_index])


def get_device_info():
    boot_version = require_value(device.get_bootloader_version(), "read boot version")
    software_version = require_value(device.get_firmware_version(), "read software version")
    device_type = require_value(device.get_device_type(), "read device type")
    uid4 = device.get_uid(0)
    uid12 = device.get_uid(1)
    if len(uid4) != 4:
        raise RuntimeError("read 4-byte UID failed")
    if len(uid12) != 12:
        raise RuntimeError("read 12-byte UID failed")
    uid4_text = "".join("%02X" % value for value in uid4)
    uid12_text = "".join("%02X" % value for value in uid12)
    print("Chain 8Servos2 UID (12-byte): " + uid12_text)
    return (
        "Boot:%s SW:%s" % (boot_version, software_version),
        "Type:%04X UID:%s" % (device_type, uid4_text),
    )


def apply_pwm():
    freq = PWM_FREQS[pwm_freq_index]
    set_pwm_frequency(0, freq)
    set_pwm_frequency(4, freq)
    for channel in range(8):
        set_pwm_output(channel, pwm_duty)


def apply_rgb():
    set_rgb_color(0, RGB_COLORS[rgb_color_index])
    set_rgb_config(rgb_channel, 1, refresh=True)


def select_rgb(channel):
    global rgb_channel

    set_mode(rgb_channel, device.MODE_INPUT)
    rgb_channel = channel % 8
    set_mode(rgb_channel, device.MODE_RGB)
    apply_rgb()
    update_rgb()


def select_servo(channel):
    global servo_channel, servo_angle, servo_direction, last_servo_move

    set_mode(servo_channel, device.MODE_INPUT)
    servo_channel = channel % 8
    servo_angle = 0
    servo_direction = 1
    set_mode(servo_channel, device.MODE_SERVO)
    set_servo(servo_channel, servo_angle)
    last_servo_move = time.ticks_ms()
    for index in range(8):
        update_channel_box(index, index == servo_channel, index == servo_channel)
    update_servo_status()


def enter_page():
    global last_refresh, output_levels, servo_angle, servo_direction

    hide_content()
    reset_channels()
    last_refresh = 0
    if page == PAGE_GPIO_INPUT:
        info_left, info_right = get_device_info()
        show_header(
            "1/7 GPIO Input",
            "Connect IO to GND or 3.3V",
            "A NEXT     B PULL: " + PULL_NAMES[input_pull_index],
            info_left,
            info_right,
        )
        apply_input_pull()
        show_channel_boxes()
        update_gpio_input()
    elif page == PAGE_GPIO_OUTPUT:
        output_levels = [False] * 8
        for channel in range(8):
            set_mode(channel, device.MODE_OUTPUT)
            set_output(channel, False)
        show_header(
            "2/7 GPIO Output",
            "Measure selected channel level",
            "A NEXT     B CHANNEL     C LEVEL",
        )
        show_channel_boxes()
        update_gpio_output()
    elif page == PAGE_ADC:
        for channel in range(8):
            set_mode(channel, device.MODE_ADC)
        show_header("3/7 ADC Input", "Apply 0-3.3V to IO0-IO7", "A NEXT     Values: 0-4095")
        show_adc()
    elif page == PAGE_PWM:
        for channel in range(8):
            set_mode(channel, device.MODE_PWM)
        apply_pwm()
        show_header(
            "4/7 PWM Output",
            "Measure frequency and duty",
            "A NEXT     B FREQ     C DUTY +20%",
        )
        show_pwm()
    elif page == PAGE_RGB:
        set_mode(rgb_channel, device.MODE_RGB)
        apply_rgb()
        show_header(
            "5/7 RGB Output",
            "Connect one RGB LED to selected IO",
            "A NEXT     B CHANNEL     C COLOR",
        )
        show_rgb()
    elif page == PAGE_SERVO:
        servo_angle = 0
        servo_direction = 1
        set_mode(servo_channel, device.MODE_SERVO)
        set_servo(servo_channel, servo_angle)
        show_header(
            "6/7 Servo Control",
            "Selected servo sweeps 0-180-0",
            "A NEXT     B PREV IO     C NEXT IO",
        )
        show_servo()
    else:
        show_header(
            "7/7 Power Telemetry",
            "Compare readings with a meter",
            "A NEXT     Updates every 500 ms",
        )
        show_power()


def handle_buttons():
    global page, input_pull_index, output_channel, pwm_freq_index, pwm_duty, rgb_color_index

    if BtnA.wasPressed():
        page = (page + 1) % PAGE_COUNT
        enter_page()
        return
    if page == PAGE_GPIO_INPUT:
        if BtnB.wasPressed():
            input_pull_index = (input_pull_index + 1) % len(PULL_NAMES)
            apply_input_pull()
    elif page == PAGE_GPIO_OUTPUT:
        if BtnB.wasPressed():
            output_channel = (output_channel + 1) % 8
            update_gpio_output()
        elif BtnC.wasPressed():
            output_levels[output_channel] = not output_levels[output_channel]
            set_output(output_channel, output_levels[output_channel])
            update_gpio_output()
    elif page == PAGE_PWM:
        if BtnB.wasPressed():
            pwm_freq_index = (pwm_freq_index + 1) % len(PWM_FREQS)
            apply_pwm()
            update_pwm()
        elif BtnC.wasPressed():
            pwm_duty = (pwm_duty + 20) % 120
            apply_pwm()
            update_pwm()
    elif page == PAGE_RGB:
        if BtnB.wasPressed():
            select_rgb(rgb_channel + 1)
        elif BtnC.wasPressed():
            rgb_color_index = (rgb_color_index + 1) % len(RGB_COLORS)
            apply_rgb()
            update_rgb()
    elif page == PAGE_SERVO:
        if BtnB.wasPressed():
            select_servo(servo_channel - 1)
        elif BtnC.wasPressed():
            select_servo(servo_channel + 1)


def update_page():
    global last_refresh, last_servo_move, servo_angle, servo_direction

    now = time.ticks_ms()
    if page == PAGE_GPIO_INPUT and time.ticks_diff(now, last_refresh) >= 100:
        last_refresh = now
        update_gpio_input()
    elif page == PAGE_ADC and time.ticks_diff(now, last_refresh) >= 200:
        last_refresh = now
        update_adc()
    elif page == PAGE_SERVO and time.ticks_diff(now, last_servo_move) >= 20:
        last_servo_move = now
        servo_angle += servo_direction * 3
        if servo_angle >= 180:
            servo_angle = 180
            servo_direction = -1
        elif servo_angle <= 0:
            servo_angle = 0
            servo_direction = 1
        set_servo(servo_channel, servo_angle)
        update_servo_status()
    elif page == PAGE_POWER and time.ticks_diff(now, last_refresh) >= 500:
        last_refresh = now
        update_power()


def setup():
    global bus2, device

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(BG)
    bus2 = ChainBus(2, tx=21, rx=22)
    device = Servos8V2Chain(bus2, 1)
    create_ui()
    enter_page()


def loop():
    M5.update()
    handle_buttons()
    update_page()
    time.sleep_ms(10)


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
