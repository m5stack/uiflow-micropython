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


class PIR
---------

Constructors
------------

.. class:: PIR(IO1,IO2)

    Create a PIR object.

    The parameters are:
        - ``IO1,IO2`` I2C pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: PIR.get_status()

    Get detection status.

    UIFLOW2:

        |get_status.png|


.. method:: PIR.enable_irq()

   Enable Human detection function.

    UIFLOW2:

        |enable_irq.png|


.. method:: PIR.disable_irq()

    Disable Human detection function.

    UIFLOW2:

        |disable_irq.png|


.. method:: PIR.set_callback()

    Polling method, placed in the loop function, constantly check.

    UIFLOW2:

        |set_callback.png|
