:mod:`keyboard`  
=====================================
usb 设备键盘 

.. include:: ../../../refs/advanced.usb.device.keyboard.ref

.. note:: 当前模块只适用于 CoreS3 主机

.. module:: keyboard
    :synopsis: bluetooth keyboard    



Micropython 案例 
--------------------------------

usb 键盘 
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../../../examples/advanced/usb/device/m5cores3_usbd_keyboard_example.py
        :language: python
        :linenos:

UIFlow2.0 案例 
------------------------------

usb 键盘
++++++++++++++++++++++++++++

    |example.png|

.. only:: builder_html

    |m5cores3_usbd_keyboard_example.m5f2|


class Keyboard  
------------------------------
.. function:: usb.device.keyboard.Keyboard()

    创建 Keyboard 对象 

    UIFlow2.0
    
        |init.png| 

.. method:: set_modifiers(right_gui: bool = False, right_alt: bool = False, right_shift: bool = False, right_ctrl: bool = False, \
                       left_gui: bool = False, left_alt: bool = False, left_shift: bool = False, left_ctrl: bool = False)

    设置修饰键

    - ``right_gui`` 右侧 GUI 键状态，True 表示按下。
    - ``right_alt`` 右侧 Alt 键状态，True 表示按下。
    - ``right_shift`` 右侧 Shift 键状态，True 表示按下。
    - ``right_ctrl`` 右侧 Ctrl 键状态，True 表示按下。
    - ``left_gui`` 左侧 GUI 键状态，True 表示按下。
    - ``left_alt`` 左侧 Alt 键状态，True 表示按下。
    - ``left_shift`` 左侧 Shift 键状态，True 表示按下。
    - ``left_ctrl`` 左侧 Ctrl 键状态，True 表示按下。

    :note: 需要调用 Keyboard.send_report() 后生效 

    UIFlow2.0
    
        |set_modifiers.png|
         

.. method:: set_keys(k0: int = 0, k1: int = 0, k2: int = 0, k3: int = 0, k4: int = 0, k5: int = 0)

    按下指定按键(最多一次输入6个键值)

    - ``k0~k5`` 输入为标准 HID 键值，详情参考 class KeyCode()

    :note: 需要调用 Keyboard.send_report() 后生效 

    example: 输入小写 'a'
    
    ::
        
        Keyboard.set_keys(k0=KeyCode.A)
        Keyboard.send_report()
        Keyboard.set_keys(k0=0)
        Keyboard.send_report()
    example: 输入大写 'A'
    
    ::
    
        Keyboard.set_modifiers(right_shift=True)
        Keyboard.set_keys(k0=KeyCode.A)
        Keyboard.send_report()
        Keyboard.set_modifiers(right_shift=False)
        Keyboard.set_keys(k0=0)
        Keyboard.send_report()

    UIFlow2.0
    
        |set_keys.png|

.. method:: send_report()

    发送键盘状态报告

    UIFlow2.0
    
        |send_report.png|
        
.. method:: input(key)

    输入键值

    - ``key`` 支持 ASCII 范围字符串，或者使用 KeyCode  

    example:

    ::

        Keyboard.input("Hello M5")
        Keyboard.input(KeyCode.A)

    UIFlow2.0
    
        |input.png|
 
