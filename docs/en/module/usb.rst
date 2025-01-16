USB Module 
=====================================

.. include:: ../refs/module.usb.ref

The USB Module is a module that uses the SPI interface to expand USB functionality, implemented with the MAX3421E.

Support the following products:

|USB Module|


Micropython Example 
--------------------------------

.. note:: Before using the following examples, please check the DIP switches on the module to ensure that the pins used in the example match the DIP switch positions. For specific configurations, please refer to the product manual page. The SPI configuration has been implemented internally, so users do not need to worry about it.

Input/Output Pin Control
++++++++++++++++++++++++++++
The module exposes 5 IN (input) pins and 5 OUT (output) pins through headers. This example demonstrates controlling the high and low level switching of the output pins, as well as reading and printing the level status of the input pins.

    .. literalinclude:: ../../../examples/module/usb/cores3_module_usb_gpio_example.py
        :language: python
        :linenos:   

Mouse 
++++++++++++++++++++++++++++
Implementing USB host to capture mouse input

    .. literalinclude:: ../../../examples/module/usb/cores3_module_usb_mouse_example.py
        :language: python
        :linenos:
 
Keyboard
++++++++++++++++++++++++++++
Implementing USB host to capture keyboard input

    .. literalinclude:: ../../../examples/module/usb/cores3_module_usb_kb_example.py
        :language: python
        :linenos:
 

UIFlow2.0 Example 
--------------------------------

Input/Output Pin Control
++++++++++++++++++++++++++++
 

    |gpio_example.png|

.. only:: builder_html

    |cores3_module_usb_gpio_example.m5f2|


Mouse
++++++++++++++++++++++++++++

    |mouse_example.png|

.. only:: builder_html

    |cores3_module_usb_mouse_example.m5f2|

Keyboard
++++++++++++++++++++++++++++

    |kb_example.png|

.. only:: builder_html

    |cores3_module_usb_kb_example.m5f2|


 

class USBModule  
------------------------------

Constructors
------------------------------

.. class:: USBModule(pin_cs: int = 1, pin_int: int = 10)

    :param int pin_cs: (RST) 复位引脚
    :param int pin_irq: (INT) 中断引脚

    UIFLOW2:

        |init.png|

.. method:: poll_data()
    
    poll data 
    
    **Note**: It needs to be called in the main loop

    UIFlow2.0

        |poll_data.png|


.. method:: is_left_btn_pressed() -> bool
    
    Check if the left mouse button is pressed.

    UIFlow2.0

        |is_left_btn_pressed.png|

.. method:: is_right_btn_pressed() -> bool
    
    Check if the right mouse button is pressed.

    UIFlow2.0

        |is_right_btn_pressed.png|

.. method:: is_middle_btn_pressed() -> bool
    
    Check if the middle mouse button is pressed.

    UIFlow2.0

        |is_middle_btn_pressed.png|

.. method:: is_forward_btn_pressed() -> bool
    
    Check if the forward mouse button is pressed.

    UIFlow2.0

        |is_forward_btn_pressed.png|

.. method:: is_back_btn_pressed() -> bool
    
    Check if the back mouse button is pressed.

    UIFlow2.0

        |is_back_btn_pressed.png|

 
.. method:: read_mouse_move() -> tuple[int, int] 
    
    Read Mouse Cursor Movement 

    Returns a tuple (x, y) containing the horizontal displacement x and vertical displacement y of the mouse;
    x range: -127 to 127; 0 indicates no movement, negative values indicate movement to the left, and positive values indicate movement to the right;
    y range: -127 to 127; 0 indicates no movement, negative values indicate movement upward, and positive values indicate movement downward.

    **Example:**
    
    :: 
    
        move = usb_module.read_mouse_move()
        x = move[0]
        y = move[1]
     
 
    UIFlow2.0

        |read_mouse_move.png|

.. method:: read_wheel_move() -> int 
    
    Read Mouse Wheel Movement 

    Returns a value in the range of -127 to 127, 0 indicates no movement, Positive values indicate forward scrolling, Negative values indicate backward scrolling.
 
    UIFlow2.0

        |read_wheel_move.png|


.. method:: read_kb_input(convert: bool = True) -> list 
  
    Read keyboard input  

    - ``convert`` Whether to convert HID Keycode to the corresponding string.

    Returns a list containing keyboard inputs (up to 6 elements, meaning a maximum of 6 key values can be input at once).

    **Example:**

    :: 
    
        res = usb_module.read_kb_input(convert=True)
        # output ['a', 'b', 'Enter']

        res = usb_module.read_kb_input(convert=False)
        # output [0x04, 0x05, 0x28]

    UIFlow2.0

        |read_kb_input.png|

.. method:: read_kb_modifier() -> int

    Read the keyboard modifier keys, namely "Ctrl", "Shift", "Alt", and "Win" keys.

    - ``Return``: The status of the keyboard modifier keys, usually represented by a bit mask to indicate the status of different modifier keys.
        - 0x01: Left Control key
        - 0x02: Left Shift key
        - 0x04: Left Alt key
        - 0x08: Left Windows key (Left GUI)
        - 0x10: Right Control key
        - 0x20: Right Shift key
        - 0x40: Right Alt key
        - 0x80: Right Windows key (Right GUI)

    **Example:**

    :: 

        modifier = module_usb.read_kb_modifier()
        if modifier & 0x01:
            print("left ctrl key pressed")

    UIFlow2.0

        |read_kb_modifier.png|

.. method:: read_gpin(pin) -> int

    Read input pin value 

    - ``pin`` pin number
    - ``Return`` 1 represents high level, and 0 represents low level.

    UIFlow2.0

        |read_gpin.png|

.. method:: write_gpout(pin, value)

    Write output pin value  

    - ``pin`` pin number
    - ``Return`` 1 represents high level, and 0 represents low level.

    UIFlow2.0

        |write_gpout.png|

