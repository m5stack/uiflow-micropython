
Relay4Unit
==========

.. include:: ../refs/unit.relay4.ref

4-Relay unit is an integrated 4-way relay module which can be controlled by I2C protocol. The maximum control voltage of each relay is AC-250V/DC-28V, the rated current is 10A and the instantaneous current can hold up to 16A. Each relay can be controlled independently, each on it's own. Each relay has status (LED) indictor as well to show the state of the relay at any given time.

Support the following products:

|Relay4Unit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from hardware import *
    from unit import Relay4Unit
    i2c = I2C(1, scl=33, sda=32)
    relay = Relay4Unit(i2c)
    for i in range(1, 5):
    relay.set_relay_state(i, 1)
    relay.set_led_state(i, 1)
    time.sleep(1)
    relay.set_relay_state(i, 0)
    relay.set_led_state(i, 0)
    time.sleep(1)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class Relay4Unit
----------------

Constructors
------------

.. class:: Relay4Unit(i2c, address)

    Initialize the Servo8.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the servo8.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: Relay4Unit.set_mode(mode)

    Set the mode of the relay.

    - ``mode``: The mode of the relay
        Options:
        - ``Relay4Unit.ASYNC_MODE``: async
        - ``Relay4Unit.SYNC_MODE``: sync

    UIFLOW2:

        |set_mode.svg|

.. method:: Relay4Unit.get_mode()

    Get the mode of the relay.


    UIFLOW2:

        |get_mode.svg|

.. method:: Relay4Unit.get_led_state(n)

    Get the state of the LED.

    - ``n``: 

    UIFLOW2:

        |get_led_state.svg|

.. method:: Relay4Unit.set_led_state(n, state)

    Set the state of the LED.

    - ``n``: The number of the LED.
    - ``state``: The state of the LED.

    UIFLOW2:

        |set_led_state.svg|

.. method:: Relay4Unit.get_relay_state(n)

    Get the state of the relay.

    - ``n``: 

    UIFLOW2:

        |get_relay_state.svg|

.. method:: Relay4Unit.set_relay_state(n, state)

    Set the state of the relay.

    - ``n``: The number of the relay.
    - ``state``: The state of the relay.

    UIFLOW2:

        |set_relay_state.svg|

.. method:: Relay4Unit.set_relay_all(state)

    Set the state of all the relay.

    - ``state``: The state of the relay.

    UIFLOW2:

        |set_relay_all.svg|





