Chain Mic
=========

.. include:: ../refs/chain.mic.ref

MicChain is the helper class for microphone devices on the Chain bus. It provides methods to read ADC values, configure threshold values, set trigger cycle, and monitor microphone trigger events.

Support the following products:

    |Chain Mic|

UiFlow2 Example
---------------

Microphone sound detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_mic_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to read ADC values from the Chain Mic sensor and monitor sound detection. 

UiFlow2 Code Block:

    |m5core_chain_mic_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

Microphone sound detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to read ADC values from the Chain Mic sensor and monitor sound detection.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/mic/m5core_chain_mic_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

MicChain
^^^^^^^^

.. autoclass:: chain.mic.MicChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.

