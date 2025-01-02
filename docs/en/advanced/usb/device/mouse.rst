:mod:`mouse`  
=====================================
usb device mouse 

.. include:: ../../../refs/advanced.usb.device.mouse.ref
 
.. note:: This module is only applicable to the CoreS3 Controller

.. module:: mouse
    :synopsis: usb mouse    



Micropython Example 
--------------------------------

USB Mouse
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../../../examples/advanced/usb/device/m5cores3_usbd_mouse_example.py
        :language: python
        :linenos:

UIFlow2.0 Example 
------------------------------

USB Mouse
++++++++++++++++++++++++++++

    |example.png|

.. only:: builder_html

    |m5cores3_usbd_mouse_example.m5f2|


class Mouse  
------------------------------

.. function:: usb.device.mouse.Mouse()

    Create Mouse object 

    UIFlow2.0
    
        |init.png| 


.. method:: set_axes(x: int = 0, y: int = 0) 

    Set Cursor Position

    - ``x`` Horizontal movement, range: -127 to 127. A value less than 0 moves the cursor to the left, and a value greater than 0 moves it to the right.
    - ``y`` Vertical movement, range: -127 to 127. A value less than 0 scrolls the cursor up, and a value greater than 0 scrolls it down.

    :note: Changes will take effect after calling Mouse.send_report().

    UIFlow2.0
    
        |set_axes.png|

.. method:: set_wheel(w: int = 0)

    Set mouse wheel value

    - ``w`` Wheel value, range: -127 to 127. A value less than 0 scrolls the wheel down, and a value greater than 0 scrolls the wheel up.

    :note: Changes will take effect after calling Mouse.send_report().

    UIFlow2.0
    
        |set_wheel.png|

.. method:: set_buttons(left: bool = False, right: bool = False, middle: bool = False) 

    Set mouse button status

    - ``left`` True indicates the left button is pressed.
    - ``right`` True indicates the right button is pressed.
    - ``middle`` True indicates the middle (wheel) button is pressed. 

    :note: Changes will take effect after calling Mouse.send_report().

    example: Mouse click left button 

    ::

        set_buttons(left=True)  # press
        send_report()
        set_buttons(left=False) # release
        send_report()

    UIFlow2.0
    
        |set_buttons.png|

.. method::send_report() 

    Send the mouse status report.

    UIFlow2.0
    
        |send_report.png|

.. method:: move(x: int = 0, y: int = 0)  

    Move cursor

    - ``x`` Horizontal movement, range: -127 to 127. A value less than 0 moves the cursor to the left, and a value greater than 0 moves it to the right.
    - ``y`` Vertical movement, range: -127 to 127. A value less than 0 moves the cursor up, and a value greater than 0 moves it down.

    UIFlow2.0
    
        |move.png|

.. method:: click_left(release: bool = True) 

    Click left button

    - ``release``  Set to True to release the left mouse button after pressing, or False to not release.

    UIFlow2.0
    
        |click_left.png|

.. method:: click_right(release: bool = True)  

    Click right button

    - ``release``  Set to True to release the right mouse button after pressing, or False to not release.

    UIFlow2.0
    
        |click_right.png|

.. method:: click_middle(release: bool = True) 

    Click middle button

    - ``release``  Set to True to release the left middle button after pressing, or False to not release.

    UIFlow2.0
    
        |click_middle.png|
         
.. method:: click_forawrd()  

    Click forward button

    - ``release``  Set to True to release the left forward button after pressing, or False to not release.

    UIFlow2.0
    
        |click_forward.png|

.. method:: click_backward()  

    Click backward button

    - ``release``  Set to True to release the left backward button after pressing, or False to not release.

    UIFlow2.0
    
        |click_backward.png|

.. method:: scroll(w: int)  

    Scroll wheel

    - ``w`` range: -127 to 127, values less than 0 scroll up, and values greater than 0 scroll down.

    UIFlow2.0
    
        |scroll.png|
         

 
