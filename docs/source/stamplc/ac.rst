StamPLC AC
==========

.. sku: A160 

.. include:: ../refs/stamplc.ac.ref

ACStamPLC is a class that drives the relay and RGB LED on the AC extension board.

Support the following products:

    |StampPLC|

UiFlow2 Example
---------------

Relay and RGB LED control
^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |stamplc_ac_example.m5f2| project in UiFlow2.

This example demonstrates interactive control of the AC relay and RGB LED. Press button A to toggle the relay state.
When the relay is turned on, the red LED lights up; when turned off, the red LED turns off.

UiFlow2 Code Block:

    |stamplc_ac_example.png|

Example output:

    None


MicroPython Example
-------------------

Relay and RGB LED control
^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates interactive control of the AC relay and RGB LED. Press button A to toggle the relay state.
When the relay is turned on, the red LED lights up; when turned off, the red LED turns off.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamplc/ac/stamplc_ac_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

ACStamPLC
^^^^^^^^^

.. class:: ACStamPLC()

    Create a ACStamPLC object.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from stamplc import ACStamPLC

            ac = ACStamPLC()

    .. method:: set_relay(state)

        Switch the AC relay output.

        :param bool state: ``True`` turns the relay on, ``False`` releases it.

        UiFlow2 Code Block:

            |set_relay.png|

        MicroPython Code Block:

            .. code-block:: python

                ac.set_relay(state)

    .. method:: set_red_led(state)

        Control the red channel of the RGB LED.

        :param bool state: ``True`` lights the LED, ``False`` turns it off.

        UiFlow2 Code Block:

            |set_red_led.png|

        MicroPython Code Block:

            .. code-block:: python

                ac.set_red_led(state)

    .. method:: set_green_led(state)

        Control the green channel of the RGB LED.

        :param bool state: ``True`` lights the LED, ``False`` turns it off.

        UiFlow2 Code Block:

            |set_green_led.png|

        MicroPython Code Block:

            .. code-block:: python

                ac.set_green_led(state)

    .. method:: set_blue_led(state)

        Control the blue channel of the RGB LED.

        :param bool state: ``True`` lights the LED, ``False`` turns it off.

        UiFlow2 Code Block:

            |set_blue_led.png|

        MicroPython Code Block:

            .. code-block:: python

                ac.set_blue_led(state)

