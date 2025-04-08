Button
======

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.button.ref


Button is used to control the built-in buttons inside the host device. Below is
the detailed Button support for the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+------+------+------+--------+--------+
    |                 | BtnA | BtnB | BtnC | BtnPWR | BtnEXT |
    +=================+======+======+======+========+========+
    | AtomS3          | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | AtomS3 Lite     | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | AtomS3U         | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | StampS3         | |S|  |      |      |        |        |
    +-----------------+------+------+------+--------+--------+
    | CoreS3          |      |      |      | |S|    |        |
    +-----------------+------+------+------+--------+--------+
    | Core2           | |S|  | |S|  | |S|  |        |        |
    +-----------------+------+------+------+--------+--------+
    | TOUGH           |      |      |      |        |        |
    +-----------------+------+------+------+--------+--------+

.. |S| unicode:: U+2714


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *

    def btnPWR_wasClicked_event(state):
        global label0
        label0.setText('clicked')

    def btnPWR_wasHold_event(state):
        global label0
        label0.setText('hold')

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 58, 43, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_HOLD, cb=btnPWR_wasHold_event)

    while True:
        M5.update()


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |button_cores3_example.m5f2|


class Button
------------

.. important::

    Methods of Button Class heavily rely on ``M5.begin()`` |M5.begin.png| and ``M5.update()`` |M5.update.png|.

    All calls to methods of Button objects should be placed after ``M5.begin()`` |M5.begin.png| and ``M5.update()`` |M5.update.png| should be called in the main loop.


Methods
-------

.. method:: Button.isHolding()

    Returns whether the Button object is in a long press state.

    UIFLOW2:

        |isHolding.png|


.. method:: Button.isPressed()

    Returns whether the Button object is in a pressed state.

    UIFLOW2:

        |isPressed.png|


.. method:: Button.isReleased()

    Returns whether the Button object is in a released state.

    UIFLOW2:

        |isReleased.png|


.. method:: Button.wasClicked()

    Returns True when the Button object is briefly pressed and released.

    UIFLOW2:

        |wasClicked.png|


.. method:: Button.wasDoubleClicked()

    Returns True when the Button object is double-clicked after a certain amount of time.

    UIFLOW2:

        |wasDoubleClicked.png|


.. method:: Button.wasHold()

    Returns True when the Button object is held down for a certain amount of time.

    UIFLOW2:

        |wasHold.png|


.. method:: Button.wasPressed()

    Returns True when the Button object is pressed.

    UIFLOW2:

        |wasPressed.png|


.. method:: Button.wasReleased()

    Returns True when the Button object is released.

    UIFLOW2:

        |wasReleased.png|


.. method:: Button.wasSingleClicked()

    Returns True when the Button object is single-clicked after a certain amount of time.

    UIFLOW2:

        |wasSingleClicked.png|


Event Handling
--------------

.. method:: Button.setCallback(type:Callback_Type, cb)

    Sets the event callback function.

    UIFLOW2:

        |setCallback.png|


Constants
---------

.. data:: Button.CB_TYPE

    A Callback_Type object.


class Callback_Type
-------------------

Constants
---------

.. data:: Callback_Type.WAS_CLICKED

    Single click event type.


.. data:: Callback_Type.WAS_DOUBLECLICKED

    Double click event type.


.. data:: Callback_Type.WAS_HOLD

    Long press event type.


.. data:: Callback_Type.WAS_PRESSED


    Press event type

.. data:: Callback_Type.WAS_RELEASED

    Release event type
