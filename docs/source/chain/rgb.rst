Chain RGB
=========

.. include:: ../refs/chain.rgb.ref

RGBChain is the helper class for Chain RGB display devices on the Chain bus. It
provides methods to control an 8 x 8 RGB display using RGB888 integer color values,
including pixel drawing, full-screen buffer refresh, ASCII character display,
scrolling text, brightness, and rotation.

Support the following products:

    |Chain RGB|


Constants
---------

Display modes use ``RGBChain.MODE_PIXEL`` and ``RGBChain.MODE_SCROLL``.

Scroll directions use ``RGBChain.SCROLL_DIR_LEFT``,
``RGBChain.SCROLL_DIR_RIGHT``, ``RGBChain.SCROLL_DIR_UP``, and
``RGBChain.SCROLL_DIR_DOWN``.

Scroll modes use ``RGBChain.SCROLL_MODE_ONCE``, ``RGBChain.SCROLL_MODE_LOOP``,
and ``RGBChain.SCROLL_MODE_BOUNCE``.

Scroll states use ``RGBChain.SCROLL_STATE_START``,
``RGBChain.SCROLL_STATE_PAUSE``, and ``RGBChain.SCROLL_STATE_RESET``.

Display rotation uses ``RGBChain.ROTATION_0``, ``RGBChain.ROTATION_90``,
``RGBChain.ROTATION_180``, and ``RGBChain.ROTATION_270``.

UiFlow2 Example
---------------

Scroll text, rotation, and brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |basic_chain_rgb_example.m5f2| project in UiFlow2.

This example initializes Chain RGB in scroll mode and displays the text
``M5STACK`` in cyan. It also shows a simple controller UI on the host display
and uses the hardware buttons to control the Chain RGB module.

- ``BtnA`` toggles the scroll state between start and pause.
- ``BtnB`` cycles the display rotation through 0, 90, 180, and 270 degrees.
- ``BtnC`` cycles the display brightness level.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Examples
--------------------

Scroll text, rotation, and brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example initializes Chain RGB in scroll mode and displays the text
``M5STACK`` in cyan. It also shows a simple controller UI on the host display and
uses the hardware buttons to control the Chain RGB module:

- ``BtnA`` toggles the scroll state between start and pause.
- ``BtnB`` cycles the display rotation through 0, 90, 180, and 270 degrees.
- ``BtnC`` cycles the display brightness level.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/rgb/basic_chain_rgb_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

RGBChain
^^^^^^^^

.. autoclass:: chain.rgb.RGBChain
    :members: set_display_mode, get_display_mode, set_pixel, set_pixels, get_pixel, get_pixels, set_display_buffer, get_display_buffer, set_display_char, set_scroll_text, set_scroll_state, get_scroll_state, set_display_rotation, get_display_rotation, set_brightness, get_brightness
    :member-order: bysource


    For general Chain device methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
