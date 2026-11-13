Board Capabilities
==================

Firmware Packages
-----------------

The table lists packages included in the standard firmware for these controllers.
``Yes`` and ``No`` indicate package inclusion. M5UI requires LVGL.

.. list-table::
    :header-rows: 1
    :widths: 25 15 15 15 15 15

    * - Board
      - unit
      - module
      - cap
      - m5ui/LVGL
      - usb.device

    * - Cardputer
      - Yes
      - No
      - No
      - No
      - Yes
    * - CardputerADV
      - Yes
      - No
      - Yes
      - No
      - Yes
    * - CoreS3
      - Yes
      - Yes
      - No
      - Yes
      - Yes
    * - StickS3
      - Yes
      - No
      - No
      - No
      - Yes
    * - StopWatch
      - Yes
      - No
      - No
      - Yes
      - Yes

Download the :download:`capability data <board-capabilities.json>`.

RGB Units
---------

Import the driver with ``from unit import RGBUnit`` and select the target
board's output pin. For other RGB strips, check the LED protocol, voltage
and pin requirements before choosing a driver.

Cap and Module Interfaces
-------------------------

Cardputer Adv supports CC1101/NFC and LoRa Caps through the ``cap`` package.
Use the matching Cap and the pins specified in its driver documentation.
The automatic pin mappings differ from the original Cardputer.

CoreS3 provides the ``module`` package and an M-Bus expansion interface.
Configure the bus, pins, power and address for the connected Module.

USB Devices
-----------

The ESP32-S3 controllers in the table include ``usb.device``. Connect the
USB cable to the native USB controller and enable USB device support in the
firmware. A USB-to-UART bridge cannot provide native USB HID.
Configuring a USB device may disconnect the USB console.

Check Installed Packages
-------------------------

Use this code to list the firmware version and available packages:

.. code-block:: python

    import os
    import sys

    print(os.uname())
    print(sys.implementation)
    for name in ("unit", "module", "cap", "m5ui", "usb.device.keyboard"):
        try:
            __import__(name)
            print(name, "import OK")
        except (ImportError, AttributeError) as exc:
            print(name, type(exc).__name__, str(exc))
    from unit import RGBUnit
    print("RGBUnit:", RGBUnit)

If an import fails, check the full exception for missing dependencies.
Use explicit imports for lazily exported classes, such as ``RGBUnit``;
they may not appear in ``dir(unit)``.
