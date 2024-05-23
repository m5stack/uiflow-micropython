DDSUnit
=======

.. include:: ../refs/unit.dds.ref

DDS is a signal source Unit. It uses the AD9833 programmable waveform
generator + STM32F0 micro controller. Based on I2C communication
interface (addr:0x31) It can easily control the signal source to output multiple
waveforms (sine wave, triangle wave, square wave output, sawtooth wave, signal
output amplitude 0-0.6V) and adjust the frequency and phase.


Support the following products:

|DDSUnit|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import DDSUnit
    i2c = I2C(1, scl=33, sda=32)
    dds = DDSUnit(i2c)
    dds.quick_output(DDSUnit.WAVE_SINE, 1000, 0)

    for x in i2c.readfrom_mem(0x31, 0x30, 6): print('%02X' %x);


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html


class DDSUnit
-------------

Constructors
------------

.. class:: DDSUnit(i2c: I2C, address: int | list | tuple = 0x31)

    Initialize the DDSUnit.

    :param I2C i2c: The i2c bus the unit is connected to.
    :param int address: The I2C address of the DDSUnit. Default is 0x31.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: DDSUnit.set_freq(index: int = 0, freq: int = 1000) -> None

    Set the frequency of the DDS.

    :param int index: The register number of the DDS, range from 0 to 1.
    :param int freq: The frequency of the DDS in Hz.

    UIFLOW2:

        |set_freq.svg|


.. method:: DDSUnit.set_phase(index: int = 0, phase: int = 0) -> None

    Set the phase of the DDS.

    :param int index: The register number of the DDS, range from 0 to 1.
    :param int phase: The phase of the DDS in degrees.

    UIFLOW2:

        |set_phase.svg|


.. method:: DDSUnit.set_freq_phase(f_index: int = 0, freq: int = 1000, p_index: int = 0, phase: int = 0) -> None

    Set the frequency and phase of the DDS.

    :param int f_index: The register number of the frequency, range from 0 to 1.
    :param int freq: The frequency of the DDS in Hz.
    :param int p_index: The register number of the phase, range from 0 to 1.
    :param int phase: The phase of the DDS in degrees.

    UIFLOW2:

        |set_freq_phase.svg|


.. method:: DDSUnit.set_mode(mode) -> None

    Set the output mode of the DDS.

    :param int mode: The output mode of the DDS.

        Options:
            - ``DDSUnit.WAVE_SINE``: Sine
            - ``DDSUnit.WAVE_TRIANGLE``: Triangle
            - ``DDSUnit.WAVE_SQUARE``: Square
            - ``DDSUnit.WAVE_SAWTOOTH``: Sawtooth
            - ``DDSUnit.WAVE_DC``: DC

    UIFLOW2:

        |set_mode.svg|


.. method:: DDSUnit.set_ctrl(f_index_sel: int = 0, p_index_sel: int = 0, disable_mclk=False, disable_dac=False, reset=False) -> None

    Set the control bytes of the DDS.

    :param int f_index_sel: The frequency register select. range from 0 to 1.
    :param int p_index_sel: The phase register select. range from 0 to 1.
    :param bool disable_mclk: disable the MCLK.
    :param bool disable_dac: disable the DAC.
    :param bool reset: reset the DDS. If is true, other parameters will be ignored.

    UIFLOW2:

        |set_ctrl.svg|


.. method:: DDSUnit.select_freq_reg(index: int = 0) -> None

    Select the frequency register of the DDS.

    :param int index: The index of the frequency register. range from 0 to 1

    UIFLOW2:

        |select_freq_reg.svg|


.. method:: DDSUnit.select_phase_reg(index: int = 0) -> None

    Select the phase register of the DDS.

    :param int index: The index of the phase register. range from 0 to 1

    UIFLOW2:

        |select_phase_reg.svg|


.. method:: DDSUnit.quick_output(mode: int = WAVE_SINE, freq: int = 1000, phase: int = 0) -> None

    Quickly set the output mode, frequency and phase of the DDS.

    :param int mode: The output mode of the DDS.

        Options:
            - ``DDSUnit.WAVE_SINE``: Sine
            - ``DDSUnit.WAVE_TRIANGLE``: Triangle
            - ``DDSUnit.WAVE_SQUARE``: Square
            - ``DDSUnit.WAVE_SAWTOOTH``: Sawtooth
            - ``DDSUnit.WAVE_DC``: DC

    :param int freq: The frequency of the DDS in Hz.
    :param int phase: The phase of the DDS in degrees.

    UIFLOW2:

        |quick_output.svg|


.. method:: DDSUnit.output(f_index: int = 0, p_index: int = 0) -> None

    Output the DDS signal.

    :param int f_index: The index of the frequency register. range from 0 to 1
    :param int p_index: The index of the phase register. range from 0 to 1

    UIFLOW2:

        |output.svg|

.. method:: DDSUnit.set_sleep_mode(mode: int = SLEEP_MODE_1) -> None

    Set the sleep mode of the DDS.

    :param int mode: The sleep mode of the DDS.

        Options:
            - ``DDSUnit.SLEEP_MODE_NONE``: None
            - ``DDSUnit.SLEEP_MODE_1``: Disable MCLK
            - ``DDSUnit.SLEEP_MODE_2``: Disable MCLK and DAC

    UIFLOW2:

        |set_sleep_mode.svg|


.. method:: DDSUnit.reset() -> None

    Reset the DDS.

    UIFLOW2:

        |reset.svg|


Constants
---------

.. data:: DDSUnit.WAVE_SINE

    Sine wave output.

.. data:: DDSUnit.WAVE_TRIANGLE

    Triangle wave output.

.. data:: DDSUnit.WAVE_SQUARE

    Square wave output.

.. data:: DDSUnit.WAVE_SAWTOOTH

    Sawtooth wave output.

.. data:: DDSUnit.WAVE_DC

    DC wave output.

.. data:: DDSUnit.SLEEP_MODE_NONE

    No sleep mode.

.. data:: DDSUnit.SLEEP_MODE_1

    Disable mclk but keep dac.

.. data:: DDSUnit.SLEEP_MODE_2

    Disable mclk and dac.
