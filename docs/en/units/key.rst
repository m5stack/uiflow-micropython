KeyUnit
=======

.. include:: ../refs/unit.key.ref


Unit Key is a single mechanical key input unit with built-in RGB LED. The key
shaft adopts Blue switch with tactile bump and audible click features. Embedded
with one programable RGB LED - SK6812, supports 256 level brightness.
Two digital IOs are available for key status and LED control key status and
lighting control. Suitable for multiple HMI applications.


Support the following products:

    |KeyUnit|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import KeyUnit
    key = KeyUnit((33,32)) # for core2
    key.set_color(0x00FF00)
    key.set_brightness(10)
    key.get_key_state()
    while True:
        key.tick(None) # update key status


class KeyUnit
-------------

Constructors
------------

.. class:: KeyUnit(port: tuple)

    Initialize the KeyUnit.

    :param tuple port: The port to which the KeyUnit is connected. port[0]: key pin, port[1]: LEDs pin.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: KeyUnit.get_key_state() -> int

    Get the state of the key.

    :return: 0: released, 1: pressed, 2: long pressed.

    UIFLOW2:

        |get_key_state.svg|


.. method:: KeyUnit.set_color(color: int) -> None

    Set the color of the LED.

    :param int color: The color of the LED.

    UIFLOW2:

        |set_color.svg|


.. method:: KeyUnit.set_brightness(br: int) -> None

    Set the brightness of the LED.

    :param int br: The brightness of the LED, range from 0 to 100.

    UIFLOW2:

        |set_brightness.svg|


.. method:: KeyUnit.isHolding()

    Returns whether the Button object is in a long press state.

    UIFLOW2:

        |isHolding.svg|


.. method:: KeyUnit.isPressed()

    Returns whether the Button object is in a pressed state.

    UIFLOW2:

        |isPressed.svg|


.. method:: KeyUnit.isReleased()

    Returns whether the Button object is in a released state.

    UIFLOW2:

        |isReleased.svg|


.. method:: KeyUnit.wasClicked()

    Returns True when the Button object is briefly pressed and released.

    UIFLOW2:

        |wasClicked.svg|


.. method:: KeyUnit.wasDoubleClicked()

    Returns True when the Button object is double-clicked after a certain amount of time.

    UIFLOW2:

        |wasDoubleClicked.svg|


.. method:: KeyUnit.wasHold()

    Returns True when the Button object is held down for a certain amount of time.

    UIFLOW2:

        |wasHold.svg|


.. method:: KeyUnit.wasPressed()

    Returns True when the Button object is pressed.

    UIFLOW2:

        |wasPressed.svg|


.. method:: KeyUnit.wasReleased()

    Returns True when the Button object is released.

    UIFLOW2:

        |wasReleased.svg|


.. method:: KeyUnit.wasSingleClicked()

    Returns True when the Button object is single-clicked after a certain amount of time.

    UIFLOW2:

        |wasSingleClicked.svg|


Event Handling
--------------

.. method:: KeyUnit.setCallback(type:Callback_Type, cb)

    Sets the event callback function.

    UIFLOW2:

        |setCallback.svg|


Constants
---------

.. data:: KeyUnit.CB_TYPE

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
