
NECO Unit
=========
.. sku:
.. include:: ../refs/unit.neco.ref

The Neco Unit is a unique RGB light board unit that features an adorable cat ear shape. It is designed with precision and comprises 35 WS2812C-2020 RGB lamp beads, providing vibrant and customizable lighting effects.

Support the following products:

|NECOUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/neco/neco_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |neco_cores3_example.m5f2|

class NECOUnit
--------------

Constructors
------------

.. class:: NECOUnit(port, number, active_low)

    Initialize the NECOUnit with a specific port, LED count, and active low configuration for the button.

    :param tuple port: A tuple containing the port information, where the first element is for the button and the second is for the WS2812 LEDs.
    :param int number: The number of LEDs in the WS2812 strip. Default is 70.
    :param bool active_low: Boolean flag indicating whether the button is active low. Default is True.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: NECOUnit.set_color_from(begin, end, rgb, per_delay)

    Set the color for a range of LEDs from the begin index to the end index with a specified color.

    :param int begin: The starting LED index.
    :param int end: The ending LED index.
    :param int rgb: The color to set, in RGB format.
    :param int per_delay: The delay between setting each LED's ;s color, in milliseconds. Default is 0.

    UIFLOW2:

        |set_color_from.png|

.. method:: NECOUnit.set_color_saturation_from(begin, end, rgb, per_delay)

    Set the color saturation for a range of LEDs from the begin index to the end index with a specified color and saturation.

    :param int begin: The starting LED index.
    :param int end: The ending LED index.
    :param int rgb: The base color in RGB format.
    :param int per_delay: The delay between setting each LED's ;s color, in milliseconds. Default is 0.

.. method:: NECOUnit.color_saturation(rgb, saturation)

    Adjust the color saturation of an RGB color.

    :param int rgb: The base color in RGB format.
    :param float saturation: The desired saturation level (0 to 100).

    :returns: The new color with adjusted saturation, in RGB format.

.. method:: NECOUnit.set_color_running_from(begin, end, rgb, per_delay)

    Set the color for a range of LEDs from the begin index to the end index, then clear them one by one, creating a running effect.

    :param int begin: The starting LED index.
    :param int end: The ending LED index.
    :param int rgb: The color to set, in RGB format.
    :param int per_delay: The delay between setting and clearing each LED's ;s color, in milliseconds. Default is 0.

    UIFLOW2:

        |set_color_running_from.png|

.. method:: NECOUnit.set_random_color_random_led_from(begin, end)

    Set a random color to each LED in a random order within the specified range.

    :param int begin: The starting LED index.
    :param int end: The ending LED index.

    UIFLOW2:

        |set_random_color_random_led_from.png|

.. method:: NECOUnit.fill(v)

    Fill the entire NECOUnit strip with the specified color.

    :param int v: A tuple containing the RGB (or RGBW) values to fill the strip with.

.. method:: NECOUnit.set_color(i, c)

    Set the color of the LED at the specified index.

    :param  i: The index of the LED to set.
    :param int c: The color value to set the LED to (in RGB or RGBW format).

    UIFLOW2:

        |set_color.png|

.. method:: NECOUnit.fill_color(c)

    Fill the entire NECOUnit strip with the specified color.

    :param int c: The color value to fill the strip with (in RGB or RGBW format).

    UIFLOW2:

        |fill_color.png|

.. method:: NECOUnit.set_brightness(br)

    Set the brightness for the NECOUnit strip.

    :param int br: The brightness level as a percentage (0-100).

    UIFLOW2:

        |set_brightness.png|



