PPS Module
==========

.. include:: ../refs/module.pps.ref

The `PPS` class controls a Programmable Power Supply (PPS), capable of providing
an output up to 30V and 5A. It allows for precise control over the output
voltage and current, with features to read back the actual output values and the
module's status.


Support the following products:

    |PPSModule|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import PPSModule

    pps = PPSModule(addr=0x35)
    pps.set_output_voltage(5.5)
    pps.set_output_current(1)
    pps.enable_output()

    # Read values and status
    print("Voltage:", pps.read_output_voltage(), "V")
    print("Current:", pps.read_output_current(), "A")
    print("Mode:", pps.read_psu_running_mode())


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html


class PPSModule
---------------

Constructors
-------------

.. class:: PPSModule(addr=0x35)

    Creates a PPS object to interact with the programmable power supply.

    - ``addr``: I2C address of the PPS device (default is `0x35`).


Methods
-------

.. method:: PPSModule.set_output(enable: bool)

    Enable or disable the PPS output.

    - ``enable``: True to enable, False to disable.

    UIFLOW2:

        |set_output.svg|


.. method:: PPSModule.enable_output()

    Enable the PPS output.

    UIFLOW2:

        |enable_output.svg|


.. method:: PPSModule.disable_output()

    Disable the PPS output.

    UIFLOW2:

        |disable_output.svg|


.. method:: PPSModule.set_output_voltage(voltage: float)

    Set the output voltage of the PPS.

    - ``voltage``: Desired output voltage from 0.0 to 30.0 volts.

    UIFLOW2:

        |set_output_voltage.svg|


.. method:: PPSModule.set_output_current(current: float)

    Set the output current of the PPS.

    - ``current``: Desired output current from 0.0A to 5.0A.

    UIFLOW2:

        |set_output_current.svg|


.. method:: PPSModule.read_psu_running_mode() -> int

    Read the PSU running mode.

    UIFLOW2:

        |read_psu_running_mode.svg|


.. method:: PPSModule.read_output_current() -> float

    Read the current output current.

    UIFLOW2:

        |read_output_current.svg|


.. method:: PPSModule.read_output_voltage() -> float

    Read the current output voltage.

    UIFLOW2:

        |read_output_voltage.svg|


.. method:: PPSModule.read_input_voltage() -> float

    Read the input voltage.

    UIFLOW2:

        |read_input_voltage.svg|


.. method:: PPSModule.read_data_update_flag() -> int

    Read the data update flag.

    UIFLOW2:

        |read_data_update_flag.svg|


.. method:: PPSModule.read_mcu_temperature() -> float

    Read the MCU temperature.

    UIFLOW2:

        |read_mcu_temperature.svg|


.. method:: PPSModule.read_module_id() -> int

    Read the module ID.

    UIFLOW2:

        |read_module_id.svg|


.. method:: PPSModule.read_uid() -> bytearray

    Read the unique identifier (UID).

    UIFLOW2:

        |read_uid.svg|


.. method:: PPSModule.get_i2c_address() -> int

    Get the current I2C address of the device.

    UIFLOW2:

        |get_i2c_address.svg|


.. method:: PPSModule.set_i2c_address(new_address: int)

    Set a new I2C address for the device.

    - ``new_address``: The new I2C address to set.

    UIFLOW2:

        |set_i2c_address.svg|
