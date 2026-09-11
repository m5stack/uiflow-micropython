DoF9 Unit
=========

.. sku: U229

.. include:: ../refs/unit.dof9.ref

This library is the driver for Unit DoF9.

Support the following products:

    |Unit DoF9|

UiFlow2 Example
----------------

Read Heading
^^^^^^^^^^^^

Open the |cores3_unit_dof9_example.m5f2| project in UiFlow2.

This example shows how to read and display the heading.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
--------------------

Read Heading
^^^^^^^^^^^^

This example shows how to read and display the heading.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/dof9/cores3_unit_dof9_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

DoF9Unit
^^^^^^^^

Constructors
------------

.. class:: DoF9Unit(i2c, addr=0x68)

    Create a DoF9Unit on the host I2C bus. The BMI270 address can be ``0x68`` or ``0x69`` (default: ``0x68``). The BMM350 address remains ``0x14``.

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

            dof = DoF9Unit(i2c)  # Default BMI270 address: 0x68
            # Use this instead when the BMI270 is configured at 0x69:
            # dof = DoF9Unit(i2c, addr=0x69)

Methods
-------

The complete DoF9 interface is listed below.

.. method:: get_accel()
    :no-index:

    Return mapped acceleration as ``(x, y, z)`` in ``m/s2``.

    :return: Acceleration tuple.
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

    :return: Angular velocity tuple.
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

.. method:: get_mag()
    :no-index:

    Return mapped and calibrated magnetic field as ``(x, y, z)`` in ``uT``.

    :return: Magnetic field tuple.
    :rtype: tuple[float, float, float]

    UiFlow2 Code Block:

        |get_mag.png|

.. method:: get_mag_raw()
    :no-index:

    Return signed 24-bit BMM350 counts from ``-8388608`` to ``8388607``.

    :return: Raw magnetic field counts.
    :rtype: tuple[int, int, int]

    UiFlow2 Code Block:

        |get_mag_raw.png|

.. method:: get_temperature(sensor="imu")
    :no-index:

    Return BMI270 or BMM350 temperature in degrees Celsius. ``sensor`` is
    ``"imu"`` or ``"magnetometer"``.

    :param sensor: Temperature source.
    :type sensor: str
    :return: Temperature in degrees Celsius.
    :rtype: float

    UiFlow2 Code Block:

        |get_temperature.png|

.. method:: get_heading()
    :no-index:

    Sample the sensors and return tilt-compensated heading from 0 to less than
    360 degrees.

    :return: Heading in degrees.
    :rtype: float

    UiFlow2 Code Block:

        |get_heading.png|

.. method:: get_attitude()
    :no-index:

    Sample the sensors and return ``(yaw, pitch, roll)`` in degrees.

    :return: Attitude angles in degrees.
    :rtype: tuple[float, float, float]

    UiFlow2 Code Block:

        |get_attitude.png|

.. method:: set_accel_range(accel_scale)
    :no-index:

    Set one of ``ACCEL_RANGE_2G``, ``ACCEL_RANGE_4G``, ``ACCEL_RANGE_8G``, or
    ``ACCEL_RANGE_16G``.

    :param accel_scale: Full-scale range in g.
    :type accel_scale: int

    UiFlow2 Code Block:

        |set_accel_range.png|

.. method:: set_gyro_range(gyro_scale)
    :no-index:

    Set one of ``GYRO_RANGE_125DPS``, ``GYRO_RANGE_250DPS``, ``GYRO_RANGE_500DPS``,
    ``GYRO_RANGE_1000DPS``, or ``GYRO_RANGE_2000DPS``.

    :param gyro_scale: Full-scale range in deg/s.
    :type gyro_scale: int

    UiFlow2 Code Block:

        |set_gyro_range.png|

.. method:: set_accel_gyro_odr(accel_odr, gyro_odr)
    :no-index:

    Set BMI270 ODR using ``ACCEL_ODR_VALUES`` and ``GYRO_ODR_VALUES``.

    :param accel_odr: Accelerometer ODR in Hz.
    :type accel_odr: float
    :param gyro_odr: Gyroscope ODR in Hz.
    :type gyro_odr: int

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

.. method:: set_magnetometer_calibration(offsets, scales)
    :no-index:

    Set hard-iron offsets in ``uT`` and unitless soft-iron scale factors.

    :param offsets: Three hard-iron offsets in uT.
    :type offsets: tuple[float, float, float]
    :param scales: Three positive scale factors.
    :type scales: tuple[float, float, float]

    UiFlow2 Code Block:

        |set_magnetometer_calibration.png|

.. method:: set_axis_mapping(sensor, x_axis, y_axis, z_axis)
    :no-index:

    Map ``accelerometer``, ``gyroscope``, or ``magnetometer`` axes. Values
    ``1/-1``, ``2/-2``, and ``3/-3`` select source X/Y/Z with sign; source axes
    cannot repeat.

    :param sensor: Sensor name.
    :type sensor: str
    :param x_axis: Source axis for output X.
    :type x_axis: int
    :param y_axis: Source axis for output Y.
    :type y_axis: int
    :param z_axis: Source axis for output Z.
    :type z_axis: int

    UiFlow2 Code Block:

        |set_axis_mapping.png|

.. method:: set_fusion_time_constant(seconds)
    :no-index:

    Set the non-negative complementary-filter time constant in seconds.

    :param seconds: Non-negative filter time constant.
    :type seconds: float

    UiFlow2 Code Block:

        |set_fusion_time_constant.png|

.. method:: reset_fusion()
    :no-index:

    Reset the attitude filter; the next attitude sample reinitializes it.

    UiFlow2 Code Block:

        |reset_fusion.png|
