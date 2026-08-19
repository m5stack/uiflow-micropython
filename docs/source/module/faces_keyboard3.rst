Faces Keyboard3 Module
======================

.. py:currentmodule:: module.faces

.. include:: ../refs/module.faces_keyboard3.ref

Faces Keyboard3 is a keyboard input module with mapped-character Normal mode
and raw-matrix Direct mode. In Direct mode, the callback receives a tuple of
currently pressed key names and the two keyboard LEDs can be controlled.

Support the following products:

    |FacesKeyboard3Module|

UiFlow2 Example
---------------

Normal mode key events
^^^^^^^^^^^^^^^^^^^^^^

This example uses Normal mode and reports each mapped key on the CoreS3
display.

.. only:: builder_html

    Open the |faces_keyboard3_cores3_example.m5f2| project in UiFlow2.

UiFlow2 Code Block:

    |example.png|

MicroPython Example
-------------------

Normal mode key events
^^^^^^^^^^^^^^^^^^^^^^

Normal mode maps key presses to character codes. Direct mode reports a tuple
of currently pressed matrix-key names and also allows LED control.

.. literalinclude:: ../../../examples/module/faces/faces_keyboard3_cores3_example.py
    :language: python
    :linenos:

API
---

.. autoclass:: module.faces.FacesKeyboard3Module
    :members:
    :inherited-members:
    :member-order: bysource

Keyboard LED constants:

.. list-table::
    :header-rows: 1
    :widths: 32 15 53

    * - Constant
      - Value
      - Description
    * - ``LED_EFFECT_OFF``
      - ``0x00``
      - Disable the preset effect
    * - ``LED_EFFECT_1``
      - ``0x01``
      - Left LED stays on
    * - ``LED_EFFECT_2``
      - ``0x02``
      - Left LED blinks slowly
    * - ``LED_EFFECT_3``
      - ``0x03``
      - Left LED blinks quickly
    * - ``LED_EFFECT_4``
      - ``0x04``
      - Right LED stays on
    * - ``LED_EFFECT_5``
      - ``0x05``
      - Right LED blinks slowly
    * - ``LED_EFFECT_6``
      - ``0x06``
      - Right LED blinks quickly
    * - ``LED_EFFECT_7``
      - ``0x07``
      - Left and right LEDs alternate slowly
    * - ``LED_EFFECT_8``
      - ``0x08``
      - Left and right LEDs alternate quickly

In Normal mode, ``KEY_BACKSPACE`` is ``0x08``, ``KEY_ENTER`` is ``0x0D``, and
``KEY_DELETE`` is ``0x7F``. LED effects and manual LED states are available
only in Direct mode.
