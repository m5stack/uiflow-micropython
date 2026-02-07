RCA Module
==========

.. sku: M125

.. include:: ../refs/module.rca.ref

Module RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).

Support the following products:

    |RCAModule|


UiFlow2 Example
---------------

Draw Text
^^^^^^^^^

Open the |core2_rca_example.m5f2| project in UiFlow2.

This example displays the text "RCA" on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None


MicroPython Example
-------------------

Draw Text
^^^^^^^^^

This example displays the text "RCA" on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/rca/core2_rca_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

Class RCAModule
^^^^^^^^^^^^^^^

.. autoclass:: module.rca.RCAModule
    :members:

    RCAModule class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
