
# Puzzle Unit

Unit-Puzzle is a colorful lighting control unit, consisting of an 8x8 RGB array of 64 colorful WS2812E RGB lamp beads.

Support the following products:

PuzzleUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import PuzzleUnit
import time

title0 = None
label0 = None
label1 = None
puzzle_0 = None

def setup():
    global title0, label0, label1, puzzle_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "UnitPuzzle M5Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Pls see the Puzzle", 76, 102, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Program will run automatically", 10, 134, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    puzzle_0 = PuzzleUnit((33, 32), 1)
    puzzle_0.set_brightness(10)

def loop():
    global title0, label0, label1, puzzle_0
    M5.update()
    puzzle_0.set_color(1, 1, 0xFFFFFF)
    puzzle_0.set_color(1, 64, 0x66FFFF)
    time.sleep(1)
    puzzle_0.fill_color(0x6600CC)
    time.sleep(1)
    puzzle_0.set_color_from(1, 1, 64, 0x6600CC, 0)
    puzzle_0.set_color_from(1, 64, 1, 0x33FF33, 30)
    time.sleep(1)
    puzzle_0.set_color_running_from(1, 1, 64, 0x6600CC, 30)
    puzzle_0.set_color_running_from(1, 64, 1, 0x33FF33, 30)
    time.sleep(1)
    puzzle_0.set_color_saturation_from(1, 1, 64, 0x6600CC, 30)
    puzzle_0.set_color_saturation_from(1, 64, 1, 0x33FF33, 30)
    time.sleep(1)
    puzzle_0.set_random_color_random_led_from(1, 1, 64)
    time.sleep(1)
    puzzle_0.set_screen(
        1,
        [
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0xFFFFFF,
        ],
    )
    time.sleep(1)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## class PuzzleUnit

## Constructors

### `class PuzzleUnit(port, led_board_count)`

    Initialize the PuzzleUnit.

    - Parameter `port` (`tuple`): The port to connect the WS2812 LED strip.
    - Parameter `led_board_count` (`int`): Number of connected PuzzleUnit boards.

## Methods

### `PuzzleUnit.fill_color(color)`

    Set the entire screen or area to a specific RGB color.

    - Parameter `color` (`int`): The RGB color to fill the area with.

### `PuzzleUnit.set_color(index, color)`

    Set the color of a specific pixel or LED.

    - Parameter `index`: The index of the pixel or LED to set the color on.
    - Parameter `color` (`int`): The color to set, specified in RGB format.

### `PuzzleUnit.set_brightness(br)`

    Adjust the brightness of the LEDs based on the given percentage.

    - Parameter `br` (`int`): The brightness percentage (0-100).

### `PuzzleUnit.set_color_from(board_num, begin, end, rgb, per_delay)`

    Set color on a range of LEDs starting from a specified board and range.

    - Parameter `board_num` (`int`): The board number (starting from 1) where the LEDs are located.
    - Parameter `begin` (`int`): The starting LED index on the board.
    - Parameter `end` (`int`): The ending LED index on the board.
    - Parameter `rgb` (`int`): The color to set, specified in RGB format.
    - Parameter `per_delay` (`int`): Delay in milliseconds between setting each LED color.

### `PuzzleUnit.set_color(board_num, index, rgb)`

    Set the color of a single LED.

    - Parameter `board_num` (`int`): The board number (starting from 1) where the LED is located.
    - Parameter `index` (`int`): The LED index to set the color on (1-based index).
    - Parameter `rgb` (`int`): The color to set, specified in RGB format.

### `PuzzleUnit.set_color_saturation_from(board_num, begin, end, rgb_color, per_delay)`

    Gradually change the color saturation from begin to end on a range of LEDs.

    - Parameter `board_num` (`int`): The board number (starting from 1) where the LEDs are located.
    - Parameter `begin` (`int`): The starting LED index on the board.
    - Parameter `end` (`int`): The ending LED index on the board.
    - Parameter `rgb_color` (`int`): The base RGB color to apply saturation to.
    - Parameter `per_delay` (`int`): Delay in milliseconds between each LED color change.

### `PuzzleUnit.set_color_running_from(board_num, begin, end, rgb, per_delay)`

    Create a running color effect on a range of LEDs from begin to end.

    - Parameter `board_num` (`int`): The board number (starting from 1) where the LEDs are located.
    - Parameter `begin` (`int`): The starting LED index on the board.
    - Parameter `end` (`int`): The ending LED index on the board.
    - Parameter `rgb` (`int`): The color to set, specified in RGB format.
    - Parameter `per_delay` (`int`): Delay in milliseconds between setting each LED color.

### `PuzzleUnit.set_random_color_random_led_from(board_num, begin, end)`

    Set a random color to each LED within the specified range.

    - Parameter `board_num` (`int`): The board number (starting from 1) where the LEDs are located.
    - Parameter `begin` (`int`): The starting LED index on the board.
    - Parameter `end` (`int`): The ending LED index on the board.

### `PuzzleUnit.set_screen(board_num, color_list)`

    Set the screen of a specific board with a list of colors.

    - Parameter `board_num` (`int`): The board number to which the colors should be applied.
    - Parameter `color_list` (`list`): A list of colors to apply to the screen.
