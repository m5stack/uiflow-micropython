from M5 import Widgets
import urequests as requests
from machine import Timer

# from micropython import schedule


class LabelPlus(Widgets.Label):
    def __init__(self, text, x, y, size, text_color, bg_color, font, url, period) -> None:
        self._url = url
        self._tim = Timer(-1)
        self._period = period
        self._key = None
        self._text_color = text_color
        self._bg_color = bg_color
        super(LabelPlus, self).__init__(text, x, y, size, text_color, bg_color, font)
        if self._period > 0:
            self._tim.init(period=self._period, mode=Timer.ONE_SHOT, callback=self._cb)

    def _cb(self, tim):
        # schedule(self._update(), self)
        self._update()
        self._tim.init(mode=Timer.ONE_SHOT, period=self._period, callback=self._cb)

    def set_url(self, url):
        self._url = url

    def _update(self):
        r = None
        try:
            r = requests.get(self._url)
            if r.status_code == 200:
                if self._key is None:
                    self._show(str(r.content))
                else:
                    try:
                        data = r.json()
                        self._show(str(data.get(self._key)))
                    except ValueError:
                        self._show_error("ValueError")
            else:
                error_str = "ERR: " + str(r.status_code)
                self._show_error(error_str)
            r.close()
        except OSError:
            self._show_error("OSError")

    def update(self):
        self._tim.deinit()
        self._update()
        self._tim.init(period=self._period, mode=Timer.ONE_SHOT, callback=self._cb)

    def show_value_of_key(self, key):
        self._tim.deinit()
        self._key = key
        self._update()
        self._tim.init(period=self._period, mode=Timer.ONE_SHOT, callback=self._cb)

    def _show_error(self, error_str):
        super().setColor(0xFF0000)
        super().setText(error_str)

    def _show(self, string):
        super().setColor(self._text_color)
        super().setText(string)
