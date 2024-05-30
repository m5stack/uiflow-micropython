
DisplayModule
=============

.. include:: ../refs/module.display.ref

Display Module 13.2 is an expansion module for HD audio and video, using GAOYUN GW1NR series FPGA chip to output display signals, and employing the LT8618S chip for signal output conditioning.

Support the following products:

|DisplayModule|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import DisplayModule
    disp = DisplayModule()
    disp.display.fill(0)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class DisplayModule
-------------------

Constructors
------------

.. class:: DisplayModule(port, width, height, refresh_rate, pixel_clock, scale_w, scale_h)

    Initialize the Module Display

    :param tuple port: The port to which the Module Display is connected. port[0]: not used, port[1]: dac pin.
    :param int width: The width of the Module Display.
    :param int height: The height of the Module Display.
    :param int refresh_rate: The refresh rate of the Module Display.
    :param int pixel_clock: The pixel clock of the Module Display.
    :param int scale_w: The scale width of the Module Display.
    :param int scale_h: The scale height of the Module Display.

    UIFLOW2:

        |init.svg|


Methods
-------





