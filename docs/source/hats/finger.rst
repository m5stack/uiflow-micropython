Finger Hat
==========

.. include:: ../refs/hat.finger.ref

The following products are supported:

    |FingerHat|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/finger/stickc_plus2_finger_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_finger_example.m5f2|


class FingerHat
---------------

Constructors
------------

.. class:: FingerHat(id: Literal[0, 1, 2] = 2, port: list | tuple = None)

    Create a FingerHat object.

    :param id: The ID of the UART, 0 or 1 or 2.
    :param port: UART pin numbers.

    UIFLOW2:

        |init.png|


FingerUnit class inherits FingerUnit class, See :ref:`unit.FingerUnit.Methods <unit.FingerUnit.Methods>` for more details.
