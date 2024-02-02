from ..app import AppBase
from ..res import (
    SELETE_BK_IMG,
    APPLIST_ICO,
    APPRUN_ICO,
    DEVELOP_ICO,
    EZDATA_ICO,
    SETTING_ICO,
)
from widgets.image import Image
from widgets.label import Label
from collections import namedtuple

Icon = namedtuple("Icon", ["name", "src"])

class LauncherApp(AppBase):
    def __init__(self) -> None:
        super().__init__()
        self._icos = (
            Icon("SETTING", SETTING_ICO),
            Icon("DEVELOP", DEVELOP_ICO),
            Icon("APP.RUN", APPRUN_ICO),
            Icon("APP.LIST", APPLIST_ICO),
            Icon("EZDATA", EZDATA_ICO),
        )
        self._id = 1

    def on_view(self):
        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(34, 29)
        self._bg_img.set_size(206, 103)
        self._bg_img.set_src(SELETE_BK_IMG)

        left = (len(self._icos) -1) if self._id - 1 < 0 else self._id - 1
        self._left_img = Image(use_sprite=False)
        self._left_img.set_pos(49, 43)
        self._left_img.set_size(48, 48)
        self._left_img.set_scale(0.75, 0.75)
        self._left_img.set_src(self._icos[left].src)

        self._left_label = Label(
            "SETTING",
            51,
            90,
            w=48 + 4,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0xFAFAFA,
            bg_color=0x333333,
            font="/system/common/font/Montserrat-Medium-10.vlw",
        )
        self._left_label.setText(self._icos[left].name)

        self._center_img = Image(use_sprite=False)
        self._center_img.set_pos(105, 36)
        self._center_img.set_size(64, 64)
        self._center_img.set_src(self._icos[self._id].src)

        self._center_label = Label(
            "DEVELOP",
            107,
            101,
            w=64,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0xFAFAFA,
            bg_color=0x333333,
            font="/system/common/font/Montserrat-Medium-12.vlw",
        )
        self._center_label.setText(self._icos[self._id].name)

        right = 0 if self._id + 1 > (len(self._icos) -1) else self._id + 1
        self._right_img = Image(use_sprite=False)
        self._right_img.set_pos(177, 43)
        self._right_img.set_size(48, 48)
        self._right_img.set_scale(0.75, 0.75)
        self._right_img.set_src(self._icos[right].src)

        self._right_label = Label(
            "APP.RUN",
            177,
            90,
            w=48 + 4,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0xFAFAFA,
            bg_color=0x333333,
            font="/system/common/font/Montserrat-Medium-10.vlw",
        )
        self._right_label.setText(self._icos[right].name)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass

    def on_uninstall(self):
        pass

    async def _kb_event_handler(self, event, fw):
        left = 0
        right = 0
        refresh = False
        if event.key in (47, 63): # right key
            self._id = self._id + 1 if self._id + 1 < len(self._icos) else 0
            left = (len(self._icos) -1) if self._id - 1 < 0 else self._id - 1
            right = 0 if self._id + 1 > (len(self._icos) -1) else self._id + 1
            refresh = True

        if event.key in (44, 60): #  left key
            self._id = self._id - 1 if self._id - 1 >= 0 else (len(self._icos) -1)
            left = (len(self._icos) -1) if self._id - 1 < 0 else self._id - 1
            right = 0 if self._id + 1 > (len(self._icos) -1) else self._id + 1
            refresh = True

        if refresh:
            self._left_img.set_src(self._icos[left].src)
            self._left_label.setText(self._icos[left].name)
            self._center_img.set_src(self._icos[self._id].src)
            self._center_label.setText(self._icos[self._id].name)
            self._right_img.set_src(self._icos[right].src)
            self._right_label.setText(self._icos[right].name)

        if event.key == 0x0D:
            app = fw._app_selector.index(self._id + 1)
            app.start()
