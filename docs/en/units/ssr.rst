
SSRUnit
=======

.. include:: ../refs/unit.ssr.ref

UNIT SSR Solid-state relays are different from traditional electromagnetic relays in that their switching life are much longer than that of electromagnetic relays. With integrated MOC3043M optocoupler isolation and zero-crossing detection,It supports input 3.3-5V DC control signal, and control output single-phase 220-250V AC power.

Support the following products:

|SSRUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import SSRUnit
    ssr = SSRUnit((33, 32))  # for core2
    ssr.on()
    ssr.off()
    ssr.set_state(1)
    ssr.set_state(0)


class SSRUnit
-------------

Constructors
------------

.. method:: SSRUnit(port)

    Initialize the SSR.

    - ``port``: The port to which the Fader is connected. port[1]: control pin

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: SSRUnit.on()

    Turn on the SSR.


    UIFLOW2:

        |on.svg|

.. method:: SSRUnit.off()

    Turn off the SSR.


    UIFLOW2:

        |off.svg|

.. method:: SSRUnit.set_state(state)

    Set the state of the SSR.

    - ``state``: The state of the SSR.

    UIFLOW2:

        |set_state.svg|


