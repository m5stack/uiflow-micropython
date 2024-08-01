
AIN4Module
==========

.. include:: ../refs/module.ain4.ref

The following products are supported:

|AIN4Module|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import AIN4Module

    title0 = None
    label0 = None
    label1 = None
    label2 = None
    label3 = None
    ain4_20ma_0 = None

    def setup():
        global title0, label0, label1, label2, label3, ain4_20ma_0

        M5.begin()
        Widgets.fillScreen(0x222222)
        title0 = Widgets.Title("AIN 4-20mA Module Test", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
        label0 = Widgets.Label("CH1 Current:", 1, 60, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label1 = Widgets.Label("CH2 Current:", 1, 96, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label2 = Widgets.Label("CH3 Current:", 1, 131, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label3 = Widgets.Label("CH4 Current:", 1, 164, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

        ain4_20ma_0 = AIN4Module(address=0x55)
        ain4_20ma_0.set_cal_current(1, 20)
        ain4_20ma_0.set_cal_current(2, 20)
        ain4_20ma_0.set_cal_current(3, 20)
        ain4_20ma_0.set_cal_current(4, 20)

    def loop():
        global title0, label0, label1, label2, label3, ain4_20ma_0
        M5.update()
        label0.setText(str((str('CH1 Current:') + str((ain4_20ma_0.get_current_value(1))))))
        label1.setText(str((str('CH2 Current:') + str((ain4_20ma_0.get_current_value(2))))))
        label2.setText(str((str('CH3 Current:') + str((ain4_20ma_0.get_current_value(3))))))
        label3.setText(str((str('CH4 Current:') + str((ain4_20ma_0.get_current_value(4))))))

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


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |ain4_core2_example.m5f2|

class AIN4Module
----------------

Constructors
------------

.. class:: AIN4Module(address)

    Init I2C Module AIN 4-20mA I2C Address.

    :param int|list|tuple address: I2C address of the AIN4Module.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: AIN4Module.get_adc_raw_value(channel) -> int

     Retrieves the raw ADC value from the specified channel.

    :param int channel: The channel number (1 to 4) to read the ADC value from.

    :return: Raw ADC value as a 12-bit integer.

    UIFLOW2:

        |get_adc_raw_value.png|

.. method:: AIN4Module.get_current_value(channel) -> int

    Retrieves the current value (in mA) from the specified channel.

    :param int channel: The channel number (1 to 4) to read the current value from.

    :return: Current value in milliamperes (mA).


    UIFLOW2:

        |get_current_value.png|

.. method:: AIN4Module.set_cal_current(channel, val)

    Sets the calibration current for the specified channel.

    :param int channel: The channel number (1 to 4) to set the calibration for.
    :param int val: The calibration current value, ranging from 4 to 20 mA.

    UIFLOW2:

        |set_cal_current.png|

.. method:: AIN4Module.get_firmware_version() -> int

    Retrieves the firmware version of the AIN 4-20mA module.

    :return: Firmware version.

    UIFLOW2:

        |get_firmware_version.png|

.. method:: AIN4Module.get_i2c_address() -> str

    Retrieves the current I2C address of the AIN 4-20mA module.

    :return: I2C address as a string in hexadecimal format.

    UIFLOW2:

        |get_i2c_address.png|

.. method:: AIN4Module.set_i2c_address(addr)

    Sets a new I2C address for the AIN 4-20mA module.

    :param int addr: The new I2C address, must be between 0x08 and 0x78.

    UIFLOW2:

        |set_i2c_address.png|





