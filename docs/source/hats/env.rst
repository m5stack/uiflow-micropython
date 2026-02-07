ENV Hat
========

.. include:: ../refs/hat.env.ref

The following products are supported:

    ================== ==================
    |ENV II|           |ENV III|
    ================== ==================


Micropython Example:

    .. literalinclude:: ../../../examples/hat/env/stickc_plus2_env_hat_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_env_hat_example.m5f2|


class ENVHat
-------------

Constructors
------------

.. class:: ENVHat(i2c: Union[I2C, PAHUBHat], type: Literal[1, 2, 3])

    Create an ENVHat object.

    parameter is:

        - ``i2c`` is an I2C object.
        - ``type`` is the type of ENVHat

            - ``1`` - ENV
            - ``2`` - ENV II
            - ``3`` - ENV III

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ENVHat.read_temperature()

    This method allows to read the temperature value collected by ENV and returns a floating point value. The hat of measurement is °C.

    UIFLOW2:

        |read_temperature.png|


.. method:: ENVHat.read_humidity()

    This method allows to read the relative humidity value collected by ENV and returns a floating point value. The hat of measurement is %RH.

    UIFLOW2:

        |read_humidity.png|


.. method:: ENVHat.read_pressure()

    This method allows to read the atmospheric pressure collected by ENV and returns a floating point value. The hat of measurement is Pa.

    UIFLOW2:

        |read_pressure.png|
