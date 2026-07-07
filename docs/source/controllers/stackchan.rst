#########
StackChan
#########

.. include:: ../refs/controllers.stackchan.ref

Support the following products:

    |StackChan|

UiFlow2 Example 
---------------

Servo zero calibration
^^^^^^^^^^^^^^^^^^^^^^

.. NOTE::
   Mechanical assembly varies between units. After flashing new firmware, calibrate the servo zero reference manually.

Open the |stackchan_servo_zero_calibrate.m5f2| project in UiFlow2.

#. Run the program.
#. Move the head by hand: on **X**, align the display with the base orientation; on **Y**, set the display perpendicular to the base.
#. Tap **Save** button.

UiFlow2 Code Block:

    |stackchan_servo_zero_calibrate.png|

Example output:

    None

Servo angle read
^^^^^^^^^^^^^^^^

Open the |stackchan_servo_read_example.m5f2| project in UiFlow2.

This example demonstrates reading X and Y servo angles in degrees with torque disabled so the head can move freely.

.. NOTE::
   **Torque on** holds the last target and resists moving by hand. **Torque off** lets you pose the head freely while readings update—handy for checking calibration.

UiFlow2 Code Block:

    |stackchan_servo_read_example.png|

Example output:

    None

Servo control
^^^^^^^^^^^^^

Open the |stackchan_servo_control_example.m5f2| project in UiFlow2.

This example demonstrates moving the servos to commanded positions and driving the X servo in PWM mode using ``set_servo_angle`` and ``set_servo_x_pwm``.

UiFlow2 Code Block:

    |stackchan_servo_control_example.png|

Example output:

    None

Face tracking
^^^^^^^^^^^^^

Open the |stackchan_face_tracking_example.m5f2| project in UiFlow2.

This demo implements face tracking.

UiFlow2 Code Block:

    |stackchan_face_tracking_example.png|

Example output:

    None

Servo power info
^^^^^^^^^^^^^^^^

Open the |stackchan_servo_power_example.m5f2| project in UiFlow2.

This example demonstrates read and display servo power information.

UiFlow2 Code Block:

    |stackchan_servo_power_example.png|

Example output:

    None

Touch & RGB
^^^^^^^^^^^

Open the |stackchan_tp_rgb_example.m5f2| project in UiFlow2.

This example demonstrates mapping touch zones to RGB strip colours (three logical touch points on two strips).

UiFlow2 Code Block:

    |stackchan_tp_rgb_example.png|

Example output:

    None

NFC
^^^

Open the |stackchan_nfc_detect_example.m5f2| project in UiFlow2.

This example demonstrates detecting NFC tags and displaying UID and tag type on screen.
For the full **NFC Unit** API reference (``detect``, read/write, tag types, etc.), see `NFC Unit <../unit/nfc.html>`__.

UiFlow2 Code Block:

    |stackchan_nfc_detect_example.png|

Example output:

    None

Infrared (IR)
^^^^^^^^^^^^^

Open the |stackchan_ir_tx_rx_example.m5f2| project in UiFlow2.

This example demonstrates infrared transmit and receive in NEC style.

UiFlow2 Code Block:

    |stackchan_ir_tx_rx_example.png|

Example output:

    None

MicroPython Example 
-------------------

Servo zero calibration
^^^^^^^^^^^^^^^^^^^^^^

.. NOTE::
   Mechanical assembly varies between units. After flashing new firmware, calibrate the servo zero reference manually.

#. Run the program.
#. Move the head by hand: on **X**, align the display with the base orientation; on **Y**, set the display perpendicular to the base.
#. Tap **Save** button.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_servo_zero_calibrate.py
        :language: python
        :linenos:

Example output:

    None

Servo angle read
^^^^^^^^^^^^^^^^

This example demonstrates reading X and Y servo angles in degrees with torque disabled so the head can move freely.

.. NOTE::
   **Torque on** holds the last target and resists moving by hand. **Torque off** lets you pose the head freely while readings update—handy for checking calibration.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_servo_read_example.py
        :language: python
        :linenos:

Example output:

    None

Servo control
^^^^^^^^^^^^^

This example demonstrates moving the servos to commanded positions and driving the X servo in PWM mode using ``set_servo_angle`` and ``set_servo_x_pwm``.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_servo_control_example.py
        :language: python
        :linenos:

Example output:

    None

Face tracking
^^^^^^^^^^^^^

This example implements face tracking.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_face_tracking_example.py
        :language: python
        :linenos:

Example output:

    None

Servo power info
^^^^^^^^^^^^^^^^

This example demonstrates read and display servo power information.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_servo_power_example.py
        :language: python
        :linenos:

Example output:

    None

Touch & RGB
^^^^^^^^^^^

This example demonstrates mapping touch zones to RGB strip colours (three logical touch points on two strips).

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_tp_rgb_example.py
        :language: python
        :linenos:

Example output:

    None

NFC
^^^

This example demonstrates detecting NFC tags and displaying UID and tag type on screen.
For the full **NFC Unit** API reference (``detect``, read/write, tag types, etc.), see `NFC Unit <../unit/nfc.html>`__.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_nfc_detect_example.py
        :language: python
        :linenos:

Example output:

    None

Infrared (IR)
^^^^^^^^^^^^^

This example demonstrates infrared transmit and receive in NEC style.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/controllers/stackchan/stackchan_ir_tx_rx_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

StackChan
^^^^^^^^^

.. class:: hardware.stackchan.StackChan

    StackChan board driver: SCS serial servos on UART, RGB and servo power on M5IOE1, Si12T touch, INA226 (battery bus), and onboard NFC (``ST25R3916``) as :class:`unit.nfc.NFCUnit`.

    The class is a **singleton**; always construct with the same ``i2c`` and ``uart`` ids.

    :param int i2c: ``I2C`` peripheral id.
    :param int uart: ``UART`` id for the 1 Mbaud servo bus.

    After init, the instance exposes ``nfc`` (a :class:`unit.nfc.NFCUnit`—see `NFC Unit <../unit/nfc.html>`__ for the complete API), ``touch``, ``i2c``, and low-level ``servo`` (``Scscl`` instance) for advanced use.

    Module constants include ``SERVO_ID_X`` (``1``), ``SERVO_ID_Y`` (``2``) and related limits—also available as class attributes on ``StackChan``.

    UiFlow2 Code Block:

        |stackchan_api_init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware.stackchan import StackChan, SERVO_ID_X, SERVO_ID_Y

            sc = StackChan(i2c=1, uart=1)

    .. method:: set_servo_zero()

        Save logical **zero** for both axes into NVS (namespace ``servo``, keys ``zero_pos_1`` / ``zero_pos_2``).

        UiFlow2 Code Block:

            |stackchan_api_set_servo_zero.png|

        MicroPython Code Block:

            .. code-block:: python

                sc.set_servo_zero()

    .. method:: set_servo_power(enable=True, settle_ms=None)

        Enable or disable servo rail power via the IO expander.

        :param bool enable: Power on or off.
        :param int settle_ms: Optional power-on wait time in milliseconds. If omitted,
            the default is 500 ms.

        UiFlow2 Code Block:

            |stackchan_api_set_servo_power.png|

        MicroPython Code Block:

            .. code-block:: python

                sc.set_servo_power(True)

    .. method:: set_servo_torque(servo_id, enable=True)

        Enable or disable torque on one servo.

        :param int servo_id: ``SERVO_ID_X`` or ``SERVO_ID_Y``.
        :param bool enable: Torque on or off.

        UiFlow2 Code Block:

            |stackchan_api_set_servo_torque.png|

        MicroPython Code Block:

            .. code-block:: python

                sc.set_servo_torque(SERVO_ID_X, True)

    .. method:: set_servo_angle(servo_id, angle_deg, time_ms=10, speed=0)

        Move the given servo to ``angle_deg`` (degrees). Use about **-135°~135°** for the X axis (``SERVO_ID_X`` / pan) and **0°~90°** for the Y axis (``SERVO_ID_Y`` / tilt).

        :param int servo_id: ``SERVO_ID_X`` or ``SERVO_ID_Y``.
        :param float angle_deg: Target angle in degrees (**-135~135** for X, **0~90** for Y).
        :param int time_ms: Move time (ms) passed to the controller; ``0`` means the time parameter does not take effect.
        :param int speed: User speed **0~100** (mapped to the bus); ``0`` means the speed parameter does not take effect.

        UiFlow2 Code Block:

            |stackchan_api_set_servo_angle_time.png|

            |stackchan_api_set_servo_angle_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                sc.set_servo_angle(SERVO_ID_X, 0.0, 500, 0)
                sc.set_servo_angle(SERVO_ID_X, 0.0, 0, 50)

    .. method:: get_servo_angle(servo_id)

        Read the servo angle in degrees.

        :param int servo_id: ``SERVO_ID_X`` or ``SERVO_ID_Y``.
        :returns: Angle in degrees, or ``None`` if the read failed.

        UiFlow2 Code Block:

            |stackchan_api_get_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                deg = sc.get_servo_angle(SERVO_ID_X)

    .. method:: set_servo_x_pwm(value)

        Run the **X** servo in PWM mode for continuous rotation. User range is **-100~100**; the sign selects rotation direction, and the magnitude sets drive strength.

        :param int value: Signed PWM strength (clamped). Positive and negative values rotate in opposite directions; ``0`` stops output.

        UiFlow2 Code Block:

            |stackchan_api_set_servo_x_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                sc.set_servo_x_pwm(50)

    .. method:: set_rgb_color(*args)

        Set RGB LEDs on the strip.

        - One argument: fill all LEDs with ``color``.
        - Two arguments: ``strip`` (``0`` or ``1``) and ``color`` for that logical strip.
        - Three arguments: ``strip``, ``index``, ``color`` for a single LED (strip ``1`` index order matches the driver).

        :returns: ``True`` on success where applicable.

        UiFlow2 Code Block:

            |stackchan_api_set_rgb_color_all.png|

            |stackchan_api_set_rgb_color_strip.png|

            |stackchan_api_set_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                sc.set_rgb_color(0x00FF00)
                sc.set_rgb_color(0, 0x0000FF)
                sc.set_rgb_color(0, 0, 0xFF0000)

    .. method:: get_rgb_color(strip, index)

        Get RGB color of a single LED.

        :param int strip: ``0`` or ``1``.
        :param int index: ``0~5`` per logical strip.
        :returns: ``tuple`` ``(r, g, b)``.

        UiFlow2 Code Block:

            |stackchan_api_get_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                r, g, b = sc.get_rgb_color(0, 0)

    .. method:: get_touch(index=None)

        Read touch state (three logical slots).

        :param int index: If ``None``, return a list of three levels; if ``0``, ``1``, or ``2``, return that slot's level.
        :returns: ``OUTPUT_NONE``...``OUTPUT_HIGH`` style values. A read failure returns
            ``OUTPUT_NONE`` values so examples can safely index the result.

        UiFlow2 Code Block:

            |stackchan_api_get_touch_all.png|

            |stackchan_api_get_touch.png|

        MicroPython Code Block:

            .. code-block:: python

                tp = sc.get_touch()
                one = sc.get_touch(0)

    .. method:: get_battery_voltage()

        Bus voltage from the INA226 (volts).

        :returns: ``float`` or ``None`` if unavailable.

        UiFlow2 Code Block:

            |stackchan_api_get_battery_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                v = sc.get_battery_voltage()

    .. method:: get_battery_current()

        Current from the INA226 (A).

        :returns: ``float`` or ``None``.

        UiFlow2 Code Block:

            |stackchan_api_get_battery_current.png|

        MicroPython Code Block:

            .. code-block:: python

                a = sc.get_battery_current()

    .. method:: get_battery_power()

        Power from the INA226 (W), when both voltage and current are valid.

        :returns: ``float`` or ``None``.

        UiFlow2 Code Block:

            |stackchan_api_get_battery_power.png|

        MicroPython Code Block:

            .. code-block:: python

                p = sc.get_battery_power()
