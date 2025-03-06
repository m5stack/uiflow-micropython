Digital Input
=============

.. include:: ../refs/hardware.plcio.digitalinput.ref

Digital Input is used to read the digital input of host devices.


UiFlow2 Example
---------------

Get the digital input status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |stamplc_digital_input_example.m5f2| project in UiFlow2.

This example demonstrates how to get the status of a digital input and display the status on the screen.

UiFlow2 Code Block:

    |stamplc_digital_input_example.png|

Example output:

    None


MicroPython Example
-------------------

Get the digital input status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to get the status of a digital input and display the status on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/plcio/digital_input/stamplc_digital_input_example.py

Example output:

    None


**API**
-------

DigitalInput
^^^^^^^^^^^^

.. class:: DigitalInput(id: int)

    Initialize a digital input object.

    :param int id: The ID of the digital input. The range of ID is 1-8.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hadrware import DigitalInput

            in1 = DigitalInput(1)


    .. method:: DigitalInput.get_status() -> bool

        Get the status of the digital input.

        :return: The status of the digital input.
        :rtype: bool

        UiFlow2 Code Block:

            |get_status.png|

        MicroPython Code Block:

            .. code-block:: python

                in1.get_status()


    .. method:: DigitalInput.value() -> int

        Get the value of the digital input.

        :return: The value of the digital input.
        :rtype: int

        UiFlow2 Code Block:

            |value.png|

        MicroPython Code Block:

            .. code-block:: python

                in1.value()

    .. method:: DigitalInput.irq(handler=None, trigger=IRQ_FALLING | IRQ_RISING) -> None

        Enable interrupt for the pin.

        :param function handler: The interrupt handler function.
        :param int trigger: The interrupt trigger mode, DigitalInput.IRQ_FALLING or DigitalInput.IRQ_RISING.

        UiFlow2 Code Block:

            |irq.png|

        MicroPython Code Block:

            .. code-block:: python

                def handler(pin):
                    print('interrupt triggered')

                in1.irq(handler, DigitalInput.IRQ_FALLING)
