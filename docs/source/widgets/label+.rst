.. currentmodule:: Widgets

class LabelPlus -- display remote text
======================================

The `LabelPlus` class extends the `Widgets.Label` class to provide additional functionalities for handling text with dynamic updates.

Currently only accepts strings in json format, and extracts data through ``json_key``.

.. include:: ../refs/widgets.label+.ref

UiFlow2 Example
---------------

Simple Usage
^^^^^^^^^^^^

Open the |cores3_labelplus_example.m5f2| project in UiFlow2.

This example demonstrates how to create and manipulate a LabelPlus widget.

UiFlow2 Code Block:

    |cores3_labelplus_example.png|

Example output:

    None


MicroPython Example
-------------------

Simple Usage
^^^^^^^^^^^^

This example demonstrates how to create and manipulate a LabelPlus widget.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/widgets/labelplus/cores3_labelplus_example.py

Example output:

    None


**API**
-------

LabelPlus
^^^^^^^^^

.. autoclass:: label_plus.LabelPlus
    :members:
    :member-order: bysource

    .. py:method:: setText(text)

        Set the text of the LabelPlus widget.

        :param str text: The text to set on the label.

        UiFlow2 Code Block:

            |setText.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus_0.setText("New Text")

    .. py:method:: setCursor(x=0, y=0)

        Sets the starting coordinates of the text cursor in the LabelPlus widget.

        :param int x: The x-coordinate of the cursor.
        :param int y: The y-coordinate of the cursor.

        UiFlow2 Code Block:

            |setCursor.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus_0.setCursor(10, 20)

    .. py:method:: setSize(size)

        Sets the font size of the text in the LabelPlus widget.

        :param float size: The font size to set.

        UiFlow2 Code Block:

            |setSize.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus_0.setSize(1.5)

    .. py:method:: setFont(font)

        Sets the font of the text in the LabelPlus widget.

        :param str font: The font to set (e.g., Widgets.FONTS.DejaVu9).

        UiFlow2 Code Block:

            |setFont.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus_0.setFont(Widgets.FONTS.DejaVu9)

    .. py:method:: setVisible(visible)

        Set the visible property of the LabelPlus widget.

        :param bool visible: True to make the label visible, False to hide it.

        UiFlow2 Code Block:

            |setVisible.png|

        MicroPython Code Block:

            .. code-block:: python

                label_plus_0.setVisible(True)
