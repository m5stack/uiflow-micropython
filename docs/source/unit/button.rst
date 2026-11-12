
Button Unit
============

.. include:: ../refs/unit.button.ref

BUTTON is a single button Unit. The button status can be detected by the input pin by simply capturing the high/low electrical level. With the default active-low configuration, pressing the button produces a low signal and releasing it produces a high signal.

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

.. class:: ButtonUnit(port, active_low=True, type=SWITCH)

    Initialize the button input. ButtonUnit is an alias of LIMITUnit.

    :param tuple port: Grove GPIO tuple; the input uses the first pin, ``port[0]``.
    :param bool active_low: Whether a low signal means pressed. Default is True.
    :param int type: ``SWITCH`` (default) or ``COUNTER``, imported from ``unit.limit``.

    The input enables ``Pin.PULL_UP`` internally. There is no
    ``pullup_active`` constructor argument.

    .. code-block:: python

        from unit import ButtonUnit
        from unit.limit import SWITCH, COUNTER

        button = ButtonUnit((33, 32), active_low=True, type=SWITCH)


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