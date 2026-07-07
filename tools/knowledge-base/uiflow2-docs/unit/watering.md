# Watering Unit

<!-- .. include:: ../refs/unit.watering.ref -->

Watering is a capacitive soil moisture detection and adjustment unit.
The product integrates water pump and measuring plates for soil moisture
detection and pump water control. It can be used for intelligent plant breeding
scenarios and can easily achieve humidity detection and Irrigation control.
The measurement electrode plate uses the capacitive design, which can
effectively avoid the corrosion problem of the electrode plate in actual use
compared with the resistive electrode plate.

Support the following products:

    |WateringUnit|

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import WateringUnit

label0 = None
label1 = None
label2 = None
label3 = None
watering_0 = None

def setup():
    global label0, label1, label2, label3, watering_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Voltage:", 50, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ADC:", 50, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 150, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 150, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    watering_0 = WateringUnit((8, 9))

def loop():
    global label0, label1, label2, label3, watering_0
    M5.update()
    label2.setText(str(watering_0.get_voltage()))
    label3.setText(str(watering_0.get_raw()))
    if (watering_0.get_raw()) > 30000:
        watering_0.on()
    else:
        watering_0.off()

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |cores3_watering_example.m5f2|

## class WateringUnit

## Constructors

<!-- .. class:: WateringUnit(port: tuple) -> None -->

    Initialize the Fader.

    :param port: The port to which the Fader is connected. port[0]: adc pin, port[1]: pump pin.

    UIFLOW2:

## Methods

<!-- .. method:: WateringUnit.get_voltage() -> float -->

    Get the voltage of the sensor.

    :return: The voltage of the sensor.

    UIFLOW2:

<!-- .. method:: WateringUnit.get_raw() -> int -->

    Read the raw value of the ADC.

    :return: The raw value of the ADC.

    UIFLOW2:

<!-- .. method:: WateringUnit.on() -> None -->

    Turn on the pump.

    UIFLOW2:

<!-- .. method:: WateringUnit.off() -> None -->

    Turn off the pump.

    UIFLOW2:

<!-- .. method:: WateringUnit.set_pump(state: int) -> None -->

    Set the state of the pump.

    :param int state: The state of the pump.

    UIFLOW2:
