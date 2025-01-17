
RCA Module
==========

.. include:: ../refs/module.rca.ref

Module RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).

Support the following products:

|RCAModule|

Micropython Example:

    .. literalinclude:: ../../../examples/module/rca/core2_rca_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |core2_rca_example.m5f2|


class RCAModule
---------------

Constructors
------------

.. class:: RCAModule(port: int =26, width: int = 216, height: int = 144, output_width: int = 216, output_height: int = 144, signal_type: int = 0, use_psram: int=0, output_level: int = 0)

    Initialize the Module RCA

    :param tuple port: The port to which the Module RCA is connected. port[0]: not used, port[1]: dac pin.
    :param int width: The width of the RCA display.
    :param int height: The height of the RCA display.
    :param int output_width: The width of the output of the RCA display.
    :param int output_height: The height of the output of the RCA display.
    :param int signal_type: The signal type of the RCA display. NTSC&#x3D;0, NTSC_J&#x3D;1, PAL&#x3D;2, PAL_M&#x3D;3, PAL_N&#x3D;4.
    :param int use_psram: The use of psram of the RCA display.
    :param int output_level: The output level of the RCA display.

    UIFLOW2:

        |init.png|


Methods
-------





