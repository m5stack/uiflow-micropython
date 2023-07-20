from M5 import Widgets
import urequests as requests
import _thread
import time
import micropython


class ImagePlus(Widgets.Image):
    def __init__(self, url, x, y, enable, period, default_img="res/img/default.jpg", parent=None):
        self._url = url
        self._x = x
        self._y = y
        self._enable = enable
        self._period = period
        self._default_img = default_img
        self._valid = False
        self.last_time = time.ticks_ms()

        self._path = "/flash/res/img/" + url.split("/")[-1]
        print("path:", self._path)
        super(ImagePlus, self).__init__(self._path, x, y, parent)
        self._draw()

        self._enable and _thread.start_new_thread(self._loop, tuple())

    def _draw(self):
        try:
            rsp = requests.get(self._url)
            if rsp.status_code == 200:
                with open(self._path, "wb") as f:
                    f.write(rsp.content)
                self._valid = True
                super().setImage(self._path)
                self.last_time = time.ticks_ms()
            else:
                self._valid = False
                super().setImage(self._default_img)
            rsp.close()
        except OSError:
            self._valid = False
            super().setImage(self._default_img)

    def set_update_enable(self, enable):
        if self._enable is True and enable is True:
            return

        if self._enable is False and enable is True:
            _thread.start_new_thread(self._loop, tuple())

        self._enable = enable

    def set_update_period(self, period):
        self._period = period

    def _loop(self):
        while self._enable:
            if time.ticks_ms() - self.last_time >= self._period:
                self._draw()
            else:
                time.sleep_ms(self._period - (time.ticks_ms() - self.last_time))
        _thread.exit()

    def is_valid_image(self):
        return self._valid

    def __del__(self):
        self._enable = False
