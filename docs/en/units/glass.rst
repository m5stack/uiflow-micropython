Glass Unit
==========

.. include:: ../refs/unit.glass.ref

Unit Glass is a 1.51-inch transparent OLED expansion screen unit. It adopts
STM32+SSD1309 driver scheme,resolution is 128*64, monochrome display,
transparent area is 128*56. The MCU adopts STM32F030F4P6, which integrates two
input buttons and one way buzzer to facilitate user interaction with the screen,
and supports control and firmware upgrade through I2C (addr: 0x3D) communication
interface. This transparent OLED screen extension is suitable for embedding in
various home products or various control devices as a display panel.


Supported products:

    |GlassUnit|


Micropython example::

    import M5
    display = M5.addDisplay({"unit_glass":{"enabled":True, "pin_scl": 33, "pin_sda": 32, "i2c_addr": 0x3D, "i2c_freq": 400000}}) # Add Glass unit
    display.clear(0xffffff) # Clear screen
