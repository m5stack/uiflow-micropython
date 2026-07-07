Chain Mono
==========

.. include:: ../refs/chain.mono.ref

MonoChain is the helper class for Chain Mono display devices on the Chain bus. It
provides methods to control an 8 x 8 monochrome display, including pixel drawing,
full-screen buffer refresh, ASCII character display, scrolling text, brightness,
and rotation.

Support the following products:

    |Chain Mono|

Constants
---------

Display modes use ``MonoChain.MODE_PIXEL`` and ``MonoChain.MODE_SCROLL``.

Scroll directions use ``MonoChain.SCROLL_DIR_LEFT``,
``MonoChain.SCROLL_DIR_RIGHT``, ``MonoChain.SCROLL_DIR_UP``, and
``MonoChain.SCROLL_DIR_DOWN``.

Scroll modes use ``MonoChain.SCROLL_MODE_ONCE``,
``MonoChain.SCROLL_MODE_LOOP``, and ``MonoChain.SCROLL_MODE_BOUNCE``.

Scroll states use ``MonoChain.SCROLL_STATE_START``,
``MonoChain.SCROLL_STATE_PAUSE``, and ``MonoChain.SCROLL_STATE_RESET``.

Display rotation uses ``MonoChain.ROTATION_0``, ``MonoChain.ROTATION_90``,
``MonoChain.ROTATION_180``, and ``MonoChain.ROTATION_270``.

UiFlow2 Example
---------------

Scroll text, rotation, and brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |basic_chain_mono_example.m5f2| project in UiFlow2.

This example initializes Chain Mono in scroll mode and displays the text
``M5STACK``. It also shows a simple controller UI on the host display and uses
the hardware buttons to control the Chain Mono module.

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

This example initializes Chain Mono in scroll mode and displays the text
``M5STACK``. It also shows a simple controller UI on the host display and uses
the hardware buttons to control the Chain Mono module:

- ``BtnA`` toggles the scroll state between start and pause.
- ``BtnB`` cycles the display rotation through 0, 90, 180, and 270 degrees.
- ``BtnC`` cycles the display brightness level.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/mono/basic_chain_mono_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

MonoChain
^^^^^^^^^

.. autoclass:: chain.mono.MonoChain
    :members: set_display_mode, get_display_mode, set_pixel, set_pixels, get_pixel, get_pixels, set_display_buffer, get_display_buffer, set_display_char, set_scroll_text, set_scroll_state, get_scroll_state, set_display_rotation, get_display_rotation, set_brightness, get_brightness
    :member-order: bysource


    For general Chain device methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
