:mod:`camera`  
=====================================
camera 模块用于拍照。

.. include:: ../refs/hardware.camera.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: camera
    :synopsis: camera sensor  

Micropython 案例 
--------------------------------

拍摄显示 
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/hardware/camera/cores3_example_camera_display.py
        :language: python
        :linenos:


UIFlow2.0 案例 
------------------------------

拍摄显示
++++++++++++++++++++++++++++

    |camera_display_example.png|

.. only:: builder_html

    |cores3_example_camera_display.m5f2|


函数 
------------------------------

.. function:: camera.init(pixformat, framesize)

    初始化摄像头

    参数 ``pixformat`` 仅接受以下值：  
        
    - ``camera.RGB565``

    参数 ``framesize`` 仅接受以下值：  

    - ``camera.QQVGA``: 160x120
    - ``camera.QCIF``: 176x144
    - ``camera.HQVGA``: 240x176
    - ``camera.FRAME_240X240``: 240x240
    - ``camera.QVGA``: 320x240

    UIFlow2.0

        |init.png|

.. function:: camera.snapshot() -> image.Iamge

    获取一帧图像 

    返回一个 ``image.Image`` 对象。

    UIFlow2.0

        |snapshot.png|

.. function:: camera.set_hmirror(enable: bool)

    开启或关闭水平镜像模式（True 表示开启，False 表示关闭）。默认为开启。

    UIFlow2.0
    
        |set_hmirror.png|

.. function:: camera.set_vflip(enable: bool)

    开启或关闭垂直翻转模式（True 表示开启，False 表示关闭）。默认为关闭。

    UIFlow2.0
    
        |set_vflip.png|

.. function:: camera.get_hmirror()

    返回当前是否启用了水平镜像模式。

    UIFlow2.0
    
        |get_hmirror.png|

.. function:: camera.get_vflip()

    返回当前是否启用了垂直翻转模式。

    UIFlow2.0
    
        |get_vflip.png|


 
