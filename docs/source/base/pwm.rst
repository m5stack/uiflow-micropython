Atomic PWM Base
============================

.. sku: A114

.. include:: ../refs/base.pwm.ref

Support the following products:

    |Atomic PWM Base|

UiFlow2 Example:
--------------------------

PWM output control  
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3r_pwm_base_example.m5f2| project in UiFlow2.

The example demonstrates controlling the PWM signal's duty cycle to fluctuate between low to high and high to low.

UiFlow2 Code Block:

    |atoms3r_pwm_base_example.png|

Example output:

    None
 
MicroPython Example:
--------------------------

PWM output control  
^^^^^^^^^^^^^^^^^^^^^^^^

The example demonstrates controlling the PWM signal's duty cycle to fluctuate between low to high and high to low.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/pwm/atoms3r_pwm_base_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------

PWM 
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: base.pwm.AtomicPWMBase
    :members:
