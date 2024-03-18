RCA Module
==========

.. include:: ../refs/module.rca.ref

Module RCA is a composite signal expansion module for audio and video, using the common S-terminal RCA connector, divided into two (left and right channels) audio and one video output. The audio part adopts the I2S power amplifier chip PCM5102APWR scheme, which can realize 32-bit stereo audio signal output; In terms of video, the DAC analog video signal function of the main control ESP32 is applied, which can generate analog video signals with a resolution of no more than 864 x 576 (PAL, PAL_M); The module contains a DC socket and a 9-24V to 5V DCDC circuit to supply power to the whole machine. This product is suitable for audio and video equipment that drives the S-terminal interface.

Supported products:

|RCAModule|

Micropython example::

	import M5
	M5.addDisplay({"module_rca":{"enabled":True}}) # Add RCA module
    M5.getDisplayCount() # Get display count
    M5.setPrimaryDisplay(1) # Set primary display
    M5.Display.clear(0xffffff) # Clear screen

UIFLOW2 example:

	|example.svg|

.. only:: builder_html
