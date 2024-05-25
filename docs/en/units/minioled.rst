MiniOLED Unit
=============

.. include:: ../refs/unit.minioled.ref

MiniOLED UNIT is a 0.42-inch I2C interface OLED screen unit, Its resolution
is 72*40, monochrome white display,and It communicates with the M5 Controller
via I2C (addr: 0x3C), This unit is suitable for embedding in various home
products, smart wearable devices, portable devices and industrial instruments.


Supported products:

    |MiniOLEDUnit|


Micropython example::

    import M5
    display = M5.addDisplay({"unit_mini_oled":{"enabled":True, "pin_scl": 33, "pin_sda": 32, "i2c_addr": 0x3C, "i2c_freq": 400000}}) # Add MiniOLED unit
    display.clear(0xffffff) # Clear screen
