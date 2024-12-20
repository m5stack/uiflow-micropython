
Puzzle Unit
===========

.. include:: ../refs/unit.puzzle.ref

Unit-Puzzle is a colorful lighting control unit, consisting of an 8x8 RGB array of 64 colorful WS2812E RGB lamp beads.

Support the following products:

|PuzzleUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/puzzle/puzzle_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |puzzle_core2_example.m5f2|

class PuzzleUnit
----------------

Constructors
------------

.. class:: PuzzleUnit(port, led_board_count)

    Initialize the PuzzleUnit.

    :param tuple port: The port to connect the WS2812 LED strip.
    :param int led_board_count: Number of connected PuzzleUnit boards.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: PuzzleUnit.fill_color(color)

    Set the entire screen or area to a specific RGB color.

    :param int color: The RGB color to fill the area with.

    UIFLOW2:

        |fill_color.png|

.. method:: PuzzleUnit.set_color(index, color)

    Set the color of a specific pixel or LED.

    :param index: The index of the pixel or LED to set the color on.
    :param int color: The color to set, specified in RGB format.

    UIFLOW2:

        |set_color.png|

.. method:: PuzzleUnit.set_brightness(br)

    Adjust the brightness of the LEDs based on the given percentage.

    :param int br: The brightness percentage (0-100).

    UIFLOW2:

        |set_brightness.png|

.. method:: PuzzleUnit.set_color_from(board_num, begin, end, rgb, per_delay)

    Set color on a range of LEDs starting from a specified board and range.

    :param int board_num: The board number (starting from 1) where the LEDs are located.
    :param int begin: The starting LED index on the board.
    :param int end: The ending LED index on the board.
    :param int rgb: The color to set, specified in RGB format.
    :param int per_delay: Delay in milliseconds between setting each LED color.

    UIFLOW2:

        |set_color_from.png|

.. method:: PuzzleUnit.set_color(board_num, index, rgb)
    :no-index:

    Set the color of a single LED.

    :param int board_num: The board number (starting from 1) where the LED is located.
    :param int index: The LED index to set the color on (1-based index).
    :param int rgb: The color to set, specified in RGB format.

    UIFLOW2:

        |set_color.png|

.. method:: PuzzleUnit.set_color_saturation_from(board_num, begin, end, rgb_color, per_delay)

    Gradually change the color saturation from begin to end on a range of LEDs.

    :param int board_num: The board number (starting from 1) where the LEDs are located.
    :param int begin: The starting LED index on the board.
    :param int end: The ending LED index on the board.
    :param int rgb_color: The base RGB color to apply saturation to.
    :param int per_delay: Delay in milliseconds between each LED color change.

    UIFLOW2:

        |set_color_saturation_from.png|

.. method:: PuzzleUnit.set_color_running_from(board_num, begin, end, rgb, per_delay)

    Create a running color effect on a range of LEDs from begin to end.

    :param int board_num: The board number (starting from 1) where the LEDs are located.
    :param int begin: The starting LED index on the board.
    :param int end: The ending LED index on the board.
    :param int rgb: The color to set, specified in RGB format.
    :param int per_delay: Delay in milliseconds between setting each LED color.

    UIFLOW2:

        |set_color_running_from.png|

.. method:: PuzzleUnit.set_random_color_random_led_from(board_num, begin, end)

    Set a random color to each LED within the specified range.

    :param int board_num: The board number (starting from 1) where the LEDs are located.
    :param int begin: The starting LED index on the board.
    :param int end: The ending LED index on the board.

    UIFLOW2:

        |set_random_color_random_led_from.png|

.. method:: PuzzleUnit.set_screen(board_num, color_list)

    Set the screen of a specific board with a list of colors.

    :param int board_num: The board number to which the colors should be applied.
    :param list color_list: A list of colors to apply to the screen.

    UIFLOW2:

        |set_screen.png|



