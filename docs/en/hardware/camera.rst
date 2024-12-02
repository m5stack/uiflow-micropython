:mod:`camera`  
=====================================
The camera module is used for taking pictures.

.. include:: ../refs/hardware.camera.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: camera
    :synopsis: camera sensor   

Micropython Example 
--------------------------------

capture display 
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/hardware/camera/cores3_example_camera_display.py
        :language: python
        :linenos:

UIFlow2.0 Example 
------------------------------

capture display 
++++++++++++++++++++++++++++

    |camera_display_example.png|

.. only:: builder_html

    |cores3_example_camera_display.m5f2|

 
    
Functions
------------------------------

.. function:: camera.init(pixformat, framesize)

    Initializes the camera sensor.

    The ``pixformat`` supports:
        
    - ``camera.RGB565``

    The ``framesize`` supports:

    - ``camera.QQVGA``: 160x120
    - ``camera.QCIF``: 176x144
    - ``camera.HQVGA``: 240x176
    - ``camera.FRAME_240X240``: 240x240
    - ``camera.QVGA``: 320x240

    UIFlow2.0

        |init.png|

.. function:: camera.snapshot() -> image.Iamge

    Capture a single frame.

    Returns An ``image.Image`` object.

    UIFlow2.0
    
        |snapshot.png|

.. function:: camera.set_hmirror(enable)

    Turns horizontal mirror mode on (True) or off (False). Defaults to on.

    UIFlow2.0
    
        |set_hmirror.png|

.. function:: camera.set_vflip(enable)

    Turns vertical flip mode on (True) or off (False). Defaults to off.

    UIFlow2.0
    
        |set_vflip.png|

.. function:: camera.get_hmirror()

    Returns if horizontal mirror mode is enabled.

    UIFlow2.0
    
        |get_hmirror.png|

.. function:: camera.get_vflip()

    Returns if vertical flip mode is enabled.

    UIFlow2.0
    
        |get_vflip.png|

 
