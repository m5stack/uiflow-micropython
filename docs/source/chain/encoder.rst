Chain Encoder
=============

.. include:: ../refs/chain.encoder.ref

EncoderChain is the helper class for encoder devices on the Chain bus. It provides methods to read encoder values and increments, reset the encoder, configure the clockwise rotation direction, and handle button events with RGB LED feedback.

Support the following products:

    |Chain Encoder|

UiFlow2 Example
---------------

Encoder reading with brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_encoder_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to read encoder values and increments, handle button click events, and control RGB LED brightness based on encoder rotation. The encoder value is displayed on screen and updated in real-time.

UiFlow2 Code Block:

    |m5core_chain_encoder_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

Encoder reading with brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to read encoder values and increments, handle button click events, and control RGB LED brightness based on encoder rotation. The encoder value is displayed on screen and updated in real-time.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/encoder/m5core_chain_encoder_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

EncoderChain
^^^^^^^^^^^^

.. autoclass:: chain.encoder.EncoderChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.

