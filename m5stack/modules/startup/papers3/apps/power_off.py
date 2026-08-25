# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import layout
import M5
import time


# Reference geometry (540x960 design space). The idle card is baked into the
# three page backgrounds. The runtime assets are cut out of those backgrounds,
# one pair per page, because the rows where the sweep of the app list tab cuts
# across the top of the card differ from page to page.
_CARD_X = 492
_CARD_Y = 479
_HIT_X = 470
_HIT_Y = 504  # one row below the app list tab, which ends at 503
_HIT_W = 100
_HIT_H = 158
_CONFIRM_TIMEOUT_MS = 5000
_ASSETS = {
    "flow.png": ("power_flow.png", "power_flow_confirm.png"),
    "config.png": ("power_config.png", "power_config_confirm.png"),
    "applist.png": ("power_applist.png", "power_applist_confirm.png"),
}


class PowerOffButton:
    """Power off tab, drawn below the app tabs, confirmed by a second tap.

    The first tap fills the card gray to show that it is armed, a second tap
    calls ``M5.Power.powerOff()``. The gray state is dropped again when it is
    not confirmed within ``_CONFIRM_TIMEOUT_MS``, or when another area is
    touched. Black stays reserved for the tab of the page that is showing.
    """

    def __init__(self, parent=M5.Lcd) -> None:
        self._lcd = parent
        self._x = layout.x(_CARD_X)
        self._y = layout.y(_CARD_Y)
        self._hit_x = layout.x(_HIT_X)
        self._hit_y = layout.y(_HIT_Y)
        self._hit_w = layout.size(_HIT_W)
        self._hit_h = layout.size(_HIT_H)
        self._cache = {}
        self._assets = None
        self._confirming = False
        self._confirm_time = 0
        self._dirty = False

    def show(self, app):
        # The app just repainted its background, which already carries the idle
        # card, so only the page specific assets are picked up here.
        self._assets = _ASSETS.get(getattr(app, "BACKGROUND", None))
        self._confirming = False
        self._dirty = False

    def handle(self, x, y):
        if not self._is_ready():
            return False
        if not self._is_select(x, y):
            if self._confirming:
                self._confirming = False
                self._dirty = True
            return False
        if self._confirming:
            self._power_off()
        else:
            self._confirming = True
            self._confirm_time = time.ticks_ms()
            self._redraw()
        return True

    def tick(self):
        if self._confirming and (
            time.ticks_diff(time.ticks_ms(), self._confirm_time) > _CONFIRM_TIMEOUT_MS
        ):
            self._confirming = False
            self._dirty = True
        if self._dirty:
            self._dirty = False
            self._redraw()

    def _power_off(self):
        print("Power off requested from startup menu")
        self._confirming = False
        self._dirty = False
        try:
            M5.Power.powerOff()
        except Exception as error:
            print("Power off failed: %s" % error)
            self._redraw()

    def _is_ready(self):
        return self._assets is not None and None not in (
            self._image(self._assets[0]),
            self._image(self._assets[1]),
        )

    def _is_select(self, x, y):
        if x < self._hit_x or x > (self._hit_x + self._hit_w):
            return False
        if y < self._hit_y or y > (self._hit_y + self._hit_h):
            return False
        return True

    def _redraw(self):
        layout.begin_full_refresh()
        try:
            self._draw()
        finally:
            layout.end_full_refresh()

    def _draw(self):
        image = self._image(self._assets[1 if self._confirming else 0])
        if image is not None:
            self._lcd.drawImage(image, self._x, self._y)

    def _image(self, name):
        if name not in self._cache:
            try:
                self._cache[name] = layout.image_source(layout.resource_path(name))
            except OSError as error:
                print("Power off image %s not available: %s" % (name, error))
                self._cache[name] = None
        return self._cache[name]
