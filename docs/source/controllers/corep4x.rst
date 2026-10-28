#######
CoreP4X
#######

.. include:: ../refs/controllers.corep4x.ref

Support the following products:

    |CoreP4X|

Supported Components
--------------------

CoreP4X supports the following components:

* `M5UI <../m5ui/index.html>`_: The ``m5ui`` LVGL component library.

* `Unit <../unit/index.html>`_: The ``unit`` package containing Unit drivers.

* `Module <../module/index.html>`_: The ``module`` package for expansion modules.

* `Chain <../chain/index.html>`_: The ``chain`` package for Chain devices.

* `USB <../advanced/usb/device/index.html>`_: The ``usb.device`` package for HID devices.

Supported Display Fonts
-----------------------

The CoreP4X firmware includes the following Montserrat fonts for LVGL and M5UI: ``lv.font_montserrat_12``, ``lv.font_montserrat_14``, ``lv.font_montserrat_16``, ``lv.font_montserrat_18``, ``lv.font_montserrat_20``, ``lv.font_montserrat_22``, ``lv.font_montserrat_24``, ``lv.font_montserrat_30``, ``lv.font_montserrat_36``, ``lv.font_montserrat_40``, ``lv.font_montserrat_44``, ``lv.font_montserrat_48``.

For ``M5.Lcd.FONTS``, the firmware also provides ``AlibabaPuHuiTiCN24``, ``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean text respectively.

Board Features
--------------

CoreP4X supports the following built-in functions and peripherals:

* 480 x 480 display and capacitive touch input.

* `IMU <../hardware/imu.html>`_ accelerometer and gyroscope readings.

* RTC date and time display and adjustment.

* USB and battery voltage monitoring, charging status, and Port A 5 V output control.

* `Speaker <../hardware/speaker.html>`_ tone playback, volume adjustment, and PA control.

* `Microphone <../hardware/mic.html>`_ recording and speaker playback.

* `Infrared <../hardware/ir.html>`_ NEC transmission and reception.

UiFlow2 Example
---------------

RTC Clock
^^^^^^^^^

Open the |corep4x_rtc_example.m5f2| project in UiFlow2.

Display the date and a blue HH:MM:SS clock from the built-in RTC, using UTC. Tap **SET TIME** to adjust hours, minutes, and seconds with the **+** and **-** buttons. Tap **SAVE** to update the RTC while preserving the date, or **CANCEL** to discard the changes.

UiFlow2 Code Block:

    |corep4x_rtc_example.png|

Example output:

    None

IMU Sensor
^^^^^^^^^^

Open the |corep4x_imu_example.m5f2| project in UiFlow2.

Display the X, Y, and Z readings from the built-in accelerometer and gyroscope. Acceleration is shown in g, and angular velocity in degrees per second (dps). Tilt or rotate the device to observe the readings.

UiFlow2 Code Block:

    |corep4x_imu_example.png|

Example output:

    None

Power Management
^^^^^^^^^^^^^^^^

Open the |corep4x_power_example.m5f2| project in UiFlow2.

Display USB VBUS and battery voltages in mV, charging status, Port A 5 V output, and charge control. The battery voltage turns green while the battery is charging. Tap **PORT A** to toggle external output and **CHARGE** to enable or disable charging. Battery percentage is not displayed.

UiFlow2 Code Block:

    |corep4x_power_example.png|

Example output:

    None

Speaker Tone
^^^^^^^^^^^^

Open the |corep4x_speaker_tone_example.m5f2| project in UiFlow2.

Use separate sliders to adjust frequency from 200 to 4000 Hz and volume from 0 to 100%. The default values are 1000 Hz and 70%. Tap **Start tone** or **Stop tone** to control playback. The PA switch controls the amplifier independently; it is enabled at startup, while tone playback is stopped. Turning PA off mutes the output without stopping the tone.

UiFlow2 Code Block:

    |corep4x_speaker_tone_example.png|

Example output:

    None

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |corep4x_audio_example.m5f2| project in UiFlow2.

Record audio in memory at 8 kHz, mono, 16 bit. Tap **RECORD** to start and **STOP REC** to finish, with a maximum duration of 30 seconds. Tap **PLAY** to play the recording or **STOP PLAY** to stop playback. The volume slider ranges from 0 to 100%, with a default of 70%. PA is enabled automatically for playback.

UiFlow2 Code Block:

    |corep4x_audio_example.png|

Example output:

    None

Infrared Transmission and Reception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |corep4x_ir_example.m5f2| project in UiFlow2.

Use the built-in infrared receiver on G13 and transmitter on G49. Tap the send button to transmit an NEC frame with address 0x08 and an incrementing data byte. The screen shows transmitted data, received address and data, and the receive count. Use an NEC-compatible infrared remote control to test reception.

UiFlow2 Code Block:

    |corep4x_ir_example.png|

Example output:

    None

MicroPython Example
-------------------

RTC Clock
^^^^^^^^^

Display the date and a blue HH:MM:SS clock from the built-in RTC, using UTC. Tap **SET TIME** to adjust hours, minutes, and seconds with the **+** and **-** buttons. Tap **SAVE** to update the RTC while preserving the date, or **CANCEL** to discard the changes.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/corep4x/corep4x_rtc_example.py
        :language: python
        :linenos:

Example output:

    None

IMU Sensor
^^^^^^^^^^

Display the X, Y, and Z readings from the built-in accelerometer and gyroscope. Acceleration is shown in g, and angular velocity in degrees per second (dps). Tilt or rotate the device to observe the readings.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/corep4x/corep4x_imu_example.py
        :language: python
        :linenos:

Example output:

    None

Power Management
^^^^^^^^^^^^^^^^

Display USB VBUS and battery voltages in mV, charging status, Port A 5 V output, and charge control. The battery voltage turns green while the battery is charging. Tap **PORT A** to toggle external output and **CHARGE** to enable or disable charging. Battery percentage is not displayed.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/corep4x/corep4x_power_example.py
        :language: python
        :linenos:

Example output:

    None

Speaker Tone
^^^^^^^^^^^^

Use separate sliders to adjust frequency from 200 to 4000 Hz and volume from 0 to 100%. The default values are 1000 Hz and 70%. Tap **Start tone** or **Stop tone** to control playback. The PA switch controls the amplifier independently; it is enabled at startup, while tone playback is stopped. Turning PA off mutes the output without stopping the tone.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/corep4x/corep4x_speaker_tone_example.py
        :language: python
        :linenos:

Example output:

    None

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Record audio in memory at 8 kHz, mono, 16 bit. Tap **RECORD** to start and **STOP REC** to finish, with a maximum duration of 30 seconds. Tap **PLAY** to play the recording or **STOP PLAY** to stop playback. The volume slider ranges from 0 to 100%, with a default of 70%. PA is enabled automatically for playback.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/corep4x/corep4x_audio_example.py
        :language: python
        :linenos:

Example output:

    None

Infrared Transmission and Reception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the built-in infrared receiver on G13 and transmitter on G49. Tap the send button to transmit an NEC frame with address 0x08 and an incrementing data byte. The screen shows transmitted data, received address and data, and the receive count. Use an NEC-compatible infrared remote control to test reception.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/corep4x/corep4x_ir_example.py
        :language: python
        :linenos:

Example output:

    None
