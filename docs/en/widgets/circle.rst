.. currentmodule:: Widgets

class Circle -- display circle
==============================

Circle is the basic object type used to display text.

.. include:: ../refs/widgets.circle.ref

Micropython Example:

    .. literalinclude:: ../../../examples/widgets/circle/circle_core2_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |circle_core2_example.m5f2|

Constructors
------------

.. class:: Widgets.Circle(x: int, y: int, r: int, fg_color: int=0xffffff, bg_color: int=0xffffff)

    Create a Circle object. It accepts the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.
        - ``r`` is the radius of the circle.
        - ``fg_color`` is the foreground color of the displayed circle.
        - ``bg_color`` is the background color of the displayed circle.

Methods
-------

.. method:: Widgets.setColor(fg_color: int=0xffffff, bg_color: int=0x000000)

    Set the color of the Circle object. Accept the following parameters:

        - ``fg_color`` is the foreground color of the displayed circle.
        - ``bg_color`` is the background color of the displayed circle.

    UIFLOW2:

        |setColor.png|


.. method:: Widgets.setCursor(x: int, y: int)

    Set the position of the Circle object. Accept the following parameters:

        - ``x`` is the starting X-axis coordinate displayed.
        - ``y`` is the starting Y-axis coordinate displayed.

    UIFLOW2:

        |setCursor.png|

.. method:: Widgets.setRadius(radius: int)

    Set the radius of the Circle object. Accept the following parameters:

        - ``r`` is the radius of the circle.

    UIFLOW2:

        |setRadius.png|

.. method:: Widgets.setVisible(visible: bool)

    Set the visibility of the Circle object. Accept the following parameters:

        - ``visible`` is the visibility of the displayed circle.

    UIFLOW2:

        |setVisible.png|
