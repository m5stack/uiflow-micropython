Chain PIR
=========

.. include:: ../refs/chain.pir.ref

PIRChain is the helper class for PIR (Passive Infrared) sensor devices on the Chain bus. It provides methods to read IR induction values, configure trigger delay, and monitor PIR trigger events.

Support the following products:

    |Chain PIR|

UiFlow2 Example
---------------

PIR motion detection
^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_pir_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to use trigger callbacks from the Chain PIR sensor to update motion status on screen. It enables trigger auto-send, configures trigger hold time, and counts the detected duration while motion is active.

UiFlow2 Code Block:

    |m5core_chain_pir_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

PIR motion detection
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use trigger callbacks from the Chain PIR sensor to update motion status on screen. It enables trigger auto-send, configures trigger hold time, and counts the detected duration while motion is active.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/pir/m5core_chain_pir_basic_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

PIRChain
^^^^^^^^

.. autoclass:: chain.pir.PIRChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.

