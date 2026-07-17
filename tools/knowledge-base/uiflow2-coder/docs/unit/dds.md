# DDS Unit

DDS is a signal source Unit. It uses the AD9833 programmable waveform
generator + STM32F0 micro controller. Based on I2C communication
interface (addr:0x31) It can easily control the signal source to output multiple
waveforms (sine wave, triangle wave, square wave output, sawtooth wave, signal
output amplitude 0-0.6V) and adjust the frequency and phase.

Support the following products:

DDSUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DDSUnit

i2c0 = None
dds_0 = None

def setup():
    global i2c0, dds_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    dds_0 = DDSUnit(i2c0, 0x31)
    dds_0.set_mode(dds_0.WAVE_SQUARE)
    dds_0.set_freq(0, 1000)

def loop():
    global i2c0, dds_0
    M5.update()

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

## class DDSUnit

## Constructors

### `class DDSUnit(i2c: I2C, address: int  list  tuple = 0x31)`

    Initialize the DDSUnit.

    - Parameter `i2c` (`I2C`): The i2c bus the unit is connected to.
    - Parameter `address` (`int`): The I2C address of the DDSUnit. Default is 0x31.

## Methods

### `DDSUnit.set_freq(index: int = 0, freq: int = 1000) -> None`

    Set the frequency of the DDS.

    - Parameter `index` (`int`): The register number of the DDS, range from 0 to 1.
    - Parameter `freq` (`int`): The frequency of the DDS in Hz.

### `DDSUnit.set_phase(index: int = 0, phase: int = 0) -> None`

    Set the phase of the DDS.

    - Parameter `index` (`int`): The register number of the DDS, range from 0 to 1.
    - Parameter `phase` (`int`): The phase of the DDS in degrees.

### `DDSUnit.set_freq_phase(f_index: int = 0, freq: int = 1000, p_index: int = 0, phase: int = 0) -> None`

    Set the frequency and phase of the DDS.

    - Parameter `f_index` (`int`): The register number of the frequency, range from 0 to 1.
    - Parameter `freq` (`int`): The frequency of the DDS in Hz.
    - Parameter `p_index` (`int`): The register number of the phase, range from 0 to 1.
    - Parameter `phase` (`int`): The phase of the DDS in degrees.

### `DDSUnit.set_mode(mode) -> None`

    Set the output mode of the DDS.

    - Parameter `mode` (`int`): The output mode of the DDS.

        Options:
            - `DDSUnit.WAVE_SINE`: Sine
            - `DDSUnit.WAVE_TRIANGLE`: Triangle
            - `DDSUnit.WAVE_SQUARE`: Square
            - `DDSUnit.WAVE_SAWTOOTH`: Sawtooth
            - `DDSUnit.WAVE_DC`: DC

### `DDSUnit.set_ctrl(f_index_sel: int = 0, p_index_sel: int = 0, disable_mclk=False, disable_dac=False, reset=False) -> None`

    Set the control bytes of the DDS.

    - Parameter `f_index_sel` (`int`): The frequency register select. range from 0 to 1.
    - Parameter `p_index_sel` (`int`): The phase register select. range from 0 to 1.
    - Parameter `disable_mclk` (`bool`): disable the MCLK.
    - Parameter `disable_dac` (`bool`): disable the DAC.
    - Parameter `reset` (`bool`): reset the DDS. If is true, other parameters will be ignored.

### `DDSUnit.select_freq_reg(index: int = 0) -> None`

    Select the frequency register of the DDS.

    - Parameter `index` (`int`): The index of the frequency register. range from 0 to 1

### `DDSUnit.select_phase_reg(index: int = 0) -> None`

    Select the phase register of the DDS.

    - Parameter `index` (`int`): The index of the phase register. range from 0 to 1

### `DDSUnit.quick_output(mode: int = WAVE_SINE, freq: int = 1000, phase: int = 0) -> None`

    Quickly set the output mode, frequency and phase of the DDS.

    - Parameter `mode` (`int`): The output mode of the DDS.

        Options:
            - `DDSUnit.WAVE_SINE`: Sine
            - `DDSUnit.WAVE_TRIANGLE`: Triangle
            - `DDSUnit.WAVE_SQUARE`: Square
            - `DDSUnit.WAVE_SAWTOOTH`: Sawtooth
            - `DDSUnit.WAVE_DC`: DC

    - Parameter `freq` (`int`): The frequency of the DDS in Hz.
    - Parameter `phase` (`int`): The phase of the DDS in degrees.

### `DDSUnit.output(f_index: int = 0, p_index: int = 0) -> None`

    Output the DDS signal.

    - Parameter `f_index` (`int`): The index of the frequency register. range from 0 to 1
    - Parameter `p_index` (`int`): The index of the phase register. range from 0 to 1

### `DDSUnit.set_sleep_mode(mode: int = SLEEP_MODE_1) -> None`

    Set the sleep mode of the DDS.

    - Parameter `mode` (`int`): The sleep mode of the DDS.

        Options:
            - `DDSUnit.SLEEP_MODE_NONE`: None
            - `DDSUnit.SLEEP_MODE_1`: Disable MCLK
            - `DDSUnit.SLEEP_MODE_2`: Disable MCLK and DAC

### `DDSUnit.reset() -> None`

    Reset the DDS.

## Constants

### `DDSUnit.WAVE_SINE`

    Sine wave output.

### `DDSUnit.WAVE_TRIANGLE`

    Triangle wave output.

### `DDSUnit.WAVE_SQUARE`

    Square wave output.

### `DDSUnit.WAVE_SAWTOOTH`

    Sawtooth wave output.

### `DDSUnit.WAVE_DC`

    DC wave output.

### `DDSUnit.SLEEP_MODE_NONE`

    No sleep mode.

### `DDSUnit.SLEEP_MODE_1`

    Disable mclk but keep dac.

### `DDSUnit.SLEEP_MODE_2`

    Disable mclk and dac.
