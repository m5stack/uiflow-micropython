######
CoreS3
######

.. include:: ../refs/controllers.cores3.ref

Support the following products:

    |CoreS3|

Supported Components
--------------------

CoreS3 supports the following components:

* `M5UI <../m5ui/index.html>`_: The ``m5ui`` LVGL component library.
* `Module <../module/index.html>`_: The ``module`` package for expansion modules.
* `Unit <../unit/index.html>`_: The ``unit`` package containing Unit drivers.
* `USB <../advanced/usb/device/index.html>`_: The ``usb.device`` package for HID devices.
* `M5Camera <../advanced/camera.html>`_: The frozen ``m5camera.py`` camera helper.
* `Chain <../chain/index.html>`_: The ``chain`` package for Chain devices.

Supported Display Fonts
-----------------------

The CoreS3 firmware includes the following Montserrat fonts for LVGL and M5UI:
``lv.font_montserrat_12``, ``lv.font_montserrat_14``, ``lv.font_montserrat_16``,
``lv.font_montserrat_18``, ``lv.font_montserrat_24``, ``lv.font_montserrat_40``,
``lv.font_montserrat_44``, and ``lv.font_montserrat_48``.

For ``M5.Lcd.FONTS``, the firmware also provides ``AlibabaPuHuiTiCN24``,
``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean
text respectively.

Board Features
--------------

CoreS3 supports the following built-in functions and board peripherals:

* `Display <../hardware/display.html>`_: 2.0-inch, 320 x 240 color LCD output.
* `Touch <../hardware/touch.html>`_: Capacitive touch input.
* `IMU <../hardware/imu.html>`_: BMI270 accelerometer and gyroscope, and BMM150 magnetometer readings.
* `ALS <../hardware/als.html>`_: Built-in LTR-553ALS-WA ambient light sensor readings.
* `Camera <../advanced/camera.html>`_: Image capture with the built-in GC0308 camera.
* `Speaker <../hardware/speaker.html>`_ playback and `microphone <../hardware/mic.html>`_ recording.
* BM8563 real-time clock for date and time keeping.
* `Power <../system/power.html>`_: Battery, charging, and external output power management.
* microSD card access through ``hardware.SDCard``.
* Grove and M-BUS expansion interfaces.
