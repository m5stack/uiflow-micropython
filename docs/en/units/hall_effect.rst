Hall Effect Unit
================

.. include:: ../refs/unit.hall_effect.ref

Support the following products:

    |HallEffect|


class HallEffectUnit
--------------------

Constructors
------------

.. class:: HallEffectUnit(port: tuple)

    Create a HallEffectUnit object.

    :param tuple port: Specify the port number according to the label on the unit.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: HallEffectUnit.get_status()

    Get the status of the Hall Effect sensor.

    UIFLOW2:

        |get_status.svg|


.. method:: HallEffectUnit.enable_irq()

    Enable HAll Effect sensor interrupt.

    UIFLOW2:

        |enable_irq.svg|


.. method:: HallEffectUnit.disable_irq()

    Disable Hall Effect sensor interrupt.

    UIFLOW2:

        |disable_irq.svg|


.. method:: HallEffectUnit.set_callback(handler, trigger=HallEffectUnit.IRQ_ACTIVE | HallEffectUnit.IRQ_NEGATIVE)

    Set the callback function.

    UIFLOW2:

        |set_callback.svg|

Constants
---------

.. data:: HallEffectUnit.IRQ_ACTIVE
          HallEffectUnit.IRQ_NEGATIVE

    used to set the trigger mode of the interrupt.
