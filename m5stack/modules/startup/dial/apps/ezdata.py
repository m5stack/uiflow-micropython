from ..app import AppBase, Descriptor
import M5
from ..res import EZDATA_IMG
from .status_bar import StatusBarApp


class EzDataApp(AppBase):
    def __init__(self, icos, data=None) -> None:
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_view(self):
        M5.Lcd.clear()
        M5.Lcd.drawImage(EZDATA_IMG, 0, 0)

    def on_ready(self):
        self._status_bar = StatusBarApp(None, self._wlan)
        self._status_bar.start()

    def on_hide(self):
        self._status_bar.stop()

    def on_exit(self):
        M5.Lcd.clear()

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass
