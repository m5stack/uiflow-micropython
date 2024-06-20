RELAY Unit
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


.. method:: RealyUnit.on()

   turn on the relay.

    UIFLOW2:

        |on.png|


.. method:: RealyUnit.off()

   Turn off the relay.

    UIFLOW2:

        |off.png|


.. method:: RealyUnit.set_status()

   Set the relay status (True or false).

    UIFLOW2:

        |set_status.png|
