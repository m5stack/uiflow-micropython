USB Host
========

.. module:: usbhost
   :synopsis: Native USB-A HID input and MJPEG UVC cameras on Tab5

This module is available on Tab5. The USB-A connector uses the ESP32-P4
high-speed OTG controller as Host. USB-C uses the separate full-speed OTG
controller for CDC/REPL and ``machine.USBDevice``. ROM download mode is retained.
After installing this firmware, reconnect the computer's serial terminal to
the Tab5 CDC port; its identity differs from the previous Serial/JTAG port.

Call ``M5.begin()`` before constructing ``HIDHost``. The host enables USB-A
VBUS through the board's IO expander. ``deinit()`` disables that supply and
releases the Host controller. Do not change the USB-A power configuration
while the host is active.

``HIDHost`` supports directly connected USB boot keyboards and
boot mice, including composite devices with multiple supported interfaces.
It does not enable hubs, mass storage, serial adapters or USB Wi-Fi drivers.
Report-only/NKRO keyboards and vendor-specific mouse reports are not decoded.
Mouse input provides three buttons and signed relative X/Y movement. Wheel
and additional buttons are not decoded. USB keyboards are not automatically
attached to the REPL, and mouse input is not automatically attached to LVGL.

Example::

    import M5
    import usbhost

    M5.begin()
    host = usbhost.HIDHost()
    try:
        while True:
            M5.update()
            event = host.read(timeout=20)
            if event is not None:
                print(event)
    finally:
        host.deinit()

Combined mouse demo
-------------------

Copy both ``examples/hardware/usbhost/tab5_usb_mouse_demo.py`` and
``tab5_mouse_transport.py`` to the device, then run::

    import tab5_usb_mouse_demo
    tab5_usb_mouse_demo.run()

The upper panel displays the USB-A mouse cursor, left/right/middle click counts,
relative movement, received reports, dropped reports and driver errors.
The lower panel turns the Tab5 touchscreen into a USB-C mouse using the existing
``usb.device.mouse.Mouse`` implementation, while retaining built-in CDC.

Slide one finger to move the computer pointer, tap briefly for a left click,
or hold still for 450 ms before moving to drag. LEFT and RIGHT can be held;
UP and DOWN send scroll-wheel reports. Touch STOP to release buttons, stop the
Host and restore the original CDC-only configuration.

HID reports are serialized to preserve press/release edges while an earlier
transfer is pending. The status panel shows submitted/completed report counts.
When USB-C is attached to a virtual machine, touch input controls that guest.
Display dimensions follow the board's existing rotation.

``HIDHost`` and ``UVCCamera`` share one native Host bus manager. This version
allows one of these classes to own USB-A at a time. Deinitialize the current
owner before switching classes. USB-C CDC/REPL remains available in either mode.

Class HIDHost
-------------

.. class:: HIDHost()

    Start the native HID Host. Only one instance may own the controller.
    A second constructor raises ``OSError``. Call ``deinit()`` before creating
    another instance. All resources are also released on MicroPython soft reset.

.. method:: HIDHost.read(timeout=0)

    Service pending attachments and return the next event dictionary, or
    ``None`` if no event arrives within ``timeout`` milliseconds. Zero polls
    without waiting. Negative values raise ``ValueError``. The timeout applies
    to waiting for input; attachment control requests have driver timeouts and
    may take longer. Call ``read`` regularly to configure newly attached devices.

    Every event includes ``event``, ``address``, ``interface``, ``protocol``,
    ``vid`` and ``pid``. The protocol is ``"keyboard"``, ``"mouse"`` or
    ``"unknown"``. Address and interface together identify a connected interface;
    USB addresses may be reused after unplugging.

    Event names are ``"connected"``, ``"disconnected"``, ``"input"``,
    ``"error"`` and ``"unsupported"``. Errors include an ESP-IDF ``error``
    code. Unsupported events identify interfaces outside the boot keyboard/mouse
    scope. VID/PID may be zero if an interface could not be opened.

    Keyboard input includes ``modifiers`` (USB modifier bitmap), ``keys``
    (tuple of currently pressed USB HID usage IDs), ``rollover`` and ``data``
    (the eight-byte boot report). An empty tuple means all ordinary keys are
    released. On keyboard rollover/error, ``rollover`` is true and ``keys`` is
    empty; this does not represent a reliable release state. No ASCII or
    keyboard-layout conversion is performed.

    Mouse input includes ``buttons`` (left=1, right=2, middle=4), ``dx``,
    ``dy`` and ``data`` (up to eight raw bytes). Positive X is right and
    positive Y is down. A malformed boot report produces an error event.

.. method:: HIDHost.devices()

    Service pending attachments and return a list of supported active HID
    interfaces, with the same identity fields as events. This enumerates
    supported HID interfaces, not every USB device or class.

.. method:: HIDHost.dropped()

    Return the cumulative number of event records dropped since startup.
    The native queue holds 32 events and discards old records on overflow.
    Poll promptly. If this counter increases, input transitions or relative
    mouse movement may have been lost; reset application input state and
    refresh ``devices()`` as needed. The counter resets when a new host starts.

.. method:: HIDHost.deinit()

    Stop and release the host. Repeated calls are allowed. Methods on a closed
    instance raise ``OSError(ENODEV)``; an old instance cannot stop a newer host.
    If cleanup fails, ``OSError`` reports it and native resources remain valid
    for a retry instead of being freed under running tasks.

.. function:: deinit()

    Stop the current native host, including after losing its Python instance
    or after a constructor failed partway through initialization.


Class UVCCamera
---------------

.. class:: UVCCamera(*, width=640, height=480, fps=0, frame_size=524288)

    Start the UVC driver for one directly connected camera's first video stream.
    Call ``M5.begin()`` first. Only MJPEG is accepted by this API; YUY2, H.264,
    H.265, audio and camera controls are not enabled.

    Width and height must be 1..4096 and must match a camera-supported format.
    FPS is an integer from 0..120; zero requests the device's default FPS.
    Unsupported format/FPS combinations raise ``OSError`` during ``start()``.

    ``frame_size`` is the maximum compressed size of one JPEG, from 16 KiB to
    4 MiB. Three driver frame buffers are allocated in PSRAM when a stream opens.
    Larger frames are discarded and counted in ``info()["overflows"]``.
    The API never silently falls back to an uncompressed format.

    Construction installs the driver and enables USB-A power; it does not wait
    for a camera or start streaming. A second camera or HID owner raises
    ``OSError``. Soft reset releases native resources.

.. method:: UVCCamera.formats(timeout=5000)

    Wait up to ``timeout`` milliseconds for enumeration and return the first
    camera stream's frame formats as dictionaries containing ``format``,
    ``width``, ``height`` and ``default_fps``. An empty list means no camera
    arrived in time. Reported formats other than ``"mjpeg"`` are informational
    and cannot be selected by this implementation.

.. method:: UVCCamera.start(timeout=5000)

    Open the first matching UVC stream and start MJPEG reception. No camera,
    an unsupported requested mode or a negotiation failure raises ``OSError``.
    ``timeout`` bounds device discovery; USB control requests have their own
    driver timeouts. Starting an already open stream raises ``OSError``.

.. method:: UVCCamera.read(timeout=1000)

    Return a complete JPEG as ``bytes``, or ``None`` on timeout. Each successful
    call copies one frame into Python-managed memory. Prefer ``readinto`` for
    continuous preview.

.. method:: UVCCamera.readinto(buffer, timeout=1000)

    Copy the next JPEG into a writable buffer and return its byte length, or
    zero on timeout. Allocate a ``bytearray(frame_size)`` once and reuse it.
    The supplied buffer must fit the actual JPEG; otherwise the frame is
    returned to the driver and ``ValueError`` is raised.

    Native callbacks retain at most two frames in a bounded queue. A slow
    consumer causes new frames to be dropped; it never grows the Python heap
    or blocks the USB event task. A received frame is copied once into the
    caller's buffer and promptly returned to the driver.

    ``read`` and ``readinto`` require a started stream. Unplugging the camera
    raises ``OSError(ENODEV)``. After reconnecting, call ``stop()`` and
    ``start()`` to negotiate the new stream.

.. method:: UVCCamera.info()

    Return ``status`` (``"waiting"``, ``"ready"`` or ``"streaming"``),
    ``format``, ``width``, ``height``, ``fps``, ``received``, ``dropped``,
    ``overflows``, ``errors`` and ``last_error``. FPS is the negotiated setting,
    not a measurement of delivered throughput. Counters reset on construction.

.. method:: UVCCamera.stop()

    Stop and close the stream, returning all queued driver frames. The driver
    and USB-A power remain available for another ``start()``. Repeated calls
    are allowed.

.. method:: UVCCamera.deinit()

    Stop streaming, uninstall the driver and release USB-A power and controller.
    Call this in ``finally``. Repeated calls are allowed; an old instance
    cannot stop a newer camera. Methods on a deinitialized instance raise
    ``OSError(ENODEV)``.

All camera timeout arguments accept 0..60000 milliseconds. This implementation
requires hardware validation with the actual camera; supported modes and frame
rates depend on that camera's descriptors and the USB/display workload.

Example::

    import M5
    import usbhost

    M5.begin()
    camera = usbhost.UVCCamera(width=640, height=480)
    try:
        print(camera.formats())
        camera.start()
        buffer = bytearray(512 * 1024)
        count = camera.readinto(buffer)
        if count:
            M5.Lcd.drawJpg(memoryview(buffer)[:count], 0, 0)
    finally:
        camera.deinit()

``examples/hardware/usbhost/tab5_uvc_camera.py`` adds continuous preview,
delivered FPS and error counters, a CAPTURE button that saves a JPEG under
``/flash`` without overwriting existing captures, and a STOP button. It is an
explicitly launched example and does not modify the launcher or ``main.py``.
