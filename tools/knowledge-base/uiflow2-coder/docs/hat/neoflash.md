# NeoFlash Hat

NeoFlash HAT is specifically designed for M5StickC, it is an RGB LED matrix.
Space on PCB board is 58x23.5mm and total include 126 RGB LEDs. Every single RGB
LED is programmable, which allows you setting the colors and brightness, plus on
the 7*18 matrix layout, you will have a nice experience on either display
digital numbers or colorful light effect.

Support the following products:

    NeoFlashHat

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import NeoFlashHat
neoflash = NeoFlashHat((26, 0))
neoflash.set_pixel(0, 0, 0xFF0000)
neoflash.set_pixel(1, 0, 0x00FF00)
```

## class NeoFlashHat

## Constructors

### `class NeoFlashHat(port: tuple)`

    Initialize the NeoFlashHat.

    - Parameter `port` (`tuple`): The port to which the NeoFlashHat is connected. port[0]: LEDs pin.

## Methods

### `NeoFlashHat.set_pixel(x: int, y: int, color: int) -> None`

    Set the color of the pixel.

    - Parameter `x` (`int`): The x coordinate of the pixel.
    - Parameter `y` (`int`): The y coordinate of the pixel.
    - Parameter `color` (`int`): The color of the pixel.

### `NeoFlashHat.set_pixels(data: list) -> None`

    Set the color of the pixels.

    - Parameter `data` (`list`): The list of the pixel position and color, [x, y, color].

## Constants

### `NeoFlashHat.WIDTH`

    The width of the NeoFlashHat.

### `NeoFlashHat.HEIGHT`

    The height of the NeoFlashHat.
