Display Module
==============

.. include:: ../refs/module.display.ref

Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN
GW1NR series FPGA chip to output display signals, and employing the LT8618S chip
for signal output conditioning. It can achieve a 24-bit color depth display
signal and up to 8-channel audio signal output, with a resolution up to 1080P.
The FPGA internally realizes the I2S audio generation function. This module
includes a DC power input socket and corresponding DC-DC circuit, enabling power
supply for the entire device. This product is suitable for various programmable
HD AV outputs and other applications.


Supported products:

    |DisplayModule|


Micropython example::

    import M5
    display = M5.addDisplay({"module_display":{"enabled":True}}) # Add ModuleDisplay module
    # or
    display = M5.addDisplay({
        "module_display":{
            "enabled":True,
            "width": 1280,
            "height": 720,
            "refresh_rate": 60,
            "output_width": 0, # 0 default
            "output_height": 0,
            "scale_w": 0, # intger
            "scale_h": 0,
            "pixel_clock": 74250000,
        }
    })
    display.clear(0xffffff) # Clear screen
