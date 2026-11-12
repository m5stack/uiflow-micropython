.. _hardware.RTC:

***
RTC
***

The ``hardware.RTC`` class manages the system clock. When RTC synchronization
is enabled for a controller, setting the clock also synchronizes its built-in
RTC. This is separate from the Grove-connected ``unit.RTCUnit`` driver.

UiFlow2 Example
===============

See the RTC clock example on the StopWatch controller page.

MicroPython Example
===================

Set UTC time, configure a fixed local offset, and read both representations:

.. code-block:: python

    import M5
    from hardware import RTC

    M5.begin()
    rtc = RTC()
    rtc.timezone("GMT+8")
    # UTC: year, month, day, weekday, hour, minute, second, microsecond
    rtc.datetime((2026, 11, 6, 4, 4, 30, 0, 0))
    print(rtc.datetime())        # UTC, approximately 04:30
    print(rtc.local_datetime())  # GMT+8, approximately 12:30

API
===

Constructors
------------

.. class:: RTC()

    Return the singleton RTC object. No constructor arguments are accepted.

Methods
-------

.. method:: RTC.init(datetime)

    Set UTC using the eight-element tuple
    ``(year, month, day, hour, minute, second, ignored, microsecond)``.
    The seventh element is ignored. This order differs from ``datetime()``.

.. method:: RTC.datetime([datetime])

    With no argument, return the current UTC date and time as
    ``(year, month, day, weekday, hour, minute, second, microsecond)``.
    Weekdays run from Monday (0) to Sunday (6).

    With an eight-element tuple
    ``(year, month, day, weekday, hour, minute, second, microsecond)``, set UTC
    time. The weekday field is ignored when setting the clock; it is computed
    when reading it.

.. method:: RTC.local_datetime([datetime])

    With no argument, return local time in the same tuple order as
    ``datetime()``, applying the configured timezone.

    With an eight-element tuple in the same layout as ``datetime()``, set the
    clock.

    .. warning::

        In the current firmware, the setter stores the supplied date/time
        fields as UTC without subtracting the timezone offset. Use
        ``datetime()`` with UTC values to set the clock.

.. method:: RTC.timezone([timezone])

    Get or set the timezone string, for example ``"GMT+8"`` for UTC+08:00 or
    ``"GMT-5"`` for UTC-05:00. The getter returns ``None`` if no timezone is set.
    Setting a timezone updates local-time conversion and saves it in NVS;
    it does not change the UTC clock. Use fixed offsets with this API.

.. method:: RTC.memory([data])

    With no argument, return the user RTC memory as ``bytes``.
    With a bytes-like object, replace its contents. Oversized buffers raise
    ``ValueError``. The default maximum size is 2048 bytes, and this method
    is absent from builds configured with ``MICROPY_HW_RTC_USER_MEM_MAX=0``.

    RTC memory can survive deep sleep and resets, depending on the board
    configuration. It is not persistent storage across power loss.
