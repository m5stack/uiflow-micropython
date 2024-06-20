
RCAUnit
=======

.. include:: ../refs/unit.rca.ref

Unit RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).

Support the following products:

|RCAUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import RCAUnit
    rca = RCAUnit()
    rca.display.fill(0)

.. only:: builder_html

class RCAUnit
-------------

Constructors
------------

.. class:: RCAUnit(port, width, height, signal_type, output_level, use_psram)

    Initialize the Unit RCA

    :param tuple port: The port to which the Unit RCA is connected. port[0]: not used, port[1]: dac pin.
    :param int width: The width of the RCA display.
    :param int height: The height of the RCA display.
    :param int signal_type: The signal type of the RCA display. NTSC&#x3D;0, NTSC_J&#x3D;1, PAL&#x3D;2, PAL_M&#x3D;3, PAL_N&#x3D;4.
    :param int output_level: The output level of the RCA display.
    :param int use_psram: The use of psram of the RCA display.

    UIFLOW2:

        |init.svg|


Methods
-------





