
SSR Unit
=========

.. include:: ../refs/unit.ssr.ref

UNIT SSR Solid-state relays are different from traditional electromagnetic relays in that their switching life are much longer than that of electromagnetic relays. With integrated MOC3043M optocoupler isolation and zero-crossing detection,It supports input 3.3-5V DC control signal, and control output single-phase 220-250V AC power.

Support the following products:

|SSRUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/ssr/cores3_ssr_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_ssr_example.m5f2|


class SSRUnit
-------------

Constructors
------------

.. method:: SSRUnit(port)

    Initialize the SSR.

    - ``port``: The port to which the Fader is connected. port[1]: control pin

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: SSRUnit.on()

    Turn on the SSR.


    UIFLOW2:

        |on.png|

.. method:: SSRUnit.off()

    Turn off the SSR.


    UIFLOW2:

        |off.png|

.. method:: SSRUnit.set_state(state)

    Set the state of the SSR.

    - ``state``: The state of the SSR.

    UIFLOW2:

        |set_state.png|


