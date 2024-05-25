RCA Unit
========

.. include:: ../refs/unit.rca.ref


Unit RCA is a female jack terminal block for transmitting composite 
video (audio or video), one of the most common A/V connectors, which transmits 
video or audio signals from a component device to an output 
device (i.e., a display or speaker).


Supported products:

    |RCAUnit|


Micropython example::

    import M5
    display = M5.addDisplay({
        "unit_rca":{
            "enabled":True,
            "width": 216,
            "height": 144,
            "output_width": 0,
            "output_height": 0,
            "signal_type": 0, # NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4
            "use_psram": 0,
            "pin_dac": 26,
            "output_level": 0,
        }
    })
    display.clear(0xffffff) # Clear screen
