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


class IRUnit
------------

Constructors
------------

.. class:: IRUnit(port)

    Create an IRUnit object.

    :param tuple port: The port to which the IR unit is connected. the tuple is a pair of values, the first value is the receive pin, and the second value is the transmit pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: IRUnit.tx()

    Sends an ir signal value to an address.

    UIFLOW2:

        |tx.png|


.. method:: IRUnit.rx_event()

    Determine when the infrared signal is read and start to do some processing procedures.

    UIFLOW2:

        |rx_event.png|
