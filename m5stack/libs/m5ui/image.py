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
        rotation=0,
        scale_x=1.0,
        scale_y=1.0,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_src("S:" + path)
        self.set_pos(x, y)
        self.set_width(lv.SIZE_CONTENT)
        self.set_height(lv.SIZE_CONTENT)
        self.set_rotation(rotation)
        self.set_scale(scale_x, scale_y)
        self.set_pivot(0, 0)

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

    def set_rotation(self, rotation):
        """Set the rotation of the image.

        :param int rotation: The rotation angle in degrees (0, 90, 180, 270).

        UiFlow2 Code Block:

            |set_rotation.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_rotation(90)
        """
        super().set_rotation(rotation * 10)

    def set_scale(self, scale, scale_y=None):
        """Set the scale of the image.

        :param float scale_x: The horizontal scale factor.
        :param float scale_y: The vertical scale factor.

        UiFlow2 Code Block:

            |set_scale.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_scale(2.0, 2.0)
        """
        if scale_y is not None:
            super().set_scale_x(int(scale * 256))
            super().set_scale_y(int(scale_y * 256))
        else:
            super().set_scale(scale * 256)

    def set_style_radius(self, radius: int, part: int) -> None:
        if radius < 0:
            raise ValueError("Radius must be a non-negative integer.")
        super().set_style_radius(radius, part)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
