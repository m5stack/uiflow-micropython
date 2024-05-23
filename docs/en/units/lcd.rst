LCD Unit
========

.. include:: ../refs/unit.lcd.ref


Unit LCD is a 1.14 inch color LCD expansion screen unit. It adopts ST7789V2
drive scheme, the resolution is 135*240, and it supports
RGB666 display (262,144 colors). The internal integration of ESP32-PICO control
core (built-in firmware, display development is more convenient), support
through I2C (addr: 0x3E) communication interface for control and firmware
upgrades. The back of the screen is integrated with a magnetic design,
which can easily adsorb the metal surface for fixing. The LCD screen extension
is suitable for embedding in various instruments or control devices that need
to display simple content as a display panel.


Supported products:

    |LCDUnit|


Micropython example::

    import M5
    display = M5.addDisplay({"unit_lcd":{"enabled":True, "pin_scl": 22, "pin_sda": 21, "i2c_addr": 0x3E, "i2c_freq": 400000}}) # Add LCD unit
    display.clear(0xffffff) # Clear screen
