Atomic HDriver Base
============================

.. sku: A092

.. include:: ../refs/base.hdriver.ref

Support the following products:

    |Atomic HDriver Base|

UiFlow2 Example:
--------------------------

Motor speed control 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3r_hdriver_base_example.m5f2| project in UiFlow2.

The example demonstrates the motor speed changing from low to high, high to low, and then reversing, changing from low to high and high to low.

UiFlow2 Code Block:

    |atoms3r_hdriver_base_example.png|

Example output:

    None
 
MicroPython Example:
--------------------------

Motor speed control
^^^^^^^^^^^^^^^^^^^^^^^^

The example demonstrates the motor speed changing from low to high, high to low, and then reversing, changing from low to high and high to low.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/hdriver/atoms3r_hdriver_base_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------

AtomicHDriverBase 
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: base.hdriver.AtomicHDriverBase
    :members:
