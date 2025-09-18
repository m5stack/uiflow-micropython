# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from M5 import Widgets
import requests

from driver import soft_timer

# from micropython import schedule


class LabelPlus(Widgets.Label):
    """Create a LabelPlus object that can fetch and display text from a URL.

    :param str text: The initial text to display on the label.
    :param int x: The x position of the label.
    :param int y: The y position of the label.
    :param int size: The font size of the label text.
    :param int text_color: The text color of the label in hexadecimal format.
    :param int bg_color: The background color of the label in hexadecimal format.
    :param font: The font to use for the label text.
    :param str url: The URL to fetch data from.
    :param int period: The update period in milliseconds. If set to 0, the label will not update automatically.
    :param bool enable: Whether to enable automatic updates.
    :param str json_key: The JSON key to extract from the fetched data.
    :param str error_msg: The message to display in case of an error.
    :param int error_msg_color: The text color to use when displaying an error message, in hexadecimal format.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from label_plus import LabelPlus

            label_plus0 = LabelPlus("label_plus0", 7, 10, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18, "http://example.com", 3000, True, "title", "error", 0xFF0000)
    """

    def __init__(
        self,
        text,
        x,
        y,
        size,
        text_color,
        bg_color,
        font,
        url,
        period,
        enable,
        json_key=None,
        error_msg=None,
        error_msg_color=0xFF0000,
    ) -> None:
        self._url = url
        # self._tim = Timer(-1)
        self._period = period
        self._enable = enable
        self._key = json_key
        self._text_color = text_color
        self._bg_color = bg_color
        self._error_msg = error_msg
        self._error_msg_color = error_msg_color
        super(LabelPlus, self).__init__(text, x, y, size, text_color, bg_color, font)

        self._data = error_msg
        self._update()
        self._init_timer()

    def _init_timer(self):
        if self._enable and self._period > 0:
            self._tim = soft_timer.SoftTimer(
                mode=soft_timer.SoftTimer.ONE_SHOT, period=self._period, callback=self._cb
            )

    def deinit(self):
        if self._enable is True:
            self._tim.deinit()
            self._enable = False

    def set_update_enable(self, enable):
        """Enable or disable automatic updates.

        :param bool enable: True to enable automatic updates, False to disable.

        UiFlow2 Code Block:

            |set_update_enable.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus0.set_update_enable(True)
        """
        if self._enable is True and enable is True:
            return
        if self._enable is True:
            self._tim.deinit()
        self._enable = enable
        self._init_timer()

    def _cb(self, tim):
        # schedule(self._update(), self)
        self._update()
        self._tim.init(mode=soft_timer.SoftTimer.ONE_SHOT, period=self._period, callback=self._cb)

    def set_update_period(self, period):
        """Set the update period for automatic updates.

        :param int period: The update period in milliseconds.

        UiFlow2 Code Block:

            |set_update_period.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus0.set_update_period(5000)
        """
        if self._enable:
            self._tim.deinit()
        self._period = period
        self._init_timer()

    def is_valid_data(self) -> bool:
        """Check if the current data is valid (i.e., not an error message).

        :return: True if the current data is valid, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |is_valid_data.png|

        MicroPython Code Block:

            .. code-block:: python

                valid = label_plus0.is_valid_data()
        """
        return False if self._data is self._error_msg else True

    def get_data(self):
        """Get the current data displayed on the label.

        :return: The current data.
        :rtype: str

        UiFlow2 Code Block:

            |get_data.png|

        MicroPython Code Block:

            .. code-block:: python

                data = label_plus0.get_data()
        """
        return self._data

    def setColor(self, fg_color, bg_color=0x000000):  # noqa: N802
        """Sets the text font color of the Label object.

        :param int fg_color: The text color in hexadecimal format.
        :param int bg_color: The background color in hexadecimal format.

        UiFlow2 Code Block:

            |setColor.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus0.setColor(0xFFFFFF, 0x000000)
        """
        self._text_color = fg_color
        super().setColor(fg_color, bg_color)

    def set_url(self, url):
        self._url = url

    def _update(self):
        r = None
        try:
            r = requests.get(self._url)
            if r.status_code == 200:
                if self._key is None:
                    self._data = r.content
                    self._show(str(r.content))
                else:
                    try:
                        data = r.json()
                        self._data = self._find_key(data)
                        self._show(str(self._data))
                    except ValueError:
                        self._show_error("ValueError")
            else:
                error_str = "ERR: " + str(r.status_code)
                self._show_error(error_str)
            r.close()
        except OSError:
            self._show_error("OSError")

    def _find_key(self, data):
        self._data = data.get(self._key)
        if self._data is not None:
            return self._data
        for _, value in data.items():
            if isinstance(value, list):
                for item in value:
                    self._find_key(item)
                    if self._data is not None:
                        return self._data
            elif isinstance(value, dict):
                self._find_key(value)
            if self._data is not None:
                return self._data

    def update(self):
        self._tim.deinit()
        self._update()
        self._init_timer()

    def show_value_of_key(self, key):
        self._tim.deinit()
        self._key = key
        self._update()
        self._init_timer()

    def _show_error(self, error_msg):
        super().setColor(self._error_msg_color)
        if self._error_msg is None:
            self._data = error_msg
            super().setText(error_msg)
        else:
            self._data = self._error_msg
            super().setText(self._error_msg)

    def _show(self, text):
        super().setColor(self._text_color)
        super().setText(text)
