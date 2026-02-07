.. currentmodule:: m5ui

M5Image
========

.. include:: ../refs/m5ui.image.ref

M5Image is a widget that can be used to create image in the user interface.

UiFlow2 Example
---------------

show image
^^^^^^^^^^^^

Open the |cores3_show_image_example.m5f2| project in UiFlow2.

This example shows how to display an image on the screen.

UiFlow2 Code Block:

    |cores3_show_image_example.png|

Example output:

    None


MicroPython Example
-------------------

show image
^^^^^^^^^^^^

This example shows how to display an image on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/image/cores3_show_image_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5Image
^^^^^^^^

.. autoclass:: m5ui.image.M5Image
    :members:

    .. py:method:: set_flag(flag, value)

        Set a flag on the object. If ``value`` is True, the flag is added; if False, the flag is removed.

        :param int flag: The flag to set.
        :param bool value: If True, the flag is added; if False, the flag is removed.

        UiFlow2 Code Block:

            |set_hidden.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_flag(lv.obj.FLAG.HIDDEN, True)

    .. py:method:: set_pos(x, y)

        Set the position of the image.

        :param int x: The x-coordinate of the image.
        :param int y: The y-coordinate of the image.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_pos(100, 100)

    .. py:method:: set_x(x)

        Set the x-coordinate of the image.

        :param int x: The x-coordinate of the image.

        UiFlow2 Code Block:

            |set_x.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_x(100)

    .. py:method:: set_y(y)

        Set the y-coordinate of the image.

        :param int y: The y-coordinate of the image.

        UiFlow2 Code Block:

            |set_y.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.set_y(100)

    .. py::method:: get_width()

        Get the width of the image.

        :return: The width of the image.
        :rtype: int

        UiFlow2 Code Block:

            |get_width.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.get_width()

    .. py::method:: get_height()

        Get the height of the image.

        :return: The height of the image.
        :rtype: int

        UiFlow2 Code Block:

            |get_height.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.get_height()

    .. py:method:: align_to(obj, align, x, y)

        Align the image to another object.

        :param lv.obj obj: The object to align to.
        :param int align: The alignment type.
        :param int x: The x-offset from the aligned object.
        :param int y: The y-offset from the aligned object.

        UiFlow2 Code Block:

            |align_to.png|

        MicroPython Code Block:

            .. code-block:: python

                image_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
