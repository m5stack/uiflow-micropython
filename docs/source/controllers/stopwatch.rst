#########
StopWatch
#########

.. include:: ../refs/controllers.stopwatch.ref

Support the following products:

    |StopWatch|

Supported Components
--------------------

StopWatch supports the following components:

* `M5UI <../m5ui/index.html>`_: The ``m5ui`` LVGL component library.
* `Unit <../unit/index.html>`_: The ``unit`` package containing Unit drivers.
* `Chain <../chain/index.html>`_: The ``chain`` package for Chain devices.

Supported Display Fonts
-----------------------

The StopWatch firmware includes the following Montserrat fonts for LVGL and M5UI:
``lv.font_montserrat_12``, ``lv.font_montserrat_14``, ``lv.font_montserrat_16``,
``lv.font_montserrat_18``, ``lv.font_montserrat_24``, ``lv.font_montserrat_40``,
``lv.font_montserrat_44``, and ``lv.font_montserrat_48``.

For ``M5.Lcd.FONTS``, the firmware also provides ``AlibabaPuHuiTiCN24``,
``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean
text respectively.

Board Features
--------------

StopWatch supports the following built-in functions and peripherals:

* `RTC <../unit/rtc.html>`_ date and time display and adjustment.
* Button input and round-display output.
* USB, battery, and Grove voltage monitoring with charging and external-output control.
* `Audio <../system/audio.html>`_ recording and playback.

UiFlow2 Example
---------------

RTC Clock
^^^^^^^^^

Open the |stopwatch_rtc_example.m5f2| project in UiFlow2.

This example displays a digital clock (HH:MM:SS) on the round screen, reading time from the built-in RTC. Press **BtnA** to cycle through hour, minute, and second adjustment modes (the active field is highlighted in red). Press **BtnB** to increment the selected field. After adjusting seconds, press **BtnA** again to write the new time to the RTC.

UiFlow2 Code Block:

    |stopwatch_rtc_example.png|

Example output:

    None

Power Management
^^^^^^^^^^^^^^^^

Open the |stopwatch_power_example.m5f2| project in UiFlow2.

This example monitors USB, battery, and Grove port voltages, and shows charging status (battery text turns green while charging). Press **BtnA** to toggle Grove external output (5V OUT). Press **BtnB** to toggle battery charging.

UiFlow2 Code Block:

    |stopwatch_power_example.png|

Example output:

    None

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |stopwatch_aduio_example.m5f2| project in UiFlow2.

This example demonstrates audio recording and playback. Press **BtnA** to start a 5-second recording (countdown shown on screen). Press **BtnB** to play back the recorded file when not recording. The UI shows **Idle**, **Recording...**, or **Playing...** status.

UiFlow2 Code Block:

    |stopwatch_aduio_example.png|

Example output:

    None

MicroPython Example
-------------------

RTC Clock
^^^^^^^^^

This example displays a digital clock (HH:MM:SS) on the round screen, reading time from the built-in RTC. Press **BtnA** to cycle through hour, minute, and second adjustment modes (the active field is highlighted in red). Press **BtnB** to increment the selected field. After adjusting seconds, press **BtnA** again to write the new time to the RTC.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stopwatch/stopwatch_rtc_example.py
        :language: python
        :linenos:

Example output:

    None

Power Management
^^^^^^^^^^^^^^^^

This example monitors USB, battery, and Grove port voltages, and shows charging status (battery text turns green while charging). Press **BtnA** to toggle Grove external output (5V OUT). Press **BtnB** to toggle battery charging.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stopwatch/stopwatch_power_example.py
        :language: python
        :linenos:

Example output:

    None

Audio Recording and Playback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates audio recording and playback. Press **BtnA** to start a 5-second recording (countdown shown on screen). Press **BtnB** to play back the recorded file when not recording. The UI shows **Idle**, **Recording...**, or **Playing...** status.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stopwatch/stopwatch_aduio_example.py
        :language: python
        :linenos:

Example output:

    None
