# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Image(lv.image):
    """Create a image object.

    :param str path: The path of the image file.
    :param int x: The x position of the image.
    :param int y: The y position of the image.
    :param lv.obj parent: The parent object to attach the image to. If not specified, the image will be attached to the default screen.

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Image
            import lvgl as lv

            m5ui.init()
            image_0 = M5Image("/flash/res/img/defalut.jpg", x=10, y=10, parent=page0)
            image_1 = M5Image("/flash/res/img/uiflow.jpg", x=50, y=50, parent=page0)
    """

    def __init__(
        self,
        path,
        x=0,
        y=0,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_src("S:" + path)
        self.set_pos(x, y)

    def set_image(self, path):
        """Set the image to be displayed.

        :param str path: The path of the image file.

        UiFlow2 Code Block:

            |set_image.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_image("/flash/res/img/uiflow.jpg")
                image_1.set_image("/sd/uiflow.png")
        """
        self.set_src("S:" + path)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
