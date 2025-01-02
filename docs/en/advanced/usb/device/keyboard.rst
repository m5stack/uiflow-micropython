:mod:`keyboard`  
=====================================
usb device keyboard

.. include:: ../../../refs/advanced.usb.device.keyboard.ref

.. note:: This module is only applicable to the CoreS3 Controller

.. module:: keyboard
    :synopsis: bluetooth keyboard    



Micropython Example 
--------------------------------

USB keyboard
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../../../examples/advanced/usb/device/m5cores3_usbd_keyboard_example.py
        :language: python
        :linenos:

UIFlow2.0 Example 
------------------------------

USB keyboard
++++++++++++++++++++++++++++

    |example.png|

.. only:: builder_html

    |m5cores3_usbd_keyboard_example.m5f2|


class Keyboard  
------------------------------
.. function:: usb.device.keyboard.Keyboard()

    Create Keyboard object 

    UIFlow2.0
    
        |init.png| 

.. method:: set_modifiers(right_gui: bool = False, right_alt: bool = False, right_shift: bool = False, right_ctrl: bool = False, \
                       left_gui: bool = False, left_alt: bool = False, left_shift: bool = False, left_ctrl: bool = False)

    Set modifier keys

    - ``right_gui`` The state of the right-side GUI key. True indicates that the key is pressed.
    - ``right_alt`` The state of the right-side Alt key. True indicates that the key is pressed.
    - ``right_shift`` The state of the right-side Shift key. True indicates that the key is pressed.
    - ``right_ctrl`` The state of the right-side Ctrl key. True indicates that the key is pressed.
    - ``left_gui`` The state of the left-side GUI key. True indicates that the key is pressed.
    - ``left_alt`` The state of the left-side Alt key. True indicates that the key is pressed.
    - ``left_shift`` The state of the left-side Shift key. True indicates that the key is pressed.
    - ``left_ctrl``  The state of the left-side Ctrl key. True indicates that the key is pressed.

    :note: Changes will take effect after calling Keyboard.send_report().

    UIFlow2.0
    
        |set_modifiers.png|
         

.. method:: set_keys(k0: int = 0, k1: int = 0, k2: int = 0, k3: int = 0, k4: int = 0, k5: int = 0)

    Press specified keys (up to 6 key values at a time)

    - ``k0~k5`` The input is a standard HID key value. For details, refer to the KeyCode() class.

    :note: Changes will take effect after calling Keyboard.send_report().

    example: Press the lowercase 'a'

    ::

        Keyboard.set_keys(k0=KeyCode.A)
        Keyboard.send_report()
        Keyboard.set_keys(k0=0)
        Keyboard.send_report()

    example: Press the uppercase 'A'

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

    Send keyboard status report

    UIFlow2.0
    
        |send_report.png|
        
.. method:: input(key)

    input key

    - ``key`` The input can be a string within the ASCII range or a value from KeyCode.

    example:
    
    ::
    
        Keyboard.input("Hello M5")
        Keyboard.input(KeyCode.A)

    UIFlow2.0
    
        |input.png|
 
