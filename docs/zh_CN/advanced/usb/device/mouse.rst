:mod:`mouse`  
=====================================
usb 设备鼠标 

.. include:: ../../../refs/advanced.usb.device.mouse.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: mouse
    :synopsis: usb mouse    



Micropython 案例 
--------------------------------

usb 鼠标 
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../../../examples/advanced/usb/device/m5cores3_usbd_mouse_example.py
        :language: python
        :linenos:

UIFlow2.0 案例 
------------------------------

usb 鼠标 
++++++++++++++++++++++++++++

    |example.png|

.. only:: builder_html

    |m5cores3_usbd_mouse_example.m5f2|


class Mouse  
------------------------------
.. function:: usb.device.mouse.Mouse()

    创建 Mouse 对象 

    UIFlow2.0
    
        |init.png| 

.. method:: set_axes(x: int = 0, y: int = 0) 

    设置光标位置

    - ``x`` 水平移动，范围：-127~127，小于0为向左移动，大于0为向右移动。
    - ``y`` 纵向移动，范围：-127~127，小于0为向上滚动，大于0为向下滚动。

    :note: 需要调用 Mouse.send_report() 后生效

    UIFlow2.0
    
        |set_axes.png|

.. method:: set_wheel(w: int = 0)

    设置鼠标滚轮值

    - ``w`` 滚轮值，范围:-127~127，小于0为向下滚动，大于0为向上滚动。 

    :note: 需要调用 Mouse.send_report() 后生效

    UIFlow2.0
    
        |set_wheel.png|

.. method:: set_buttons(left: bool = False, right: bool = False, middle: bool = False) 

    设置鼠标按钮状态

    - ``left`` True 为按下左键
    - ``right`` True 为按下右键
    - ``middle`` True 为按下滚轮 

    :note: 需要调用 Mouse.send_report() 后生效

    example: 鼠标左键单击 
    ::
    
        set_buttons(left=True)  # 按下
        send_report()
        set_buttons(left=False) # 释放
        send_report()

    UIFlow2.0
    
        |set_buttons.png|

.. method::send_report() 

    发送鼠标状态报告

    UIFlow2.0
    
        |send_report.png|

.. method:: move(x: int = 0, y: int = 0)  

    移动光标

    - ``x`` 水平移动，范围：-127~127，小于0为向左移动，大于0为向右移动。
    - ``y`` 纵向移动，范围：-127~127，小于0为向上滚动，大于0为向下滚动。

    UIFlow2.0
    
        |move.png|

.. method:: click_left(release: bool = True) 

    单击左键

    - ``release`` 设为 True 为按下鼠标左键后释放， False 为不释放 

    UIFlow2.0
    
        |click_left.png|

.. method:: click_right(release: bool = True)  

    单击右键

    - ``release`` 设为 True 为按下鼠标右键后释放， False 为不释放 

    UIFlow2.0
    
        |click_right.png|

.. method:: click_middle(release: bool = True) 

    单击滚轮

    - ``release`` 设为 True 为按下鼠标滚轮后释放， False 为不释放 

    UIFlow2.0
    
        |click_middle.png|
         
.. method:: click_forawrd()  

    单击前进按键

    - ``release`` 设为 True 为按下鼠标前进键后释放， False 为不释放 

    UIFlow2.0
    
        |click_forawrd.png|

.. method:: click_backward()  

    单击后退按键

    - ``release`` 设为 True 为按下鼠标前后退后释放， False 为不释放 

    UIFlow2.0
    
        |click_backward.png|

.. method:: scroll(w: int)  

    滚动滚轮

    - ``w`` 范围：-127~127，小于0向上滚动，大于0向下滚动。  

    UIFlow2.0
    
        |scroll.png|
         

 
