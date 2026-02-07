MQ Unit
==========

.. sku: U199

.. include:: ../refs/unit.mq.ref

This is the driver library of MQ Unit, which is used to obtain data from the
MQ sensor.

Support the following products:

    |MQ|


UiFlow2 Example
---------------

get MQ ADC value
^^^^^^^^^^^^^^^^^

Open the |mq_core2_example.m5f2| project in UiFlow2.

This example gets the ADC value of the MQ Unit and displays it on the screen.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

get MQ ADC value
^^^^^^^^^^^^^^^^^

This example gets the ADC value of the MQ Unit and displays it on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/mq/mq_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

MQUnit
^^^^^^^^^

.. autoclass:: unit.mq.MQUnit
    :members: