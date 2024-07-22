
RCAModule
=========

.. include:: ../refs/module.rca.ref

Module RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).

Support the following products:

|RCAModule|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import RCAModule
    rca = RCAModule()
    rca.display.fill(0)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class RCAModule
---------------

Constructors
------------

.. class:: RCAModule(port, width, height, signal_type, output_level, use_psram)

    Initialize the Module RCA

    :param tuple port: The port to which the Module RCA is connected. port[0]: not used, port[1]: dac pin.
    :param int width: The width of the RCA display.
    :param int height: The height of the RCA display.
    :param int signal_type: The signal type of the RCA display. NTSC&#x3D;0, NTSC_J&#x3D;1, PAL&#x3D;2, PAL_M&#x3D;3, PAL_N&#x3D;4.
    :param int output_level: The output level of the RCA display.
    :param int use_psram: The use of psram of the RCA display.

    UIFLOW2:

        |init.svg|


Methods
-------





