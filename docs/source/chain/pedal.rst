Chain Pedal
===========

.. include:: ../refs/chain.pedal.ref

PedalChain is the helper class for Chain Pedal devices on the Chain bus. It
provides access to the physical pedal state, logical switch state, event
callbacks, work modes, and the four RGB LEDs.

Support the following products:

    |Chain Pedal|

Product Features
----------------

- Read the physical pedal state or the latched logical switch state.
- Use single-click mode or switch mode, and receive click or status-change
  callbacks when event reporting is enabled.
- Control four RGB LEDs independently and select which LEDs show the pedal
  event overlay.
- Configure how long the pedal must be held to enter local configuration mode.
- Optionally save the work mode, configuration-entry time, RGB overlay mask,
  and RGB brightness to flash.

UiFlow2 Example
---------------

Switch status callbacks
^^^^^^^^^^^^^^^^^^^^^^^

Open the |chain_pedal_core2_example.m5f2| project in UiFlow2.

This example configures Chain Pedal in switch mode, sets the RGB LEDs, and
prints a message when the switch status changes.

UiFlow2 Code Block:

    |example.png|

Example output:

    .. code-block:: text

        switch open
        switch close

MicroPython Example
-------------------

Switch status callbacks
^^^^^^^^^^^^^^^^^^^^^^^

This example configures Chain Pedal in switch mode, sets the RGB LEDs, and
prints a message when the switch status changes.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/chain/pedal/chain_pedal_core2_example.py
        :language: python
        :linenos:

Example output:

    .. code-block:: text

        switch open
        switch close

**API**
-------

PedalChain
^^^^^^^^^^

.. autoclass:: chain.pedal.PedalChain
    :members:
    :inherited-members:
    :member-order: bysource
    :exclude-members: RGB_COUNT, WORK_MODE_SINGLE, WORK_MODE_SWITCH, MODE_POLL, MODE_EVENT, STATUS_CLOSE, STATUS_OPEN
