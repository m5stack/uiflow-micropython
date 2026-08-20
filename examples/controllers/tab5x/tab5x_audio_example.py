# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from audio import Recorder
from audio import Player
import time


page0 = None
label_title = None
button_record = None
button_play = None
label_status = None
label_format = None
recorder = None
player = None


recordDuration = None
playing = None
recordStart = None
recording = None
hasRecording = None
playStart = None
audioBuffer = None
recordTime = None


def button_record_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    if recorder.is_recording():
        recordDuration = time.ticks_diff((time.ticks_ms()), recordStart)
        recorder.stop()
        recording = False
        hasRecording = True
        button_record.set_btn_text(str("START RECORD"))
        label_status.set_text(str("Recording stopped"))
    else:
        if playing:
            player.stop()
            playing = False
            button_play.set_btn_text(str("START PLAY"))
        Speaker.setPA(False)
        hasRecording = False
        recordStart = time.ticks_ms()
        button_record.set_btn_text(str("STOP RECORD"))
        label_status.set_text(str("Recording... maximum 10 seconds"))
        audioBuffer = recorder.create_pcm_buf(recordTime)
        recorder.record_into(audioBuffer, False)
        recording = True


def button_play_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    if playing:
        player.stop()
        playing = False
        button_play.set_btn_text(str("START PLAY"))
        label_status.set_text(str("Playback stopped"))
    else:
        if recorder.is_recording():
            label_status.set_text(str("Wait for recording to stop"))
        else:
            if hasRecording:
                Speaker.setPA(True)
                time.sleep_ms(100)
                button_play.set_btn_text(str("STOP PLAY"))
                label_status.set_text(str("Playing..."))
                player.play_raw(
                    audioBuffer, sample=16000, stereo=False, bits=16, pos=0, volume=80, sync=False
                )
                playStart = time.ticks_ms()
                playing = True
            else:
                label_status.set_text(str("Record audio first"))


def button_record_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_record_pressed_event(event_struct)
    return


def button_play_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_play_pressed_event(event_struct)
    return


def setup():
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "Audio Example",
        x=480,
        y=35,
        text_c=0xE99628,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_record = m5ui.M5Button(
        text="START RECORD",
        x=70,
        y=175,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_play = m5ui.M5Button(
        text="START PLAY",
        x=710,
        y=175,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_status = m5ui.M5Label(
        "Ready. Maximum recording length: 10s",
        x=70,
        y=420,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_format = m5ui.M5Label(
        "16 kHz / 16-bit / mono PCM",
        x=70,
        y=535,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    button_record.add_event_cb(button_record_event_handler, lv.EVENT.ALL, None)
    button_play.add_event_cb(button_play_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    button_record.set_size(500, 140)
    button_play.set_size(500, 140)
    Mic.end()
    recorder = Recorder(16000, 16, False)
    player = Player(None)
    player.stop()
    player.set_vol(100)
    recordTime = 10
    audioBuffer = recorder.create_pcm_buf(recordTime)
    recording = False
    playing = False
    hasRecording = False
    recordStart = 0
    recordDuration = 10000
    playStart = 0


def loop():
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    M5.update()
    if recording and not (recorder.is_recording()):
        recordDuration = time.ticks_diff((time.ticks_ms()), recordStart)
        recording = False
        hasRecording = True
        button_record.set_btn_text(str("START RECORD"))
        label_status.set_text(str("Recording complete"))
    if playing and (time.ticks_diff((time.ticks_ms()), playStart)) >= recordDuration:
        player.stop()
        Speaker.setPA(False)
        playing = False
        button_play.set_btn_text(str("START PLAY"))
        label_status.set_text(str("Playback complete"))


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
