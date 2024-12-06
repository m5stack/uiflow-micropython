
Button Unit
==========

.. include:: ../refs/unit.button.ref

BUTTON is a single button Unit. The button status can be detected by the input pin by simply capturing the high/low electrical level. If the button is pressed, the signal level will be *high* if the button is released, the signal level will be *low*.

Support the following products:

|ButtonUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/button/button_core2_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |button_core2_example.m5f2|

class ButtonUnit
----------------

Constructors
------------

.. class:: ButtonUnit(pin_num, active_low, pullup_active)

    Initialize a Button instance with the specified pin, active-low configuration, and pull-up resistor state.

    :param  pin_num: The GPIO pin number connected to the button.
    :param bool active_low: Determines whether the button signal is active-low. Default is True.
    :param bool pullup_active: Specifies whether the internal pull-up resistor is enabled. Default is True.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: ButtonUnit.count_reset()

    Reset the count value to zero.


    UIFLOW2:

        |count_reset.png|


.. method:: ButtonUnit.isHolding()

    Check if the button is currently being held.


    UIFLOW2:

        |isHolding.png|

.. method:: ButtonUnit.setCallback(type, cb)

    Set a callback function for a specified button event type.

    :param  type: The event type (e.g., WAS_CLICKED, WAS_DOUBLECLICKED).
    :param  cb: The callback function to be executed for the event.

    UIFLOW2:

        |setCallback.png|

.. method:: ButtonUnit.tick(pin)

    Monitor the state transitions of a button based on its pin state and trigger appropriate handlers.

    UIFLOW2:

        |tick.png|