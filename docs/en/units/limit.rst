
LimitUnit
==========

.. include:: ../refs/unit.limit.ref

The Unit Limit is a travel switch unit that provides a limit trigger signal to the MCU or other master peripherals by pulling the digital signal interface from 3.3V high to 0V low when the switch handle is closed by an external force. It is suitable for all kinds of moving machinery and equipment to control its stroke and carry out terminal limit protection.

Support the following products:

|LimitUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/limit/limit_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |limit_core2_example.m5f2|

class LimitUnit
----------------

Constructors
------------

.. class:: LimitUnit(pin_num, active_low, pullup_active)

    Initialize a Limit instance with the specified pin, active-low configuration, and pull-up resistor state.

    :param  pin_num: The GPIO pin number connected to the limit.
    :param bool active_low: Determines whether the limit signal is active-low. Default is True.
    :param bool pullup_active: Specifies whether the internal pull-up resistor is enabled. Default is True.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: LimitUnit.count_reset()

    Reset the count value to zero.


    UIFLOW2:

        |count_reset.png|


.. method:: LimitUnit.isHolding()

    Check if the limit is currently being held.


    UIFLOW2:

        |isHolding.png|

.. method:: LimitUnit.setCallback(type, cb)

    Set a callback function for a specified limit event type.

    :param  type: The event type (e.g., WAS_CLICKED, WAS_DOUBLECLICKED).
    :param  cb: The callback function to be executed for the event.

    UIFLOW2:

        |setCallback.png|

.. method:: LimitUnit.tick(pin)

    Monitor the state transitions of a limit based on its pin state and trigger appropriate handlers.

    UIFLOW2:

        |tick.png|