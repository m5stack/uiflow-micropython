Relay Unit
==================

.. include:: ../refs/unit.relay.ref

Support the following products:

    |RELAY|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/relay/relay_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |relay_core_example.m5f2|


class RelayUnit
---------------

Constructors
------------

.. class:: RelayUnit(io)

    Create a RelayUnit object.

    The parameters is:
        - ``io`` Define the control pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: RelayUnit.get_status()

    Gets the relay switch status.

    UIFLOW2:

        |get_status.png|


.. method:: RelayUnit.on()

    Turn on the relay.

    UIFLOW2:

        |on.png|


.. method:: RelayUnit.off()

    Turn off the relay.

    UIFLOW2:

        |off.png|


.. method:: RelayUnit.set_status(x: bool)

    Set the relay status.

    :param bool x: ``True`` turns the relay on; ``False`` turns it off.

    UIFLOW2:

        |set_status.png|
