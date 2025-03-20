# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from driver.adxl34x import ADXL345


class AccelUnit(ADXL345):
    """Create an AccelUnit object.

    :param I2C i2c: The I2C bus the Accel Unit is connected to.
    :param int address: The I2C address of the device. Default is 0x53.

    UiFlow2 Code Block:

        |init.svg|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C
            from unit import AccelUnit

            acceli2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            accel_0 = AccelUnit(i2c0)
    """

    def __init__(self, i2c, address=0x53):
        super().__init__(i2c, address=address)

    def get_accel(self) -> tuple[float, float, float]:
        """The x, y, z acceleration values returned in a 3-tuple in :math:`m / s ^ 2`.

        :returns: x, y, z acceleration values in :math:`m / s ^ 2`.
        :rtype: tuple[float, float, float]

        UiFlow2 Code Block:

            |get_accel.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.get_accel()
        """
        return self.acceleration

    def enable_motion_detection(self, *, threshold: int = 18) -> None:
        """The activity detection parameters.

        :param int threshold: The value that acceleration on any axis must
                              exceed to register as active. The scale factor is
                              62.5 mg/LSB.

        If you wish to set them yourself rather than using the defaults,
        you must use keyword arguments::

            accelerometer.enable_motion_detection(threshold=20)

        UiFlow2 Code Block:

            |enable_motion_detection1.png|

            |enable_motion_detection2.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.enable_motion_detection(threshold=18)
        """
        super().enable_motion_detection(threshold=threshold)

    def disable_motion_detection(self) -> None:
        """Disable motion detection.

        UiFlow2 Code Block:

            |disable_motion_detection.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.disable_motion_detection()
        """

    def get_data_rate(self) -> int:
        """Get the data rate of the sensor.

        :returns: The data rate of the sensor.
        :rtype: int

        UiFlow2 Code Block:

            |get_data_rate.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.get_data_rate()
        """
        return self.data_rate

    def set_data_rate(self, rate: int) -> None:
        """Set the data rate of the sensor.

        :param int rate: The data rate of the sensor.

        UiFlow2 Code Block:

            |set_data_rate.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.set_data_rate(accel_0.RATE_3200_HZ)
        """
        self.data_rate = rate

    def get_range(self) -> int:
        """Get the measurement range of the sensor.

        :returns: The measurement range of the sensor.
        :rtype: int

        UiFlow2 Code Block:

            |get_range.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.get_range()
        """
        return self.range

    def set_range(self, range: int) -> None:
        """The measurement range of the sensor.

        :param int range: The measurement range of the sensor.

        UiFlow2 Code Block:

            |set_range.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.set_range(accel_0.RANGE_2_G)
        """
        self.range = range

    def is_tap(self) -> bool:
        """Returns True if a tap has been detected.

        :returns: True if a tap has been detected.
        :rtype: bool

        UiFlow2 Code Block:

            |is_tap.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.is_tap()
        """
        ret = self.events.get("tap")
        return ret if ret else False

    def is_motion(self) -> bool:
        """Returns True if motion has been detected.

        :returns: True if motion has been detected.
        :rtype: bool

        UiFlow2 Code Block:
            |is_motion.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.is_motion()
        """
        ret = self.events.get("motion")
        return ret if ret else False

    def is_freefall(self) -> bool:
        """Returns True if freefall has been detected.

        :returns: True if freefall has been detected.
        :rtype: bool

        UiFlow2 Code Block:

            |is_freefall.svg|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.is_freefall()
        """
        ret = self.events.get("freefall")
        return ret if ret else False

    def enable_freefall_detection(self, *, threshold: int = 10, time: int = 25) -> None:
        """Freefall detection parameters:

        :param int threshold: The value that acceleration on all axes must be
                              under to register as dropped. The scale factor
                              is 62.5 mg/LSB.

        :param int time: The amount of time that acceleration on all axes must be
                         less than ``threshold`` to register as dropped. The scale
                         factor is 5 ms/LSB. Values between 100 ms and 350 ms
                         (20 to 70) are recommended.

        If you wish to set them yourself rather than using the defaults,
        you must use keyword arguments:

        .. code-block:: python

            accelerometer.enable_freefall_detection(time=30)

        UiFlow2 Code Block:

            |enable_freefall_detection1.png|

            |enable_freefall_detection2.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.enable_freefall_detection()
        """
        super().enable_freefall_detection(threshold=threshold, time=time)

    def disable_freefall_detection(self) -> None:
        """Disable freefall detection.

        UiFlow2 Code Block:

            |disable_freefall_detection.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.disable_freefall_detection()
        """
        super().disable_freefall_detection()

    def enable_tap_detection(
        *,
        tap_count: int = 1,
        threshold: int = 20,
        duration: int = 50,
        latency: int = 20,
        window: int = 255,
    ) -> None:
        """The tap detection parameters.

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

        UiFlow2 Code Block:

            |enable_tap_detection1.png|

            |enable_tap_detection2.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)
        """
        super().enable_tap_detection(
            tap_count=tap_count,
            threshold=threshold,
            duration=duration,
            latency=latency,
            window=window,
        )

    def disable_tap_detection(self) -> None:
        """Disable tap detection.

        UiFlow2 Code Block:

            |disable_tap_detection.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_0.disable_tap_detection()
        """
        super().disable_tap_detection()
