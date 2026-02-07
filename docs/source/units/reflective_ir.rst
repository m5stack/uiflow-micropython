Reflective IR Unit
==================

.. include:: ../refs/unit.reflective_ir.ref

Support the following products:

    |Reflective IR Unit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/reflective_ir/stickc_plus_reflectiverir_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus_reflectiverir_example.m5f2|


class ReflectiveIRUnit
----------------------

Constructors
------------

.. class:: ReflectiveIRUnit(port: tuple)

    Create a ReflectiveIRUnit object.

    :param tuple port: Specify the port to which the Reflective IR Unit is connected.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ReflectiveIRUnit.get_analog_value() -> int

    This method allows read the ADC value of the Reflective IR Unit and return an integer value. The value ranges from 0 to 65535.

    UIFLOW2:

        |get_analog_value.png|


.. method:: ReflectiveIRUnit.get_digital_value() -> int

    This method allows read the digital value of the Reflective IR Unit and return an integer value. The value ranges from 0 to 1.

    UIFLOW2:

        |get_digital_value.png|


.. method:: ReflectiveIRUnit.enable_irq() -> None

   Enable Obstacle detection event

    UIFLOW2:

        |enable_irq.png|


.. method:: ReflectiveIRUnit.disable_irq() -> None

    Disable Obstacle detection event

    UIFLOW2:

        |disable_irq.png|


.. method:: ReflectiveIRUnit.set_callback(handler, trigger=ReflectiveIRUnit.EVENT_DETECTED | ReflectiveIRUnit.EVENT_NOT_DETECTED) -> None

    Set the callback function for the Reflective IR Unit.

    :param handler: The callback function to be set.
    :param trigger: The trigger condition for the callback function.

    UIFLOW2:

        |set_callback.png|

Constants
---------

.. data:: ReflectiveIRUnit.EVENT_DETECTED
          ReflectiveIRUnit.EVENT_NOT_DETECTED

    select the EVENT type of the Reflective IR Unit.
