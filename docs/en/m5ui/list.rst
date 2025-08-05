.. currentmodule:: m5ui

M5List
=======

.. include:: ../refs/m5ui.list.ref

M5List is a widget that can be used to create lists in user interfaces. It is basically a rectangle with vertical layout to which Buttons and Text can be added.


UiFlow2 Example
---------------

list example
^^^^^^^^^^^^

Open the |cores3_list_example.m5f2| project in UiFlow2.

This example demonstrates how to create a list that displays a series of items.

UiFlow2 Code Block:

    |cores3_list_example.png|

Example output:

    None


MicroPython Example
-------------------

list example
^^^^^^^^^^^^

This example demonstrates how to create a list that displays a series of items.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/m5ui/list/cores3_list_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

M5List
^^^^^^^

.. autoclass:: m5ui.list.M5List
    :members:

    .. py:method:: move_background()

        Move the background of the list to the end.

        UiFlow2 Code Block:

            |button_move_to_index.png|

            |label_move_to_index.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.move_background()
                text_0.move_background()

    
    .. py:method:: move_foreground()

        Move the foreground of the list to the end.

        UiFlow2 Code Block:

            |button_move_to_index.png|

            |label_move_to_index.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.move_foreground()
                text_0.move_foreground()

    .. py:method:: move_to_index(index)

        Move the item at the specified index to the end of the list.

        UiFlow2 Code Block:

            |button_move_to_index.png|

            |label_move_to_index.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.move_to_index(0)
                text_0.move_to_index(1)

    .. py:method:: delete()

        Delete the item from the list.

        UiFlow2 Code Block:

            |button_delete.png|

            |label_delete.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.delete()
                text_0.delete()