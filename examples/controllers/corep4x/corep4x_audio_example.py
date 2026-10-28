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
label_state = None
label_duration = None
label_message = None
label_volume_name = None
label_volume = None
volume_slider = None
record_button = None
play_button = None


record_pending = None
play_pending = None
volume = None
volume_pending = None
stop_requested = None
record_buffer = None
state = None
queued_chunks = None
next_is_a = None
recorded_bytes = None
buffer_a = None
buffer_b = None
record_start = None
speaker_ready = None
play_started = None


def record_button_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    record_pending = True


def play_button_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    play_pending = True


def volume_slider_value_changed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    volume = volume_slider.get_value()
    label_volume.set_text(str((str(volume) + str("%"))))
    volume_pending = True


def record_button_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        record_button_clicked_event(event_struct)
    return


def play_button_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        play_button_clicked_event(event_struct)
    return


def volume_slider_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        volume_slider_value_changed_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "Audio",
        x=24,
        y=24,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_state = m5ui.M5Label(
        "IDLE",
        x=48,
        y=90,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_duration = m5ui.M5Label(
        "0.0 / 30 s",
        x=48,
        y=170,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_message = m5ui.M5Label(
        "Tap RECORD to start",
        x=48,
        y=227,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume_name = m5ui.M5Label(
        "Volume",
        x=24,
        y=280,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume = m5ui.M5Label(
        "70%",
        x=384,
        y=280,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    volume_slider = m5ui.M5Slider(
        x=40,
        y=335,
        w=400,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=70,
        bg_c=0x38383C,
        color=0x8EDA91,
        parent=page0,
    )
    record_button = m5ui.M5Button(
        text="RECORD",
        x=24,
        y=388,
        bg_c=0x7A2731,
        text_c=0xF4F4F5,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    play_button = m5ui.M5Button(
        text="PLAY",
        x=252,
        y=388,
        bg_c=0x303034,
        text_c=0xF4F4F5,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    record_button.add_event_cb(record_button_event_handler, lv.EVENT.ALL, None)
    play_button.add_event_cb(play_button_event_handler, lv.EVENT.ALL, None)
    volume_slider.add_event_cb(volume_slider_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.stop()
    Speaker.end()
    Mic.end()
    record_buffer = bytearray(0)
    buffer_a = bytearray(4000)
    buffer_b = bytearray(4000)
    Speaker.setPA(True)
    state = "IDLE"
    volume = 70
    record_pending = False
    play_pending = False
    volume_pending = False
    next_is_a = True
    queued_chunks = 0
    stop_requested = False
    record_start = 0
    recorded_bytes = 0
    speaker_ready = False
    play_started = False
    record_button.set_size(204, 64)
    play_button.set_size(204, 64)


def loop():
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    M5.update()
    if record_pending:
        record_pending = False
        if state == "RECORDING":
            stop_requested = True
            state = "STOPPING"
            label_state.set_text(str(state))
            label_message.set_text(str("Finishing recording..."))
        else:
            if state != "STOPPING":
                Speaker.stop()
                Speaker.end()
                play_button.set_btn_text(str("PLAY"))
                Mic.end()
                Mic.setSampleRate(8000)
                Mic.begin()
                record_buffer = bytearray(0)
                recorded_bytes = 0
                queued_chunks = 0
                next_is_a = True
                stop_requested = False
                label_duration.set_text(str((str((recorded_bytes / 16000)) + str(" / 30 s"))))
                if Mic.isRunning():
                    Mic.record(buffer_a, 8000, False)
                    Mic.record(buffer_b, 8000, False)
                    if (Mic.isRecording()) == 2:
                        queued_chunks = 2
                        record_start = time.ticks_ms()
                        state = "RECORDING"
                        label_state.set_text(str(state))
                        label_message.set_text(str("Tap STOP REC to finish"))
                        record_button.set_btn_text(str("STOP REC"))
                    else:
                        Mic.end()
                        queued_chunks = 0
                        state = "IDLE"
                        label_state.set_text(str(state))
                        label_message.set_text(str("Recorder failed"))
                        record_button.set_btn_text(str("RECORD"))
                else:
                    state = "IDLE"
                    label_state.set_text(str(state))
                    label_message.set_text(str("Microphone failed"))
                    record_button.set_btn_text(str("RECORD"))
    if state == "RECORDING" or state == "STOPPING":
        if (Mic.isRecording()) < queued_chunks:
            if next_is_a:
                record_buffer.extend(buffer_a)
            else:
                record_buffer.extend(buffer_b)
            recorded_bytes = recorded_bytes + 4000
            queued_chunks = queued_chunks - 1
            record_start = time.ticks_ms()
            if not stop_requested and recorded_bytes + queued_chunks * 4000 < 480000:
                if next_is_a:
                    Mic.record(buffer_a, 8000, False)
                else:
                    Mic.record(buffer_b, 8000, False)
                queued_chunks = queued_chunks + 1
            next_is_a = not next_is_a
            label_duration.set_text(str((str((recorded_bytes / 16000)) + str(" / 30 s"))))
            if queued_chunks == 0:
                Mic.end()
                state = "READY"
                label_state.set_text(str(state))
                if recorded_bytes >= 480000:
                    label_message.set_text(str("30 s limit reached"))
                else:
                    label_message.set_text(str("Recording ready"))
                record_button.set_btn_text(str("RECORD"))
                play_button.set_btn_text(str("PLAY"))
        if (state == "RECORDING" or state == "STOPPING") and (
            time.ticks_diff((time.ticks_ms()), record_start)
        ) > 2000:
            Mic.end()
            if recorded_bytes > 0:
                state = "READY"
            else:
                state = "IDLE"
            label_state.set_text(str(state))
            queued_chunks = 0
            label_message.set_text(str("Recording timed out"))
            record_button.set_btn_text(str("RECORD"))
    if play_pending:
        play_pending = False
        if state == "PLAYING":
            Speaker.stop()
            Speaker.end()
            state = "READY"
            label_state.set_text(str(state))
            play_button.set_btn_text(str("PLAY"))
        else:
            if state == "READY":
                Mic.end()
                speaker_ready = Speaker.begin()
                if speaker_ready:
                    Speaker.setVolume(int((volume * 255 + 50) / 100))
                    Speaker.setPA(True)
                    play_started = Speaker.playRaw(record_buffer, 8000)
                    if play_started:
                        state = "PLAYING"
                        label_state.set_text(str(state))
                        label_message.set_text(str(""))
                        play_button.set_btn_text(str("STOP PLAY"))
                    else:
                        label_message.set_text(str("Playback failed"))
                else:
                    label_message.set_text(str("Speaker failed"))
    if state == "PLAYING" and (Speaker.isPlaying()) == 0:
        Speaker.stop()
        Speaker.end()
        state = "READY"
        label_state.set_text(str(state))
        play_button.set_btn_text(str("PLAY"))
    if volume_pending:
        volume_pending = False
        if state == "PLAYING":
            Speaker.setVolume(int((volume * 255 + 50) / 100))
    time.sleep_ms(10)


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
