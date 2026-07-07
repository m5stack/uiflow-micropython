Chain Buzzer
============

.. include:: ../refs/chain.buzzer.ref

BuzzerChain is the helper class for buzzer devices on the Chain bus. It provides methods to control buzzer frequency, duty cycle, play modes (auto play, manual play, note play), and play musical notes.

Support the following products:

    |Chain Buzzer|

UiFlow2 Example
---------------

Button tone playback
^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_buzzer_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Chain Buzzer in auto play mode. It initializes the buzzer RGB indicator, then plays 500 Hz, 1000 Hz, or 1500 Hz tones when button A, B, or C is clicked.

UiFlow2 Code Block:

    |m5core_chain_buzzer_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

Button tone playback
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to use the Chain Buzzer in auto play mode. It initializes the buzzer RGB indicator, then plays 500 Hz, 1000 Hz, or 1500 Hz tones when button A, B, or C is clicked.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/buzzer/m5core_chain_buzzer_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

BuzzerChain
^^^^^^^^^^^

.. autoclass:: chain.buzzer.BuzzerChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.

