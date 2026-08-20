#####
Tab5X
#####

.. include:: ../refs/controllers.tab5x.ref

Support the following products:

    |Tab5X|

Supported Components
--------------------

Tab5X inherits the Tab5 manifest and includes these user-facing packages:

* **M5UI**: The ``m5ui`` LVGL component library, including ``m5ui.M5Keyboard``.
* **Module**: The ``module`` package for M-BUS expansion modules.
* **Unit**: The ``unit`` package for Unit drivers.
* **USB**: The ``usb.device`` package, including HID, mouse, and keyboard support.
* **Chain**: The ``chain`` package for Chain devices.
* **Tab5**: The ``tab5`` package for Tab5 and Tab5X keyboard support.

Supported Display Fonts
-----------------------

The Tab5X firmware includes the following Montserrat fonts for LVGL and M5UI:
``lv.font_montserrat_12``, ``lv.font_montserrat_14``, ``lv.font_montserrat_16``,
``lv.font_montserrat_18``, ``lv.font_montserrat_20``, ``lv.font_montserrat_22``,
``lv.font_montserrat_24``, ``lv.font_montserrat_30``, ``lv.font_montserrat_36``,
``lv.font_montserrat_40``, ``lv.font_montserrat_44``, and
``lv.font_montserrat_48``.

For ``M5.Lcd.FONTS``, the firmware also provides ``AlibabaPuHuiTiCN24``,
``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean
text respectively.

UiFlow2 Example
---------------

Power Management
^^^^^^^^^^^^^^^^

Open the |tab5x_power_example.m5f2| project in UiFlow2.

This example controls the PORT.A output, USB Type-A output, and battery charging.
It also displays the battery level, voltage, current, and charging state.

UiFlow2 Code Block:

    |tab5x_power_example.png|

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |tab5x_audio_example.m5f2| project in UiFlow2.

This example records up to 10 seconds of 16 kHz, 16-bit mono PCM audio and plays
the recording back. The controls update as recording and playback state changes.

UiFlow2 Code Block:

    |tab5x_audio_example.png|

IMU Sensor
^^^^^^^^^^

Open the |tab5x_imu_example.m5f2| project in UiFlow2.

This example displays the three-axis accelerometer data in ``g`` and the
three-axis gyroscope data in ``dps``.

UiFlow2 Code Block:

    |tab5x_imu_example.png|

RTC
^^^

Open the |tab5x_rtc_example.m5f2| project in UiFlow2.

This example displays the date and time from the hardware RTC. The hour, minute,
and second controls update the RTC immediately.

UiFlow2 Code Block:

    |tab5x_rtc_example.png|

MicroPython Example
-------------------

Power Management
^^^^^^^^^^^^^^^^

This example controls PORT.A, USB Type-A, and battery charging while displaying
battery level, voltage, current, and charging state.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/tab5x/tab5x_power_example.py
        :language: python
        :linenos:

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example records up to 10 seconds of PCM audio and plays the recorded buffer.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/tab5x/tab5x_audio_example.py
        :language: python
        :linenos:

IMU Sensor
^^^^^^^^^^

This example reads and displays the three accelerometer and three gyroscope axes.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/tab5x/tab5x_imu_example.py
        :language: python
        :linenos:

RTC
^^^

This example displays and updates the hardware RTC date and time.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/tab5x/tab5x_rtc_example.py
        :language: python
        :linenos:
