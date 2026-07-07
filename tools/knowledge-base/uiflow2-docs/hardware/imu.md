# IMU

<!-- .. include:: ../refs/system.ref -->
<!-- .. include:: ../refs/hardware.imu.ref -->

IMU is used to control the built-in accelerometer and gyroscope inside the host
device. Below is the detailed IMU support for the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |                 | MPU6886 | BMI270 | BMM150 |

###### | AtomS3          | |S|     |        |        |

###### | AtomS3 Lite     |         |        |        |

###### | AtomS3U         |         |        |        |

###### | StampS3         |         |        |        |

###### | CoreS3          |         | |S|    | |S|    |

###### | Core2           | |S|     |        |        |

###### | TOUGH           |         |        |        |

###### | StickC Plus     | |S|     |        |        |

###### | StickC Plus2    | |S|     |        |        |

<!-- .. |S| unicode:: U+2714 -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *

title0 = None
label2 = None
label0 = None
label3 = None
label1 = None
label4 = None
label5 = None

def setup():
    global title0, label2, label0, label3, label1, label4, label5

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("IMU CoreS3 example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Acc_z:", 1, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Acc_x:", 1, 32, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Gyro_x:", 1, 135, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Acc_y:", 1, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Gyro_y:", 1, 168, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Gyro_z:", 1, 198, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

def loop():
    global title0, label2, label0, label3, label1, label4, label5
    M5.update()
    label0.setText(str((str("Acc_x:") + str(((Imu.getAccel())[0])))))
    label1.setText(str((str("Acc_y:") + str(((Imu.getAccel())[1])))))
    label2.setText(str((str("Acc_z:") + str(((Imu.getAccel())[2])))))
    label3.setText(str((str("Gyro_x:") + str(((Imu.getGyro())[0])))))
    label4.setText(str((str("Gyro_y:") + str(((Imu.getGyro())[1])))))
    label5.setText(str((str("Gyro_z:") + str(((Imu.getGyro())[2])))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |imu_cores3_example.m5f2|

## class IMU

<!-- .. important:: -->

    Methods of the IMU Class heavily rely on ``M5.begin()``  and ``M5.update()`` .

    All calls to methods of IMU objects should be placed after ``M5.begin()`` , and ``M5.update()``  should be called in the main loop.

## Methods

<!-- .. method:: IMU.getAccel() -> tuple[float, float, float] -->

    Get the tuple of x, y, and z values of the accelerometer.

    UIFLOW2:

<!-- .. method:: IMU.getGyro() -> tuple[float, float, float] -->

    Get the tuple of x, y, and z values of the gyroscope.

    UIFLOW2:

<!-- .. method:: IMU.getMag() -> tuple[float, float, float] -->

    Get the tuple of x, y, and z values of the magnetometer.

    UIFLOW2:

## class IMU_TYPE

## Constants

<!-- .. data:: IMU_TYPE.NULL -->
          IMU_TYPE.UNKNOWN
          IMU_TYPE.SH200Q
          IMU_TYPE.MPU6050
          IMU_TYPE.MPU6886
          IMU_TYPE.MPU9250
          IMU_TYPE.BMI270
    :type: int

    The model of the IMU.
