Pin
===

.. include:: ../refs/hardware.pin.ref

The Pin class is used to manage GPIO operations. Below is the detailed support for the Pin class:

Micropython Example:

    .. literalinclude:: ../../../examples/hardware/pin/pin_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |pin_cores3_example.m5f2|

class Pin
---------

Constructors
------------

.. class:: Pin(id, mode=-1, pull=-1)

    Access the pin peripheral (GPIO pin) associated with the given ``id``.

    :param int id: is mandatory and can be an arbitrary object.
    :param int mode: specifies the pin mode.

        - ``Pin.IN`` - Pin is configured for input.  If viewed as an output the pin is in high-impedance state.

        - ``Pin.OUT`` - Pin is configured for (normal) output.

    :param int pull: specifies if the pin has a (weak) pull resistor attached.

        - ``None`` - No pull up or down resistor.
        - ``Pin.PULL_UP`` - Pull up resistor enabled.
        - ``Pin.PULL_DOWN`` - Pull down resistor enabled.

    UIFLOW2:

        |init.png|

Methods
--------
.. method:: Pin.value([value])

   Set the value of the pin.

   The argument ``value`` can be anything that converts to a boolean.
   If it converts to ``True``, the pin is set to state '1', otherwise it is set
   to state '0'.

   The behaviour of this method depends on the mode of the pin:

     - ``Pin.IN`` - The value is stored in the output buffer for the pin.  The
       pin state does not change, it remains in the high-impedance state.  The
       stored value will become active on the pin as soon as it is changed to
       ``Pin.OUT`` mode.
     - ``Pin.OUT`` - The output buffer is set to the given value immediately.

    UIFLOW2:

        |set_value.png|

        |set_value1.png|

        |get_value.png|



.. method:: Pin.off() -> None

    Sets the pin to low level.

    UIFLOW2:

        |off.png|

.. method:: Pin.on() -> None

    Sets the pin to high level.

    UIFLOW2:

        |on.png|

Constants
---------

.. data:: Pin.IN

    Input mode

.. data:: Pin.OUT

    Output mode

.. data:: Pin.PULL_UP

    Pull-up resistor

.. data:: Pin.PULL_DOWN

    Pull-down resistor