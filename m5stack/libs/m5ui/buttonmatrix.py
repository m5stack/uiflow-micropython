# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5ButtonMatrix(lv.buttonmatrix):
    """Create a button matrix object.

    :param list map: A list of button labels. Use "\\\\n" to create a new row.
    :param int x: The x position of the button matrix.
    :param int y: The y position of the button matrix.
    :param int w: The width of the button matrix.
    :param int h: The height of the button matrix.
    :param m5ui.M5TextArea target_textarea: A M5TextArea to display the button text when a button is pressed.
    :param lv.obj parent: The parent object to attach the button matrix to.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            import m5ui
            import lvgl as lv

            m5ui.init()
            page0 = m5ui.M5Page()
            page0.screen_load()
            textarea0 = m5ui.M5TextArea(x=10, y=10, w=200, h=60, parent=page0)
            buttonmatrix_0 = m5ui.M5ButtonMatrix(
                ["0", "1", "2", "3", "4","\\n", "5", "6", "7", "8", "9",],
                x=10, y=80, w=260, h=130,
                target_textarea=textarea0,
                parent=page0
            )

    """

    def __init__(
        self,
        map,
        x=0,
        y=0,
        w=260,
        h=130,
        target_textarea=None,
        parent=None,
    ):
        super().__init__(parent)
        self.set_map(map)
        self.set_pos(x, y)
        self.set_size(w, h)

        self.add_event_cb(self.value_changed_event, lv.EVENT.VALUE_CHANGED, None)
        self.textarea = target_textarea  # To hold a reference to a M5TextArea if set

    def value_changed_event(self, event_struct):
        btn_id = self.get_selected_button()
        if self.textarea:
            self.textarea.add_text(self.get_button_text(btn_id))

    def toggle_button_ctrl(self, btn_id, ctrl):
        """Toggle control flags for a specific button.

        :param int btn_id: The button ID to toggle control flags for.
        :param int ctrl: The control flags to toggle.

        UiFlow2 Code Block:

            |toggle_button_ctrl.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.toggle_button_ctrl(0, lv.buttonmatrix.CTRL.HIDDEN)
        """
        if self.has_button_ctrl(btn_id, ctrl):
            self.clear_button_ctrl(btn_id, ctrl)
        else:
            self.set_button_ctrl(btn_id, ctrl)

    def set_textarea(self, textarea):
        """Set a M5TextArea to display button text.

        :param m5ui.M5TextArea textarea: The M5TextArea to set.

        UiFlow2 Code Block:

            |set_textarea.png|

        MicroPython Code Block:

            .. code-block:: python

                buttonmatrix_0.set_textarea(textarea0)
        """
        self.textarea = textarea

    def get_textarea(self):
        """Get the currently set M5TextArea.

        :return: The M5TextArea currently set for the button matrix.
        :rtype: m5ui.M5TextArea

        UiFlow2 Code Block:

            |get_textarea.png|

        MicroPython Code Block:

            .. code-block:: python

                textarea = buttonmatrix_0.get_textarea()
        """
        return self.textarea

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
