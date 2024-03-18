Display Module
==============

.. include:: ../refs/module.display.ref

Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN GW1NR series FPGA chip to output display signals, and employing the LT8618S chip for signal output conditioning. It can achieve a 24-bit color depth display signal and up to 8-channel audio signal output, with a resolution up to 1080P. The FPGA internally realizes the I2S audio generation function. This module includes a DC power input socket and corresponding DC-DC circuit, enabling power supply for the entire device. This product is suitable for various programmable HD AV outputs and other applications.


Supported products:

|DisplayModule|

Micropython example::

    import M5
    M5.addDisplay({"module_display":{"enabled":True}}) # Add ModuleDisplay module
    M5.getDisplayCount() # Get display count
    M5.setPrimaryDisplay(1) # Set primary display
    M5.Display.clear(0xffffff) # Clear screen

UIFLOW2 example:

    |example.svg|

.. only:: builder_html
