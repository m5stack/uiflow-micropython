
PLUS Module
=========

.. include:: ../refs/module.plus.ref

Support the following products:

|PLUS Module|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import PLUSModule



    title0 = None
    label2 = None
    label0 = None
    label1 = None
    plus_0 = None


    btn_state = None
    last_btn_state = None


    def setup():
        global title0, label2, label0, label1, plus_0, btn_state, last_btn_state

        M5.begin()
        Widgets.fillScreen(0x222222)
        title0 = Widgets.Title("PLUS Core2 Test", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
        label2 = Widgets.Label("Btn rotray:", 1, 166, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label0 = Widgets.Label("Rotary:", 1, 60, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
        label1 = Widgets.Label("Rotary Inc:", 1, 111, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

        plus_0 = PLUSModule(address=0x62)
        plus_0.set_rotary_value(0)


    def loop():
        global title0, label2, label0, label1, plus_0, btn_state, last_btn_state
        M5.update()
        btn_state = plus_0.get_button_status()
        label0.setText(str((str('Rotary:') + str((plus_0.get_rotary_value())))))
        label2.setText(str((str('Btn rotray:') + str(btn_state))))
        if btn_state and btn_state != last_btn_state:
            label1.setText(str((str('Rotary Inc:') + str((plus_0.get_rotary_increments())))))
        last_btn_state = btn_state


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

    |plus_core2_example.m5f2|

class PLUSModule
---------------

Constructors
------------

.. class:: PLUSModule(address)

    Init I2C Module PLUS I2C Address.

    :param int|list|tuple address: I2C address of the PLUSModule.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: PLUSModule.get_rotary_value() -> int

    Get the current value of the rotary.

    :return: The value of the rotary relative to the zero point.

    UIFLOW2:

        |get_rotary_value.png|

.. method:: PLUSModule.set_rotary_value(value)

    Set the rotary value.

    :param int value: rotary value.

    UIFLOW2:

        |set_rotary_value.png|

.. method:: PLUSModule.reset_rotary_value()

    Reset the rotary value.

    UIFLOW2:

        |reset_rotary_value.png|

.. method:: PLUSModule.set_rotary_value(value)

    Set the rotary value.

    :param int value: rotary value.

    UIFLOW2:

        |set_rotary_value.png|

.. method:: PLUSModule.get_rotary_increments() -> int

    Get the increments of the rotary value since the last call of this function.

    :return: The increment value of the rotary.

    UIFLOW2:

        |get_rotary_increments.png|

.. method:: HMIModule.get_button_status() -> int

    Get the state of a specific button.

    UIFLOW2:

        |get_button_status.png|

