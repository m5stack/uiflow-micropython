#######
DualKey
#######

.. include:: ../refs/controllers.dualkey.ref

Support the following products:

    |DualKey|

UiFlow2 Example 
---------------

Button LED Control
^^^^^^^^^^^^^^^^^^

Open the |dualkey_button_led_example.m5f2| project in UiFlow2.

This example demonstrates button callback functions to toggle RGB LEDs. When the left button (BtnA) is clicked, it toggles the left RGB LED (LED 0). When the right button (BtnB) is clicked, it toggles the right RGB LED (LED 1).

UiFlow2 Code Block:

    |dualkey_button_led_example.png|

Example output:

    None

Power Detection
^^^^^^^^^^^^^^^^

Open the |dualkey_power_detection_example.m5f2| project in UiFlow2.

This example demonstrates battery voltage monitoring and switch position detection. It reads the switch position (left/middle/right) and displays corresponding RGB LED colors, while also periodically reading and displaying the battery voltage in millivolts.

UiFlow2 Code Block:

    |dualkey_power_detection_example.png|

Example output:

    None

USB Mouse
^^^^^^^^^

Open the |dualkey_usb_mouse_example.m5f2| project in UiFlow2.

This example demonstrates USB HID mouse functionality with button-triggered clicks. When the left button (BtnA) is clicked, it sends a left mouse click and lights up the left RGB LED. When the right button (BtnB) is clicked, it sends a right mouse click and lights up the right RGB LED. The LEDs automatically turn off after 300ms.

UiFlow2 Code Block:

    |dualkey_usb_mouse_example.png|

Example output:

    None

MicroPython Example 
-------------------

Button LED Control
^^^^^^^^^^^^^^^^^^

This example demonstrates button callback functions to toggle RGB LEDs. When the left button (BtnA) is clicked, it toggles the left RGB LED (LED 0). When the right button (BtnB) is clicked, it toggles the right RGB LED (LED 1).

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/dualkey/dualkey_button_led_example.py
        :language: python
        :linenos:

Example output:

    None

Power Detection
^^^^^^^^^^^^^^^^

This example demonstrates battery voltage monitoring and switch position detection. It reads the switch position (left/middle/right) and displays corresponding RGB LED colors, while also periodically reading and displaying the battery voltage in millivolts.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/dualkey/dualkey_power_detection_example.py
        :language: python
        :linenos:

Example output:

    None

USB Mouse
^^^^^^^^^

This example demonstrates USB HID mouse functionality with button-triggered clicks. When the left button (BtnA) is clicked, it sends a left mouse click and lights up the left RGB LED. When the right button (BtnB) is clicked, it sends a right mouse click and lights up the right RGB LED. The LEDs automatically turn off after 300ms.

.. note:: When USB mouse is initialized, the USB-CDC REPL may disconnect. You may need to reconnect to the device after running this example.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/dualkey/dualkey_usb_mouse_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

class DualKey  
^^^^^^^^^^^^^

.. class:: hardware.dualkey.DualKey()

    DualKey module - voltage and switch detection (singleton).

    The DualKey class is a singleton that provides methods to monitor battery voltage, VBUS voltage, charging status, and switch position.

    MicroPython Code Block:

        .. code-block:: python

            from hardware import dualkey

    .. method:: get_battery_voltage()

        Get battery voltage.

        :returns: Battery voltage value in millivolts (mV).
        :rtype: int

        UiFlow2 Code Block:

            |get_battery_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = dualkey.get_battery_voltage()
                print(f"Battery voltage: {voltage} mV")

    .. method:: get_vbus_voltage()

        Get VBUS(USB power) voltage.

        :returns: VBUS voltage value in millivolts (mV).
        :rtype: int

        UiFlow2 Code Block:

            |get_vbus_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                vbus_voltage = dualkey.get_vbus_voltage()
                print(f"VBUS voltage: {vbus_voltage} mV")

    .. method:: is_charging()

        Check if the device is charging.

        :returns: Returns `True` if charging, `False` if not charging.
        :rtype: bool

        UiFlow2 Code Block:

            |is_charging.png|

        MicroPython Code Block:

            .. code-block:: python

                if dualkey.is_charging():
                    print("Device is charging")
                else:
                    print("Device is not charging")

    .. method:: get_switch_position()

        Get switch position.

        :returns: Switch position value:
            - ``0``: left
            - ``1``: middle
            - ``2``: right
        :rtype: int

        UiFlow2 Code Block:

            |get_switch_position.png|

        MicroPython Code Block:

            .. code-block:: python

                position = dualkey.get_switch_position()
                if position == 0:
                    print("Switch position: left")
                elif position == 1:
                    print("Switch position: middle")
                elif position == 2:
                    print("Switch position: right")

