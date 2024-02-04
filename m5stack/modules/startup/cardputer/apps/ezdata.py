from ..app import AppBase
import M5


class EzDataApp(AppBase):
    def __init__(self, icos, data=None) -> None:
        super().__init__()

    def on_install(self):
        pass

    def on_view(self):
        M5.Lcd.fillRect(30, 19, 210, 116, 0x333333)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass
