Rotary
======

.. include:: ../refs/hardware.rotary.ref


Rotary is used to control the rotary encoder integrated inside the host. Below
is the detailed Rotary support for the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+--------+
    | Controller      | Rotary |
    +=================+========+
    | Dial            | |S|    |
    +-----------------+--------+
    | DinMeter        | |S|    |
    +-----------------+--------+

.. |S| unicode:: U+2714


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *

    label0 = None
    rotary = None

    def btnA_wasClicked_event(state):
        global label0, rotary
        rotary.reset_rotary_value()
        label0.setText(str(rotary.get_rotary_value()))

    def setup():
        global label0, rotary

        M5.begin()
        Widgets.fillScreen(0x222222)
        label0 = Widgets.Label("0", 96, 80, 1.0, 0xffa000, 0x222222, Widgets.FONTS.DejaVu72)

        BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

        rotary = Rotary()

    def loop():
        global label0, rotary
        M5.update()
        if rotary.get_rotary_status():
            label0.setText(str(rotary.get_rotary_value()))

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

    |example.svg|


class Rotary
------------

Constructors
------------

.. class:: Rotary()

    Creates a Rotary object.

    UIFLOW2:

        |init.svg|

Methods
-------

.. method:: Rotary.get_rotary_status() -> bool

    Gets the rotation status of the Rotary object.

    UIFLOW2:

        |get_rotary_status.svg|


.. method:: Rotary.get_rotary_value() -> int

    .. note:: Cannot be used simultaneously with :meth:`Rotary.get_rotary_increments()`.

    Gets the rotation value of the Rotary object.

    UIFLOW2:

        |get_rotary_value.svg|


.. method:: Rotary.get_rotary_increments() -> int

    .. note:: Cannot be used simultaneously with :meth:`Rotary.get_rotary_increments()`.

    Gets the rotation increment of the Rotary object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.svg|


.. method:: Rotary.reset_rotary_value() -> None

    Resets the rotation value of the Rotary object.

    UIFLOW2:

        |reset_rotary_value.svg|


.. method:: Rotary.set_rotary_value() -> None

    Sets the rotation value of the Rotary object.

    UIFLOW2:

        |set_rotary_value.svg|
