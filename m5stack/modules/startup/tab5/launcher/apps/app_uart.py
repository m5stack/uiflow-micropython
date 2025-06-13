# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .app import AppBase
from ..hal import *
from ..common import *
import lvgl as lv
import asyncio


class AppUart(AppBase):
    class _UartState:
        CLOSED = 0
        OPENED = 1

    _BAUDRATE_OPTIONS = [115200]
    _TX_PIN_OPTIONS = [20]
    _RX_PIN_OPTIONS = [21]

    async def main(self):
        self._state = self._UartState.CLOSED

        self._ta_rx = lv.textarea(self.get_app_panel())
        self._ta_rx.align(lv.ALIGN.TOP_LEFT, 14, 15)
        self._ta_rx.set_size(660, 145)
        self._ta_rx.set_style_border_width(0, lv.PART.MAIN)
        self._ta_rx.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        self._ta_rx.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

        self._ta_tx = lv.textarea(self.get_app_panel())
        self._ta_tx.align(lv.ALIGN.TOP_LEFT, 14, 183)
        self._ta_tx.set_size(660, 46)
        self._ta_tx.set_one_line(True)
        self._ta_tx.set_style_border_width(0, lv.PART.MAIN)
        self._ta_tx.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        self._ta_tx.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN)

        self._kb = lv.keyboard(self.get_app_panel())
        self._kb.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._kb.set_height(lv.pct(52))
        self._kb.add_event_cb(self._handle_kb_clicked, lv.EVENT.CLICKED, None)
        self._kb.set_textarea(self._ta_tx)

        self._btn_open = lv.button(self.get_app_panel())
        self._btn_open.align(lv.ALIGN.TOP_MID, 410, 183)
        self._btn_open.set_size(280, 42)
        self._btn_open.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_open.add_event_cb(self._handle_open_btn_clicked, lv.EVENT.CLICKED, None)

        self._label_open = lv.label(self._btn_open)
        self._label_open.set_align(lv.ALIGN.CENTER)
        self._label_open.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)

        self._btn_clear = lv.button(self.get_app_panel())
        self._btn_clear.align(lv.ALIGN.TOP_MID, 185, 102)
        self._btn_clear.set_size(110, 42)
        self._btn_clear.set_style_bg_color(lv.color_hex(0x2DA4E0), lv.PART.MAIN)
        self._btn_clear.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_clear.add_event_cb(self._handle_clear_btn_clicked, lv.EVENT.CLICKED, None)

        self._label_clear = lv.label(self._btn_clear)
        self._label_clear.set_align(lv.ALIGN.CENTER)
        self._label_clear.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_clear.set_text("CLEAR")

        self._btn_send = lv.button(self.get_app_panel())
        self._btn_send.align(lv.ALIGN.TOP_MID, 185, 183)
        self._btn_send.set_size(110, 42)
        self._btn_send.set_style_bg_color(lv.color_hex(0x2DA4E0), lv.PART.MAIN)
        self._btn_send.set_style_shadow_width(0, lv.PART.MAIN)
        self._btn_send.add_event_cb(self._handle_send_btn_clicked, lv.EVENT.CLICKED, None)

        self._label_send = lv.label(self._btn_send)
        self._label_send.set_align(lv.ALIGN.CENTER)
        self._label_send.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._label_send.set_text("SEND")

        self._dd_baudrate = lv.dropdown(self.get_app_panel())
        self._dd_baudrate.align(lv.ALIGN.TOP_MID, 470, 15)
        self._dd_baudrate.set_size(164, 48)
        self._dd_baudrate.set_style_shadow_width(0, lv.PART.MAIN)
        self._dd_baudrate.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._dd_baudrate.set_style_border_width(0, lv.PART.MAIN)
        self._dd_baudrate.set_options("\n".join([str(b) for b in self._BAUDRATE_OPTIONS]))

        self._dd_tx_pin = lv.dropdown(self.get_app_panel())
        self._dd_tx_pin.align(lv.ALIGN.TOP_MID, 352, 98)
        self._dd_tx_pin.set_size(98, 48)
        self._dd_tx_pin.set_style_shadow_width(0, lv.PART.MAIN)
        self._dd_tx_pin.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._dd_tx_pin.set_style_border_width(0, lv.PART.MAIN)
        self._dd_tx_pin.set_options("\n".join([str(p) for p in self._TX_PIN_OPTIONS]))

        self._dd_rx_pin = lv.dropdown(self.get_app_panel())
        self._dd_rx_pin.align(lv.ALIGN.TOP_MID, 503, 98)
        self._dd_rx_pin.set_size(98, 48)
        self._dd_rx_pin.set_style_shadow_width(0, lv.PART.MAIN)
        self._dd_rx_pin.set_style_text_font(lv.font_montserrat_20, lv.PART.MAIN)
        self._dd_rx_pin.set_style_border_width(0, lv.PART.MAIN)
        self._dd_rx_pin.set_options("\n".join([str(p) for p in self._RX_PIN_OPTIONS]))

        self._label_baudrate = lv.label(self.get_app_panel())
        self._label_baudrate.align(lv.ALIGN.TOP_MID, 327, 28)
        self._label_baudrate.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        self._label_baudrate.set_text("Baudrate:")

        self._label_tx_pin = lv.label(self.get_app_panel())
        self._label_tx_pin.align(lv.ALIGN.TOP_MID, 278, 112)
        self._label_tx_pin.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        self._label_tx_pin.set_text("TX:")

        self._label_rx_pin = lv.label(self.get_app_panel())
        self._label_rx_pin.align(lv.ALIGN.TOP_MID, 427, 112)
        self._label_rx_pin.set_style_text_font(lv.font_montserrat_18, lv.PART.MAIN)
        self._label_rx_pin.set_text("RX:")

        self._set_state_to(self._UartState.CLOSED)

        while True:
            await asyncio.sleep(0.2)
            if self._state == self._UartState.OPENED:
                data = get_hal().uart_read()
                if data:
                    for c in data:
                        self._ta_rx.add_char(c)

    def _handle_kb_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()

    def _handle_open_btn_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._state == self._UartState.CLOSED:
            self._set_state_to(self._UartState.OPENED)
        else:
            self._set_state_to(self._UartState.CLOSED)

    def _handle_clear_btn_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        self._ta_rx.set_text("")

    def _handle_send_btn_clicked(self, e: lv.event_t):
        get_hal().play_click_sfx()
        if self._state == self._UartState.OPENED:
            get_hal().uart_write(self._ta_tx.get_text())

    def _set_state_to(self, new_state: _UartState):
        if new_state == self._UartState.OPENED:
            # Update ui
            self._btn_open.set_style_bg_color(lv.color_hex(0x1EB561), lv.PART.MAIN)
            self._label_open.set_text("CLOSE")

            # Init uart
            get_hal().uart_init(
                self._BAUDRATE_OPTIONS[self._dd_baudrate.get_selected()],
                self._TX_PIN_OPTIONS[self._dd_tx_pin.get_selected()],
                self._RX_PIN_OPTIONS[self._dd_rx_pin.get_selected()],
            )
        else:
            # Update ui
            self._btn_open.set_style_bg_color(lv.color_hex(0x2DA4E0), lv.PART.MAIN)
            self._label_open.set_text("OPEN")

            # Deinit uart
            get_hal().uart_deinit()

        self._state = new_state

    def on_cleanup(self):
        get_hal().uart_deinit()
