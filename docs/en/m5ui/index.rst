M5UI
====

.. module:: m5ui
    :synopsis: A UI library based on LVGL v9.3

M5UI is a UI library based on LVGL v9.3. It provides a set of widgets and functions to create user interfaces for M5Stack devices.

It has been adapted for M5Stack devices and you only need to call ``m5ui.init()`` to start using it.


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
    calendar.rst
    checkbox.rst
    image.rst
    label.rst
    line.rst
    slider.rst
    switch.rst
    textarea.rst
