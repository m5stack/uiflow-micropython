# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import get_hal
import lvgl as lv
import asyncio


class AdcPanel:
    class _AdcState:
        CLOSED = 0
        OPENED = 1

    def __init__(self, parent: lv.obj, pos_x: int, pos_y: int, pins: list[int]):
        self._state = self._AdcState.CLOSED
        self._pins = pins
        self._current_pin = 0

        panel = lv.obj(parent)
        panel.set_size(530, 200)
        panel.align(lv.ALIGN.TOP_LEFT, pos_x, pos_y)
        panel.set_style_border_width(0, lv.PART.MAIN)
        panel.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        panel.set_style_pad_all(0, lv.PART.MAIN)

        self._chart = lv.chart(panel)
        self._chart.set_size(360, 200)
        self._chart.align(lv.ALIGN.LEFT_MID, 0, 0)
        self._chart.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)
        self._chart.set_type(lv.chart.TYPE.LINE)
        self._chart.set_div_line_count(13, 22)
        self._chart.set_update_mode(lv.chart.UPDATE_MODE.SHIFT)
        self._chart.set_point_count(100)
        self._chart.set_axis_range(lv.chart.AXIS.PRIMARY_Y, 1800, 4096)
        self._chart.set_style_size(0, 0, lv.PART.INDICATOR)

        self._chart_series = self._chart.add_series(
            lv.palette_main(lv.PALETTE.RED), lv.chart.AXIS.PRIMARY_Y
        )

        self._label_value = lv.label(self._chart)
        self._label_value.align(lv.ALIGN.TOP_RIGHT, -5, -5)
        self._label_value.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        self._label_value.set_style_text_color(lv.color_hex(0x6A6A6A), lv.PART.MAIN)
        self._label_value.set_style_text_align(lv.TEXT_ALIGN.RIGHT, lv.PART.MAIN)

        self._btn_open = lv.button(panel)
        self._btn_open.set_size(140, 48)
        self._btn_open.align(lv.ALIGN.TOP_LEFT, 383, 146)
        self._btn_open.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_open.add_event_cb(self._handle_open_btn_clicked, lv.EVENT.CLICKED, None)

        self._label_open = lv.label(self._btn_open)
        self._label_open.set_align(lv.ALIGN.CENTER)
        self._label_open.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)

        self._dd_pins = lv.dropdown(panel)
        self._dd_pins.align(lv.ALIGN.TOP_LEFT, 426, 71)
        self._dd_pins.set_size(97, 48)
        self._dd_pins.set_style_shadow_width(0, lv.PART.MAIN)
        self._dd_pins.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._dd_pins.set_style_border_width(0, lv.PART.MAIN)
        self._dd_pins.set_options("\n".join([str(b) for b in self._pins]))

        label_dd_pins = lv.label(panel)
        label_dd_pins.align_to(self._dd_pins, lv.ALIGN.OUT_LEFT_MID, -48, -2)
        label_dd_pins.set_text("PIN:")
        label_dd_pins.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)

        self._set_state_to(self._AdcState.CLOSED)

    def _handle_open_btn_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._state == self._AdcState.CLOSED:
            self._set_state_to(self._AdcState.OPENED)
        else:
            self._set_state_to(self._AdcState.CLOSED)

    def _set_state_to(self, new_state: _AdcState):
        if new_state == self._AdcState.OPENED:
            # Update ui
            self._btn_open.set_style_bg_color(lv.color_hex(0x1EB561), lv.PART.MAIN)
            self._label_open.set_text("CLOSE")

            # Init adc
            self._current_pin = self._pins[self._dd_pins.get_selected()]
            get_hal().adc_init(self._current_pin)
        else:
            # Update ui
            self._btn_open.set_style_bg_color(lv.color_hex(0x2DA4E0), lv.PART.MAIN)
            self._label_open.set_text("OPEN")

            # Deinit adc
            get_hal().adc_deinit(self._current_pin)

        self._state = new_state

    def update(self):
        if self._state == self._AdcState.OPENED:
            value = get_hal().adc_read(self._current_pin)
            self._label_value.set_text(f"{value}")
            self._chart.set_next_value(self._chart_series, value)
            self._chart.refresh()

    def cleanup(self):
        get_hal().adc_deinit(self._current_pin)

        self._label_value.delete()
        self._label_value = None
        self._chart_series = None
        self._chart.delete()
        self._chart = None
        self._label_open.delete()
        self._label_open = None
        self._btn_open.delete()
        self._btn_open = None
        self._dd_pins.delete()
        self._dd_pins = None


class AppAdc(AppBase):
    async def main(self):
        self._adc_panels = []
        self._adc_panels.append(AdcPanel(self.get_app_panel(), 32, 29, [54]))
        self._adc_panels.append(AdcPanel(self.get_app_panel(), 586, 29, [53]))
        self._adc_panels.append(AdcPanel(self.get_app_panel(), 32, 270, [50]))
        self._adc_panels.append(AdcPanel(self.get_app_panel(), 586, 270, [49]))

        while True:
            await asyncio.sleep_ms(500)
            for panel in self._adc_panels:
                panel.update()

    def on_cleanup(self):
        for panel in self._adc_panels:
            panel.cleanup()
