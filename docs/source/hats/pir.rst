PIR Hat
========

.. include:: ../refs/hat.pir.ref

Support the following products:

    |PIR|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/pir/stickc_plus2_pir_hat_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_pir_hat_example.m5f2|


class PIRHat
------------

Constructors
------------

.. class:: PIRHat(port)

    Create a PIRHat object.

    The parameters are:
        - ``port`` GPIO pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: PIRHat.get_status()

    Get detection status.

    UIFLOW2:

        |get_status.png|


.. method:: PIRHat.enable_irq()

   Enable Human detection function.

    UIFLOW2:

        |enable_irq.png|


.. method:: PIRHat.disable_irq()

    Disable Human detection function.

    UIFLOW2:

        |disable_irq.png|


.. method:: PIRHat.set_callback()

    Polling method, placed in the loop function, constantly check.

    UIFLOW2:

        |set_callback.png|
