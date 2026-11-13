# RGB Unit

For compatible firmware and host interfaces, see
[Board Capabilities](../quick-reference/board-capabilities.md).

The following products are supported:

    RGB

Micropython Example:
```python
import M5
from M5 import *
from unit import RGBUnit

M5.begin()
rgb_0 = RGBUnit((36, 26), 3)
Widgets.fillScreen(0x222222)

rgb_0.set_brightness(80)
rgb_0.fill_color(0xff0000)
rgb_0.set_color(0, 0x33ff33)
```

## class RGBUnit

## Constructors

### `class RGBUnit(port, number)`

    Create an RGBUnit object.

    parameter is:
        - `port` is the pins number of the port
        - `number` is the number of RGB lamp beads

## Methods

### `RGBUnit.set_brightness(br: int)`

    This method is used to set the brightness of RGB lamp beads, and the setting range is 0-100.

### `RGBUnit.fill_color(c: int)`

    This method is used to set the color of all RGB lamp beads, and the input value is 3-byte RGB888.

### `RGBUnit.set_color(i, c: int)`

    This method is used to set the specified RGB lamp bead color. The input value is the lamp bead index and 3-byte RGB888.
