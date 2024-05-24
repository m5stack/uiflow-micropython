Accel Unit
==========

.. include:: ../refs/unit.accel.ref

Support the following products:

    |ACCEL|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import AccelUnit

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    accel_0 = AccelUnit(i2c0)


class AccelUnit
---------------

Constructors
------------

.. class:: AccelUnit(i2c0, address: int = 0x53)

    Create an AccelUnit object.

    :param I2C i2c0: I2C object
    :param int address: The I2C address of the device. Default is 0x53.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: AccelUnit.get_accel() -> tuple[float, float, float]

    The x, y, z acceleration values returned in a 3-tuple in :math:`m / s ^ 2`

    :returns: x, y, z acceleration values in :math:`m / s ^ 2`

    UIFLOW2:

        |get_accel.svg|


.. method:: AccelUnit.enable_motion_detection(*, threshold: int = 18) -> None

    The activity detection parameters.

    :param int threshold: The value that acceleration on any axis must exceed to
                          register as active. The scale factor is 62.5 mg/LSB.

    If you wish to set them yourself rather than using the defaults,
    you must use keyword arguments::

        accelerometer.enable_motion_detection(threshold=20)

    UIFLOW2:

        |enable_motion_detection1.svg|

        |enable_motion_detection2.svg|


.. method:: AccelUnit.disable_motion_detection() -> None

    Disable motion detection.

    UIFLOW2:

        |disable_motion_detection.svg|


.. method:: AccelUnit.is_tap() -> bool

    Returns True if a tap has been detected.

    :returns: True if a tap has been detected.

    UIFLOW2:

        |is_tap.svg|


.. method:: AccelUnit.is_motion() -> bool

    Returns True if motion has been detected.

    :returns: True if motion has been detected.

    UIFLOW2:

        |is_motion.svg|


.. method:: AccelUnit.is_freefall() -> bool

    Returns True if freefall has been detected.

    :returns: True if freefall has been detected.

    UIFLOW2:

        |is_freefall.svg|


.. method:: AccelUnit.enable_freefall_detection(*, threshold: int = 10, time: int = 25) -> None

    Freefall detection parameters:

    :param int threshold: The value that acceleration on all axes must be under
                          to register as dropped. The scale factor is 62.5 mg/LSB.

    :param int time: The amount of time that acceleration on all axes must be
                     less than ``threshold`` to register as dropped. The scale
                     factor is 5 ms/LSB. Values between 100 ms and 350 ms
                     (20 to 70) are recommended.

    If you wish to set them yourself rather than using the defaults,
    you must use keyword arguments:

    .. code-block:: python

        accelerometer.enable_freefall_detection(time=30)

    UIFLOW2:

        |enable_freefall_detection1.svg|

        |enable_freefall_detection2.svg|


.. method:: AccelUnit.disable_freefall_detection() -> None

    Disable freefall detection.

    UIFLOW2:

        |disable_freefall_detection.svg|


.. method:: AccelUnit.enable_tap_detection(*, tap_count: int = 1, threshold: int = 20, duration: int = 50, latency: int = 20, window: int = 255) -> None

    The tap detection parameters.

    :param int tap_count: 1 to detect only single taps, and 2 to detect only
                          double taps.

    :param int threshold: A threshold for the tap detection. The scale factor is
                          62.5 mg/LSB The higher the value the less sensitive
                          the detection.

    :param int duration: This caps the duration of the impulse above
                         ``threshold``. Anything above ``duration`` won't
                         register as a tap. The scale factor is 625 µs/LSB.

    :param int latency: (double tap only) The length of time after the initial
                        impulse falls below ``threshold`` to start the window
                        looking for a second impulse. The scale factor is
                        1.25 ms/LSB.

    :param int window: (double tap only) The length of the window in which to
                       look for a second tap. The scale factor is 1.25 ms/LSB.

    If you wish to set them yourself rather than using the defaults,
    you must use keyword arguments:

    .. code-block:: python

        accelerometer.enable_tap_detection(duration=30, threshold=25)

    UIFLOW2:

        |enable_tap_detection1.svg|

        |enable_tap_detection2.svg|


.. method:: AccelUnit.disable_tap_detection() -> None

    Disable tap detection.

    UIFLOW2:

        |disable_tap_detection.svg|


.. method:: AccelUnit.get_data_rate() -> int

    The data rate of the sensor.

    :returns: The data rate of the sensor.

    UIFLOW2:

        |get_data_rate.svg|


.. method:: AccelUnit.set_data_rate(rate: int) -> None

    The data rate of the sensor.

    UIFLOW2:

        |set_data_rate.svg|


.. method:: AccelUnit.get_range() -> int

    The measurement range of the sensor.

    :returns: The measurement range of the sensor.

    UIFLOW2:

        |get_range.svg|


.. method:: AccelUnit.set_range(rate: int) -> None

    The measurement range of the sensor.

    UIFLOW2:

        |set_range.svg|


Constants
---------

.. data:: AccelUnit.RATE_3200_HZ
          AccelUnit.RATE_1600_HZ
          AccelUnit.RATE_800_HZ
          AccelUnit.RATE_400_HZ
          AccelUnit.RATE_200_HZ
          AccelUnit.RATE_100_HZ
          AccelUnit.RATE_50_HZ
          AccelUnit.RATE_25_HZ
          AccelUnit.RATE_12_5_HZ
          AccelUnit.RATE_6_25HZ
          AccelUnit.RATE_3_13_HZ
          AccelUnit.RATE_1_56_HZ
          AccelUnit.RATE_0_78_HZ
          AccelUnit.RATE_0_39_HZ
          AccelUnit.RATE_0_20_HZ
          AccelUnit.RATE_0_10_HZ

    The data rate of the sensor.

.. data:: AccelUnit.RANGE_2_G
          AccelUnit.RANGE_4_G
          AccelUnit.RANGE_8_G
          AccelUnit.RANGE_16_G

    The measurement range of the sensor.
