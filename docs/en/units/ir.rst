IR Unit
=======

.. include:: ../refs/unit.ir.ref

Support the following products:

    |IR|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/ir/ir_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |ir_core_example.m5f2|


class IR
--------------

Constructors
--------------

.. class:: IR(IO1,IO2)

    Create an IR object.

    The parameters is:
        - ``IO1,IO2`` Receive and transmit pin definitions.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ir.tx()

    Sends an ir signal value to an address.

    UIFLOW2:

        |tx.png|


.. method:: ir.rx_event()

    Determine when the infrared signal is read and start to do some processing procedures.

    UIFLOW2:

        |rx_event.png|
