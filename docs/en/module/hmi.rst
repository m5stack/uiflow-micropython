
HMI Module
==========

.. include:: ../refs/module.hmi.ref

Support the following products:

|HMI Module|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import HMIModule
    import time


    title0 = None
    label0 = None
    label1 = None
    label2 = None
    label3 = None
    label4 = None
    label5 = None
    label6 = None
    hmi_0 = None


    led_a_state = None
    led_b_state = None
    btn_a_state = None
    btn_b_state = None


    def setup():
        global title0, label0, label1, label2, label3, label4, label5, label6, hmi_0, led_a_state, led_b_state, btn_a_state, btn_b_state

        M5.begin()
        Widgets.fillScreen(0x222222)
        title0 = Widgets.Title("HMI Core2 Test", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
        label0 = Widgets.Label("Btn enc:", 0, 81, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label1 = Widgets.Label("Btn A:", 0, 129, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label2 = Widgets.Label("Btn B:", 0, 176, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label3 = Widgets.Label("Rotary:", 0, 37, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label4 = Widgets.Label("LED A:", 173, 106, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label5 = Widgets.Label("LED B:", 173, 164, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label6 = Widgets.Label("Rotary Inc:", 173, 41, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

        hmi_0 = HMIModule(address=0x41)
        hmi_0.set_rotary_value(0)


    def loop():
        global title0, label0, label1, label2, label3, label4, label5, label6, hmi_0, led_a_state, led_b_state, btn_a_state, btn_b_state
        M5.update()
        led_a_state = hmi_0.get_led_state(1)
        led_b_state = hmi_0.get_led_state(2)
        btn_a_state = hmi_0.get_button_status(2)
        btn_b_state = hmi_0.get_button_status(3)
        label0.setText(str((str('Rotary:') + str((hmi_0.get_button_status(1))))))
        label1.setText(str((str('Btn A:') + str(btn_a_state))))
        label2.setText(str((str('Btn B:') + str(btn_b_state))))
        label4.setText(str((str('LED A:') + str(led_a_state))))
        label5.setText(str((str('LED B:') + str(led_b_state))))
        label3.setText(str((str('Enc:') + str((hmi_0.get_rotary_value())))))
        if hmi_0.get_button_status(1):
            label6.setText(str((str('Rotary Inc:') + str((hmi_0.get_rotary_increments())))))
        elif btn_a_state:
            led_a_state = not led_a_state
            hmi_0.set_led_state(1, led_a_state)
        elif btn_b_state:
            led_b_state = not led_b_state
            hmi_0.set_led_state(2, led_b_state)
            hmi_0.reset_rotary_value()
        time.sleep_ms(200)


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

    |hmi_core2_example.m5f2|

class HMIModule
---------------

Constructors
------------

.. class:: HMIModule(address)

    Init I2C Module HMI I2C Address.

    :param int|list|tuple address: I2C address of the HMIModule.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: HMIModule.get_rotary_value() -> int

    Get the current value of the rotary.


    UIFLOW2:

        |get_rotary_value.png|

.. method:: HMIModule.set_rotary_value(value)

    Set the rotary value.

    :param int value: rotary value(-2147483648-2147483647).


    UIFLOW2:

        |set_rotary_value.png|

.. method:: HMIModule.reset_rotary_value()

    Reset the rotary value.

    UIFLOW2:

        |reset_rotary_value.png|

.. method:: HMIModule.get_rotary_increments() -> int

    Get the increment value of the rotary.

    UIFLOW2:

        |get_rotary_increments.png|

.. method:: HMIModule.get_button_status(btn_num) -> int

    Get the state of a specific button.

    :param int btn_num: : Button number (1 to 3).

    UIFLOW2:

        |get_button_status.png|

.. method:: HMIModule.get_led_state(led_num) -> int

    Get the state of a specific LED.

    :param int led_num: : LED number (1 to 2).

    UIFLOW2:

        |get_led_state.png|

.. method:: HMIModule.set_led_state(led_num, state)

    Set the state of a specific LED.

    :param int led_num: : LED number (1 to 2).
    :param int state: : The state to set for the LED.

    UIFLOW2:

        |set_led_state.png|

.. method:: HMIModule.get_firmware_version() -> int

    Get the firmware version of the HMI module.


    UIFLOW2:

        |get_firmware_version.png|

.. method:: HMIModule.get_i2c_address() -> int

    Get the current I2C address of the HMI module.

    UIFLOW2:

        |get_i2c_address.png|

.. method:: HMIModule.set_i2c_address(addr)

    Set a new I2C address for the HMI module.

    :param int addr: : The new I2C address to set.

    UIFLOW2:

        |set_i2c_address.png|
