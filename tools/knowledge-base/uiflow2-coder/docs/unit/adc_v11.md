
# ADC V1.1 Unit

ADC V1.1 Unit is an A/D conversion module that utilizes the ADS1110 chip, a 16-bit self-calibrating analog-to-digital converter. It is designed with an I2C interface, offering convenient connectivity. The module offers conversion speeds of 8, 16, 32, and 128 samples per second (SPS), providing varying levels of accuracy at 16, 15, 14, and 12 bits of resolution respectively.

Support the following products:

ADCV11Unit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ADCV11Unit

title0 = None
label1 = None
label0 = None
i2c0 = None
adc_v11_0 = None

def setup():
    global title0, label1, label0, i2c0, adc_v11_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ADCV11Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "ADC 16Bit Value:", 1, 130, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("ADC Value:", 1, 91, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    adc_v11_0 = ADCV11Unit(i2c0)
    adc_v11_0.set_sample_rate(0x00)
    adc_v11_0.set_mode(0x00)
    adc_v11_0.start_single_conversion()
    adc_v11_0.set_gain(0x00)

def loop():
    global title0, label1, label0, i2c0, adc_v11_0
    M5.update()
    label0.setText(str((str("ADC Value:") + str((adc_v11_0.get_voltage())))))
    label1.setText(str((str("ADC 16Bit Value:") + str((adc_v11_0.get_adc_raw_value())))))

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

## class ADCV11Unit

## Constructors

### `class ADCV11Unit(i2c)`

    Initialize the ADCV11Unit with an I2C or PAHUBUnit interface.

    - Parameter `i2c`: The I2C or PAHUBUnit instance used for communication.

## Methods

### `ADCV11Unit.get_voltage()`

    Get the measured voltage from the ADC V1.1 Unit.

    - Returns: The measured voltage value, rounded to two decimal places.

### `ADCV11Unit.set_gain(gain)`

    Set the gain configuration for the ADC.

    - Parameter `gain`: The gain value to configure.

### `ADCV11Unit.set_sample_rate(rate)`

    Configure the ADC's sampling rate.

    - Parameter `rate`: The sample rate to set.

### `ADCV11Unit.set_mode(mode)`

    Set the ADC's operating mode.

    - Parameter `mode`: The mode to configure, e.g., continuous or single conversion.

### `ADCV11Unit.set_config()`

    Update the ADC configuration register with the current settings.

### `ADCV11Unit.get_adc_raw_value()`

    Read the raw ADC value.
