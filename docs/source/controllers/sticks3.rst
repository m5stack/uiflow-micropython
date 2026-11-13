#######
StickS3
#######

.. py:currentmodule:: controllers.sticks3

.. include:: ../refs/controllers.sticks3.ref

Support the following products:

    |StickS3|

Supported Components
--------------------

StickS3 supports the following components:

* `Unit <../unit/index.html>`_: The ``unit`` package containing Unit drivers.
* `Chain <../chain/index.html>`_: The ``chain`` package for Chain devices.
* `HAT <../hat/index.html>`_: The ``hat`` package for HAT devices.
* `USB <../advanced/usb/device/index.html>`_: The ``usb.device`` package for HID devices.

Supported Display Fonts
-----------------------

Use ``M5.Lcd`` and ``M5.Widgets`` fonts for the StickS3 display.
The firmware does not include M5UI/LVGL.

For ``M5.Lcd.FONTS``, the firmware also provides ``AlibabaPuHuiTiCN24``,
``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean
text respectively.

Board Features
--------------

StickS3 supports the following built-in functions and connected peripherals:

* Button input and display output.
* `IMU <../hardware/imu.html>`_ accelerometer and gyroscope readings.
* Battery, VBUS, charging, and external output power management.
* `Infrared <../hardware/ir.html>`_ transmit and receive.
* `Microphone <../hardware/mic.html>`_ / `Speaker <../hardware/speaker.html>`_ WAV recording and playback.
* `RTC <../unit/rtc.html>`_ date and time functions (supported on StickS3 Lite and StickS3 v1.1 or later).
* `ToF HAT <../hat/tof.html>`_ distance measurement.

Grove and System I2C
---------------------

Grove uses SDA GPIO9 and SCL GPIO10. The internal system I2C bus uses
SDA GPIO47 / SCL GPIO48 and is managed by M5Unified. Use ``I2C(1, ...)`` with
the external Grove pins, not a new bus on GPIO1/GPIO2 or the internal pins.
Enable Grove power when the connected peripheral needs the board's 5V output.
See the `I2C scan example <../hardware/i2c.html>`_ and the
`official StickS3 pin map <https://docs.m5stack.com/en/core/StickS3>`_.

Audio Compatibility
--------------------

For WAV recording and playback, use
``M5.Mic.recordWavFile(..., rate=16000, time=1)`` and
``M5.Speaker.playWavFile(...)``. Create the recording directory first; see
`Resource Files and Paths <../quick-reference/resource-files.html>`_.

.. note::
   The ADF ``sticks3_audio_example`` may hang during codec/I2S initialization.

UiFlow2 Example 
----------------

Button Control
^^^^^^^^^^^^^^

Open the |sticks3_button_example.m5f2| project in UiFlow2.

This example demonstrates button callback functions. When button A (BtnA) is clicked, it increments a counter and updates the display. When button B (BtnB) is clicked, it also increments a counter and updates the display.

UiFlow2 Code Block:

    |sticks3_button_example.png|

Example output:

    None

IMU Sensor
^^^^^^^^^^

Open the |sticks3_imu_example.m5f2| project in UiFlow2.

This example demonstrates the built-in IMU (Inertial Measurement Unit) sensor functionality. It reads and displays accelerometer and gyroscope data in real-time, showing acceleration values in g and gyroscope values in degrees per second (dps).

UiFlow2 Code Block:

    |sticks3_imu_example.png|

Example output:

    None

Power Management
^^^^^^^^^^^^^^^^

Open the |sticks3_power_example.m5f2| project in UiFlow2.

This example demonstrates power management features including battery voltage monitoring, VBUS voltage reading, charging status detection, and control of battery charging and external output. Press BtnA to toggle external output (5V OUT), and press BtnB to toggle battery charging.

UiFlow2 Code Block:

    |sticks3_power_example.png|

Example output:

    None

IR Transmission
^^^^^^^^^^^^^^^

Open the |sticks3_ir_tx_example.m5f2| project in UiFlow2.

This example demonstrates infrared (IR) transmission functionality. When button A is pressed, it sends IR data with a specified address and data value. The example displays the address and data being transmitted.

.. NOTE::
   When using IR transmission, the external output mode should be enabled.

UiFlow2 Code Block:

    |sticks3_ir_tx_example.png|

Example output:

    None

IR Reception
^^^^^^^^^^^^

Open the |sticks3_ir_rx_example.m5f2| project in UiFlow2.

This example demonstrates infrared (IR) reception functionality using NEC decode protocol. When IR data is received, it displays the address and data values on the screen.

.. NOTE::
   When using IR reception, the PA (Power Amplifier) should be turned off and the external output mode should be enabled.

UiFlow2 Code Block:

    |sticks3_ir_rx_example.png|

Example output:

    None

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |sticks3_audio_example.m5f2| project in UiFlow2.

This example demonstrates audio recording and playback functionality. Press button A to start recording for 5 seconds. After recording completes, the audio will automatically play back. The example displays the recording status and countdown timer.

UiFlow2 Code Block:

    |sticks3_audio_example.png|

Example output:

    None

HAT ToF Sensor
^^^^^^^^^^^^^^

Open the |sticks3_hat_tof_example.m5f2| project in UiFlow2.

This example demonstrates how to use the ToF (Time of Flight) HAT sensor to measure distance. The example reads distance values from the sensor and displays them on the screen.

UiFlow2 Code Block:

    |sticks3_hat_tof_example.png|

Example output:

    None

RTC Clock
^^^^^^^^^

Open the |sticks3_rtc_example.m5f2| project in UiFlow2.

.. note::
   This example supports StickS3 Lite and StickS3 v1.1 or later.
   Earlier StickS3 hardware versions do not include the RTC used by this example.

This example reads the built-in RTC and displays the current time. Press **BtnA**
to select the hour, minute, or second field. Press **BtnB** to increment the
selected field. Press **BtnA** again after the seconds field to write the new
time to the RTC.

UiFlow2 Code Block:

    |sticks3_rtc_example.png|

Example output:

    None

MicroPython Example 
--------------------

Button Control
^^^^^^^^^^^^^^

This example demonstrates button callback functions. When button A (BtnA) is clicked, it increments a counter and updates the display. When button B (BtnB) is clicked, it also increments a counter and updates the display.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_button_example.py
        :language: python
        :linenos:

Example output:

    None

IMU Sensor
^^^^^^^^^^

This example demonstrates the built-in IMU (Inertial Measurement Unit) sensor functionality. It reads and displays accelerometer and gyroscope data in real-time, showing acceleration values in g and gyroscope values in degrees per second (dps).

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_imu_example.py
        :language: python
        :linenos:

Example output:

    None

Power Management
^^^^^^^^^^^^^^^^

This example demonstrates power management features including battery voltage monitoring, VBUS voltage reading, charging status detection, and control of battery charging and external output. Press BtnA to toggle external output (5V OUT), and press BtnB to toggle battery charging.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_power_example.py
        :language: python
        :linenos:

Example output:

    None

IR Transmission
^^^^^^^^^^^^^^^

This example demonstrates infrared (IR) transmission functionality. When button A is pressed, it sends IR data with a specified address and data value. The example displays the address and data being transmitted.

.. NOTE::
   When using IR transmission, the external output mode should be enabled.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_ir_tx_example.py
        :language: python
        :linenos:

Example output:

    None

IR Reception
^^^^^^^^^^^^

This example demonstrates infrared (IR) reception functionality using NEC decode protocol. When IR data is received, it displays the address and data values on the screen in real-time.

.. NOTE::
   When using IR reception, the PA (Power Amplifier) should be turned off and the external output mode should be enabled.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_ir_rx_example.py
        :language: python
        :linenos:

Example output:

    None

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates audio recording and playback functionality. Press button A to start recording for 5 seconds. 
After recording completes, the audio will automatically play back. The example displays the recording status and countdown timer.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_audio_example.py
        :language: python
        :linenos:

Example output:

    None

HAT ToF Sensor
^^^^^^^^^^^^^^

This example demonstrates how to use the ToF (Time of Flight) HAT sensor to measure distance. The example reads distance values from the sensor and displays them on the screen in real-time.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_hat_tof_example.py
        :language: python
        :linenos:

Example output:

    None

RTC Clock
^^^^^^^^^

This example reads and updates the built-in RTC time.

.. note::
   This example supports StickS3 Lite and StickS3 v1.1 or later.
   Earlier StickS3 hardware versions do not include the RTC used by this example.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/sticks3/sticks3_rtc_example.py
        :language: python
        :linenos:

Example output:

    None
