Rotary
======

.. include:: ../refs/hardware.rotary.ref


Rotary is used to control the rotary encoder integrated inside the host. Below
is the detailed Rotary support for the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+--------+
    | Controller      | Rotary |
    +=================+========+
    | Dial            | |S|    |
    +-----------------+--------+
    | DinMeter        | |S|    |
    +-----------------+--------+

.. |S| unicode:: U+2714


Micropython Example:

    .. literalinclude:: ../../../examples/hardware/rotary/dial_rotary_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |dial_rotary_example.m5f2|


class Rotary
------------

Constructors
------------

.. class:: Rotary()

    Creates a Rotary object.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: Rotary.get_rotary_status() -> bool

    Gets the rotation status of the Rotary object.

    UIFLOW2:

        |get_rotary_status.png|


.. method:: Rotary.get_rotary_value() -> int

    .. note:: Cannot be used simultaneously with :meth:`Rotary.get_rotary_increments()`.

    Gets the rotation value of the Rotary object.

    UIFLOW2:

        |get_rotary_value.png|


.. method:: Rotary.get_rotary_increments() -> int

    .. note:: Cannot be used simultaneously with :meth:`Rotary.get_rotary_increments()`.

    Gets the rotation increment of the Rotary object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.png|


.. method:: Rotary.reset_rotary_value() -> None

    Resets the rotation value of the Rotary object.

    UIFLOW2:

        |reset_rotary_value.png|


.. method:: Rotary.set_rotary_value() -> None

    Sets the rotation value of the Rotary object.

    UIFLOW2:

        |set_rotary_value.png|
