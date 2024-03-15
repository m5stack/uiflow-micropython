# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from M5 import Widgets

try:
    import urequests as requests
except ImportError:
    import requests
from machine import Timer

# from micropython import schedule


class LabelPlus(Widgets.Label):
    def __init__(
        self,
        text,
        x,
        y,
        size,
        text_color,
        bg_color,
        font,
        url,
        period,
        enable,
        json_key=None,
        error_msg=None,
        error_msg_color=0xFF0000,
    ) -> None:
        self._url = url
        self._tim = Timer(-1)
        self._period = period
        self._enable = enable
        self._key = json_key
        self._text_color = text_color
        self._bg_color = bg_color
        self._error_msg = error_msg
        self._error_msg_color = error_msg_color
        super(LabelPlus, self).__init__(text, x, y, size, text_color, bg_color, font)

        self._data = error_msg
        self._init_timer()

    def _init_timer(self):
        if self._enable and self._period > 0:
            self._tim.init(period=self._period, mode=Timer.ONE_SHOT, callback=self._cb)

    def set_update_enable(self, enable):
        if self._enable is True and enable is True:
            return
        if self._enable is True:
            self._tim.deinit()
        self._enable = enable
        self._init_timer()

    def _cb(self, tim):
        # schedule(self._update(), self)
        self._update()
        self._tim.init(mode=Timer.ONE_SHOT, period=self._period, callback=self._cb)

    def set_update_period(self, period):
        if self._enable:
            self._tim.deinit()
        self._period = period
        self._init_timer()

    def is_valid_data(self) -> bool:
        return False if self._data is self._error_msg else True

    def get_data(self):
        return self._data

    def setColor(self, fg_color, bg_color=0x000000):
        self._text_color = fg_color
        super().setColor(fg_color, bg_color)

    def set_url(self, url):
        self._url = url

    def _update(self):
        r = None
        try:
            r = requests.get(self._url)
            if r.status_code == 200:
                if self._key is None:
                    self._data = r.content
                    self._show(str(r.content))
                else:
                    try:
                        data = r.json()
                        self._data = self._find_key(data)
                        self._show(str(self._data))
                    except ValueError:
                        self._show_error("ValueError")
            else:
                error_str = "ERR: " + str(r.status_code)
                self._show_error(error_str)
            r.close()
        except OSError:
            self._show_error("OSError")

    def _find_key(self, data):
        self._data = data.get(self._key)
        if self._data is not None:
            return self._data
        for _, value in data.items():
            if type(value) == list:
                for item in value:
                    self._find_key(item)
                    if self._data is not None:
                        return self._data
            elif type(value) == dict:
                self._find_key(value)
            if self._data is not None:
                return self._data

    def update(self):
        self._tim.deinit()
        self._update()
        self._init_timer()

    def show_value_of_key(self, key):
        self._tim.deinit()
        self._key = key
        self._update()
        self._init_timer()

    def _show_error(self, error_msg):
        super().setColor(self._error_msg_color)
        if self._error_msg is None:
            self._data = error_msg
            super().setText(error_msg)
        else:
            self._data = self._error_msg
            super().setText(self._error_msg)

    def _show(self, text):
        super().setColor(self._text_color)
        super().setText(text)
