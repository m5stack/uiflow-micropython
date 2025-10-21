.. currentmodule:: m5ui

M5Menu
========

.. include:: ../refs/m5ui.menu.ref

M5Menu is a widget that can be used to create multi-level menus in the user interface.

UiFlow2 Example
---------------

menu event
^^^^^^^^^^^^^^

Open the |menu_core2_example.m5f2| project in UiFlow2.

This example creates a multi-level menus.

UiFlow2 Code Block:

    |menu_core2_example.png|

Example output:

    None

MicroPython Example
-------------------

menu event
^^^^^^^^^^^^^^

This example creates a multi-level menus.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/menu/menu_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------
M5Menu
^^^^^^^^

.. autoclass:: m5ui.menu.M5Menu
    :members:

    .. py:method:: set_page(page)

        Set main page for the menu.

        :param lv.obj page: The main page object.

        UiFlow2 Code Block:

            |set_page.png|

        MicroPython Code Block:

            .. code-block:: python

                menu0.set_page(menu0.main_page)

    .. py:method:: set_mode_header(mode)

        Set the mode header for the menu.

        :param int mode: The mode header text.

            Options:

                - ``lv.menu.HEADER.TOP_FIXED``
                - ``lv.menu.HEADER.TOP_UNFIXED``
                - ``lv.menu.HEADER.BOTTOM_FIXED``

        UiFlow2 Code Block:

            |set_mode_header.png|

        MicroPython Code Block:

            .. code-block:: python

                menu0.set_mode_header(lv.menu.HEADER.TOP_FIXED)

    .. py:method:: set_pos(x, y)

        Set the position of the menu.

        :param int x: The x-coordinate of the menu.
        :param int y: The y-coordinate of the menu.

        UiFlow2 Code Block:

            |set_pos.png|

        MicroPython Code Block:

            .. code-block:: python

                menu0.set_pos(100, 100)

    .. py:method:: set_size(width, height)

        Set the size of the menu.

        :param int width: The width of the menu.
        :param int height: The height of the menu.

        UiFlow2 Code Block:

            |set_size.png|

        MicroPython Code Block:

            .. code-block:: python

                menu0.set_size(100, 50)