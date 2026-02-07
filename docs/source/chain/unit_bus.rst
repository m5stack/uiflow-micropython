Unit Chain Bus
==============

.. include:: ../refs/chain.unit_bus.ref

BusChainUnit is the helper class for Bus devices on the Chain bus. 
It provides methods to configure GPIO pins (input, output, external interrupt), read ADC values, and communicate with I2C devices. 
The class supports multiple work modes including GPIO output, GPIO input, external interrupt, ADC, and I2C.

Support the following products:

    |Unit Chain Bus|

UiFlow2 Example
---------------

GPIO control
^^^^^^^^^^^^

Open the |m5basic_unit_chain_bus_gpio_example.m5f2| project in UiFlow2.

This example demonstrates how to configure and use GPIO pins with the Unit Chain Bus module.
The example configures GPIO1 as input mode with pull-up, and GPIO2 as output mode with push-pull configuration.
It continuously reads GPIO1 input value every 200ms and displays the state (HIGH/LOW) on screen.
GPIO2 output level toggles every 1 second (every 5 cycles) between HIGH and LOW, demonstrating output control functionality.

UiFlow2 Code Block:

    |m5basic_unit_chain_bus_gpio_example.png|

Example output:

    None

ADC reading
^^^^^^^^^^^

Open the |m5basic_unit_chain_bus_adc_example.m5f2| project in UiFlow2.

This example demonstrates how to read ADC values from the Unit Chain Bus module and use them to control RGB brightness.

UiFlow2 Code Block:

    |m5basic_unit_chain_bus_adc_example.png|

Example output:

    None

I2C device communication
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5basic_unit_chain_bus_i2c_dlight_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Unit Chain Bus module to communicate with I2C devices. The example shows how to configure the bus for I2C mode and use it with I2C devices like the DLight sensor.

UiFlow2 Code Block:

    |m5basic_unit_chain_bus_i2c_example.png|

Example output:

    None

MicroPython Example
-------------------

GPIO control
^^^^^^^^^^^^

This example demonstrates how to configure and use GPIO pins with the Unit Chain Bus module.
The example configures GPIO1 as input mode with pull-up, and GPIO2 as output mode with push-pull configuration.
It continuously reads GPIO1 input value every 200ms and displays the state (HIGH/LOW) on screen.
GPIO2 output level toggles every 1 second (every 5 cycles) between HIGH and LOW, demonstrating output control functionality.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/unit_bus/m5basic_unit_chain_bus_gpio_example.py
        :language: python
        :linenos:

Example output:

    None

ADC reading
^^^^^^^^^^^

This example demonstrates how to read ADC values from the Unit Chain Bus module and use them to control RGB brightness.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/unit_bus/m5basic_unit_chain_bus_adc_example.py
        :language: python
        :linenos:

Example output:

    None

I2C device communication
^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use the Unit Chain Bus module to communicate with I2C devices. The example shows how to configure the bus for I2C mode and use it with I2C devices like the DLight sensor.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/unit_bus/m5basic_unit_chain_bus_i2c_dlight_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

BusChainUnit
^^^^^^^^^^^^

.. autoclass:: chain.unit_bus.BusChainUnit
    :members:
    :member-order: bysource
    :exclude-members:
