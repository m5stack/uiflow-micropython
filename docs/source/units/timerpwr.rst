
TimerPWR Unit
=============

.. include:: ../refs/unit.timerpwr.ref

The TimerPWR Unit is a timed power supply unit whose main functions are "charging & discharging + timed switching + screen display + boost output." It features an internal STM32 microcontroller that implements RTC and overall control, allowing users to set automatic power on/off times as needed. It is powered via the Type-C interface and can be connected to an external rechargeable battery via a 1.25-2P interface. The unit includes a built-in battery charging circuit supporting a charging current of 330mA. It also features an integrated DCDC boost circuit that provides a 5V/800mA (1400mA @ 1C battery power) power output to external devices via the Grove port. Additionally, the INA3221 sensor is built-in, allowing real-time monitoring of power input and output current and voltage. The unit is equipped with a 0.66-inch OLED display and two side buttons for user interaction, making it easy to view real-time system status and modify settings. Users can set parameters such as power on/off using the side buttons or via the I2C bus through the Grove interface with I2C commands. This product is suitable for smart homes, industrial automation, and timed control devices.

Support the following products:

|TimerPWRUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/timerpwr/atoms3_timerpwr_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |atoms3_timerpwr_example.m5f2|

class TimerPWRUnit
------------------

Constructors
------------

.. class:: TimerPWRUnit(i2c, address)

    Create a TimerPWR object.

    :param  i2c: I2C object
    :param int address: I2C address, 0x56 by default

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: TimerPWRUnit.get_firmware_version()

    Get firmware version.

    :return (int): Firmware version.

    UIFLOW2:

        |get_firmware_version.png|

.. method:: TimerPWRUnit.get_battery_voltage()

    Get battery voltage.

    :return (int): Battery voltage, in millivolt.

    UIFLOW2:

        |get_battery_voltage.png|

.. method:: TimerPWRUnit.get_battery_current()

    Get battery current.

    :return (int): Battery current, in milliamperes.

    UIFLOW2:

        |get_battery_current.png|

.. method:: TimerPWRUnit.get_usb_voltage()

    Get USB voltage.

    :return (int): USB voltage, in millivolt.

    UIFLOW2:

        |get_usb_voltage.png|

.. method:: TimerPWRUnit.get_usb_current()

    Get USB current.

    :return (int): USB current, in milliamperes.

    UIFLOW2:

        |get_usb_current.png|

.. method:: TimerPWRUnit.get_grove_voltage()

    Get Grove voltage.

    :return (int): Grove voltage, in millivolt.

    UIFLOW2:

        |get_grove_voltage.png|

.. method:: TimerPWRUnit.get_grove_current()

    Get Grove current.

    :return (int): Grove current, in milliamperes.

    UIFLOW2:

        |get_grove_current.png|

.. method:: TimerPWRUnit.is_charging()

    Check if the battery is charging.

    :return (bool): True if charging, False if not.

    UIFLOW2:

        |is_charging.png|

.. method:: TimerPWRUnit.get_button_status(btn)

    Get button status.

    :param int btn: button index.

        Options:
            - ``A``: 0
            - ``B``: 1

    :return (bool): True if pressed, False if not.

    UIFLOW2:

        |get_button_status.png|

.. method:: TimerPWRUnit.save_data_to_flash()

    Save data to flash.


    UIFLOW2:

        |save_data_to_flash.png|

.. method:: TimerPWRUnit.get_grove_output_status()

    Get Grove output status

    :return (bool): True if enabled, False if disabled.

    UIFLOW2:

        |get_grove_output_status.png|

.. method:: TimerPWRUnit.set_grove_output_status(enable)

    Set Grove output status.

    :param bool enable: Enable or disable Grove output.

        Options:
            - ``Enable``: True
            - ``Disable``: False

    UIFLOW2:

        |set_grove_output_status.png|

.. method:: TimerPWRUnit.get_oled_backlight_status()

    Get OLED backlight status.

    :return (bool): True if enabled, False if disabled.

    UIFLOW2:

        |get_oled_backlight_status.png|

.. method:: TimerPWRUnit.set_oled_backlight_status(enable)

    Set OLED backlight status.

    :param bool enable: Enable or disable OLED backlight.

        Options:
            - ``Enable``: True
            - ``Disable``: False

    UIFLOW2:

        |set_oled_backlight_status.png|

.. method:: TimerPWRUnit.sleep_once(whours, wmintues, wseconds, shours, smintues, sseconds)

    Set sleep once after hours, mintues, seconds and wake up in hours, mintues, seconds.

    :param int whours: Hours to wait before sleep.
    :param int wmintues: Mintues to wait before sleep.
    :param int wseconds: Seconds to wait before sleep.
    :param int shours: Hours to wait before wake up.
    :param int smintues: Mintues to wait before wake up.
    :param int sseconds: Seconds to wait before wake up.

    UIFLOW2:

        |sleep_once.png|

.. method:: TimerPWRUnit.set_power_on_time(hours, mintues, seconds)

    Set power on time.

    :param int hours: Hours to power on.
    :param int mintues: Mintues to power on.
    :param int seconds: Seconds to power on.

.. method:: TimerPWRUnit.set_power_off_time(hours, mintues, seconds)

    Set power off time.

    :param int hours: Hours to power off.
    :param int mintues: Mintues to power off.
    :param int seconds: Seconds to power off.

.. method:: TimerPWRUnit.sleep_cycle(whours, wmintues, wseconds, shours, smintues, sseconds)

    Set sleep cycle after hours, mintues, seconds and wake up in hours, mintues, seconds.

    :param int whours: Hours to wait before sleep.
    :param int wmintues: Mintues to wait before sleep.
    :param int wseconds: Seconds to wait before sleep.
    :param int shours: Hours to wait before wake up.
    :param int smintues: Mintues to wait before wake up.
    :param int sseconds: Seconds to wait before wake up.

    UIFLOW2:

        |sleep_cycle.png|

.. method:: TimerPWRUnit.set_cycle_sleep(enable)

    Set cycle sleep.

    :param bool enable: Enable or disable cycle sleep.

        Options:
            - ``Enable``: True
            - ``Disable``: False

.. method:: TimerPWRUnit.set_wakeup_trigger(trigger)

    Set wake-up trigger.

    :param  trigger: Set wake-up trigger.

        Options:
            - ``ALL``: timerpwrunit_0.TRIG_ALL
            - ``TIMER``: timerpwrunit_0.TRIG_TIMER
            - ``BUTTON``: timerpwrunit_0.TRIG_BUTTON
            - ``NONE``: timerpwrunit_0.TRIG_NONE

    UIFLOW2:

        |set_wakeup_trigger.png|

.. method:: TimerPWRUnit.set_sleep_trigger(trigger)

    Set sleep trigger.

    :param  trigger: Set sleep trigger.

        Options:
            - ``ALL``: timerpwrunit_0.TRIG_ALL
            - ``TIMER``: timerpwrunit_0.TRIG_TIMER
            - ``BUTTON``: timerpwrunit_0.TRIG_BUTTON
            - ``I2C``: timerpwrunit_0.TRIG_I2C
            - ``NONE``: timerpwrunit_0.TRIG_NONE

    UIFLOW2:

        |set_sleep_trigger.png|

.. method:: TimerPWRUnit.set_callback(event, callback)

    Set callback function.

    :param  event: event type.

        Options:
            - ``USB inserted``: timerpwrunit_0.EVENT_USB_INSERTED
            - ``USB removed``: timerpwrunit_0.EVENT_USB_REMOVED
            - ``Button A pressed``: timerpwrunit_0.EVENT_BUTTONA_PRESSED
            - ``Button A released``: timerpwrunit_0.EVENT_BUTTONA_RELEASED
            - ``Button B pressed``: timerpwrunit_0.EVENT_BUTTONB_PRESSED
            - ``Button B released``: timerpwrunit_0.EVENT_BUTTONB_RELEASED
            - ``Not charging``: timerpwrunit_0.EVENT_NOT_CHARGING
            - ``Charging``: timerpwrunit_0.EVENT_CHARGING

    :param  callback: callback function.

    UIFLOW2:

        |usb_callback.png|

        |charging_callback.png|

        |button_callback.png|

.. method:: TimerPWRUnit.tick()

    Update status in loop.


    UIFLOW2:

        |tick.png|



Constants
---------

.. data:: TimerPWRUnit._SLEEP_COMMAND_REG
.. data:: TimerPWRUnit._CYCLE_REG
.. data:: TimerPWRUnit._GROVE_OUTPUT_REG
.. data:: TimerPWRUnit._OLED_BACKLIGHT_REG
.. data:: TimerPWRUnit._WAKE_UP_TRIGGER_REG
.. data:: TimerPWRUnit._SLEEP_TRIGGER_REG
.. data:: TimerPWRUnit._POWER_ON_TIME_REG
.. data:: TimerPWRUnit._POWER_OFF_TIME_REG
.. data:: TimerPWRUnit._BUTTON_STATUS_REG
.. data:: TimerPWRUnit._USB_VOLTAGE_REG
.. data:: TimerPWRUnit._USB_CURRENT_REG
.. data:: TimerPWRUnit._GROVE_VOLTAGE_REG
.. data:: TimerPWRUnit._GROVE_CURRENT_REG
.. data:: TimerPWRUnit._BATTERY_VOLTAGE_REG
.. data:: TimerPWRUnit._BATTERY_CURRENT_REG
.. data:: TimerPWRUnit._CHARGING_STATUS_REG
.. data:: TimerPWRUnit._SAVE_DATA_TO_FLASH_REG
.. data:: TimerPWRUnit._FW_VERSION_REG
.. data:: TimerPWRUnit._I2C_ADDRESS_REG

    register address.

    
.. data:: TimerPWRUnit.TRIG_ALL
.. data:: TimerPWRUnit.TRIG_TIMER
.. data:: TimerPWRUnit.TRIG_BUTTON
.. data:: TimerPWRUnit.TRIG_I2C
.. data:: TimerPWRUnit.TRIG_NONE

    trigger type.

    
.. data:: TimerPWRUnit.EVENT_USB_INSERTED
.. data:: TimerPWRUnit.EVENT_USB_REMOVED
.. data:: TimerPWRUnit.EVENT_BUTTONA_RELEASED
.. data:: TimerPWRUnit.EVENT_BUTTONA_PRESSED
.. data:: TimerPWRUnit.EVENT_BUTTONB_RELEASED
.. data:: TimerPWRUnit.EVENT_BUTTONB_PRESSED
.. data:: TimerPWRUnit.EVENT_NOT_CHARGING
.. data:: TimerPWRUnit.EVENT_CHARGING

    event type.

    
.. data:: TimerPWRUnit._USB
.. data:: TimerPWRUnit._BUTTON_A
.. data:: TimerPWRUnit._BUTTON_B
.. data:: TimerPWRUnit._CHARGING

    index.

    
