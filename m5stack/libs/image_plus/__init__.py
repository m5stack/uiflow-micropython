from M5 import Widgets
import urequests as requests
import _thread
import time


class ImagePlus(Widgets.Image):
    def __init__(self, url, x, y, enable, period, parent=None):
        self._url = url
        self._x = x
        self._y = y
        self._enable = enable
        self._period = period

        self._path = "/flash/res/img/" + url.split("/")[-1]
        print("path:", self._path)
        rsp = requests.get(self._url)
        if rsp.status_code == 200:
            with open(self._path, "wb") as f:
                f.write(rsp.content)
        else:
            pass
        rsp.close()
        super(ImagePlus, self).__init__(self._path, x, y, parent)
        if self._enable:
            _thread.start_new_thread(self._loop, tuple())

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

            rsp = requests.get(self._url)
            if rsp.status_code == 200:
                with open(self._path, "wb") as f:
                    f.write(rsp.content)
            else:
                pass
            super().setImage(self._path)
            rsp.close()

            time.sleep_ms(self._period)

        _thread.exit()
