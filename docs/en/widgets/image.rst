.. currentmodule:: Widgets

class Image -- display image
==============================

Image is the basic object type used to display images.

.. include:: ../refs/widgets.image.ref

Micropython Example:

    .. literalinclude:: ../../../examples/widgets/image/image_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |image_cores3_example.m5f2|

Constructors
------------

.. class:: Widgets.Image(str: file, x: int, y: int, parent)

    Create an Image object. It accepts the following parameters:

        - ``file`` is the path to the image file to be displayed. Supported formats are BMP, JPG, and PNG.
        - ``x`` is the starting X-axis coordinate where the image will be displayed.
        - ``y`` is the starting Y-axis coordinate where the image will be displayed.
        - ``parent`` is the graphical object on which the image will be drawn. If not provided, the default display will be used.

Methods
-------

.. method:: Widgets.setCursor(x: int, y: int)
    :no-index:

    Set the position of the Imgae object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

        |setCursor.png|

.. method:: Widgets.setImage(str: file)

    Set the image to be displayed.

        - ``file`` is the path to the new image file to be displayed.

    UIFLOW2:

        |setImage.png|

        |setImage1.png|


.. method:: Widgets.setVisible(visible: bool)
    :no-index:

    Set the visibility of the Imgae object. Accept the following parameters:

        - ``visible`` is the visibility of the displayed image.

    UIFLOW2:

        |setVisible.png|
