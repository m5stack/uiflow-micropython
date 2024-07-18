Hall Effect Unit
================

.. include:: ../refs/unit.hall_effect.ref

Support the following products:

    |HallEffect|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/hall_effect/cores3_hall_effect_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_hall_effect_example.m5f2|


class HallEffectUnit
--------------------

Constructors
------------

.. class:: HallEffectUnit(port: tuple)

    Create a HallEffectUnit object.

    :param tuple port: Specify the port number according to the label on the unit.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: HallEffectUnit.get_status()

    Get the status of the Hall Effect sensor.

    UIFLOW2:

        |get_status.png|


.. method:: HallEffectUnit.enable_irq()

    Enable HAll Effect sensor interrupt.

    UIFLOW2:

        |enable_irq.png|


.. method:: HallEffectUnit.disable_irq()

    Disable Hall Effect sensor interrupt.

    UIFLOW2:

        |disable_irq.png|


.. method:: HallEffectUnit.set_callback(handler, trigger=HallEffectUnit.IRQ_ACTIVE | HallEffectUnit.IRQ_NEGATIVE)

    Set the callback function.

    UIFLOW2:

        |set_callback.png|

Constants
---------

.. data:: HallEffectUnit.IRQ_ACTIVE
          HallEffectUnit.IRQ_NEGATIVE

    used to set the trigger mode of the interrupt.
