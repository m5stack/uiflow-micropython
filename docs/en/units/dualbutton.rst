Dual_Button Unit
================

.. include:: ../refs/unit.dual_button.ref

Support the following products:

    |Dual_Button|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/dualbutton/dual_button_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |dual_button_core_example.m5f2|


class DualButton
-----------------

Constructors
------------

.. class:: DualButton(IO1,IO2)

    Create a DualButton object.

    The parameters are:
        - ``IO1,IO2`` Define two key pins.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Dual_Button.isHolding()

    The parameters are:

    UIFLOW2:

        |get_status.png|


.. method:: Dual_Button.setCallback()

    Execute the program when the key is pressed.

    UIFLOW2:

        |setCallback.png|


.. method:: Dual_Button.tick()

    The polling method, placed in the loop function, constantly detects the state of the key.

    UIFLOW2:

        |tick.png|
