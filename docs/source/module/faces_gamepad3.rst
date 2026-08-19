Faces Gamepad3 Module
=====================

.. py:currentmodule:: module.faces

.. include:: ../refs/module.faces_gamepad3.ref

Faces Gamepad3 is an eight-button input module. Button states are active-low:
a cleared bit means that the button is pressed.

Support the following products:

    |FacesGamepad3Module|

UiFlow2 Example
---------------

Button event display
^^^^^^^^^^^^^^^^^^^^

This example reports press and release events for the Up and Down buttons.
The callback receives ``True`` when the selected button is pressed and
``False`` when it is released.

.. only:: builder_html

    Open the |faces_gamepad3_cores3_example.m5f2| project in UiFlow2.

UiFlow2 Code Block:

    |example.png|

MicroPython Example
-------------------

Button event display
^^^^^^^^^^^^^^^^^^^^

Register one callback for each button that should be monitored, then call
:meth:`FacesGamepad3Module.tick` regularly from the main loop.

.. literalinclude:: ../../../examples/module/faces/faces_gamepad3_cores3_example.py
    :language: python
    :linenos:

API
---

.. autoclass:: module.faces.FacesGamepad3Module
    :members:
    :inherited-members:
    :member-order: bysource

Gamepad button masks:

.. list-table::
    :header-rows: 1
    :widths: 40 15

    * - Constant
      - Value
    * - ``BUTTON_UP``
      - ``0x01``
    * - ``BUTTON_DOWN``
      - ``0x02``
    * - ``BUTTON_LEFT``
      - ``0x04``
    * - ``BUTTON_RIGHT``
      - ``0x08``
    * - ``BUTTON_A``
      - ``0x10``
    * - ``BUTTON_B``
      - ``0x20``
    * - ``BUTTON_SELECT``
      - ``0x40``
    * - ``BUTTON_START``
      - ``0x80``
