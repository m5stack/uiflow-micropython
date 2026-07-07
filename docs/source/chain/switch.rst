Chain Switch
============

.. include:: ../refs/chain.switch.ref

SwitchChain is the helper class for switch devices on the Chain bus. It provides methods to read ADC values (12-bit and 8-bit), configure switch thresholds, set slip mode, and monitor switch status changes.

Support the following products:

    |Chain Switch|

UiFlow2 Example
---------------

Switch status monitoring
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_switch_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to read ADC values and switch status from the Chain Switch sensor and display them on screen. It registers open/close trigger callbacks and updates the status label when the switch state changes.

UiFlow2 Code Block:

    |m5core_chain_switch_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

Switch status monitoring
^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to read ADC values and switch status from the Chain Switch sensor and display them on screen. It registers open/close trigger callbacks and updates the status label when the switch state changes.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/switch/m5core_chain_switch_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

SwitchChain
^^^^^^^^^^^

.. autoclass:: chain.switch.SwitchChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.

