.. currentmodule:: Widgets

class Label -- display text
===========================

.. include:: ../refs/widgets.label.ref

Label is the basic object type used to display text.


Micropython Example:

    .. literalinclude:: ../../../examples/widgets/label/cores3_label_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_label_example.m5f2|


Constructors
------------

.. class:: Widgets.Label(text: str, x: int, y: int, text_sz: float, text_c: int=0xFFFFFF, bg_c: int=0x000000, font=None, parent=None)

    Create a Label object. It accepts the following parameters:

        - ``text`` is the text to be displayed.
        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.
        - ``text_sz`` is the font size for displaying text, usually 1.0.
        - ``text_c`` is the font color for displaying text. The default is white.
        - bg_c is the background color of the displayed text, the default is black.
        - ``font`` is the set of fonts used to display text. For the built-in fonts, see ``Widgets.FONTS``.
        - parent is the output target of the Label object, the default output is to the LCD, can also be output to the Canvas.

Methods
-------

.. method:: Label.setColor(text_c:int, bg_c: int=-1)

    Sets the text font color of the Label object. Accept the following parameters:

        - ``text_c`` is the font color for displaying text.
        - bg_c is the background color of the displayed text, the default is black.

    UIFLOW2:

        |setColor.png|


.. method:: Label.setCursor(x: int, y: int)

    Sets the starting coordinates of the Label object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

        |setCursor.png|

.. method:: Label.setFont(font)

    Sets the font set of the Label object. font is the set of fonts used to display text, the built-in font, see ``Widgets.FONTS``.

    UIFLOW2:

        |setFont.png|

.. method:: Label.setSize(text_sz: float)

    Set the text font size of the Label object, text_sz is the font size of the displayed text.

    UIFLOW2:

        |setSize.png|

.. method:: Label.setText(text: str)

    Sets the text content of the Label object.

    UIFLOW2:

        |setText.png|

.. method:: Label.setVisible(visible: bool)
    
    Set the visible property of the Label object, when ``visible`` is True, the Label object content will be visible, otherwise it will not be visible.

    UIFLOW2:

        |setVisible.png|
