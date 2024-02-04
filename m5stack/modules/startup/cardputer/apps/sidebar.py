from ..app import AppBase
from ..res import (
    Aa_IMG,
    Aa0_IMG,
    ALT_IMG,
    ALT0_IMG,
    CTRL_IMG,
    CTRL0_IMG,
    FN_IMG,
    FN0_IMG,
    OPT_IMG,
    OPT0_IMG,
)
import M5


class SidebarApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        return super().on_launch()

    def on_view(self):
        M5.Lcd.fillRoundRect(2, 4, 28, 127, 15, 0xC4C4C4)
        M5.Lcd.drawImage(Aa0_IMG, 5, 20)
        M5.Lcd.drawImage(FN0_IMG, 5, 39)
        M5.Lcd.drawImage(CTRL0_IMG, 5, 58)
        M5.Lcd.drawImage(OPT0_IMG, 5, 77)
        M5.Lcd.drawImage(ALT0_IMG, 5, 96)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_key(self, state):
        if state.shift:
            M5.Lcd.drawImage(Aa_IMG, 5, 20)
        else:
            M5.Lcd.drawImage(Aa0_IMG, 5, 20)

        if state.fn:
            M5.Lcd.drawImage(FN_IMG, 5, 39)
        else:
            M5.Lcd.drawImage(FN0_IMG, 5, 39)

        if state.ctrl:
            M5.Lcd.drawImage(CTRL_IMG, 5, 58)
        else:
            M5.Lcd.drawImage(CTRL0_IMG, 5, 58)

        if state.opt:
            M5.Lcd.drawImage(OPT_IMG, 5, 77)
        else:
            M5.Lcd.drawImage(OPT0_IMG, 5, 77)

        if state.alt:
            M5.Lcd.drawImage(ALT_IMG, 5, 96)
        else:
            M5.Lcd.drawImage(ALT0_IMG, 5, 96)
