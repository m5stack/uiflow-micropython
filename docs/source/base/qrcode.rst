Atomic QRCode Base
============================

.. sku: A133 

.. include:: ../refs/base.qrcode.ref

This library is the driver for Atomic QRCode Base, and the module communicates via UART.

Support the following products:

    |Atomic QRCode Base|

UiFlow2 Example:
--------------------------

QRCode Scan in Key Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3_qrcode_key_mode_example.m5f2| project in UiFlow2.

In **Key Mode**, the module starts decoding when the button is pressed and stops decoding when the button is released. After a successful decoding, it stops decoding. To continue decoding, the button must be released and pressed again.

UiFlow2 Code Block:

    |atoms3_qrcode_key_mode_example.png|

Example output:

    None

QRCode Scan in Host Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3_qrcode_host_mode_example.m5f2| project in UiFlow2.

In **Host Mode**, pressing the button once starts decoding, and pressing the button again stops decoding.

UiFlow2 Code Block:

    |atoms3_qrcode_host_mode_example.png|

Example output:

    None

QRCode Scan in Auto Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3_qrcode_auto_mode_example.m5f2| project in UiFlow2.

In **Auto Mode**, the module starts decoding when powered on and cannot be stopped.

UiFlow2 Code Block:

    |atoms3_qrcode_auto_mode_example.png|

Example output:

    None

QRCode Scan in Pulse Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3_qrcode_pulse_mode_example.m5f2| project in UiFlow2.

In **Pulse Mode**, set the TRIG pin to hold a low level for more than 20ms to trigger decoding once.

UiFlow2 Code Block:

    |atoms3_qrcode_pulse_mode_example.png|

Example output:

    None

QRCode Scan in Motion Sensing Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3_qrcode_motion_sensing_mode_example.m5f2| project in UiFlow2.

In **Motion Sensing Mode**, the module automatically triggers decoding when it detects a change in the scene based on visual recognition information.

UiFlow2 Code Block:

    |atoms3_qrcode_motion_sensing_mode_example.png|

Example output:

    None

 
MicroPython Example:
--------------------------

QRCode Scan in Key Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **Key Mode**, the module starts decoding when the button is pressed and stops decoding when the button is released. After a successful decoding, it stops decoding. To continue decoding, the button must be released and pressed again.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/qrcode/atoms3_qrcode_key_mode_example.py
        :language: python
        :linenos:

Example output:

    None

QRCode Scan in Host Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **Host Mode**, pressing the button once starts decoding, and pressing the button again stops decoding.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/qrcode/atoms3_qrcode_host_mode_example.py
        :language: python
        :linenos:

Example output:

    None

QRCode Scan in Auto Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **Auto Mode**, the module starts decoding when powered on and cannot be stopped.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/qrcode/atoms3_qrcode_auto_mode_example.py
        :language: python
        :linenos:

Example output:

    None

QRCode Scan in Pulse Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **Pulse Mode**, set the TRIG pin to hold a low level for more than 20ms to trigger decoding once.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/qrcode/atoms3_qrcode_pulse_mode_example.py
        :language: python
        :linenos:

Example output:

    None

QRCode Scan in Motion Sensing Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **Motion Sensing Mode**, the module automatically triggers decoding when it detects a change in the scene based on visual recognition information.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/qrcode/atoms3_qrcode_motion_sensing_mode_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------

AtomicQRCodeBase 
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: base.qrcode.AtomicQRCodeBase
    :members:
