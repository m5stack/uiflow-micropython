
# M5LED

M5LED is a lightweight widget that simulates a light-emitting diode indicator in the user interface.

## MicroPython Example

#### LED Basic Usage Example

This example demonstrates how to create and control an LED widget.
It shows how to turn the LED on and off, change its color, adjust brightness.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import m5utils

page0 = None
led0 = None
switch0 = None
slider0 = None
label0 = None
brightness = None

def switch0_checked_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    led0.set_color(0x3366FF)
    led0.on()

def switch0_unchecked_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    led0.off()
    led0.set_color(0x000000)

def slider0_value_changed_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    brightness = slider0.get_value()
    led0.set_brightness(int(m5utils.remap(brightness, 0, 100, 80, 255)))
    label0.set_text(str((str("Brightness: ") + str((str(brightness) + str("%"))))))
    print(led0.get_brightness())

def switch0_event_handler(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return

def slider0_event_handler(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider0_value_changed_event(event_struct)
    return

def setup():
    global page0, led0, switch0, slider0, label0, brightness
    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    led0 = m5ui.M5LED(x=135, y=14, size=50, color=0x00FF00, on=True, parent=page0)
    switch0 = m5ui.M5Switch(
        x=110,
        y=159,
        w=100,
        h=40,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )
    slider0 = m5ui.M5Slider(
        x=20,
        y=118,
        w=280,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Brightness: 0%",
        x=99,
        y=85,
        text_c=0x2193F3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)
    slider0.add_event_cb(slider0_event_handler, lv.EVENT.ALL, None)
    page0.screen_load()
    led0.off()
    brightness = 0
    slider0.set_value(0, True)
    led0.align_to(page0, lv.ALIGN.TOP_MID, 0, 5)
    label0.align_to(slider0, lv.ALIGN.CENTER, 0, -25)
    led0.set_brightness(80)
    print(led0.get_brightness())

def loop():
    global page0, led0, switch0, slider0, label0, brightness
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Example output:

    None.

## **API**

#### M5LED

## `M5LED`
Create a LED object.

- Parameter `x` (`int`): The x position of the LED.
- Parameter `y` (`int`): The y position of the LED.
- Parameter `size` (`int`): The size (width and height) of the LED.
- Parameter `color` (`int`): The color of the LED in RGB888 format.
- Parameter `on` (`bool`): Initial state of the LED (True for ON, False for OFF).
- Parameter `parent` (`lv.obj`): The parent object to attach the LED to. If not specified, the LED will be attached to the default screen.

    None

```python
from m5ui import M5Led
import lvgl as lv

m5ui.init()
led_0 = M5Led(x=50, y=50, size=50, color=0x00FF00, on=True, parent=page0)
```

### `set_color`

### `set_brightness`
Set the brightness of the LED.

- Parameter `brightness` (`int`): Brightness level (0-100). Will be mapped to 80-255 internally.

```python
led_0.set_brightness(50)  # Set brightness to 50%
```

### `get_brightness`
Get the brightness of the LED.

- Returns: Brightness level (0-100).
- Return type: int

```python
brightness = led_0.get_brightness()
```

### `on()`

        Turn on the LED.

        - Returns: None

```python
led_0.on()
```
### `off()`

        Turn off the LED.

        - Returns: None

```python
led_0.off()
```
### `toggle()`

        Toggle the state of a LED.

        - Returns: None

```python
led_0.toggle()
```
### `set_color(color)`

        Set the color of the LED.

        - Parameter `color` (`int`): The color of the LED (RGB888 format).
        - Returns: None

```python
led_0.set_color(color)
```
### `set_pos(x, y)`

        Set the position of the LED.

        - Parameter `x` (`int`): The x position of the LED.
        - Parameter `y` (`int`): The y position of the LED.
        - Returns: None

```python
led_0.set_pos(x, y)
```
### `set_x(x)`

        Set the x position of the LED.

        - Parameter `x` (`int`): The x position of the LED.
        - Returns: None

```python
led_0.set_x(x)
```
### `set_y(y)`

        Set the y position of the LED.

        - Parameter `y` (`int`): The y position of the LED.
        - Returns: None

```python
led_0.set_y(y)
```
### `get_x()`

        Get the x position of the LED.

        - Returns: The x position of the LED.
        - Return type: int

```python
x = led_0.get_x()
```
### `get_y()`

        Get the y position of the LED.

        - Returns: The y position of the LED.
        - Return type: int

```python
y = led_0.get_y()
```
### `set_size(width, height)`

        Set the size of the LED.

        - Parameter `width` (`int`): The width of the LED.
        - Parameter `height` (`int`): The height of the LED.
        - Returns: None

```python
led_0.set_size(width, height)
```
### `set_width(width)`

        Set the width of the LED.

        - Parameter `width` (`int`): The width of the LED.
        - Returns: None

```python
led_0.set_width(width)
```
### `set_height(height)`

        Set the height of the LED.

        - Parameter `height` (`int`): The height of the LED.
        - Returns: None

```python
led_0.set_height(height)
```
### `align_to(obj, align, x, y)`

        Align the LED relative to another object.

        - Parameter `obj`: The reference object (e.g. page0).
        - Parameter `align` (`int`): Alignment option (see lv.ALIGN constants below).
        - Parameter `x` (`int`): X offset after alignment.
        - Parameter `y` (`int`): Y offset after alignment.
        - Returns: None

```python
led_0.align_to(page0, lv.ALIGN.CENTER, 0, 0)
```
### `lv.ALIGN`

        Alignment options for positioning objects.

        - lv.ALIGN.DEFAULT
        - lv.ALIGN.TOP_LEFT
        - lv.ALIGN.TOP_MID
        - lv.ALIGN.TOP_RIGHT
        - lv.ALIGN.BOTTOM_LEFT
        - lv.ALIGN.BOTTOM_MID
        - lv.ALIGN.BOTTOM_RIGHT
        - lv.ALIGN.LEFT_MID
        - lv.ALIGN.RIGHT_MID
        - lv.ALIGN.CENTER
        - lv.ALIGN.OUT_TOP_LEFT
        - lv.ALIGN.OUT_TOP_MID
        - lv.ALIGN.OUT_TOP_RIGHT
        - lv.ALIGN.OUT_BOTTOM_LEFT
        - lv.ALIGN.OUT_BOTTOM_MID
        - lv.ALIGN.OUT_BOTTOM_RIGHT
        - lv.ALIGN.OUT_LEFT_TOP
        - lv.ALIGN.OUT_LEFT_MID
        - lv.ALIGN.OUT_LEFT_BOTTOM
        - lv.ALIGN.OUT_RIGHT_TOP
        - lv.ALIGN.OUT_RIGHT_MID
        - lv.ALIGN.OUT_RIGHT_BOTTOM
