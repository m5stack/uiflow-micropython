:mod:`Widgets` --- A basic UI library
=====================================

.. module:: Widgets
    :synopsis: A basic UI library

.. include:: ../refs/widgets.ref

M5 Series Display Libraries
---------------------------

1. Display
^^^^^^^^^^^
- A low-level graphics library providing basic screen drawing, text, lines, and color management.
- Can be used independently, suitable for scenarios that only require drawing graphics or text.

2. M5Widgets
^^^^^^^^^^^^^
- A basic UI widget library providing labels, image displays, and other UI controls.
- Built on top of M5GFX.
- Suitable for simple interactive UI elements.
- **Recommendation**: For new interactive UI projects, prefer M5UI/LVGL. Use M5.Widgets for simple or legacy UI components.

3. M5UI
^^^^^^^^
- A high-level UI framework based on LVGL.
- Provides page management, multi-widget layouts, and unified event handling.
- **Recommendation**: Prefer M5UI/LVGL for new interactive UI projects.

Usage Tips
^^^^^^^^^^
- ⚠️ Do not mix M5GFX, M5Widgets, and M5UI simultaneously, as it may cause rendering issues or event conflicts.
- For graphics-only drawing → use M5GFX.
- For simple interactive widgets → use M5Widgets.
- For multi-page UI → use M5UI/LVGL (recommended for new projects).

Micropython Example:

    .. literalinclude:: ../../../examples/widgets/screen/cores3_widgets_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_widgets_example.m5f2|

Screen functions
----------------

.. function:: Widgets.setBrightness(brightness: int)

    Set the backlight of the monitor。``brightness`` ranges from 0 to 255.

    UIFLOW2:

        |setBrightness.png|

.. function:: Widgets.fillScreen(color: int)

    Set the background color of the monitor. ``color`` accepts the color code of RGB888.

    UIFLOW2:

        |fillScreen.png|

.. function:: Widgets.setRotation(rotation: int)

    Set the rotation Angle of the display.

    The ``rotation`` parameter only accepts the following values:

        - ``0``: 0°
        - ``1``: 90°
        - ``2``: 180°
        - ``3``: 270°

    .. note::

        See :ref:`display-rotation` for board-specific dimensions and migration from older examples. Set the desired rotation before initializing M5UI/LVGL.

    UIFLOW2:

        |setRotation.png|

Classes
-------

.. toctree::
    :maxdepth: 1

    circle.rst
    image.rst
    image+.rst
    label.rst
    label+.rst
