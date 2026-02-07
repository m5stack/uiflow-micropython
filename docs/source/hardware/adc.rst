ADC (analog to digital conversion)
====================================

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.adc.ref

On the ESP32 chip, ADC functionality is available on pins 32-39 (ADC channel 1) and
pins 0, 2, 4, 12-15 and 25-27 (ADC channel 2).

On the ESP32S3 chip, ADC functionality is available on pins 1-10 (ADC channel 1) and
pins 11-14 and 17-20 (ADC block 2).

ADC channel 2 is also used by WiFi and so attempting to read analog values from
channel 2 pins when WiFi is active will raise an exception.


Micropython Example:

    .. literalinclude:: ../../../examples/hardware/adc/adc_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |adc_cores3_example.m5f2|


class ADC
---------

.. class:: ADC(pin, *, atten)

    Return the ADC object for the specified pin. ESP32 does not support
    different timings for ADC sampling and so the ``sample_ns`` keyword argument
    is not supported.

    To read voltages above the reference voltage, apply input attenuation with
    the ``atten`` keyword argument. Valid values (and approximate linear
    measurement ranges) are:

      - ``ADC.ATTN_0DB``: No attenuation (100mV - 950mV)
      - ``ADC.ATTN_2_5DB``: 2.5dB attenuation (100mV - 1250mV)
      - ``ADC.ATTN_6DB``: 6dB attenuation (150mV - 1750mV)
      - ``ADC.ATTN_11DB``: 11dB attenuation (150mV - 2450mV)

    UIFLOW2:

        |init.png|

.. Warning::
   Note that the absolute maximum voltage rating for input pins is 3.6V. Going
   near to this boundary risks damage to the IC!

Methods
-------
.. method:: ADC.read()

    This method returns the raw ADC value ranged according to the resolution of
    the block, e.g., 0-4095 for 12-bit resolution.

    UIFLOW2:

        |read.png|

.. method:: ADC.read_u16()

   Take an analog reading and return an integer in the range 0-65535.
   The return value represents the raw reading taken by the ADC, scaled
   such that the minimum value is 0 and the maximum value is 65535.

    UIFLOW2:

        |read_u16.png|

.. method:: ADC.read_uv()

    This method uses the known characteristics of the ADC and per-package eFuse
    values - set during manufacture - to return a calibrated input voltage
    (before attenuation) in microvolts. The returned value has only millivolt
    resolution (i.e., will always be a multiple of 1000 microvolts).

    The calibration is only valid across the linear range of the ADC. In
    particular, an input tied to ground will read as a value above 0 microvolts.
    Within the linear range, however, more accurate and consistent results will
    be obtained than using `read_u16()` and scaling the result with a constant.

    UIFLOW2:

        |read_uv.png|

.. method:: ADC.atten(atten)

    Equivalent to ``ADC.init(atten=atten)``.

    UIFLOW2:

        |atten.png|

.. method:: ADC.width(bits)

    Equivalent to ``ADC.block().init(bits=bits)``.

    For compatibility, the ``ADC`` object also provides constants matching the
    supported ADC resolutions:

    - ``ADC.WIDTH_9BIT`` = 9
    - ``ADC.WIDTH_10BIT`` = 10
    - ``ADC.WIDTH_11BIT`` = 11
    - ``ADC.WIDTH_12BIT`` = 12

    UIFLOW2:

        |width.png|
