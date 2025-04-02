.. _hat.Speaker2:

Speaker2 Hat
=============

.. sku: U055-B

.. include:: ../refs/hat.speaker2.ref

This is the driver library of Speaker2 Hat, which is provides a set of methods to control the speaker.

Support the following products:

    |Speaker2|


UiFlow2 Example
---------------
play audio
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |speaker2_stickcplus2_example.m5f2| project in UiFlow2.

This example demonstrates how to play audio.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

play audio
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to play audio.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hat/speaker2/speaker2_stickcplus2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

Speaker2
^^^^^^^^^

.. autoclass:: unit.speaker2.Speaker2
    :members:

    Speaker2 class inherits Speaker class, See :ref:`hardware.Speaker.Methods <hardware.Speaker.Methods>` for more details.
