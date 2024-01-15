Miniscale Unit
==============

.. include:: ../refs/unit.adc.ref

The ``Miniscale`` class is designed for interfacing with a mini scale weight sensor, which includes a HX711 22-bit ADC. This sensor is capable of measuring weight and also includes additional functionalities like LED control and various filters.

Support the following products:


|ADC|              



Micropython Example::

	import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import MiniScaleUnit

	i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
	scale = MiniScaleUnit(i2c)
	scale.setLed(255, 0, 0)
	print(miniscale.weight)


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html



Creating a Miniscale Object
---------------------------

To create a new ``Miniscale`` object, initialize it with the following parameters:

.. code-block:: python

    miniscale = unit.get(unit.MINISCALE, unit.PORTA)

Methods and Properties
----------------------

adc (Property)
^^^^^^^^^^^^^^

Returns the raw ADC value.

.. code-block:: python

    adc_value = miniscale.adc

weight (Property)
^^^^^^^^^^^^^^^^^

Returns the weight in grams.

.. code-block:: python

    weight_value = miniscale.weight

button (Property)
^^^^^^^^^^^^^^^^^

Returns the button state. True: pressing, False: Not pressing.

.. code-block:: python

    button_state = miniscale.button

setLed
^^^^^^

Sets the RGB LED color.

.. code-block:: python

    miniscale.setLed(r, g, b)

- ``r``: Red value (0 - 255).
- ``g``: Green value (0 - 255).
- ``b``: Blue value (0 - 255).

Reset
^^^^^

Resets sensor.

.. code-block:: python

    miniscale.reset()

calibration
^^^^^^^^^^^

Calibrates the MiniScale sensor.

.. code-block:: python

    miniscale.calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)

- ``weight1_g``: Weight1 in grams.
- ``weight1_adc``: Weight1 in ADC value.
- ``weight2_g``: Weight2 in grams.
- ``weight2_adc``: Weight2 in ADC value.

calibration steps:

1. Reset sensor;
2. Get adc, this is weight1_adc (should be zero). And weight1_g is also 0.
3. Put some weight on it, then get adc, this is weight2_adc. And weight2_g is weight in gram you put on it.

setLowPassFilter
^^^^^^^^^^^^^^^^

Enables or disables the low pass filter.

.. code-block:: python

    miniscale.setLowPassFilter(enabled)

- ``enabled``: Boolean to enable or disable the filter.

getLowPassFilter
^^^^^^^^^^^^^^^^

Returns the status of the low pass filter (enabled or not).

.. code-block:: python

    filter_status = miniscale.getLowPassFilter()

setAverageFilterLevel
^^^^^^^^^^^^^^^^^^^^^

Sets the level of the average filter.

.. code-block:: python

    miniscale.setAverageFilterLevel(level)

- ``level``: Level of the average filter (0 - 50). Larger value for smoother result but more latency

getAverageFilterLevel
^^^^^^^^^^^^^^^^^^^^^

Returns the level of the average filter.

.. code-block:: python

    filter_level = miniscale.getAverageFilterLevel()

setEMAFilterAlpha
^^^^^^^^^^^^^^^^^

Sets the alpha value for the EMA filter.

The EMA (Exponential Moving Average) filter is more sensitive to changes in data compared to the average filter.

.. code-block:: python

    miniscale.setEMAFilterAlpha(alpha)

- ``alpha``: Alpha value for the EMA filter (0 - 99). Smaller value for smoother result but more latency

getEMAFilterAlpha
^^^^^^^^^^^^^^^^^

Returns the alpha value for the EMA filter.

.. code-block:: python

    alpha_value = miniscale.getEMAFilterAlpha()

Filter Compare
^^^^^^^^^^^^^^

.. image:: C:\Users\tongy\OneDrive\work\M5\uiflow\image\filter.png
