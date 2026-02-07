IR
===

.. include:: ../refs/hardware.ir.ref

IR is used to control the infrared receiving/transmitting tube built into the host device.

The specific support of the host for IR is as follows:

.. table::
    :widths: auto
    :align: center

    +-------------------+-----------------+-------------+
    | Controller        | IR Transmitter  | IR Receiver |
    +===================+=================+=============+
    | Atom Lite         | |S|             |             |
    +-------------------+-----------------+-------------+
    | Atom Matrix       | |S|             |             |
    +-------------------+-----------------+-------------+
    | Atom U            | |S|             |             |
    +-------------------+-----------------+-------------+
    | AtomS3 Lite       | |S|             |             |
    +-------------------+-----------------+-------------+
    | AtomS3U           | |S|             |             |
    +-------------------+-----------------+-------------+
    | M5StickC          | |S|             |             |
    +-------------------+-----------------+-------------+
    | M5StickC PLUS     | |S|             |             |
    +-------------------+-----------------+-------------+
    | M5StickC PLUS2    | |S|             |             |
    +-------------------+-----------------+-------------+
    | Cardputer         | |S|             |             |
    +-------------------+-----------------+-------------+
    | M5Capsule         | |S|             |             |
    +-------------------+-----------------+-------------+

.. |S| unicode:: U+2714

Micropython Example:

    .. literalinclude:: ../../../examples/hardware/ir/ir_stickcplus2_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |ir_stickcplus2_example.m5f2|

.. only:: builder_html

class IR
--------

Constructors
------------

.. class:: IR()

    Initializes the IR unit with the appropriate pins based on the M5Stack board type.


    UIFLOW2:

        |init.png|


Methods
-------

.. method:: IR.tx(cmd, data)

    Transmits an IR signal with the specified command and data using the NEC protocol.

    :param  cmd: The command code to be transmitted.
    :param  data: The data associated with the command.

    UIFLOW2:

        |tx.png|
