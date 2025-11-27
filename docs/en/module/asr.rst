
ASR Module
============
.. sku:M147
.. include:: ../refs/module.asr.ref

This is the driver library of ASR Module.

Support the following products:

|ASRModule|

UiFlow2 Example
---------------

ASR Example
^^^^^^^^^^^^^

Open the |asr_core2_example.m5f2| project in UiFlow2.

This example shows how to use Module ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

ASR Example
^^^^^^^^^^^^^

This example shows how to use Module ASR to get the current command word, command number, and trigger an event when you say hello to do something you want to do.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/asr/asr_core2_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

ASRModule
^^^^^^^^^

.. autoclass:: module.asr.ASRModule
    :members:
    :member-order: bysource