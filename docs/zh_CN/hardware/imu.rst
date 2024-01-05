IMU
===

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.imu.ref

IMU 用于控制主机内部集成加速计与陀螺仪的按键。以下是主机的 IMU 支持详细：

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

    IMU Class的方法重度依赖 ``M5.begin()`` |M5.begin.svg| 和 ``M5.update()`` |M5.update.svg|。

    调用 IMU 对象的所有方法，需要放在 ``M5.begin()`` |M5.begin.svg| 的后面，
    并在主循环中调用 ``M5.update()`` |M5.update.svg|。

Methods
-------

.. method:: IMU.getAccel() -> tuple[float, float, float]

    获取加速度计的 x、y 和 z 值的三元组。

    UIFLOW2:

        |getAccel.svg|

.. method:: IMU.getGyro() -> tuple[float, float, float]

    获取角速度传感器（陀螺仪）的 x、y 和 z 值的三元组。

    UIFLOW2:

        |getGyro.svg|

.. method:: IMU.isEnabled() -> bool

    获取 IMU 对象是否使能。

    UIFLOW2:

        None

.. method:: IMU.getType() -> int

    获取 IMU 的芯片型号。

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

    IMU 的型号。
