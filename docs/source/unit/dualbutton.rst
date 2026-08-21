Dual Button Unit
================

.. include:: ../refs/unit.dual_button.ref

The Dual Button Unit provides two independent buttons. Use ``DualButtonUnit``
for click, double-click, hold, and callback handling, or
``SimpleDualButtonUnit`` for direct pin reads and debounced edge polling.

Support the following products:

    |Dual_Button|

UiFlow2 Example
---------------

Button events
^^^^^^^^^^^^^

Open the |dual_button_core_example.m5f2| project in UiFlow2.

This example demonstrates how to read the button state and handle button
events in UiFlow2.

UiFlow2 Code Block:

    |example.png|

Example output:

    The button state is shown when a button event occurs.

MicroPython Example
-------------------

Button events and callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use ``DualButtonUnit`` for button state,
click, hold, and callback handling.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/dualbutton/dual_button_core_example.py
        :language: python
        :linenos:

Example output:

    The button state is printed when the blue button event occurs.

Simple polling
^^^^^^^^^^^^^^

This example demonstrates how to use ``SimpleDualButtonUnit`` to read the
pins directly and poll debounced press and release edges without ``tick()``
or callbacks.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/dualbutton/dual_button_simple_example.py
        :language: python
        :linenos:

Example output:

    Press and release events for the blue and red buttons are printed.

**API**
-------

DualButtonUnit
^^^^^^^^^^^^^^

.. function:: DualButtonUnit(port)

    Create two full-featured button objects.

    :param tuple port: Two button pin numbers.
    :return: The blue and red :class:`hardware.Button` objects.
    :rtype: tuple

    UiFlow2 Code Block:

        |init.png|

.. method:: Dual_Button.isHolding()

    Return whether the button is currently being held.

    UiFlow2 Code Block:

        |get_status.png|

.. method:: Dual_Button.setCallback(type, cb)

    Register a callback for the specified button event.

    :param int type: Button event type.
    :param callable cb: Function called when the event occurs.

    UiFlow2 Code Block:

        |setCallback.png|

.. method:: Dual_Button.tick(pin)

    Poll the button state machine. Call this method regularly in the loop.

    :param pin: Optional pin argument passed by an interrupt handler. Use
        ``None`` when polling from the loop.

    UiFlow2 Code Block:

        |tick.png|

SimpleDualButtonUnit
^^^^^^^^^^^^^^^^^^^^

.. function:: SimpleDualButtonUnit(port, active_low=True, debounce_ms=50)

    Create two :class:`SimpleButton` objects for direct polling.

    :param tuple port: Two button pin numbers.
    :param bool active_low: Use low level as the active state when ``True``.
        Active-low inputs use an internal pull-up and active-high inputs use
        an internal pull-down.
    :param int debounce_ms: Time in milliseconds that an input must remain
        stable before generating an edge event. Set to ``0`` to disable
        debounce.
    :return: The blue and red button objects.
    :rtype: tuple

SimpleButton
^^^^^^^^^^^^

.. class:: SimpleButton(pin_num, active_low=True, debounce_ms=50)

    Provide direct pin reads and debounced edge polling without callbacks.

    Call :meth:`SimpleButton.update` regularly before reading edge events.
    The :meth:`SimpleButton.value` and :meth:`SimpleButton.is_active` methods
    read the pin directly and do not require ``update()``.

    .. method:: SimpleButton.value()

        Return the raw pin value.

        :return: ``0`` or ``1``.
        :rtype: int

    .. method:: SimpleButton.is_active()

        Return whether the button is currently active according to
        ``active_low``.

        :return: ``True`` when the button is active.
        :rtype: bool

    .. method:: SimpleButton.update()

        Sample the pin and update the debounced edge state. Call this method
        once per loop iteration.

    .. method:: SimpleButton.was_pressed()

        Return whether a debounced press was detected by the latest call to
        :meth:`SimpleButton.update`.

        :rtype: bool

    .. method:: SimpleButton.was_released()

        Return whether a debounced release was detected by the latest call to
        :meth:`SimpleButton.update`.

        :rtype: bool
