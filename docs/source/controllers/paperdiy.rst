########
PaperDIY
########

.. include:: ../refs/controllers.paperdiy.ref

PaperDIY is an ESP32-S3 controller with a 4.7-inch, 960x540 monochrome e-paper display, 16MB Flash, and 8MB PSRAM.

Support the following products:

    |PaperDIY|

Supported Components
--------------------

PaperDIY supports the following components:

* `Display <../hardware/display.html>`_: Screen drawing through ``M5.Lcd``.
* `Widgets <../widgets/index.html>`_: Labels and basic UI components through ``M5.Widgets`` and the ``widgets`` package.
* `Unit <../unit/index.html>`_: The ``unit`` package containing Unit drivers.
* `Chain <../chain/index.html>`_: The ``chain`` package for Chain devices.
* ``usb.device``: USB HID keyboard and mouse support.

The PaperDIY firmware uses M5GFX for display rendering. LVGL and M5UI are not enabled in this firmware.

Supported Display Fonts
-----------------------

The PaperDIY firmware provides the following Montserrat fonts through ``M5.Lcd.FONTS`` and ``M5.Widgets.FONTS``: ``Montserrat12``, ``Montserrat14``, ``Montserrat16``, ``Montserrat18``, ``Montserrat24``, ``Montserrat40``, ``Montserrat44``, and ``Montserrat48``.

The firmware also provides ``AlibabaPuHuiTiCN24``, ``AlibabaSansJA24``, and ``AlibabaSansKR24`` for Chinese, Japanese, and Korean text respectively.

Board Features
--------------

PaperDIY supports the following built-in functions and peripherals:

* A 4.7-inch monochrome e-paper display with portrait and landscape orientations.
* `Button <../hardware/button.html>`_ input through ``BtnA`` and ``BtnB``.
* `Power <../system/power.html>`_ monitoring through M5PM1: USB and battery voltages, charging status, and battery-charging control.
* TF (microSD) card storage.
* Wi-Fi networking and native USB programming.

The e-paper display has no touch panel or backlight.

UiFlow2 Example
---------------

Button Counter
^^^^^^^^^^^^^^

Open the |paperdiy_button_counter_example.m5f2| project in UiFlow2.

This example displays two independent button counters in portrait orientation. Press **BtnA** or **BtnB** to increment its own counter. Both counters start at 0 when the example starts.

UiFlow2 Code Block:

    |paperdiy_button_counter_example.png|

Example output:

    None

Charge Detection
^^^^^^^^^^^^^^^^

Open the |paperdiy_charge_detection_example.m5f2| project in UiFlow2.

This example displays battery voltage and USB voltage in millivolts (mV), together with charging status. Battery charging starts enabled. Press **BtnA** to enable or disable it. The readings refresh every 15 seconds and immediately after a button press.

UiFlow2 Code Block:

    |paperdiy_charge_detection_example.png|

Example output:

    None

MicroPython Example
-------------------

Button Counter
^^^^^^^^^^^^^^

This example displays two independent button counters in portrait orientation. Press **BtnA** or **BtnB** to increment its own counter. Both counters start at 0 when the example starts.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/paperdiy/paperdiy_button_counter_example.py
        :language: python
        :linenos:

Example output:

    None

Charge Detection
^^^^^^^^^^^^^^^^

This example displays battery voltage and USB voltage in millivolts (mV), together with charging status. Battery charging starts enabled. Press **BtnA** to enable or disable it. The readings refresh every 15 seconds and immediately after a button press.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/paperdiy/paperdiy_charge_detection_example.py
        :language: python
        :linenos:

Example output:

    None
