# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import startup
from . import framework
from . import apps
import M5
from M5 import Speaker, Widgets
import esp32
import time
import machine


_SERVO_NVS_NS = "servo"
_SERVO_ZERO_KEYS = ("zero_pos_1", "zero_pos_2")
_SERVO_RAW_MIN = 0
_SERVO_RAW_MAX = 1000
_DEVICE_IMG = "/system/stackchan/01.png"
_CENTER_DEVICE_IMG = "/system/stackchan/02.png"
_HOLD_BOX = (218, 67, 94, 94)
_PROGRESS_BOX = (64, 225, 192, 8)
_HOLD_SAVE_MS = 2800
_BG_COLOR = 0xFFFFFF
_FRAME_COLOR = 0x0DC9F4
_PANEL_COLOR = 0x0DC9F4
_HINT_COLOR = 0x00E000
_TEXT_COLOR = 0x3D4D57
_BOX_TEXT_COLOR = 0xFFFFFF
_MUTED_COLOR = 0xC9D5DC
_PROGRESS_BG_COLOR = 0xEAF6FB
_NUMBER_COLOR = 0xFF0000


def _calibration_tone(freq, duration):
    try:
        Speaker.tone(freq, duration)
    except Exception:
        pass


def _has_valid_servo_zero_data():
    try:
        nvs = esp32.NVS(_SERVO_NVS_NS)
        for key in _SERVO_ZERO_KEYS:
            value = nvs.get_i32(key)
            if not (_SERVO_RAW_MIN <= value <= _SERVO_RAW_MAX):
                print("[StackChan] invalid servo zero %s=%d" % (key, value))
                return False
        return True
    except OSError as e:
        print("[StackChan] missing servo zero data: %s" % e)
        return False


def _draw_hold_box():
    x, y, w, h = _HOLD_BOX
    M5.Lcd.drawRoundRect(x, y, w, h, 10, _FRAME_COLOR)
    M5.Lcd.drawRoundRect(x + 1, y + 1, w - 2, h - 2, 9, _FRAME_COLOR)

    M5.Lcd.setFont(Widgets.FONTS.Montserrat18)
    M5.Lcd.setTextColor(_FRAME_COLOR, _BG_COLOR)
    M5.Lcd.drawCenterString("Touch", x + w // 2, y + 15)
    M5.Lcd.drawCenterString("for 3S to", x + w // 2, y + 39)
    M5.Lcd.drawCenterString("confirm", x + w // 2, y + 63)
    _draw_hold_prompt()
    _draw_hold_progress(0)


def _draw_hold_prompt():
    bar_x, bar_y, bar_w, _ = _PROGRESS_BOX
    prompt_y = bar_y - 40
    M5.Lcd.setFont(Widgets.FONTS.Montserrat24)
    M5.Lcd.setTextColor(_FRAME_COLOR, _BG_COLOR)
    M5.Lcd.drawCenterString("Adjust as shown above", bar_x + bar_w // 2, prompt_y)


def _draw_hold_progress(hold_ms=0):
    bar_x, bar_y, bar_w, bar_h = _PROGRESS_BOX
    progress = min(bar_w, max(0, int(bar_w * hold_ms // _HOLD_SAVE_MS)))
    M5.Lcd.fillRoundRect(bar_x, bar_y, bar_w, bar_h, bar_h // 2, _PROGRESS_BG_COLOR)
    M5.Lcd.drawRoundRect(bar_x, bar_y, bar_w, bar_h, bar_h // 2, _FRAME_COLOR)
    if progress > 0:
        M5.Lcd.fillRoundRect(bar_x, bar_y, progress, bar_h, bar_h // 2, _HINT_COLOR)


def _draw_calibration_tip(tip=None):
    if tip:
        bar_x, _, bar_w, _ = _PROGRESS_BOX
        M5.Lcd.fillRect(bar_x - 20, 205, bar_w + 40, 18, _BG_COLOR)
        M5.Lcd.setFont(Widgets.FONTS.Montserrat14)
        M5.Lcd.setTextColor(_FRAME_COLOR, _BG_COLOR)
        M5.Lcd.drawCenterString(tip, bar_x + bar_w // 2, 205)


def _draw_calibration_steps():
    image_y = 64
    number_y = 35
    slots = ((0, _DEVICE_IMG), (107, _CENTER_DEVICE_IMG))
    M5.Lcd.setFont(Widgets.FONTS.Montserrat24)
    M5.Lcd.setTextColor(_NUMBER_COLOR, _BG_COLOR)
    for index, (x, image) in enumerate(slots, 1):
        M5.Lcd.drawCenterString(str(index), x + 50, number_y)
        M5.Lcd.drawImage(image, x, image_y)
    x, _, w, _ = _HOLD_BOX
    M5.Lcd.drawCenterString("3", x + w // 2, number_y)


def _draw_servo_zero_calibration(tip=None, hold_ms=0):
    M5.Lcd.fillRect(0, 0, 320, 240, _BG_COLOR)
    M5.Lcd.setFont(Widgets.FONTS.Montserrat24)
    M5.Lcd.setTextColor(_FRAME_COLOR, _BG_COLOR)
    M5.Lcd.drawString("Head Calibration", 55, 6)

    _draw_calibration_steps()
    _draw_hold_box()
    _draw_calibration_tip(tip)
    _draw_hold_progress(hold_ms)


def _update_servo_zero_calibration(hold_ms=0):
    _draw_hold_progress(hold_ms)


def _touch_box_hit(box, x, y):
    bx, by, bw, bh = box
    return bx <= x <= bx + bw and by <= y <= by + bh


def _run_servo_zero_calibration_if_needed():
    if _has_valid_servo_zero_data():
        return

    stackchan = None
    _draw_servo_zero_calibration()
    try:
        from hardware.stackchan import StackChan

        stackchan = StackChan(i2c=1, uart=1)
        stackchan.set_servo_power(enable=True)
        time.delay_ms(500)
        stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
        stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)
        Speaker.begin()
        Speaker.setVolumePercentage(0.6)
        _calibration_tone(1000, 100)
    except Exception as e:
        print("[StackChan] servo calibration init failed: %s" % e)

    last_refresh = 0
    hold_start = None
    hold_ms = 0
    while True:
        M5.update()
        now = time.ticks_ms()
        touching_save = False
        if M5.Touch.getCount() > 0:
            x = M5.Touch.getX()
            y = M5.Touch.getY()
            touching_save = _touch_box_hit(_HOLD_BOX, x, y)

        if touching_save:
            if hold_start is None:
                hold_start = now
                _calibration_tone(880, 40)
            hold_ms = time.ticks_diff(now, hold_start)
        else:
            hold_start = None
            hold_ms = 0

        if hold_ms >= _HOLD_SAVE_MS:
            if stackchan is None:
                print("[StackChan] servo calibration is unavailable")
                _calibration_tone(400, 180)
                hold_start = None
                hold_ms = 0
                _draw_hold_progress(0)
                continue
            if stackchan.set_servo_zero():
                _calibration_tone(1200, 100)
                # _draw_servo_zero_calibration(tip="Calibration saved", hold_ms=_HOLD_SAVE_MS)
                time.sleep(0.3)
                stackchan.set_servo_power(False)
                return
            _calibration_tone(400, 180)
            _draw_calibration_tip("Save failed, retry")
            machine.soft_reset()
            time.sleep(0.5)
            hold_start = None
            hold_ms = 0
            _draw_hold_progress(0)

        if time.ticks_diff(now, last_refresh) >= 100:
            last_refresh = now
            _update_servo_zero_calibration(hold_ms)

        time.sleep_ms(20)


class StackChan_Startup:
    def __init__(self) -> None:
        self._wlan = startup.Startup()
        # self._status_bar = StatusBarApp(None, self._wifi)

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
    ) -> None:
        self._wlan.connect_network(
            ssid, pswd, protocol=protocol, ip=ip, netmask=netmask, gateway=gateway, dns=dns
        )
        M5.Lcd.drawImage("/system/stackchan/boot.png", 0, 0)
        time.sleep(0.2)
        _run_servo_zero_calibration_if_needed()

        M5.Lcd.clear(_BG_COLOR)
        sprite = M5.Lcd.newCanvas(320, 160, 16, True)

        fw = framework.Framework()
        dev_app = apps.DevApp(sprite, data=self._wlan)
        fw.install_bar(apps.StatusBarApp(None, self._wlan))
        fw.install_launcher(dev_app)
        fw.install(apps.SettingsApp(sprite, data=self._wlan))
        fw.install(dev_app)
        fw.install(apps.RunApp(None))
        fw.install(apps.ListApp(sprite))
        fw.install(apps.EzDataApp(sprite))
        fw.start()
