Faces Calculator3 Module
========================

.. py:currentmodule:: module.faces

.. include:: ../refs/module.faces_calculator3.ref

Faces Calculator3 is a calculator keypad module. It reports released key
codes through a callback and uses I2C address ``0x08`` by default.

Support the following products:

    |FacesCalculator3Module|

UiFlow2 Example
---------------

Key event display
^^^^^^^^^^^^^^^^^

This example reports the key released on the CoreS3 display. The callback
receives the released key code, converts it to a character, and displays it.

.. only:: builder_html

    Open the |faces_calculator3_cores3_example.m5f2| project in UiFlow2.

UiFlow2 Code Block:

    |example.png|

MicroPython Example
-------------------

Key event display
^^^^^^^^^^^^^^^^^

Call :meth:`FacesCalculator3Module.tick` regularly from the main loop to poll
for new key events.

.. literalinclude:: ../../../examples/module/faces/faces_calculator3_cores3_example.py
    :language: python
    :linenos:

API
---

.. autoclass:: module.faces.FacesCalculator3Module
    :members:
    :inherited-members:
    :member-order: bysource

Calculator key constants:

.. list-table::
    :header-rows: 1
    :widths: 40 15 45

    * - Constant
      - Value
      - Key
    * - ``KEY_BACKSPACE``
      - ``0x08``
      - Backspace
    * - ``KEY_ENTER``
      - ``0x0D``
      - Enter
    * - ``KEY_AC``
      - ``0x41``
      - All clear
    * - ``KEY_MEMORY``
      - ``0x4D``
      - Memory
    * - ``KEY_PERCENT``
      - ``0x25``
      - Percent
    * - ``KEY_DIVIDE``
      - ``0x2F``
      - Divide
    * - ``KEY_MULTIPLY``
      - ``0x2A``
      - Multiply
    * - ``KEY_MINUS``
      - ``0x2D``
      - Minus
    * - ``KEY_PLUS``
      - ``0x2B``
      - Plus
    * - ``KEY_SIGN``
      - ``0x60``
      - Sign
    * - ``KEY_EQUAL``
      - ``0x3D``
      - Equal
