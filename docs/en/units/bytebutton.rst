
ByteButtonUnit
==============
.. sku:U192
.. include:: ../refs/unit.bytebutton.ref

Unit ByteButton is an 8-button touch switch input unit equipped with 8 button inputs and 9 WS2812C RGB LEDs. It uses the STM32 microcontroller and supports I2C communication. The board includes two Port A interfaces and supports cascading multiple Unit ByteButton modules, making it suitable for complex systems. It can achieve button input detection and dynamic lighting feedback, ideal for smart home control, gaming devices, educational platforms, industrial status displays, and interactive exhibitions.

Support the following products:

|ByteButtonUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/bytebutton/bytebutton_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |bytebutton_cores3_example.m5f2|

class ByteButtonUnit
--------------------

Constructors
------------

.. class:: ByteButtonUnit(i2c, address)

    Initialize the ByteButtonUnit with a specified I2C address.

    :param I2C i2c: The I2C interface instance for communication.
    :param int address: The I2C address of the ByteButtonUnit, default is 0x47.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ByteButtonUnit.get_byte_button_status() -> int

    Get the status of all buttons as an integer, where each bit represents the state of each button.


    UIFLOW2:

        |get_byte_button_status.png|

.. method:: ByteButtonUnit.get_button_state(num) -> bool

    Get the state of a specific button.

    :param int num: The index of the button (0-7).

    UIFLOW2:

        |get_button_state.png|

.. method:: ByteButtonUnit.get_led_show_mode() -> int

    Get the current LED show mode.

    UIFLOW2:

        |get_led_show_mode.png|

.. method:: ByteButtonUnit.set_led_show_mode(mode)

    Set the LED show mode.

    :param int mode: The LED show mode to set.

        Options:
            - ``BYTEBUTTON_LED_USER_MODE``: 0
            - ``BYTEBUTTON_LED_SYS_MODE``: 1

    UIFLOW2:

        |set_led_show_mode.png|

.. method:: ByteButtonUnit.set_led_brightness(num, brightness)

    Set the brightness of a specific LED.

    :param int num: The index of the LED (0-7).
    :param int brightness: The brightness level (0-255).

    UIFLOW2:

        |set_led_brightness.png|

.. method:: ByteButtonUnit.get_led_brightness(num) -> int

    Get the brightness of a specific LED.

    :param int num: The index of the LED (0-7).

    UIFLOW2:

        |get_led_brightness.png|

.. method:: ByteButtonUnit.set_led_color(num, color, led_show_mode, btn_is_pressed)

    Set the color of a specific LED.

    :param int num: The index of the LED (0-7).
    :param int color: The RGB888 color value to set.
    :param int led_show_mode: The LED show mode, default is BYTEBUTTON_LED_SYS_MODE.
    :param bool btn_is_pressed: Whether the button is pressed (affects color in SYS mode).

    UIFLOW2:

        |set_sys_mode_led_color.png|
        
        |set_user_mode_led_color.png|

.. method:: ByteButtonUnit.get_led_color(num, led_show_mode, btn_is_pressed) -> int

    Get the color of a specific LED.

    :param int num: The index of the LED (0-7).
    :param int led_show_mode: The LED show mode, default is BYTEBUTTON_LED_SYS_MODE.
    :param bool btn_is_pressed: Whether the button is pressed (affects color in SYS mode).

    UIFLOW2:

        |get_sys_mode_led_color.png|

        |get_user_mode_led_color.png|

.. method:: ByteButtonUnit.set_indicator_brightness(brightness)

    Set the brightness of the indicator LED.

    :param int brightness: The brightness level (0-255).

    UIFLOW2:

        |set_indicator_brightness.png|

.. method:: ByteButtonUnit.get_indicator_brightness() -> int

    Get the brightness of the indicator LED.


    UIFLOW2:

        |get_indicator_brightness.png|

.. method:: ByteButtonUnit.set_indicator_color(color)

    Set the color of the indicator LED in RGB888 format.

    :param int color: The RGB888 color value to set.

    UIFLOW2:

        |set_indicator_color.png|

.. method:: ByteButtonUnit.get_indicator_color() -> int

    Get the color of the indicator LED in RGB888 format.


    UIFLOW2:

        |get_indicator_color.png|

.. method:: ByteButtonUnit.rgb888_to_rgb233(color)

    Convert an RGB888 color value to RGB233 format.

    :param int color: The RGB888 color value as a 32-bit integer.

.. method:: ByteButtonUnit.set_rgb233(num, color)

    Set the color of a specific LED in RGB233 format.

    :param int num: The index of the LED (0-7).
    :param int color: The RGB233 color value to set.

.. method:: ByteButtonUnit.get_rgb233(num)

    Get the color of a specific LED in RGB233 format.

    :param int num: The index of the LED (0-7).

.. method:: ByteButtonUnit.set_irq_enable(enable)

    Enable or disable IRQ functionality.

    :param bool enable: Whether to enable (True) or disable (False) IRQ.

.. method:: ByteButtonUnit.get_irq_enable()

    Get the current IRQ enable status.

.. method:: ByteButtonUnit.save_to_flash()

    Save the current user settings to flash.


    UIFLOW2:

        |save_to_flash.png|

.. method:: ByteButtonUnit.get_firmware_version() -> int

    Get the firmware version of the ByteButtonUnit.


    UIFLOW2:

        |get_firmware_version.png|

.. method:: ByteButtonUnit.set_i2c_address(new_addr)

    Set a new I2C address for the ByteButtonUnit.

    :param int new_addr: The new I2C address to set. Must be in the range 0x08 to 0x78.

    UIFLOW2:

        |set_i2c_address.png|

.. method:: ByteButtonUnit.get_i2c_address() -> int

    Get the current I2C address of the ByteButtonUnit.


    UIFLOW2:

        |get_i2c_address.png|



