Chain Angle
===========

.. include:: ../refs/chain.angle.ref

AngleChain is the helper class for angle sensor devices on the Chain bus. It provides methods to read angle values in different resolutions (12-bit and 8-bit ADC) and configure the clockwise rotation direction.

Support the following products:

    |Chain Angle|

UiFlow2 Example
---------------

Angle reading with RGB brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |m5core_chain_angle_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to read angle values from the Chain Angle sensor and control RGB brightness based on the angle value. 
The example reads 8-bit ADC values (0-255) and maps them to brightness values (0-100) for visual feedback.

UiFlow2 Code Block:

    |m5core_chain_angle_basic_example.png|

Example output:

    None

MicroPython Example
-------------------

Angle reading with RGB brightness control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to read angle values from the Chain Angle sensor and control RGB brightness based on the angle value. 
The example reads 8-bit ADC values (0-255) and maps them to brightness values (0-100) for visual feedback.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/angle/m5core_chain_angle_basic_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

AngleChain
^^^^^^^^^^

.. autoclass:: chain.angle.AngleChain
    :members:
    :member-order: bysource
    :exclude-members:

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.

