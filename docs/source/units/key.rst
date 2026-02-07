Key Unit
========

.. include:: ../refs/unit.key.ref


Unit Key is a single mechanical key input unit with built-in RGB LED. The key
shaft adopts Blue switch with tactile bump and audible click features. Embedded
with one programable RGB LED - SK6812, supports 256 level brightness.
Two digital IOs are available for key status and LED control key status and
lighting control. Suitable for multiple HMI applications.


Support the following products:

    |KeyUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/key/cores3_key_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_key_example.m5f2|


class KeyUnit
-------------

Constructors
------------

.. class:: KeyUnit(port: tuple)

    Initialize the KeyUnit.

    :param tuple port: The port to which the KeyUnit is connected. port[0]: key pin, port[1]: LEDs pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: KeyUnit.get_key_state() -> int

    Get the state of the key.

    :return: 0: released, 1: pressed, 2: long pressed.

    UIFLOW2:

        |get_key_state.png|


.. method:: KeyUnit.set_color(color: int) -> None

    Set the color of the LED.

    :param int color: The color of the LED.

    UIFLOW2:

        |set_color.png|


.. method:: KeyUnit.set_brightness(br: int) -> None

    Set the brightness of the LED.

    :param int br: The brightness of the LED, range from 0 to 100.

    UIFLOW2:

        |set_brightness.png|


.. method:: KeyUnit.isHolding()

    Returns whether the Button object is in a long press state.

    UIFLOW2:

        |isHolding.png|


.. method:: KeyUnit.isPressed()

    Returns whether the Button object is in a pressed state.

    UIFLOW2:

        |isPressed.png|


.. method:: KeyUnit.isReleased()

    Returns whether the Button object is in a released state.

    UIFLOW2:

        |isReleased.png|


.. method:: KeyUnit.wasClicked()

    Returns True when the Button object is briefly pressed and released.

    UIFLOW2:

        |wasClicked.png|


.. method:: KeyUnit.wasDoubleClicked()

    Returns True when the Button object is double-clicked after a certain amount of time.

    UIFLOW2:

        |wasDoubleClicked.png|


.. method:: KeyUnit.wasHold()

    Returns True when the Button object is held down for a certain amount of time.

    UIFLOW2:

        |wasHold.png|


.. method:: KeyUnit.wasPressed()

    Returns True when the Button object is pressed.

    UIFLOW2:

        |wasPressed.png|


.. method:: KeyUnit.wasReleased()

    Returns True when the Button object is released.

    UIFLOW2:

        |wasReleased.png|


.. method:: KeyUnit.wasSingleClicked()

    Returns True when the Button object is single-clicked after a certain amount of time.

    UIFLOW2:

        |wasSingleClicked.png|


Event Handling
--------------

.. method:: KeyUnit.setCallback(type:Callback_Type, cb)

    Sets the event callback function.

    UIFLOW2:

        |setCallback.png|


Constants
---------

.. data:: KeyUnit.CB_TYPE

    A CB_TYPE object.


class CB_TYPE
-------------------

Constants
---------

.. data:: CB_TYPE.WAS_CLICKED

    Single click event type.


.. data:: CB_TYPE.WAS_DOUBLECLICKED

    Double click event type.


.. data:: CB_TYPE.WAS_HOLD

    Long press event type.

.. data:: CB_TYPE.WAS_PRESSED

    Press event type

.. data:: CB_TYPE.WAS_RELEASED

    Release event type