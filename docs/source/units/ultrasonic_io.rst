
UltrasoundIO Unit
=================
.. sku:U098-B2
.. include:: ../refs/unit.ultrasonic_io.ref

UNIT SONIC IO is a GPIO interface ultrasonic range sensor. This module features an RCWL-9620 ultrasonic distance measurement chip with a 16mm probe, which the ranging accuracy can reach 2cm-450cm (accuracy up to ±2%). This sensor determines the distance to a target by measuring time lapses between the transmitting and receiving of the pulse signal, users can directly obtain the distance value through IO control mode. It is ideal to apply in robotics obstacle avoidance, fluid level detection, and other applications that require you to perform measurements.

Support the following products:

|UltrasoundIOUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/ultrasonicio/ultrasonicio_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |ultrasonicio_cores3_example.m5f2|

class UltrasoundIOUnit
----------------------

Constructors
------------

.. class:: UltrasoundIOUnit(port, echo_timeout_us)

    Initialize the ultrasonic unit with the specified port and echo timeout.

    :param  port: A tuple representing the port pins for trigger (output) and echo (input).
    :param int echo_timeout_us: Timeout for the echo signal in microseconds, default is 1,000,000.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: UltrasoundIOUnit.tx_pulse_rx_echo()

    Send a trigger pulse and wait to receive the echo response.

.. method:: UltrasoundIOUnit.get_target_distance(mode)

    Calculate the distance to the target based on echo response time.

    :param int mode: The unit of measurement for the distance. Use 1 for millimeters, 2 for centimeters.

    :returns: The distance to the target in the specified unit.

    UIFLOW2:

        |get_target_distance.png|



