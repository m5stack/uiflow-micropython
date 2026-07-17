

# Servo2 Module

Servo2 is an updated servo driver module in the M5Stack stackable module series. It uses a PCA9685 16-channel PWM controller to drive up to 16 servos simultaneously. Power input is 6–12 V DC, with two SY8368AQQC chips for step-down regulation.

Support the following products:

    Servo2Module

## MicroPython Example

#### Servo angle control

This example initializes the Servo2 module on the I2C bus, drives two servo channels, and shows the current angle on screen. Button A sets both servos to 0°, Button B to 45°, and Button C to 90°; one channel is released after setup.

```python
import os, sys, io
import M5
from M5 import *
from module import Servo2Module

title = None
label_angle = None
servo2_0 = None
angle = None

def btna_was_clicked_event(state):
  global title, label_angle, servo2_0, angle
  angle = 0
  label_angle.setText(str((str('Angle: ') + str(angle))))
  servo2_0.position(1, degrees=angle)
  servo2_0.position(2, degrees=angle)

def btnb_was_clicked_event(state):
  global title, label_angle, servo2_0, angle
  angle = 45
  label_angle.setText(str((str('Angle: ') + str(angle))))
  servo2_0.position(1, degrees=angle)
  servo2_0.position(2, degrees=angle)

def btnc_was_clicked_event(state):
  global title, label_angle, servo2_0, angle
  angle = 90
  label_angle.setText(str((str('Angle: ') + str(angle))))
  servo2_0.position(1, degrees=angle)
  servo2_0.position(2, degrees=angle)

def setup():
  global title, label_angle, servo2_0, angle

  M5.begin()
  Widgets.setRotation(1)
  Widgets.fillScreen(0x222222)
  title = Widgets.Title("Module Servo2 Example", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
  label_angle = Widgets.Label("Angle: ", 46, 98, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)

  BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
  BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
  BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

  servo2_0 = Servo2Module(0x40, 50, 400, 2350, 180)
  angle = 0
  label_angle.setText(str((str('Angle: ') + str(angle))))
  servo2_0.position(1, degrees=angle)
  servo2_0.position(2, degrees=angle)
  servo2_0.release(0)

def loop():
  global title, label_angle, servo2_0, angle
  M5.update()

if __name__ == '__main__':
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

## **API**

#### Servo2Module

### `class Servo2Module(address=0x40, freq=50, min_us=400, max_us=2350, degrees=180)`

    Create a Servo2 module instance on the I2C bus.

    - Parameter `address` (`int`): I2C address of the PCA9685 (default 0x40).
    - Parameter `freq` (`int`): PWM frequency in Hz (default 50).
    - Parameter `min_us` (`int`): Minimum pulse width in microseconds (default 400).
    - Parameter `max_us` (`int`): Maximum pulse width in microseconds (default 2350).
    - Parameter `degrees` (`int`): Maximum angle in degrees (default 180).

```python
from module import Servo2Module

servo2 = Servo2Module(address=0x40, freq=50, min_us=400, max_us=2350, degrees=180)
```
### `Servo2Module.position(index, degrees=None, radians=None, us=None, duty=None)`

        Set the servo position for the given channel.

        - Parameter `index` (`int`): Channel index (0-15).
        - Parameter `degrees` (`float`): Angle in degrees (optional).
        - Parameter `radians` (`float`): Angle in radians (optional).
        - Parameter `us` (`int`): Pulse width in microseconds (optional).
        - Parameter `duty` (`float`): Duty cycle in percent (optional). Exactly one of *degrees*, *radians*, *us*, or *duty* may be given.

```python
servo2.position(0, degrees=90)
servo2.position(0, duty=50)
servo2.position(0, us=1500)
servo2.position(0, radians=1.57)
```
### `Servo2Module.release(index)`

        Release the servo (stop driving the channel).

        - Parameter `index` (`int`): Channel index (0–15).

```python
servo2.release(0)
```
### `Servo2Module.deinit()`

        Release the module. No-op for Servo2Module; provided for compatibility.

```python
servo2.deinit()
```
