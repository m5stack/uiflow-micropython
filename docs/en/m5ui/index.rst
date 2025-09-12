M5UI
====

.. module:: m5ui
    :synopsis: A UI library based on LVGL v9.3

M5UI is a UI library based on LVGL v9.3. It provides a set of widgets and functions to create user interfaces for M5Stack devices.

It has been adapted for M5Stack devices and you only need to call ``m5ui.init()`` to start using it.

M5 Series Display Libraries
---------------------------

1. Display
^^^^^^^^^^^
- A low-level graphics library providing basic screen drawing, text, lines, and color management.
- Can be used independently, suitable for scenarios that only require drawing graphics or text.

2. Widgets
^^^^^^^^^^^
- A basic UI widget library providing labels, image displays, and other UI controls.
- Built on top of M5GFX.
- Suitable for simple interactive UI elements.

3. M5UI
^^^^^^^^
- A high-level UI framework based on LVGL.
- Provides page management, multi-widget layouts, and unified event handling.

Usage Tips
^^^^^^^^^^
- ⚠️ Do not mix M5GFX, M5Widgets, and M5UI simultaneously, as it may cause rendering issues or event conflicts.
- For graphics-only drawing → use M5GFX.
- For simple interactive widgets → use M5Widgets.
- For multi-page UI → use M5UI.


Functions
---------

.. function:: m5ui.init()

    Initialize the M5UI library. This function must be called before using any other M5UI functions.

    :return: None


.. function:: m5ui.deinit()

    Deinitialize the M5UI library. This function should be called when you no longer need to use M5UI.

    :return: None


Classes
-------

.. toctree::
    :maxdepth: 1

    page.rst
    arc.rst
    bar.rst
    button.rst
    buttonmatrix.rst
    calendar.rst
    canvas.rst
    checkbox.rst
    dropdown.rst
    image.rst
    keyboard.rst
    label.rst
    line.rst
    list.rst
    msgbox.rst
    roller.rst
    scale.rst
    slider.rst
    spinbox.rst
    spinner.rst
    switch.rst
    textarea.rst
    win.rst
