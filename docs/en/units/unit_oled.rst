OLED Unit
=========

.. include:: ../refs/unit.oled.ref

Unit OLED is a 1.3-inch OLED expansion screen unit. It adopts SH1107 drive scheme, supports black/white display, and the resolution is 128*64. The driver chip selects the I2C communication interface, and the user can mount it to the I2C bus of the existing device when in use, which saves IO. The back of the screen is integrated with a magnetic design, which can easily be fixed on the metal surface by adsorption. The OLED screen extension is suitable for being embedded in various instruments or control devices that need to display simple content as a display panel.

Supported products:

|OLEDUnit|

Micropython example::

    import M5
    display = M5.addDisplay({"unit_oled":{"enabled":True, "pin_scl": 33, "pin_sda": 32, "i2c_addr": 0x3C, "i2c_freq": 400000}}) # Add OLED unit
    display.clear(0xffffff) # Clear screen

UIFLOW2 example:

    |example.svg|

.. only:: builder_html
