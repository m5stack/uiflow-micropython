.. _unit.PDMUnit:

PDM Unit
==========

.. sku: U089

.. include:: ../refs/unit.pdm.ref

This is the driver library of PDM Unit, which is provides a set of methods to control the PDM microphone. Through the
I2S interface, the module can record audio data and save it as WAV files.

Support the following products:

    |PDM|


UiFlow2 Example
---------------

record voice and play voice
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |pdm_cores3_example.m5f2| project in UiFlow2.

This example records voice and plays voice.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

record voice and play voice
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example records voice and plays voice.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/pdm/pdm_cores3_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

PDMUnit
^^^^^^^^^

.. autoclass:: unit.pdm.PDMUnit
    :members:

    PDMUnit class inherits Mic class, See :ref:`hardware.Mic <hardware.Mic>` for more details.
