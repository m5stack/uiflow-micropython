WDT
===
.. include:: ../refs/hardware.wdt.ref

The WDT is used to restart the system when the application crashes and ends
up into a non recoverable state. Once started it cannot be stopped or reconfigured in any way.
After enabling, the application must "feed" the
watchdog periodically to prevent it from expiring and resetting the system.

Micropython Example:

    .. literalinclude:: ../../../examples/hardware/wdt/wdt_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |wdt_cores3_example.m5f2|


class WDT -- watchdog timer
----------------------------
Constructors
------------

.. class:: WDT(id=0, timeout=5000)

   Create a WDT object and start it. The timeout must be given in milliseconds.
   Once it is running the timeout cannot be changed and the WDT cannot be stopped either.

   Notes: On the esp8266 a timeout cannot be specified, it is determined by the underlying system.
   On rp2040 devices, the maximum timeout is 8388 ms.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: WDT.feed()

   Feed the WDT to prevent it from resetting the system. The application
   should place this call in a sensible place ensuring that the WDT is
   only fed after verifying that everything is functioning correctly.

    UIFLOW2:

        |feed.png|