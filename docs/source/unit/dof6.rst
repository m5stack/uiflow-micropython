DoF6 Unit
=========

.. sku: U228

.. include:: ../refs/unit.dof6.ref

This library is the driver for Unit DoF6.

Support the following products:

    |Unit DoF6|

UiFlow2 Example
----------------

Read Attitude
^^^^^^^^^^^^^

Open the |cores3_unit_dof6_example.m5f2| project in UiFlow2.

This example shows how to read and display yaw, pitch, and roll.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
--------------------

Read Attitude
^^^^^^^^^^^^^

This example shows how to read and display yaw, pitch, and roll.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/dof6/cores3_unit_dof6_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

DoF6Unit
^^^^^^^^

Constructors
------------

.. class:: DoF6Unit(i2c, addr=0x68)

    Create a DoF6Unit on the host I2C bus. The BMI270 address can be ``0x68`` or ``0x69`` (default: ``0x68``).

    :param i2c: Initialized I2C or PAHUBUnit interface.
    :type i2c: I2C or PAHUBUnit
    :param int addr: BMI270 I2C address, 0x68 or 0x69. Defaults to 0x68.
    :raises TypeError: addr is not an integer.
    :raises ValueError: addr is not 0x68 or 0x69.
    :raises UnitError: No BMI270 responds at the selected address.
    :raises OSError: Sensor initialization or I2C communication fails.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            dof = DoF6Unit(i2c)  # Default BMI270 address: 0x68
            # Use this instead when the BMI270 is configured at 0x69:
            # dof = DoF6Unit(i2c, addr=0x69)

Methods
-------

.. method:: get_accel()
    :no-index:

    Return mapped acceleration as ``(x, y, z)`` in ``m/s2``. The full scale is
    selected by :meth:`set_accel_range`.

    :return: Acceleration tuple in m/s2.
    :rtype: tuple[float, float, float]

    UiFlow2 Code Block:

        |get_accel.png|

.. method:: get_accel_raw()
    :no-index:

    Return signed 16-bit BMI270 counts from ``-32768`` to ``32767``.

    :return: Raw acceleration counts.
    :rtype: tuple[int, int, int]

    UiFlow2 Code Block:

        |get_accel_raw.png|

.. method:: get_gyro()
    :no-index:

    Return mapped, offset-corrected angular velocity as ``(x, y, z)`` in
    ``rad/s``.

    :return: Angular velocity tuple in rad/s.
    :rtype: tuple[float, float, float]

    UiFlow2 Code Block:

        |get_gyro.png|

.. method:: get_gyro_raw()
    :no-index:

    Return signed 16-bit BMI270 gyroscope counts from ``-32768`` to ``32767``.

    :return: Raw gyroscope counts.
    :rtype: tuple[int, int, int]

    UiFlow2 Code Block:

        |get_gyro_raw.png|

.. method:: get_temperature()
    :no-index:

    Return BMI270 temperature in degrees Celsius.

    :return: IMU temperature.
    :rtype: float

    UiFlow2 Code Block:

        |get_temperature.png|

.. method:: get_attitude()
    :no-index:

    Sample BMI270 and return fused ``(yaw, pitch, roll)`` in degrees.

    :return: Attitude angles in degrees.
    :rtype: tuple[float, float, float]

    UiFlow2 Code Block:

        |get_attitude.png|

.. method:: set_accel_range(accel_scale)
    :no-index:

    Set full scale to one of ``ACCEL_RANGE_2G``, ``ACCEL_RANGE_4G``,
    ``ACCEL_RANGE_8G``, or ``ACCEL_RANGE_16G``.

    :param accel_scale: Full-scale range in g.
    :type accel_scale: int
    :raises ValueError: If the range is unsupported.

    UiFlow2 Code Block:

        |set_accel_range.png|

.. method:: set_gyro_range(gyro_scale)
    :no-index:

    Set full scale to one of ``GYRO_RANGE_125DPS``, ``GYRO_RANGE_250DPS``,
    ``GYRO_RANGE_500DPS``, ``GYRO_RANGE_1000DPS``, or ``GYRO_RANGE_2000DPS``.

    :param gyro_scale: Full-scale range in deg/s.
    :type gyro_scale: int
    :raises ValueError: If the range is unsupported.

    UiFlow2 Code Block:

        |set_gyro_range.png|

.. method:: set_accel_gyro_odr(accel_odr, gyro_odr)
    :no-index:

    Set BMI270 ODR. ``ACCEL_ODR_VALUES`` is ``(0.78, 1.5, 3.1, 6.25, 12.5,
    25, 50, 100, 200, 400, 800, 1600)`` Hz; ``GYRO_ODR_VALUES`` is ``(25,
    50, 100, 200, 400, 800, 1600, 3200)`` Hz.

    :param accel_odr: Accelerometer output data rate in Hz.
    :type accel_odr: float
    :param gyro_odr: Gyroscope output data rate in Hz.
    :type gyro_odr: int
    :raises ValueError: If an ODR is unsupported.

    UiFlow2 Code Block:

        |set_accel_gyro_odr.png|

.. method:: set_gyro_offsets(x, y, z)
    :no-index:

    Set mapped gyroscope offsets in ``rad/s``.

    :param x: X-axis offset in rad/s.
    :type x: float
    :param y: Y-axis offset in rad/s.
    :type y: float
    :param z: Z-axis offset in rad/s.
    :type z: float

    UiFlow2 Code Block:

        |set_gyro_offsets.png|

.. method:: calibrate_gyro(samples=32)
    :no-index:

    Estimate offsets while stationary and return ``True`` on success.

    :param samples: Number of samples.
    :type samples: int
    :return: Whether calibration succeeded.
    :rtype: bool

    UiFlow2 Code Block:

        |calibrate_gyro.png|

.. method:: set_fusion_time_constant(seconds)
    :no-index:

    Set the non-negative complementary-filter time constant in seconds.

    :param seconds: Non-negative filter time constant.
    :type seconds: float
    :raises ValueError: If seconds is negative.

    UiFlow2 Code Block:

        |set_fusion_time_constant.png|

.. method:: reset_fusion()
    :no-index:

    Reset the attitude filter; the next attitude sample reinitializes it.

    UiFlow2 Code Block:

        |reset_fusion.png|

.. method:: set_axis_mapping(sensor, x_axis, y_axis, z_axis)
    :no-index:

    Map ``accelerometer`` or ``gyroscope`` axes. Values ``1/-1``, ``2/-2``,
    and ``3/-3`` select source X/Y/Z with sign; source axes cannot repeat.

    :param sensor: ``"accelerometer"`` or ``"gyroscope"``.
    :type sensor: str
    :param x_axis: Source axis for output X.
    :type x_axis: int
    :param y_axis: Source axis for output Y.
    :type y_axis: int
    :param z_axis: Source axis for output Z.
    :type z_axis: int
    :raises ValueError: If the sensor or mapping is invalid.

    UiFlow2 Code Block:

        |set_axis_mapping.png|
