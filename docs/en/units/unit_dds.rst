
DDSUnit
=======

.. include:: ../refs/unit.dds.ref

DDS is a signal source Unit. It uses the AD9833 programmable waveform generator + STM32F0 micro controller. Based on I2C communication interface (addr:0x31) It can easily control the signal source to output multiple waveforms (sine wave, triangle wave, square wave output, sawtooth wave, signal output amplitude 0-0.6V) and adjust the frequency and phase.

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

.. method:: DDSUnit(i2c, address)

    Initialize the DDSUnit.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the DDSUnit.

    UIFLOW2:

        |__init__.svg|


Attributes
----------

- ``WAVE_SINE``: Sine wave output.
- ``WAVE_TRIANGLE``: Triangle wave output.
- ``WAVE_SQUARE``: Square wave output.
- ``WAVE_SAWTOOTH``: Sawtooth wave output.
- ``WAVE_DC``: DC wave output.
- ``SLEEP_MODE_1``: Disable mclk but keep dac.
- ``SLEEP_MODE_2``: Disable mclk and dac.

Methods
-------

.. method:: DDSUnit.set_freq(index, freq)

    Set the frequency of the DDS.

    - ``index``: The register number of the DDS, range from 0 to 1.
    - ``freq``: The frequency of the DDS in Hz.

    UIFLOW2:

        |set_freq.svg|

.. method:: DDSUnit.set_phase(index, phase)

    Set the phase of the DDS.

    - ``index``: The register number of the DDS, range from 0 to 1.
    - ``phase``: The phase of the DDS in degrees.

    UIFLOW2:

        |set_phase.svg|

.. method:: DDSUnit.set_freq_phase(f_index, freq, p_index, phase)

    Set the frequency and phase of the DDS.

    - ``f_index``: The register number of the frequency. range from 0 to 1.
    - ``freq``: The frequency of the DDS in Hz.
    - ``p_index``: The register number of the phase. range from 0 to 1.
    - ``phase``: The phase of the DDS in degrees.

    UIFLOW2:

        |set_freq_phase.svg|

.. method:: DDSUnit.set_mode(mode)

    Set the output mode of the DDS.

    - ``mode``: The output mode of the DDS.
        Options:
        - ``DDSUnit.WAVE_SINE``: Sine
        - ``DDSUnit.WAVE_TRIANGLE``: Triangle
        - ``DDSUnit.WAVE_SQUARE``: Square
        - ``DDSUnit.WAVE_SAWTOOTH``: Sawtooth
        - ``DDSUnit.WAVE_DC``: DC

    UIFLOW2:

        |set_mode.svg|

.. method:: DDSUnit.set_ctrl(f_index_sel, p_index_sel, disable_mclk, disable_dac, reset)

    Set the control bytes of the DDS.

    - ``f_index_sel``: The frequency register select. range from 0 to 1.
    - ``p_index_sel``: The phase register select. range from 0 to 1.
    - ``disable_mclk``: disable the MCLK.
    - ``disable_dac``: disable the DAC.
    - ``reset``: reset the DDS. If is true, other parameters will be ignored.

    UIFLOW2:

        |set_ctrl.svg|

.. method:: DDSUnit.select_freq_reg(index)

    Select the frequency register of the DDS.

    - ``index``: The index of the frequency register. range from 0 to 1

    UIFLOW2:

        |select_freq_reg.svg|

.. method:: DDSUnit.select_phase_reg(index)

    Select the phase register of the DDS.

    - ``index``: The index of the phase register. range from 0 to 1

    UIFLOW2:

        |select_phase_reg.svg|

.. method:: DDSUnit.quick_output(mode, freq, phase)

    Quickly set the output mode, frequency and phase of the DDS.

    - ``mode``: The output mode of the DDS.
        Options:
        - ``DDSUnit.WAVE_SINE``: Sine
        - ``DDSUnit.WAVE_TRIANGLE``: Triangle
        - ``DDSUnit.WAVE_SQUARE``: Square
        - ``DDSUnit.WAVE_SAWTOOTH``: Sawtooth
        - ``DDSUnit.WAVE_DC``: DC
    - ``freq``: The frequency of the DDS in Hz.
    - ``phase``: The phase of the DDS in degrees.

    UIFLOW2:

        |quick_output.svg|

.. method:: DDSUnit.output(f_index, p_index)

    Output the DDS signal.

    - ``f_index``: The index of the frequency register. range from 0 to 1
    - ``p_index``: The index of the phase register. range from 0 to 1

    UIFLOW2:

        |output.svg|

.. method:: DDSUnit.set_sleep_mode(mode)

    Set the sleep mode of the DDS.

    - ``mode``: The sleep mode of the DDS.
        Options:
        - ``DDSUnit.SLEEP_MODE_NONE``: None
        - ``DDSUnit.SLEEP_MODE_1``: Disable MCLK
        - ``DDSUnit.SLEEP_MODE_2``: Disable MCLK and DAC

    UIFLOW2:

        |set_sleep_mode.svg|

.. method:: DDSUnit.reset()

    Reset the DDS.


    UIFLOW2:

        |reset.svg|


