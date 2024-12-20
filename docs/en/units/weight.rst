
Weight Unit
============
.. sku:U030
.. include:: ../refs/unit.weight.ref

Weight unit integrates a HX711 24 bits A/D chip that is specifically designed for electronic weighing device.

Support the following products:

|WEIGHTUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/weight/weight_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |weight_cores3_example.m5f2|

class WEIGHTUnit
----------------

Constructors
------------

.. class:: WEIGHTUnit(port)

    Initialize the WEIGHTUnit with specified port pins.

    :param  port: A tuple containing data and clock pin numbers.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: WEIGHTUnit.get_raw_weight()

    Read the raw weight value from the HX711.


    UIFLOW2:

        |get_raw_weight.png|

.. method:: WEIGHTUnit.get_scale_weight()

    Get the scaled weight value based on calibration.


    UIFLOW2:

        |get_scale_weight.png|

.. method:: WEIGHTUnit.set_tare()

    Set the tare weight to zero out the scale.


    UIFLOW2:

        |set_tare.png|

.. method:: WEIGHTUnit.set_calibrate_scale(weight)

    Calibrate the scale with a known weight.

    :param  weight: The known weight used for calibration.

    UIFLOW2:

        |set_calibrate_scale.png|

.. method:: WEIGHTUnit.is_ready_wait()

    Check if the HX711 is ready to provide data.


    UIFLOW2:

        |is_ready_wait.png|

.. method:: WEIGHTUnit.set_channel(chan)

    Set the channel for the HX711.

    :param int chan: The channel to set (1, 2, or 3).

    UIFLOW2:

        |set_channel.png|



