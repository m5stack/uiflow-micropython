PIR Unit
========

.. include:: ../refs/unit.pir.ref

Support the following products:

    |PIR|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/pir/pir_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |pir_core_example.m5f2|


class PIRUnit
-------------

Constructors
------------

Import with ``from unit import PIRUnit``.

.. class:: PIRUnit(port)

    Create a PIRUnit object.

    The parameters are:
        - ``port`` is a pin tuple; port[0] is the digital input.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: PIRUnit.get_status()

    Get detection status.

    UIFLOW2:

        |get_status.png|


.. method:: PIRUnit.enable_irq()

   Enable Human detection function.

    UIFLOW2:

        |enable_irq.png|


.. method:: PIRUnit.disable_irq()

    Disable Human detection function.

    UIFLOW2:

        |disable_irq.png|


.. method:: PIRUnit.set_callback()

    Polling method, placed in the loop function, constantly check.

    UIFLOW2:

        |set_callback.png|
