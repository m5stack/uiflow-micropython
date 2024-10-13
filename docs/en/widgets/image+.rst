.. currentmodule:: Widgets

class ImagePlus -- display remote image
=========================================

The `ImagePlus` class extends the `Widgets.Image` class to provide additional functionalities for handling images with dynamic updates.

.. include:: ../refs/widgets.image+.ref

Micropython Example:

    .. literalinclude:: ../../../examples/widgets/imageplus/imageplus_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |imageplus_cores3_example.m5f2|

Constructors
------------

.. class:: ImagePlus(url, x, y, enable, period, default_img="res/img/default.jpg", parent=None)

    Create an `ImagePlus` object. It accepts the following parameters:

        - ``url`` is the URL of the image to be fetched and displayed.
        - ``x`` is the starting X-axis coordinate where the image will be displayed.
        - ``y`` is the starting Y-axis coordinate where the image will be displayed.
        - ``enable`` is a boolean indicating whether periodic updates of the image are enabled.
        - ``period`` is the update period in milliseconds when `enable` is `True`.
        - ``default_img`` is the path to the default image file to be displayed if the URL fetch fails. Supported formats are BMP, JPG, and PNG. Default is `"res/img/default.jpg"`.
        - ``parent`` is the graphical object on which the image will be drawn. If not provided, the default display will be used.

Methods
-------

.. method:: ImagePlus.set_update_enable(enable: bool)

    Enable or disable periodic updates of the image. Accept the following parameters:

        - ``enable`` is a boolean indicating whether updates should be enabled.

    UIFLOW2:

        |set_update_enable.png|

.. method:: ImagePlus.set_update_period(period: int)

    Set the update period for fetching and displaying the image. Accept the following parameters:

        - ``period`` is the update period in milliseconds.

    UIFLOW2:

        |set_update_period.png|

.. method:: ImagePlus.setCursor(x: int, y: int)

    Set the position of the ImagePlus object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

        |setCursor.png|

.. method:: ImagePlus.setVisible(visible: bool)

    Set the visibility of the ImagePlus object. Accept the following parameters:

        - ``visible`` is the visibility of the displayed iamge.

    UIFLOW2:

        |setVisible.png|


.. method:: ImagePlus.is_valid_image() -> bool

    Check if the fetched image is valid. Returns `True` if the image is valid, otherwise `False`.

    UIFLOW2:

        |is_valid_image.png|