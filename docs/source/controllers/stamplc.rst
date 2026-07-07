StamPLC
-------

.. sku: K141

.. include:: ../refs/stamplc.plc.ref

``StamPLC`` is the board-level helper for the built-in PLC I/O on StamPLC.

Supported Products:

    |StamPLC|

Create one ``StamPLC`` object, then access relay outputs, digital inputs, and the
built-in RGB LED from that object.

Channels are 1-based:

* ``relay[1]`` to ``relay[4]`` control the four relay outputs.
* ``input[1]`` to ``input[8]`` read the eight digital inputs.
* ``led.red``, ``led.green``, and ``led.blue`` control the built-in RGB LED.

MicroPython Examples
--------------------

Relay control
^^^^^^^^^^^^^

Open the |stamplc_relay_control_example.m5f2| project in UiFlow2.

This example uses button A to toggle relay output 1 and turns on the built-in blue LED.

UiFlow2 Code Block:

    |stamplc_relay_control_example.png|

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stamplc/stamplc_relay_control_example.py
        :language: python
        :linenos:

Digital input control
^^^^^^^^^^^^^^^^^^^^^

Open the |stamplc_input_example.m5f2| project in UiFlow2.

This example reads digital inputs 1-3 and uses them to control relay outputs 1-3.

UiFlow2 Code Block:

    |stamplc_input_example.png|

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stamplc/stamplc_input_example.py
        :language: python
        :linenos:

**API**
-------

StamPLC
^^^^^^^

.. class:: StamPLC()

    Create a StamPLC board helper.

    UiFlow2 Code Block:

        |stamplc_init.png|

    MicroPython Code Block:

        .. code-block:: python

            from stamplc import StamPLC

            plc = StamPLC()

    .. attribute:: relay

        Relay output bank. Relay channels are indexed from 1 to 4.
        Relays are initialized to ``False``/off when ``StamPLC()`` is created.

        .. method:: relay[channel].on()

            Turn one relay output on.

            :param int channel: Relay channel, 1-4.

            UiFlow2 Code Block:

                |relay_set_state2.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.relay[1].on()

        .. method:: relay[channel].off()

            Turn one relay output off.

            :param int channel: Relay channel, 1-4.

            UiFlow2 Code Block:

                |relay_set_state2.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.relay[1].off()

        .. method:: relay[channel].toggle()

            Toggle one relay output.

            :param int channel: Relay channel, 1-4.

            UiFlow2 Code Block:

                |relay_set_state2.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.relay[1].toggle()

        .. method:: relay[channel].value(state=None)

            Get or set one relay output.

            :param int channel: Relay channel, 1-4.
            :param bool state: Optional output state. ``True`` turns the relay on, ``False`` turns it off.
            :returns: Relay state when ``state`` is omitted.
            :rtype: bool or None

            UiFlow2 Code Block:

                |relay_set_value2.png|

                |relay_get_value2.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.relay[1].value(True)
                    state = plc.relay[1].value()

    .. attribute:: input

        Digital input bank. All digital input channels are initialized as inputs
        when ``StamPLC()`` is created. Input channels are indexed from 1 to 8.

        .. method:: input[channel].value()

            Read one input channel.

            :param int channel: Input channel, 1-8.
            :returns: The selected input value, ``0`` or ``1``.
            :rtype: int

            UiFlow2 Code Block:

                |digital_input_get_value2.png|

            MicroPython Code Block:

                .. code-block:: python

                    input_1 = plc.input[1].value()

        .. method:: input[channel].irq(handler, trigger)

            Set an interrupt handler for one input channel.
            The callback receives the input pin object; use ``pin.channel`` to get the channel number.

            :param int channel: Input channel, 1-8.
            :param function handler: Interrupt callback.
            :param int trigger: ``plc.input.IRQ_FALLING`` or ``plc.input.IRQ_RISING``.

            UiFlow2 Code Block:

                |digital_input_event2.png|

            MicroPython Code Block:

                .. code-block:: python

                    def input_1_falling_event(pin):
                        print("input", pin.channel, "falling")

                    plc.input[1].irq(input_1_falling_event, plc.input.IRQ_FALLING)

    .. attribute:: led

        Built-in RGB LED controller. The LED is driven by PI4IOE5V6408:
        red maps to P6, green maps to P5, and blue maps to P4.

        ``led.red``, ``led.green``, and ``led.blue`` provide the same methods.

        .. method:: led.red.on()

            Turn the red LED on.

            UiFlow2 Code Block:

                |led_set_state.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.led.red.on()

        .. method:: led.red.off()

            Turn the red LED off.

            UiFlow2 Code Block:

                |led_set_state.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.led.red.off()

        .. method:: led.red.toggle()

            Toggle the red LED.

            UiFlow2 Code Block:

                |led_set_state.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.led.red.toggle()

        .. method:: led.red.value(state=None)

            Get or set the red LED state.

            :param bool state: Optional LED state. ``True`` turns the LED on, ``False`` turns it off.
            :returns: LED state when ``state`` is omitted.
            :rtype: bool or None

            UiFlow2 Code Block:

                |led_set_value.png|

            MicroPython Code Block:

                .. code-block:: python

                    plc.led.red.value(True)
                    state = plc.led.red.value()

        MicroPython Code Block:

            .. code-block:: python

                plc.led.green.on()
                plc.led.blue.off()
                plc.led.blue.toggle()
