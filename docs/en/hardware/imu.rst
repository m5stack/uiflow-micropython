IMU
===

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.imu.ref

IMU is used to control the built-in accelerometer and gyroscope inside the host
device. Below is the detailed IMU support for the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+--------+--------+
    |                 | MPU6886 | BMI270 | BMM150 |
    +=================+=========+========+========+
    | AtomS3          | |S|     |        |        |
    +-----------------+---------+--------+--------+
    | AtomS3 Lite     |         |        |        |
    +-----------------+---------+--------+--------+
    | AtomS3U         |         |        |        |
    +-----------------+---------+--------+--------+
    | StampS3         |         |        |        |
    +-----------------+---------+--------+--------+
    | CoreS3          |         | |S|    | |S|    |
    +-----------------+---------+--------+--------+
    | Core2           | |S|     |        |        |
    +-----------------+---------+--------+--------+
    | TOUGH           |         |        |        |
    +-----------------+---------+--------+--------+
    | StickC Plus     | |S|     |        |        |
    +-----------------+---------+--------+--------+
    | StickC Plus2    | |S|     |        |        |
    +-----------------+---------+--------+--------+

.. |S| unicode:: U+2714


Micropython Example::

    pass


UIFLOW2 Example::

    pass


class IMU
---------

.. important::

    Methods of the IMU Class heavily rely on ``M5.begin()`` |M5.begin.svg| and ``M5.update()`` |M5.update.svg|.

    All calls to methods of IMU objects should be placed after ``M5.begin()`` |M5.begin.svg|, and ``M5.update()`` |M5.update.svg| should be called in the main loop.


Methods
-------

.. method:: IMU.getAccel() -> tuple[float, float, float]

    Get the tuple of x, y, and z values of the accelerometer.

    UIFLOW2:

        |getAccel.svg|


.. method:: IMU.getGyro() -> tuple[float, float, float]

    Get the tuple of x, y, and z values of the gyroscope.

    UIFLOW2:

        |getGyro.svg|


.. method:: IMU.isEnabled() -> bool

    Get whether the IMU object is enabled.

    UIFLOW2:

        None


.. method:: IMU.getType() -> int

    Get the chip model of the IMU.

    UIFLOW2:

        None


class IMU_TYPE
-------------------

Constants
---------

.. data:: IMU_TYPE.NULL
          IMU_TYPE.UNKNOWN
          IMU_TYPE.SH200Q
          IMU_TYPE.MPU6050
          IMU_TYPE.MPU6886
          IMU_TYPE.MPU9250
          IMU_TYPE.BMI270
    :type: int

    The model of the IMU.
