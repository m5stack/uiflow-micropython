####
Tab5
####

.. include:: ../refs/controllers.tab5.ref

Support the following products:

    |Tab5|

Supported Components
--------------------

Tab5 includes these user-facing packages:

* `M5UI <../m5ui/index.html>`_: The ``m5ui`` LVGL component library, including ``m5ui.M5Keyboard``.
* `Module <../module/index.html>`_: The ``module`` package for M-BUS expansion modules.
* `Unit <../unit/index.html>`_: The ``unit`` package for Unit drivers.
* `USB <../advanced/usb/device/index.html>`_: The ``usb.device`` package, including HID, mouse, and keyboard support.
* `Chain <../chain/index.html>`_: The ``chain`` package for Chain devices.
* `Tab5 <../tab5/index.html>`_: The ``tab5`` package for Tab5 keyboard support.

Supported Display Fonts
-----------------------

The Tab5 firmware includes the following Montserrat fonts for LVGL and M5UI:
``lv.font_montserrat_12``, ``lv.font_montserrat_14``, ``lv.font_montserrat_16``,
``lv.font_montserrat_18``, ``lv.font_montserrat_20``, ``lv.font_montserrat_22``,
``lv.font_montserrat_24``, ``lv.font_montserrat_30``, ``lv.font_montserrat_36``,
``lv.font_montserrat_40``, ``lv.font_montserrat_44``, and
``lv.font_montserrat_48``.

For ``M5.Lcd.FONTS``, the firmware also provides ``AlibabaPuHuiTiCN24``,
``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean
text respectively.

Board Features
--------------

Tab5 supports the following built-in functions and board peripherals:

* `Display <../hardware/display.html>`_: 5-inch, 1280 x 720 MIPI-DSI touchscreen display.
* `Touch <../hardware/touch.html>`_: Capacitive touch input.
* `IMU <../hardware/imu.html>`_: BMI270 accelerometer and gyroscope readings.
* `Speaker <../hardware/speaker.html>`_ playback and `microphone <../hardware/mic.html>`_ recording.
* RX8130CE real-time clock for date and time keeping.
* `Power <../system/power.html>`_: Battery monitoring, charging, PORT.A output, and USB Type-A output control.
* microSD card access through ``hardware.SDCard``.
* `PWR485 <../hardware/pwr485.html>`_: RS485 communication.
* Grove and M-BUS expansion interfaces.
