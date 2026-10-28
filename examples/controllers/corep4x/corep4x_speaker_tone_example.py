# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time


page0 = None
label_title = None
label_output = None
label_pa = None
pa_switch = None
label_frequency_title = None
label_frequency = None
frequency_slider = None
label_frequency_min = None
label_frequency_max = None
label_volume_title = None
label_volume = None
volume_slider = None
label_volume_min = None
label_volume_max = None
tone_button = None


pa_requested = None
frequency = None
tone_toggle_pending = None
volume = None
pa_change_pending = None
frequency_change_pending = None
volume_change_pending = None
tone_enabled = None
pa_enabled = None


def pa_switch_checked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    pa_requested = pa_switch.has_state(lv.STATE.CHECKED)
    pa_change_pending = True


def pa_switch_unchecked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    pa_requested = pa_switch.has_state(lv.STATE.CHECKED)
    pa_change_pending = True


def frequency_slider_value_changed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    frequency = frequency_slider.get_value()
    label_frequency.set_text(str((str(frequency) + str(" Hz"))))
    label_frequency.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 152)
    frequency_change_pending = True


def tone_button_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    tone_toggle_pending = True


def volume_slider_value_changed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    volume = volume_slider.get_value()
    label_volume.set_text(str((str(volume) + str("%"))))
    label_volume.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 272)
    volume_change_pending = True


def pa_switch_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            pa_switch_checked_event(event_struct)
        else:
            pa_switch_unchecked_event(event_struct)
    return


def frequency_slider_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        frequency_slider_value_changed_event(event_struct)
    return


def tone_button_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        tone_button_clicked_event(event_struct)
    return


def volume_slider_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        volume_slider_value_changed_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "Speaker",
        x=24,
        y=24,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_output = m5ui.M5Label(
        "Stopped",
        x=384,
        y=28,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_pa = m5ui.M5Label(
        "Amplifier on",
        x=24,
        y=96,
        text_c=0x8EDA91,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    pa_switch = m5ui.M5Switch(
        x=384,
        y=84,
        w=72,
        h=40,
        bg_c=0x38383C,
        bg_c_checked=0x8EDA91,
        circle_c=0xF4F4F5,
        parent=page0,
    )
    label_frequency_title = m5ui.M5Label(
        "Frequency",
        x=24,
        y=158,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_frequency = m5ui.M5Label(
        "1000 Hz",
        x=320,
        y=152,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    frequency_slider = m5ui.M5Slider(
        x=40,
        y=206,
        w=400,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=200,
        max_value=4000,
        value=1000,
        bg_c=0x38383C,
        color=0x4DA6FF,
        parent=page0,
    )
    label_frequency_min = m5ui.M5Label(
        "200",
        x=40,
        y=232,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_frequency_max = m5ui.M5Label(
        "4000",
        x=384,
        y=232,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume_title = m5ui.M5Label(
        "Volume",
        x=24,
        y=278,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume = m5ui.M5Label(
        "70%",
        x=320,
        y=272,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    volume_slider = m5ui.M5Slider(
        x=40,
        y=326,
        w=400,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=70,
        bg_c=0x38383C,
        color=0x4DA6FF,
        parent=page0,
    )
    label_volume_min = m5ui.M5Label(
        "0",
        x=40,
        y=352,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume_max = m5ui.M5Label(
        "100%",
        x=384,
        y=352,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    tone_button = m5ui.M5Button(
        text="Start tone",
        x=24,
        y=388,
        bg_c=0x245A85,
        text_c=0xF4F4F5,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    pa_switch.add_event_cb(pa_switch_event_handler, lv.EVENT.ALL, None)
    frequency_slider.add_event_cb(frequency_slider_event_handler, lv.EVENT.ALL, None)
    tone_button.add_event_cb(tone_button_event_handler, lv.EVENT.ALL, None)
    volume_slider.add_event_cb(volume_slider_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.stop()
    frequency = 1000
    frequency_change_pending = False
    pa_requested = True
    pa_change_pending = False
    Speaker.setPA(True)
    pa_enabled = True
    tone_toggle_pending = False
    tone_enabled = False
    volume = 70
    volume_change_pending = False
    pa_requested = pa_enabled
    pa_switch.set_state(lv.STATE.CHECKED, pa_enabled)
    Speaker.setVolume(int((volume * 255 + 50) / 100))
    if pa_enabled:
        label_pa.set_text(str("Amplifier on"))
        label_pa.set_text_color(0x8EDA91, 255, 0)
    else:
        label_pa.set_text(str("Amplifier off"))
        label_pa.set_text_color(0x9A9A9F, 255, 0)
    if tone_enabled and (Speaker.isPlaying()):
        label_output.set_text(str("Playing"))
        label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
        label_output.set_text_color(0x8EDA91, 255, 0)
    else:
        label_output.set_text(str("Stopped"))
        label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
        label_output.set_text_color(0x9A9A9F, 255, 0)
    if tone_enabled:
        tone_button.set_btn_text(str("Stop tone"))
        tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        tone_button.set_btn_text(str("Start tone"))
        tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    tone_button.set_size(432, 64)
    label_frequency.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 152)
    label_volume.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 272)
    label_frequency_max.align_to(page0, lv.ALIGN.TOP_RIGHT, -40, 232)
    label_volume_max.align_to(page0, lv.ALIGN.TOP_RIGHT, -40, 352)
    frequency_slider.set_bg_color(0x4DA6FF, 255, lv.PART.KNOB | lv.STATE.DEFAULT)
    volume_slider.set_bg_color(0x4DA6FF, 255, lv.PART.KNOB | lv.STATE.DEFAULT)
    frequency_slider.set_bg_color(0x38383C, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    volume_slider.set_bg_color(0x38383C, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def loop():
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    M5.update()
    if pa_change_pending:
        pa_change_pending = False
        if pa_requested:
            Speaker.setPA(True)
            pa_enabled = True
        else:
            Speaker.setPA(False)
            pa_enabled = False
        if pa_enabled:
            label_pa.set_text(str("Amplifier on"))
            label_pa.set_text_color(0x8EDA91, 255, 0)
        else:
            label_pa.set_text(str("Amplifier off"))
            label_pa.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled and (Speaker.isPlaying()):
            label_output.set_text(str("Playing"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x8EDA91, 255, 0)
        else:
            label_output.set_text(str("Stopped"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled:
            tone_button.set_btn_text(str("Stop tone"))
            tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            tone_button.set_btn_text(str("Start tone"))
            tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    if tone_toggle_pending:
        tone_toggle_pending = False
        tone_enabled = not tone_enabled
        if tone_enabled:
            Speaker.tone(frequency, 60000)
        else:
            Speaker.stop()
        if pa_enabled:
            label_pa.set_text(str("Amplifier on"))
            label_pa.set_text_color(0x8EDA91, 255, 0)
        else:
            label_pa.set_text(str("Amplifier off"))
            label_pa.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled and (Speaker.isPlaying()):
            label_output.set_text(str("Playing"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x8EDA91, 255, 0)
        else:
            label_output.set_text(str("Stopped"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled:
            tone_button.set_btn_text(str("Stop tone"))
            tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            tone_button.set_btn_text(str("Start tone"))
            tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    if frequency_change_pending:
        frequency_change_pending = False
        if tone_enabled:
            Speaker.stop()
            Speaker.tone(frequency, 60000)
        if pa_enabled:
            label_pa.set_text(str("Amplifier on"))
            label_pa.set_text_color(0x8EDA91, 255, 0)
        else:
            label_pa.set_text(str("Amplifier off"))
            label_pa.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled and (Speaker.isPlaying()):
            label_output.set_text(str("Playing"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x8EDA91, 255, 0)
        else:
            label_output.set_text(str("Stopped"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled:
            tone_button.set_btn_text(str("Stop tone"))
            tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            tone_button.set_btn_text(str("Start tone"))
            tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    if tone_enabled and not (Speaker.isPlaying()):
        Speaker.tone(frequency, 60000)
    time.sleep_ms(10)
    if volume_change_pending:
        volume_change_pending = False
        Speaker.setVolume(int((volume * 255 + 50) / 100))


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
