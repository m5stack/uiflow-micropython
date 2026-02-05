#######
StickS3
#######

.. include:: ../refs/controllers.sticks3.ref

Support the following products:

    |StickS3|

UiFlow2 Example 
---------------

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

This example demonstrates the built-in IMU (Inertial Measurement Unit) sensor functionality. It reads and displays accelerometer and gyroscope data in real-time, showing acceleration values in m/s² and gyroscope values in degrees per second (dps).

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

MicroPython Example 
-------------------

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

This example demonstrates the built-in IMU (Inertial Measurement Unit) sensor functionality. It reads and displays accelerometer and gyroscope data in real-time, showing acceleration values in m/s² and gyroscope values in degrees per second (dps).

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
