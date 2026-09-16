Stamp Timer Power 2
===================

.. sku: S021
.. py:currentmodule:: stamp
.. include:: ../refs/stamp.stp2.ref

StampTimerPower2 provides power management, GPIO, ADC, PWM, NeoPixel, button events, IRQ, wakeup, watchdog, timers and RTC RAM through I2C.

Support the following products:

    |Stamp Timer Power 2|

UiFlow2 Example
---------------

GPIO input
^^^^^^^^^^

Open the |basic_stp2_gpio_input_example.m5f2| project in UiFlow2.

G4 is a pull-up input. Connect G4 to GND for Low (0), or release it for High (1).

UiFlow2 Code Block:

    |basic_stp2_gpio_input_example.png|

Example output:

    None

GPIO output
^^^^^^^^^^^

Open the |basic_stp2_gpio_output_example.m5f2| project in UiFlow2.

G3 is the output. Button A sets Low, B toggles the level, and C sets High. The display shows the commanded level and pin readback.

UiFlow2 Code Block:

    |basic_stp2_gpio_output_example.png|

Example output:

    None

GPIO interrupt
^^^^^^^^^^^^^^

Open the |basic_stp2_gpio_irq_example.m5f2| project in UiFlow2.

Connect STP2 G0 to Basic G26 for IRQ. Connect G4 to GND and release it to generate input changes. Button A clears the count, B pauses IRQ handling, and C resumes it. The display shows the count and G4 level.

UiFlow2 Code Block:

    |basic_stp2_gpio_irq_example.png|

Example output:

    None

ADC input
^^^^^^^^^

Open the |basic_stp2_adc_example.m5f2| project in UiFlow2.

Read raw ADC values from G1 and G2. Each value is in the range 0 to 4095.

UiFlow2 Code Block:

    |basic_stp2_adc_example.png|

Example output:

    None

PWM output
^^^^^^^^^^

Open the |basic_stp2_pwm_example.m5f2| project in UiFlow2.

PWM0 uses G3 at 1 kHz. Button A decreases duty by 10 percentage points, B sets duty to zero, and C increases duty by 10 percentage points. Duty is limited to 0 to 100 percent.

UiFlow2 Code Block:

    |basic_stp2_pwm_example.png|

Example output:

    None

NeoPixel control
^^^^^^^^^^^^^^^^

Open the |basic_stp2_neopixel_example.m5f2| project in UiFlow2.

Connect the LED data input to G0 and share GND. Button A cycles through red, green, blue and white; B decreases brightness by 10 percentage points and C increases it by 10. The example controls one LED, starting with red at 20 percent brightness.

UiFlow2 Code Block:

    |basic_stp2_neopixel_example.png|

Example output:

    None

Power control
^^^^^^^^^^^^^

Open the |basic_stp2_power_config_example.m5f2| project in UiFlow2.

Button A toggles LDO and button B toggles DCDC. The display and serial output show the enable states read from the module every 100 ms.

UiFlow2 Code Block:

    |basic_stp2_power_config_example.png|

Example output:

    None

Timed power-on
^^^^^^^^^^^^^^

Open the |basic_stp2_timer_example.m5f2| project in UiFlow2.

Button A toggles LDO output retention during shutdown (Off by default). Button B cycles the power-on delay through 5, 10 and 15 seconds (5 seconds by default). Button C (Shutdown) applies the setting, arms the power-on timer and immediately shuts down STP2. Buttons are locked until the countdown finishes.

Keep Basic independently powered so it can display the countdown while STP2 is shut down.

The graphical example displays Timer elapsed when the countdown finishes; it does not verify the wake source.

UiFlow2 Code Block:

    |basic_stp2_timer_example.png|

Example output:

    None

MicroPython Example
-------------------

GPIO input
^^^^^^^^^^

G4 is a pull-up input. Connect G4 to GND for Low (0), or release it for High (1).

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_gpio_input_example.py
        :language: python
        :linenos:

Example output:

    None

GPIO output
^^^^^^^^^^^

G3 is the output. Button A sets Low, B toggles the level, and C sets High. The display shows the commanded level and pin readback.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_gpio_output_example.py
        :language: python
        :linenos:

Example output:

    None

GPIO interrupt
^^^^^^^^^^^^^^

Connect STP2 G0 to Basic G26 for IRQ. Connect G4 to GND and release it to generate input changes. Button A clears the count, B pauses IRQ handling, and C resumes it. The display shows the count and G4 level.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_gpio_irq_example.py
        :language: python
        :linenos:

Example output:

    None

ADC input
^^^^^^^^^

Read raw ADC values from G1 and G2. Each value is in the range 0 to 4095.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_adc_example.py
        :language: python
        :linenos:

Example output:

    None

PWM output
^^^^^^^^^^

PWM0 uses G3 at 1 kHz. Button A decreases duty by 10 percentage points, B sets duty to zero, and C increases duty by 10 percentage points. Duty is limited to 0 to 100 percent.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_pwm_example.py
        :language: python
        :linenos:

Example output:

    None

NeoPixel control
^^^^^^^^^^^^^^^^

Connect the LED data input to G0 and share GND. Button A cycles through red, green, blue and white; B decreases brightness by 10 percentage points and C increases it by 10. The example controls one LED, starting with red at 20 percent brightness.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_neopixel_example.py
        :language: python
        :linenos:

Example output:

    None

Power control
^^^^^^^^^^^^^

Button A toggles LDO and button B toggles DCDC. The display and serial output show the enable states read from the module every 100 ms.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_power_config_example.py
        :language: python
        :linenos:

Example output:

    None

Timed power-on
^^^^^^^^^^^^^^

Button A toggles LDO output retention during shutdown (Off by default). Button B cycles the power-on delay through 5, 10 and 15 seconds (5 seconds by default). Button C (Shutdown) applies the setting, arms the power-on timer and immediately shuts down STP2. Buttons are locked until the countdown finishes.

Keep Basic independently powered so it can display the countdown while STP2 is shut down.

The Python example reads the wake source after the countdown and displays whether a timer wake was detected.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/timer_power2/basic_stp2_timer_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

StampTimerPower2
^^^^^^^^^^^^^^^^

Constructors
~~~~~~~~~~~~

.. py:class:: StampTimerPower2(i2c, *, pm1_int_gpio=-1, mcu_int_gpio=-1)

    Create the module at fixed I2C address ``0x6E``. The application owns the I2C object. Supply both IRQ GPIOs or leave both at ``-1``.

    :param i2c: Caller-owned I2C bus.
    :type i2c: I2C
    :param pm1_int_gpio: Module IRQ output GPIO, 0~4; -1 disables IRQ. Default: -1. Keyword-only parameter.
    :type pm1_int_gpio: int
    :param mcu_int_gpio: Basic IRQ input GPIO; use 26 for this wiring, or -1 without IRQ. Default: -1. Keyword-only parameter.
    :type mcu_int_gpio: int


    :raises ValueError: Invalid GPIO arguments or an incomplete IRQ pair.
    :raises OSError: I2C communication failed.
    :raises RuntimeError: Host IRQ support is unavailable.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            import M5
            from hardware import I2C, Pin
            from stamp import StampTimerPower2

            M5.begin()
            i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
            stp2 = StampTimerPower2(i2c)
            # For INT callbacks only: connect STP2 G0 to Basic G26.
            # stp2 = StampTimerPower2(i2c, pm1_int_gpio=0, mcu_int_gpio=26)

Constants
~~~~~~~~~

.. list-table::
    :header-rows: 1

    * - Constant
      - Value
      - Meaning
    * - ``StampTimerPower2.PIN_FUNCTION_GPIO``
      - 0
      - Normal GPIO function.
    * - ``StampTimerPower2.PIN_FUNCTION_IRQ``
      - 1
      - Active-low IRQ output function.
    * - ``StampTimerPower2.PIN_FUNCTION_WAKE``
      - 2
      - Power-off wake input function.
    * - ``StampTimerPower2.PIN_FUNCTION_OTHER``
      - 3
      - ADC, PWM, NeoPixel, or another alternate function.
    * - ``StampTimerPower2.GPIO_MODE_IN``
      - 0
      - Digital input mode.
    * - ``StampTimerPower2.GPIO_MODE_OUT``
      - 1
      - Push-pull output mode.
    * - ``StampTimerPower2.GPIO_MODE_OPEN_DRAIN``
      - 2
      - Open-drain output mode.
    * - ``StampTimerPower2.GPIO_PULL_NONE``
      - 0
      - No internal pull resistor.
    * - ``StampTimerPower2.GPIO_PULL_UP``
      - 1
      - Internal pull-up enabled.
    * - ``StampTimerPower2.GPIO_PULL_DOWN``
      - 2
      - Internal pull-down enabled.
    * - ``StampTimerPower2.DRIVE_PUSH_PULL``
      - 0
      - Push-pull drive.
    * - ``StampTimerPower2.DRIVE_OPEN_DRAIN``
      - 1
      - Open-drain drive.
    * - ``StampTimerPower2.POWER_SOURCE_NONE``
      - 0
      - No power-source flag is active.
    * - ``StampTimerPower2.POWER_SOURCE_5VIN``
      - 1
      - 5VIN / USB input is active.
    * - ``StampTimerPower2.POWER_SOURCE_5VINOUT``
      - 2
      - The bidirectional 5VINOUT input is active.
    * - ``StampTimerPower2.POWER_SOURCE_BATTERY``
      - 4
      - Battery input is active.
    * - ``StampTimerPower2.WAKE_SOURCE_TIMER``
      - 1
      - Timer wake.
    * - ``StampTimerPower2.WAKE_SOURCE_VIN``
      - 2
      - 5VIN insertion wake.
    * - ``StampTimerPower2.WAKE_SOURCE_POWER_BUTTON``
      - 4
      - Power-button wake.
    * - ``StampTimerPower2.WAKE_SOURCE_RESET_BUTTON``
      - 8
      - Reset-button wake.
    * - ``StampTimerPower2.WAKE_SOURCE_COMMAND_RESET``
      - 16
      - Command-reset wake.
    * - ``StampTimerPower2.WAKE_SOURCE_GPIO``
      - 32
      - GPIO input wake.
    * - ``StampTimerPower2.WAKE_SOURCE_5V_INOUT``
      - 64
      - 5VINOUT event wake.
    * - ``StampTimerPower2.BUTTON_TIMING_CLICK``
      - 0
      - Single-click timing selector.
    * - ``StampTimerPower2.BUTTON_TIMING_DOUBLE``
      - 1
      - Double-click timing selector.
    * - ``StampTimerPower2.BUTTON_TIMING_LONG``
      - 2
      - Long-press timing selector.
    * - ``StampTimerPower2.TIMER_ACTION_STOP``
      - 0
      - Stop when the timer expires.
    * - ``StampTimerPower2.TIMER_ACTION_FLAG``
      - 1
      - Generate an event flag when the timer expires.
    * - ``StampTimerPower2.TIMER_ACTION_REBOOT``
      - 2
      - Reboot when the timer expires.
    * - ``StampTimerPower2.TIMER_ACTION_POWER_ON``
      - 3
      - Power on when the timer expires.
    * - ``StampTimerPower2.TIMER_ACTION_POWER_OFF``
      - 4
      - Power off when the timer expires.
    * - ``StampTimerPower2.IRQ_GROUP_GPIO``
      - 0
      - irq group gpio
    * - ``StampTimerPower2.IRQ_GROUP_SYSTEM``
      - 1
      - irq group system
    * - ``StampTimerPower2.IRQ_GROUP_BUTTON``
      - 2
      - irq group button
    * - ``StampTimerPower2.WAKE_EDGE_FALLING``
      - 0
      - wake edge falling
    * - ``StampTimerPower2.WAKE_EDGE_RISING``
      - 1
      - wake edge rising

Combine EVENT flags with bitwise OR for add_event_cb(). The namespace refers to the existing driver constants without copying values.

.. list-table::
    :header-rows: 1

    * - Constant
      - Value
      - Meaning
    * - ``StampTimerPower2.EVENT.GPIO0_CHANGE``
      - 0x1
      - gpio0 change
    * - ``StampTimerPower2.EVENT.GPIO1_CHANGE``
      - 0x2
      - gpio1 change
    * - ``StampTimerPower2.EVENT.GPIO2_CHANGE``
      - 0x4
      - gpio2 change
    * - ``StampTimerPower2.EVENT.GPIO3_CHANGE``
      - 0x8
      - gpio3 change
    * - ``StampTimerPower2.EVENT.GPIO4_CHANGE``
      - 0x10
      - gpio4 change
    * - ``StampTimerPower2.EVENT.VIN_INSERT``
      - 0x20
      - vin insert
    * - ``StampTimerPower2.EVENT.VIN_REMOVE``
      - 0x40
      - vin remove
    * - ``StampTimerPower2.EVENT.VINOUT_INSERT``
      - 0x80
      - vinout insert
    * - ``StampTimerPower2.EVENT.VINOUT_REMOVE``
      - 0x100
      - vinout remove
    * - ``StampTimerPower2.EVENT.BATTERY_INSERT``
      - 0x200
      - battery insert
    * - ``StampTimerPower2.EVENT.BATTERY_REMOVE``
      - 0x400
      - battery remove
    * - ``StampTimerPower2.EVENT.BUTTON_CLICK``
      - 0x800
      - button click
    * - ``StampTimerPower2.EVENT.WAKE``
      - 0x1000
      - wake
    * - ``StampTimerPower2.EVENT.BUTTON_DOUBLE``
      - 0x2000
      - button double
    * - ``StampTimerPower2.EVENT.ALL``
      - 0x3fff
      - all

Methods
~~~~~~~

Methods below are called on the StampTimerPower2 instance. Register transactions may raise OSError; failed communication is reported as False by is_connected(). Setters and action methods return None unless a return value is listed. Inputs are converted and validated by the current implementation; validation errors may be ValueError or TypeError.

.. py:currentmodule:: None

.. method:: add_event_cb(callback, filter, *, user_data=None)

    Register an event listener. The IRQ output and MCU falling-edge input are initialized by the StampTimerPower2 constructor. The driver combines all filters, configures IRQ masks, and automatically switches GPIO event inputs to GPIO input mode without changing their pull settings. The original GPIO configuration is restored after its last listener is removed.

    :param callback: Callback receiving one ``Event`` object.
    :type callback: callable
    :param filter: One or more ORed ``StampTimerPower2.EVENT.*`` flags.
    :type filter: int
    :param user_data: Application data exposed as ``event.user_data``. Default: ``None``. Keyword-only parameter.
    :type user_data: object

    :returns: Registration handle accepted by ``remove_event_cb()``.
    :rtype: int

    :raises TypeError: Invalid argument type.
    :raises ValueError: Invalid argument value.

    Callbacks run in scheduled MicroPython context. Each triggered bit produces one Event with target, code and user_data. code contains one EVENT flag. Calling without an IRQ pair raises RuntimeError; remove callbacks by their returned handle.

    UiFlow2 Code Block:

        |add_event_cb.png|

    MicroPython Code Block:

        .. code-block:: python

            # Requires an stp2 instance configured for INT callbacks.
            def on_event(event):
                print(event.code)

            handle = stp2.add_event_cb(on_event, StampTimerPower2.EVENT.GPIO4_CHANGE)
            # Keep the Basic main loop running; when finished:
            # stp2.remove_event_cb(handle)
            # stp2.deinit()

.. method:: remove_event_cb(handle_or_callback)

    Remove one listener by handle or all registrations using the same callback object.

    :param handle_or_callback: Registration handle or callback object.
    :type handle_or_callback: int / callable

    :returns: Number of registrations removed.
    :rtype: int

    :raises TypeError: Invalid argument type.

    UiFlow2 Code Block:

        |remove_event_cb.png|

    MicroPython Code Block:

        .. code-block:: python

            # handle was returned by add_event_cb().
            removed = stp2.remove_event_cb(handle)

.. method:: deinit()

    Release the host IRQ registration owned by this driver.

    This operation is idempotent. Ordinary register access remains available, and add_event_cb() can recreate the IRQ registration when the pins were configured.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |deinit.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.deinit()

.. method:: wake()

    Wake StampTimerPower2 and wait for communication to recover. The driver sends an empty I2C transaction and ignores a NACK from the first wake attempt.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |wake.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.wake()

.. method:: is_connected()

    Check whether a device responds at the configured I2C address.

    :returns: ``True`` when the device responds, otherwise ``False``.
    :rtype: bool

    UiFlow2 Code Block:

        |is_connected.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.is_connected()
            print(value)

.. method:: get_device_info()

    Read the device information block.

    :returns: ``(device_id, device_model, hardware_version, firmware_version)``.
    :rtype: tuple

    UiFlow2 Code Block:

        |get_device_info.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_device_info()
            print(value)

.. method:: get_uid()

    Read the 12-byte device unique identifier.

    :returns: The 12-byte device UID.
    :rtype: bytes

    UiFlow2 Code Block:

        |get_uid.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_uid()
            print(value)

.. method:: get_device_id()

    Read the device ID.

    :returns: Device ID in the range ``0~255``.
    :rtype: int

    UiFlow2 Code Block:

        |get_device_id.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_device_id()
            print(value)

.. method:: get_device_model()

    Read the device model.

    :returns: Device model in the range ``0~255``.
    :rtype: int

    UiFlow2 Code Block:

        |get_device_model.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_device_model()
            print(value)

.. method:: get_hardware_version()

    Read the hardware version.

    :returns: Hardware version in the range ``0~255``.
    :rtype: int

    UiFlow2 Code Block:

        |get_hardware_version.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_hardware_version()
            print(value)

.. method:: get_firmware_version()

    Read the firmware version.

    :returns: Firmware version in the range ``0~255``.
    :rtype: int

    UiFlow2 Code Block:

        |get_firmware_version.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_firmware_version()
            print(value)

.. method:: Pin(gpio, mode=None, pull=-1, *, value=None)
    :no-index:

    Create a MicroPython Pin-style object backed by StampTimerPower2 GPIO registers.

    :param gpio: StampTimerPower2 GPIO number in the range ``0~4``.
    :type gpio: int
    :param mode: ``Pin.IN``, ``Pin.OUT``, or ``Pin.OPEN_DRAIN``; ``None`` preserves the current mode. Default: ``None``.
    :type mode: int / None
    :param pull: ``Pin.PULL_UP``, ``Pin.PULL_DOWN``, or ``None``; ``-1`` preserves the current setting. Default: ``-1``.
    :type pull: int / None
    :param value: Initial output level; ``None`` leaves the output latch unchanged. Default: ``None``. Keyword-only parameter.
    :type value: int / bool / None

    :returns: Configured StampTimerPower2 GPIO object.
    :rtype: Pin

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |Pin.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin
            pin = stp2.Pin(4)
            # Use the returned object, then release it.
            pin.deinit()

.. method:: ADC(channel)
    :no-index:

    Create a MicroPython ADC-style object for GPIO1 or GPIO2.

    :param channel: ADC channel; only ``1`` (GPIO1) or ``2`` (GPIO2) is supported.
    :type channel: int

    :returns: A new ADC object for the selected input.
    :rtype: ADC

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |ADC.png|

    MicroPython Code Block:

        .. code-block:: python

            adc = stp2.ADC(1)
            # Use the returned object, then release it.
            adc.deinit()

.. method:: PWM(channel, *, freq=None, duty_u16=0, duty_ns=None, invert=False)
    :no-index:

    Create a MicroPython PWM-style object for PWM0 or PWM1.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int
    :param freq: Shared frequency in the range ``1~65535`` Hz; ``None`` preserves it, falling back to 500 Hz when the frequency register is zero. Default: ``None``. Keyword-only parameter.
    :type freq: int / None
    :param duty_u16: Initial duty in the range ``0~65535``. Default: ``0``. Keyword-only parameter.
    :type duty_u16: int
    :param duty_ns: Initial high pulse width in nanoseconds; mutually exclusive with nonzero ``duty_u16``. Default: ``None``. Keyword-only parameter.
    :type duty_ns: int / None
    :param invert: ``True`` selects inverted output polarity. Default: ``False``. Keyword-only parameter.
    :type invert: bool

    :returns: Configured StampTimerPower2 PWM object.
    :rtype: PWM

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |PWM.png|

    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0)
            # Use the returned object, then release it.
            pwm.deinit()

.. method:: NeoPixel(gpio, count, *, bpp=3, timing=1)
    :no-index:

    Create a buffered MicroPython NeoPixel-style object.

    :param gpio: NeoPixel output pin; only StampTimerPower2 GPIO0 is supported.
    :type gpio: int
    :param count: Number of buffered LEDs in the range ``1~32``.
    :type count: int
    :param bpp: Bytes per pixel; only RGB value ``3`` is supported. Default: ``3``. Keyword-only parameter.
    :type bpp: int
    :param timing: NeoPixel protocol timing selector, ``0`` or ``1``; StampTimerPower2 uses fixed hardware timing for both. Default: ``1``. Keyword-only parameter.
    :type timing: int

    :returns: A new buffered NeoPixel object.
    :rtype: NeoPixel

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |NeoPixel.png|

    MicroPython Code Block:

        .. code-block:: python

            pixels = stp2.NeoPixel(0, 1)
            # Use the returned object, then release it.
            pixels.deinit()

.. method:: set_pin_function(gpio, function)

    Set a GPIO function mux.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int
    :param function: GPIO function selected with a ``PIN_FUNCTION_*`` constant.
    :type function: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pin_function.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pin_function(4, StampTimerPower2.PIN_FUNCTION_GPIO)

.. method:: set_pin_mode(gpio, mode)

    Set a GPIO input/output mode.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int
    :param mode: ``GPIO_MODE_IN``, ``GPIO_MODE_OUT``, or ``GPIO_MODE_OPEN_DRAIN``.
    :type mode: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pin_mode.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pin_mode(4, StampTimerPower2.GPIO_MODE_IN)

.. method:: set_pin_pull(gpio, pull)

    Set GPIO pull configuration.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int
    :param pull: ``GPIO_PULL_NONE``, ``GPIO_PULL_UP``, or ``GPIO_PULL_DOWN``.
    :type pull: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pin_pull.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pin_pull(4, StampTimerPower2.GPIO_PULL_UP)

.. method:: set_pin_drive(gpio, drive)

    Set GPIO output drive type.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int
    :param drive: ``DRIVE_PUSH_PULL`` or ``DRIVE_OPEN_DRAIN``.
    :type drive: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pin_drive.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pin_drive(4, StampTimerPower2.DRIVE_PUSH_PULL)

.. method:: set_pin_value(gpio, value)

    Write a GPIO output latch value.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int
    :param value: Output level: ``0``, ``1``, ``False``, or ``True``.
    :type value: int / bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pin_value.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pin_value(4, 1)

.. method:: read_pin(gpio)

    Read a GPIO input value.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int

    :returns: Current input level, ``0`` or ``1``.
    :rtype: int

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |read_pin.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_pin(4)
            print(value)

.. method:: get_power_source()

    Read the active power-source bit mask.

    :returns: ORed ``POWER_SOURCE_*`` flags.
    :rtype: int

    UiFlow2 Code Block:

        |get_power_source.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_power_source()
            print(value)

.. method:: get_power_config()

    Read the power-configuration bit mask.

    :returns: Raw power-configuration bit mask in the range ``0~255``.
    :rtype: int

    UiFlow2 Code Block:

        |get_power_config.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_power_config()
            print(value)

.. method:: is_charging_enabled()

    Return whether battery charging is enabled.

    :returns: ``True`` when the charging-enable bit is set.
    :rtype: bool

    UiFlow2 Code Block:

        |is_charging_enabled.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.is_charging_enabled()
            print(value)

.. method:: is_dcdc_enabled()

    Return whether the DCDC power rail is enabled.

    :returns: ``True`` when the DCDC rail is enabled.
    :rtype: bool

    UiFlow2 Code Block:

        |is_dcdc_enabled.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.is_dcdc_enabled()
            print(value)

.. method:: is_ldo_enabled()

    Return whether the LDO power rail is enabled.

    :returns: ``True`` when the LDO rail is enabled.
    :rtype: bool

    UiFlow2 Code Block:

        |is_ldo_enabled.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.is_ldo_enabled()
            print(value)

.. method:: is_boost_enabled()

    Return whether the BOOST / 5VINOUT power rail is enabled.

    :returns: ``True`` when the BOOST / 5VINOUT rail is enabled.
    :rtype: bool

    UiFlow2 Code Block:

        |is_boost_enabled.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.is_boost_enabled()
            print(value)

.. method:: enable_charging()

    Enable battery charging.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_charging.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_charging()

.. method:: disable_charging()

    Disable battery charging.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_charging.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_charging()

.. method:: enable_dcdc()

    Enable the DCDC power rail.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_dcdc.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_dcdc()

.. method:: disable_dcdc()

    Disable the DCDC power rail.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_dcdc.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.disable_dcdc()

.. method:: enable_ldo()

    Enable the LDO power rail.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_ldo.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_ldo()

.. method:: disable_ldo()

    Disable the LDO power rail.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_ldo.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.disable_ldo()

.. method:: enable_boost()

    Enable the BOOST / 5VINOUT power rail.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_boost.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_boost()

.. method:: disable_boost()

    Disable the BOOST / 5VINOUT power rail.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_boost.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.disable_boost()

.. method:: set_led_enable_level(level)

    Set the LED_EN default output level bit.

    :param level: Default LED_EN output level: ``0``/``False`` for low, ``1``/``True`` for high.
    :type level: int / bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_led_enable_level.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_led_enable_level(True)

.. method:: set_battery_low_voltage_threshold_mv(voltage_mv)

    Set the battery low-voltage protection threshold.

    :param voltage_mv: Low-voltage threshold in millivolts; one of ``3000``, ``3100``, ``3200``, or ``3300``.
    :type voltage_mv: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_battery_low_voltage_threshold_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_battery_low_voltage_threshold_mv(3000)

.. method:: get_battery_low_voltage_threshold_mv()

    Read the configured battery low-voltage threshold.

    :returns: Configured threshold in millivolts: ``3000``, ``3100``, ``3200``, or ``3300``.
    :rtype: int

    UiFlow2 Code Block:

        |get_battery_low_voltage_threshold_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_battery_low_voltage_threshold_mv()
            print(value)

.. method:: enable_gpio_power_hold(gpio)

    Enable power-hold behavior for one GPIO output.

    :param gpio: GPIO output index in the range ``0~4``.
    :type gpio: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_gpio_power_hold.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_gpio_power_hold(4)

.. method:: disable_gpio_power_hold(gpio)

    Disable power-hold behavior for one GPIO output.

    :param gpio: GPIO output index in the range ``0~4``.
    :type gpio: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_gpio_power_hold.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_gpio_power_hold(4)

.. method:: enable_ldo_power_hold()

    Enable LDO power hold.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_ldo_power_hold.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_ldo_power_hold()

.. method:: disable_ldo_power_hold()

    Disable LDO power hold.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_ldo_power_hold.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_ldo_power_hold()

.. method:: enable_boost_power_hold()

    Enable BOOST / 5VINOUT power hold.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_boost_power_hold.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_boost_power_hold()

.. method:: disable_boost_power_hold()

    Disable BOOST / 5VINOUT power hold.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_boost_power_hold.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_boost_power_hold()

.. method:: read_adc_raw(channel)

    Read a raw ADC conversion value.

    :param channel: ADC channel; use ``1``, ``2``, or internal temperature channel ``6``.
    :type channel: int

    :returns: Native 12-bit ADC code in the range ``0~4095``.
    :rtype: int

    :raises ValueError: Invalid argument value.
    :raises OSError: Operation failed.

    UiFlow2 Code Block:

        |read_adc_raw.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_adc_raw(1)
            print(value)

.. method:: read_adc_mv(channel)

    Read an external ADC channel in millivolts.

    :param channel: External ADC channel; only ``1`` (GPIO1) or ``2`` (GPIO2) is supported.
    :type channel: int

    :returns: External ADC input voltage in millivolts.
    :rtype: int

    :raises ValueError: Invalid argument value.
    :raises OSError: Operation failed.

    UiFlow2 Code Block:

        |read_adc_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_adc_mv(1)
            print(value)

.. method:: read_temperature_raw()

    Read the internal temperature sensor raw code.

    :returns: Internal temperature-channel code in the range ``0~4095``.
    :rtype: int

    :raises OSError: Operation failed.

    UiFlow2 Code Block:

        |read_temperature_raw.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_temperature_raw()
            print(value)

.. method:: read_button()

    Read the current PM1 button state.

    :returns: Current button level: ``0`` when released or ``1`` when pressed.
    :rtype: int

    UiFlow2 Code Block:

        |read_button.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_button()
            print(value)

.. method:: read_button_event()

    Read the sticky button-pressed flag.

    :returns: ``True`` when the sticky pressed flag was set; reading clears the hardware flag.
    :rtype: bool

    UiFlow2 Code Block:

        |read_button_event.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_button_event()
            print(value)

.. method:: set_button_timing(event, duration_ms)

    Configure button timing.

    :param event: ``BUTTON_TIMING_CLICK``, ``BUTTON_TIMING_DOUBLE``, or ``BUTTON_TIMING_LONG``.
    :type event: int
    :param duration_ms: Button timing in milliseconds: click/double-click accepts 125, 250, 500 or 1000; long press accepts 1000, 2000, 3000 or 4000.
    :type duration_ms: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_button_timing.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_button_timing(StampTimerPower2.BUTTON_TIMING_CLICK, 250)

.. method:: read_reference_voltage_mv()

    Read the PM1 reference voltage.

    :returns: Current reference voltage in millivolts.
    :rtype: int

    UiFlow2 Code Block:

        |read_reference_voltage_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_reference_voltage_mv()
            print(value)

.. method:: read_battery_voltage_mv()

    Read the battery voltage.

    :returns: Battery voltage in millivolts.
    :rtype: int

    UiFlow2 Code Block:

        |read_battery_voltage_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_battery_voltage_mv()
            print(value)

.. method:: read_vin_voltage_mv()

    Read the voltage at the external module 5VIN input.

    :returns: 5VIN voltage in millivolts.
    :rtype: int

    UiFlow2 Code Block:

        |read_vin_voltage_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_vin_voltage_mv()
            print(value)

.. method:: read_5v_inout_voltage_mv()

    Read the voltage at the external module 5VINOUT port.

    :returns: 5VINOUT voltage in millivolts.
    :rtype: int

    UiFlow2 Code Block:

        |read_5v_inout_voltage_mv.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_5v_inout_voltage_mv()
            print(value)

.. method:: get_wake_source(*, clear=False)

    Read wake-source flags.

    :param clear: Clear the wake-source flags returned by this read. Default: ``False``. Keyword-only parameter.
    :type clear: bool

    :returns: Wake-source bit mask.
    :rtype: int

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |get_wake_source.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_wake_source()
            print(value)

.. method:: clear_wake_source(mask=None)

    Clear wake-source flags.

    :param mask: Wake-source bits to clear; ``None`` clears every valid wake-source bit. Default: ``None``.
    :type mask: int / None

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |clear_wake_source.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.clear_wake_source()

.. method:: set_pwm_frequency(frequency)

    Set the shared PWM frequency.

    :param frequency: Shared PWM frequency in the range ``1~65535`` Hz.
    :type frequency: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pwm_frequency.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pwm_frequency(1000)

.. method:: get_pwm_frequency()

    Read the shared PWM frequency.

    :returns: Shared PWM frequency in hertz.
    :rtype: int

    UiFlow2 Code Block:

        |get_pwm_frequency.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_pwm_frequency()
            print(value)

.. method:: set_pwm_duty_percent(channel, percent, *, invert=False)

    Set a PWM channel duty by percent.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int
    :param percent: Duty cycle in percent. Range: ``0~100``.
    :type percent: int
    :param invert: ``True`` selects inverted output polarity. Default: ``False``. Keyword-only parameter.
    :type invert: bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pwm_duty_percent.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pwm_duty_percent(0, 50)

.. method:: set_pwm_duty_u12(channel, duty_u12, *, invert=False)

    Set a PWM channel duty by 12-bit code.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int
    :param duty_u12: Unsigned 12-bit duty code. Range: ``0~4095``.
    :type duty_u12: int
    :param invert: ``True`` selects inverted output polarity. Default: ``False``. Keyword-only parameter.
    :type invert: bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pwm_duty_u12.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pwm_duty_u12(0, 2048)

.. method:: enable_pwm(channel)

    Enable a PWM output channel.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_pwm.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_pwm(0)

.. method:: disable_pwm(channel)

    Disable a PWM output channel.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_pwm.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_pwm(0)

.. method:: get_pwm_duty_percent(channel)

    Read a PWM channel duty by percent.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int

    :returns: Duty percentage in the range ``0~100``.
    :rtype: int

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |get_pwm_duty_percent.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_pwm_duty_percent(0)
            print(value)

.. method:: get_pwm_duty_u12(channel)

    Read a PWM channel duty by 12-bit code.

    :param channel: PWM channel; only ``0`` (GPIO3) or ``1`` (GPIO4) is supported.
    :type channel: int

    :returns: 12-bit duty value in the range ``0~4095``.
    :rtype: int

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |get_pwm_duty_u12.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_pwm_duty_u12(0)
            print(value)

.. method:: set_neopixel_count(count)

    Set the active NeoPixel LED count.

    :param count: Active LED count in the range ``0~32``; ``0`` disables output.
    :type count: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_neopixel_count.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_neopixel_count(1)

.. method:: set_neopixel_color(index, color)

    Write one RGB888 color into LED RAM.

    :param index: LED RAM index in the range ``0~31``.
    :type index: int
    :param color: ``0xRRGGBB`` or ``(r, g, b)`` with each component in ``0~255``.
    :type color: int / tuple

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_neopixel_color.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_neopixel_color(0, (32, 0, 0))

.. method:: write_neopixels(colors, *, auto_refresh=True)

    Write multiple RGB888 colors into LED RAM.

    :param colors: Up to 32 RGB colors in integer or tuple form.
    :type colors: iterable
    :param auto_refresh: Refresh the LED output after writing. Default: ``True``. Keyword-only parameter.
    :type auto_refresh: bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |write_neopixels.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.write_neopixels([(32, 0, 0)])

.. method:: refresh_neopixels()

    Refresh NeoPixel output from LED RAM.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |refresh_neopixels.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.refresh_neopixels()

.. method:: clear_neopixels(*, auto_refresh=True)

    Clear LED RAM to black.

    :param auto_refresh: Refresh the LED output after clearing. Default: ``True``. Keyword-only parameter.
    :type auto_refresh: bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |clear_neopixels.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.clear_neopixels()

.. method:: enable_neopixels()

    Enable NeoPixel output without changing LED RAM. After disable_neopixels(), the remembered count is cleared; enabling starts with one LED. Call set_neopixel_count() to select another count.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_neopixels.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_neopixels()

.. method:: disable_neopixels()

    Disable NeoPixel output without clearing LED RAM.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_neopixels.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_neopixels()

.. method:: set_aw8737a_pulse(gpio, pulses, *, refresh=True)

    Configure AW8737A pulse output.

    :param gpio: AW8737A mode-control GPIO in the range ``0~4``.
    :type gpio: int
    :param pulses: Pulse count in the range ``0~255``.
    :type pulses: int
    :param refresh: Execute the configured pulse output immediately. Default: ``True``. Keyword-only parameter.
    :type refresh: bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_aw8737a_pulse.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_aw8737a_pulse(4, 1)

.. method:: refresh_aw8737a()

    Execute the last configured AW8737A pulse output.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |refresh_aw8737a.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.refresh_aw8737a()

.. method:: set_aw8737a_mode(gpio, mode, *, refresh=True)

    Set AW8737A gain mode.

    :param gpio: AW8737A mode-control GPIO in the range ``0~4``.
    :type gpio: int
    :param mode: Gain mode in the range ``0~3``, mapped directly to the pulse count.
    :type mode: int
    :param refresh: Execute the configured pulse output immediately. Default: ``True``. Keyword-only parameter.
    :type refresh: bool

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_aw8737a_mode.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_aw8737a_mode(4, 1)

.. method:: get_irq_status(group, *, clear=False)

    Read an IRQ status group.

    :param group: IRQ group constant or corresponding string.
    :type group: int / str
    :param clear: Clear the flags returned by this read. Default: ``False``. Keyword-only parameter.
    :type clear: bool

    :returns: Status bit mask for the selected IRQ group.
    :rtype: int

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |get_irq_status.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_irq_status(StampTimerPower2.IRQ_GROUP_GPIO)
            print(value)

.. method:: clear_irq(group, mask=None)

    Clear IRQ status bits.

    :param group: IRQ group constant or corresponding string.
    :type group: int / str
    :param mask: Group-local status bits to clear; ``None`` clears every valid bit in the group. Default: ``None``.
    :type mask: int / None

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |clear_irq.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.clear_irq(StampTimerPower2.IRQ_GROUP_GPIO)

.. method:: disable_irq_events(group, events)

    Mask IRQ bits.

    :param group: IRQ group constant or corresponding string.
    :type group: int / str
    :param events: Group-local event bit mask to disable.
    :type events: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_irq_events.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_irq_events(StampTimerPower2.IRQ_GROUP_GPIO, 0x10)

.. method:: enable_irq_events(group, events)

    Unmask IRQ bits.

    :param group: IRQ group constant or corresponding string.
    :type group: int / str
    :param events: Group-local event bit mask to enable.
    :type events: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_irq_events.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_irq_events(StampTimerPower2.IRQ_GROUP_GPIO, 0x10)

.. method:: enable_pin_wakeup(gpio)

    Enable GPIO wakeup.

    :param gpio: Wake GPIO in the range ``0~4``; GPIO1 does not support wakeup.
    :type gpio: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_pin_wakeup.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_pin_wakeup(4)

.. method:: disable_pin_wakeup(gpio)

    Disable GPIO wakeup.

    :param gpio: GPIO index in the range ``0~4``.
    :type gpio: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_pin_wakeup.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_pin_wakeup(4)

.. method:: set_pin_wakeup_edge(gpio, edge)

    Set GPIO wakeup edge.

    :param gpio: Wake GPIO in the range ``0~4``; GPIO1 does not support wakeup.
    :type gpio: int
    :param edge: ``WAKE_EDGE_FALLING`` or ``WAKE_EDGE_RISING``.
    :type edge: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_pin_wakeup_edge.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_pin_wakeup_edge(4, StampTimerPower2.WAKE_EDGE_FALLING)

.. method:: enable_watchdog(timeout_s)

    Set watchdog timeout.

    :param timeout_s: Watchdog timeout in the range ``1~255`` seconds.
    :type timeout_s: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_watchdog.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.enable_watchdog(10)

.. method:: disable_watchdog()

    Disable the watchdog.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_watchdog.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_watchdog()

.. method:: feed_watchdog()

    Feed the watchdog.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |feed_watchdog.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.feed_watchdog()

.. method:: get_watchdog_countdown_s()

    Read the watchdog countdown.

    :returns: Remaining watchdog time in seconds.
    :rtype: int

    UiFlow2 Code Block:

        |get_watchdog_countdown_s.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_watchdog_countdown_s()
            print(value)

.. method:: set_timer(duration_s, action)

    Set the PM1 timer and timeout action.

    :param duration_s: Timer duration in seconds, range ``0~2147483647``.
    :type duration_s: int
    :param action: Timer action selected with a ``TIMER_ACTION_*`` constant.
    :type action: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_timer.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_timer(5, StampTimerPower2.TIMER_ACTION_FLAG)

.. method:: clear_timer()

    Stop and clear the PM1 timer.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |clear_timer.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.clear_timer()

.. method:: set_i2c_sleep_timeout_s(timeout_s)

    Set PM1 I2C idle sleep timeout.

    :param timeout_s: Idle sleep timeout in seconds, range ``0~15``.
    :type timeout_s: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_i2c_sleep_timeout_s.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_i2c_sleep_timeout_s(10)

.. method:: get_i2c_sleep_timeout_s()

    Read PM1 I2C idle sleep timeout.

    :returns: Idle-sleep timeout in the range ``0~15`` seconds.
    :rtype: int

    UiFlow2 Code Block:

        |get_i2c_sleep_timeout_s.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_i2c_sleep_timeout_s()
            print(value)

.. method:: set_i2c_frequency(frequency)

    Set PM1 device-side I2C speed mode.

    :param frequency: I2C frequency; only ``100000`` or ``400000`` Hz is supported.
    :type frequency: int

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |set_i2c_frequency.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.set_i2c_frequency(100000)

.. method:: get_i2c_frequency()

    Read the PM1 device-side I2C speed mode.

    :returns: I2C frequency, either ``100000`` or ``400000`` Hz.
    :rtype: int

    UiFlow2 Code Block:

        |get_i2c_frequency.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.get_i2c_frequency()
            print(value)

.. method:: read_rtc_ram(offset=0, length=32)

    Read a region of the 32-byte RTC retention RAM. Retention depends on the module power conditions; this is not flash storage.

    :param offset: Byte offset in the range 0~31; offset + length must not exceed 32. Default: ``0``.
    :type offset: int
    :param length: Number of bytes to read; ``offset + length`` must not exceed ``32``. Default: ``32``.
    :type length: int

    :returns: Requested RTC RAM byte sequence.
    :rtype: bytes

    :raises ValueError: Invalid argument value.

    UiFlow2 Code Block:

        |read_rtc_ram.png|

    MicroPython Code Block:

        .. code-block:: python

            value = stp2.read_rtc_ram()
            print(value)

.. method:: write_rtc_ram(offset, data)

    Write a region of the 32-byte RTC retention RAM. Retention depends on the module power conditions.

    :param offset: Byte offset in the range 0~31; offset + len(data) must not exceed 32.
    :type offset: int
    :param data: Bytes to write; ``offset + len(data)`` must not exceed ``32``.
    :type data: buffer / iterable

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |write_rtc_ram.png|

    MicroPython Code Block:

        .. code-block:: python

            original = stp2.read_rtc_ram(24, 2)
            try:
                stp2.write_rtc_ram(24, bytes([0x55, 0xAA]))
            finally:
                stp2.write_rtc_ram(24, original)

.. method:: restore_defaults()

    Restore writable StampTimerPower2 configuration to the documented defaults, including power, GPIO, wake, ADC, PWM, timer, IRQ, button, NeoPixel, and AW8737A settings, and clear sticky wake and IRQ status. Event callbacks are removed. Device information, UID, and the 32-byte RTC RAM are preserved, and the chip is not rebooted.

    The StampTimerPower2 I2C speed returns to 100 kHz. Configure the host I2C bus for the same speed before subsequent access. Existing ``Pin``, ``ADC``, ``PWM``, and ``NeoPixel`` objects must be reinitialized before reuse.

    **Exceptions**

    ``OSError`` is raised on I2C failure; configuration may then be only partially restored.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |restore_defaults.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.restore_defaults()

.. method:: power_off()

    Send a power-off command to the external StampTimerPower2. Basic remains powered by its own USB or battery supply.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |power_off.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.power_off()

.. method:: reboot()

    Reboot the external StampTimerPower2. Basic continues running; wait for the module to recover before further I2C access.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |reboot.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.reboot()

.. method:: enter_download_mode()

    Request PM1 download mode.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enter_download_mode.png|

    MicroPython Code Block:

        .. code-block:: python

            # Manual power test only; affects the external STP2.
            stp2.enter_download_mode()

.. method:: enable_download_lock()

    Enable the PM1 download-mode lock.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_download_lock.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_download_lock()

.. method:: disable_download_lock()

    Disable the PM1 download-mode lock.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_download_lock.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_download_lock()

.. method:: enable_single_click_reset()

    Enable single-click reset behavior.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_single_click_reset.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_single_click_reset()

.. method:: disable_single_click_reset()

    Disable single-click reset behavior.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_single_click_reset.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_single_click_reset()

.. method:: enable_double_click_power_off()

    Enable double-click poweroff behavior.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |enable_double_click_power_off.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.enable_double_click_power_off()

.. method:: disable_double_click_power_off()

    Disable double-click poweroff behavior.

    :returns: No return value.
    :rtype: None

    UiFlow2 Code Block:

        |disable_double_click_power_off.png|

    MicroPython Code Block:

        .. code-block:: python

            stp2.disable_double_click_power_off()

Pin object methods
^^^^^^^^^^^^^^^^^^

Create this helper through ``stp2.Pin()``. The following methods belong to the returned object, not the StampTimerPower2 instance.

.. method:: init(mode=None, pull=-1, *, value=None)
    :no-index:

    Initialize or reconfigure the GPIO pin.

    :param mode: ``Pin.IN``, ``Pin.OUT``, or ``Pin.OPEN_DRAIN``; ``None`` preserves the current mode. Default: ``None``.
    :type mode: int / None
    :param pull: ``Pin.PULL_UP``, ``Pin.PULL_DOWN``, or ``None``; ``-1`` preserves the current setting. Default: ``-1``.
    :type pull: int / None
    :param value: Initial output level; ``None`` leaves the output latch unchanged. Default: ``None``. Keyword-only parameter.
    :type value: int / bool / None

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin
            pin = stp2.Pin(4, Pin.IN, pull=Pin.PULL_UP)
            try:
                pin.init()
            finally:
                pin.deinit()

.. method:: deinit()
    :no-index:

    Restore a floating GPIO input and deactivate this object.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin
            pin = stp2.Pin(4, Pin.IN, pull=Pin.PULL_UP)
            try:
                pin.deinit()
            finally:
                pin.deinit()

.. method:: value(value=None)
    :no-index:

    Read or write the GPIO value.

    :param value: Output level; ``None`` reads, while ``0``, ``1``, ``False``, or ``True`` writes. Default: ``None``.
    :type value: int / bool / None

    :returns: ``0`` or ``1`` when reading; ``None`` when writing.
    :rtype: int / None

    :raises RuntimeError: The object is not in a valid state.
    :raises ValueError: Invalid argument value.


    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin
            pin = stp2.Pin(4, Pin.IN, pull=Pin.PULL_UP)
            try:
                value = pin.value()
                print(value)
            finally:
                pin.deinit()

.. method:: on()
    :no-index:

    Set the GPIO output high.

    :raises RuntimeError: The object is not in a valid state.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin
            pin = stp2.Pin(3, Pin.OUT, value=0)
            try:
                pin.on()
            finally:
                pin.deinit()

.. method:: off()
    :no-index:

    Set the GPIO output low.

    :raises RuntimeError: The object is not in a valid state.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            from hardware import Pin
            pin = stp2.Pin(3, Pin.OUT, value=0)
            try:
                pin.off()
            finally:
                pin.deinit()

``pin()`` reads the level and ``pin(value)`` writes it, as aliases for value(). Use ``hardware.Pin.IN``, ``OUT``, ``OPEN_DRAIN``, ``PULL_UP`` and ``PULL_DOWN`` for the helper arguments.

ADC object methods
^^^^^^^^^^^^^^^^^^

Create this helper through ``stp2.ADC()``. The following methods belong to the returned object, not the StampTimerPower2 instance.

.. method:: init()
    :no-index:

    Initialize or reinitialize the ADC input.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            adc = stp2.ADC(1)
            try:
                adc.init()
            finally:
                adc.deinit()

.. method:: deinit()
    :no-index:

    Release the ADC function and restore a floating GPIO input.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            adc = stp2.ADC(1)
            try:
                adc.deinit()
            finally:
                adc.deinit()

.. method:: read()
    :no-index:

    Read the native 12-bit ADC code.

    :returns: Native 12-bit ADC code in the range ``0~4095``.
    :rtype: int

    :raises RuntimeError: The object is not in a valid state.
    :raises OSError: Operation failed.


    MicroPython Code Block:

        .. code-block:: python

            adc = stp2.ADC(1)
            try:
                value = adc.read()
                print(value)
            finally:
                adc.deinit()

.. method:: read_u16()
    :no-index:

    Read a full-scale normalized unsigned 16-bit value.

    :returns: Full-scale normalized value in the range ``0~65535``.
    :rtype: int

    :raises RuntimeError: The object is not in a valid state.
    :raises OSError: Operation failed.


    MicroPython Code Block:

        .. code-block:: python

            adc = stp2.ADC(1)
            try:
                value = adc.read_u16()
                print(value)
            finally:
                adc.deinit()

.. method:: read_uv()
    :no-index:

    Read the ADC input voltage in microvolts.

    :returns: ADC input voltage in microvolts.
    :rtype: int

    :raises RuntimeError: The object is not in a valid state.
    :raises OSError: Operation failed.


    MicroPython Code Block:

        .. code-block:: python

            adc = stp2.ADC(1)
            try:
                value = adc.read_uv()
                print(value)
            finally:
                adc.deinit()

PWM object methods
^^^^^^^^^^^^^^^^^^

Create this helper through ``stp2.PWM()``. The following methods belong to the returned object, not the StampTimerPower2 instance.

.. method:: init(*, freq=None, duty_u16=None, duty_ns=None, invert=None)
    :no-index:

    Initialize or reconfigure the PWM output.

    :param freq: Shared frequency in the range ``1~65535`` Hz; ``None`` preserves it, falling back to 500 Hz when the frequency register is zero. Default: ``None``. Keyword-only parameter.
    :type freq: int / None
    :param duty_u16: Duty in the range ``0~65535``; ``None`` preserves it. Default: ``None``. Keyword-only parameter.
    :type duty_u16: int / None
    :param duty_ns: High pulse width in nanoseconds; mutually exclusive with ``duty_u16``. Default: ``None``. Keyword-only parameter.
    :type duty_ns: int / None
    :param invert: Output polarity; ``None`` preserves it. Default: ``None``. Keyword-only parameter.
    :type invert: bool / None

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
            try:
                pwm.init()
            finally:
                pwm.deinit()

.. method:: deinit()
    :no-index:

    Disable PWM and restore its fixed pin as a floating input.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
            try:
                pwm.deinit()
            finally:
                pwm.deinit()

.. method:: freq(value=None)
    :no-index:

    Read or set the shared PWM frequency.

    :param value: Shared frequency in the range ``1~65535`` Hz; ``None`` reads it. Default: ``None``.
    :type value: int / None

    :returns: Frequency in hertz when reading; ``None`` when setting.
    :rtype: int / None

    :raises RuntimeError: The object is not in a valid state.
    :raises ValueError: Invalid argument value.


    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
            try:
                value = pwm.freq()
                print(value)
            finally:
                pwm.deinit()

.. method:: duty_u16(value=None)
    :no-index:

    Read or set duty using the MicroPython unsigned 16-bit scale.

    :param value: Duty in the range ``0~65535``; ``None`` reads it. Default: ``None``.
    :type value: int / None

    :returns: Duty in the range ``0~65535`` when reading; ``None`` when setting.
    :rtype: int / None

    :raises RuntimeError: The object is not in a valid state.
    :raises ValueError: Invalid argument value.


    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
            try:
                value = pwm.duty_u16()
                print(value)
            finally:
                pwm.deinit()

.. method:: duty_ns(value=None)
    :no-index:

    Read or set PWM pulse width in nanoseconds.

    :param value: High pulse width in nanoseconds; ``None`` reads it. The value cannot exceed the current PWM period. Default: ``None``.
    :type value: int / None

    :returns: High pulse width in nanoseconds when reading; ``None`` when setting.
    :rtype: int / None

    :raises RuntimeError: The object is not in a valid state.
    :raises ValueError: Invalid argument value.


    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
            try:
                value = pwm.duty_ns()
                print(value)
            finally:
                pwm.deinit()

.. method:: invert(value=None)
    :no-index:

    Read or set output invert.

    :param value: ``True`` selects inverted polarity, ``False`` selects normal polarity, and ``None`` reads it. Default: ``None``.
    :type value: bool / None

    :returns: Invert state when reading; ``None`` when setting.
    :rtype: bool / None

    :raises ValueError: Invalid argument value.
    :raises RuntimeError: The object is not in a valid state.


    MicroPython Code Block:

        .. code-block:: python

            pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
            try:
                value = pwm.invert()
                print(value)
            finally:
                pwm.deinit()

Use duty_u16() or duty_ns(); this implementation does not provide duty(). Frequency is shared between both channels.

NeoPixel object methods
^^^^^^^^^^^^^^^^^^^^^^^

Create this helper through ``stp2.NeoPixel()``. The following methods belong to the returned object, not the StampTimerPower2 instance.

.. method:: init()
    :no-index:

    Initialize or reinitialize the fixed GPIO0 NeoPixel output.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            pixels = stp2.NeoPixel(0, 1)
            try:
                pixels.init()
            finally:
                pixels.deinit()

.. method:: deinit()
    :no-index:

    Clear LEDs, disable output, and restore GPIO0 as an input.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            pixels = stp2.NeoPixel(0, 1)
            try:
                pixels.deinit()
            finally:
                pixels.deinit()

.. method:: fill(color)
    :no-index:

    Fill the local buffer without writing the LEDs.

    :param color: ``0xRRGGBB`` or ``(r, g, b)`` with each component in ``0~255``.
    :type color: int / tuple

    :raises ValueError: Invalid argument value.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            pixels = stp2.NeoPixel(0, 1)
            try:
                pixels.fill((32, 0, 0))
                pixels.write()
            finally:
                pixels.deinit()

.. method:: write()
    :no-index:

    Convert the RGB buffer to RGB565 and refresh the LED output.

    :raises RuntimeError: The object is not in a valid state.

    :returns: No return value.
    :rtype: None


    MicroPython Code Block:

        .. code-block:: python

            pixels = stp2.NeoPixel(0, 1)
            try:
                pixels.fill((32, 0, 0))
                pixels.write()
            finally:
                pixels.deinit()

``len(pixels)`` returns the LED count. ``pixels[index]`` reads or writes an RGB tuple in the local buffer; call write() to display changes. Indices range from 0 to count-1, and RGB components from 0 to 255.
