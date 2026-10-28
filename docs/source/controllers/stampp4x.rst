########
StampP4X
########

.. include:: ../refs/controllers.stampp4x.ref

Support the following products:

    |StampP4X|

UiFlow2 Example
---------------

ADC Input
^^^^^^^^^

Open the |stampp4x_adc_example.m5f2| project in UiFlow2.

.. image:: https://static-cdn.m5stack.com/mpy_docs/controllers/stampp4x/stamp4x_adc_example.png

This example reads the 16-bit ADC value from GPIO23 every 200 ms and prints the result to the serial console.

GPIO Output
^^^^^^^^^^^

Open the |stampp4x_gpio_example.m5f2| project in UiFlow2.

.. image:: https://static-cdn.m5stack.com/mpy_docs/controllers/stampp4x/stamp4x_gpio_example.png

This example toggles GPIO15 high and low once per second and prints the current output state to the serial console.

PWM Output
^^^^^^^^^^

Open the |stampp4x_pwm_example.m5f2| project in UiFlow2.

.. image:: https://static-cdn.m5stack.com/mpy_docs/controllers/stampp4x/stamp4x_pwm_example.png

This example outputs a 20 kHz PWM signal on GPIO15. The duty value repeatedly ramps between 0 and 1023 and is printed to the serial console.

MicroPython Example
-------------------

ADC Input
^^^^^^^^^

This example reads the 16-bit ADC value from GPIO23 every 200 ms and prints the result to the serial console.

.. literalinclude:: ../../../examples/controllers/stampp4x/stampp4x_adc_example.py
    :language: python
    :linenos:

GPIO Output
^^^^^^^^^^^

This example toggles GPIO15 high and low once per second and prints the current output state to the serial console.

.. literalinclude:: ../../../examples/controllers/stampp4x/stampp4x_gpio_example.py
    :language: python
    :linenos:

PWM Output
^^^^^^^^^^

This example outputs a 20 kHz PWM signal on GPIO15. The duty value repeatedly ramps between 0 and 1023 and is printed to the serial console.

.. literalinclude:: ../../../examples/controllers/stampp4x/stampp4x_pwm_example.py
    :language: python
    :linenos:
