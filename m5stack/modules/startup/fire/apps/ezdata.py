from ..app import AppBase
import M5
from ..res import EZDATA_UNSELECTED_IMG, EZDATA_SELECTED_IMG


class EzDataApp(AppBase):
    def __init__(self, icos) -> None:
        self._lcd = icos
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage(EZDATA_UNSELECTED_IMG, 5 + 62 * 4, 0)

    def on_view(self):
        M5.Lcd.drawImage(EZDATA_SELECTED_IMG, 5 + 62 * 4, 0)

        self._origin_x = 0
        self._origin_y = 56
        self._lcd.clear()
        self._lcd.push(self._origin_x, self._origin_y)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        M5.Lcd.drawImage(EZDATA_UNSELECTED_IMG, 5 + 62 * 4, 0)
        self._lcd.clear()
        self._lcd.push(self._origin_x, self._origin_y)

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        pass

    async def _btnc_event_handler(self, fw):
        pass
