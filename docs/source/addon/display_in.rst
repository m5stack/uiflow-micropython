addon DisplayIn
===============

.. py:currentmodule:: addon.display_in

.. include:: ../refs/addon.display_in.ref

``DisplayIn`` captures HDMI input from the Display In Add-on (U220) connected
to Unit PoE-P4 and saves a frame as a JPEG file. It initializes the LT6911
HDMI receiver when created and releases the capture resources with
:meth:`DisplayIn.deinit`.

The current capture format is ``1280x720``. Connect an HDMI source before
calling :meth:`DisplayIn.capture`.

Support the following products:

    |display_in|

UiFlow2 Example
---------------

HDMI input
^^^^^^^^^^

Create a DisplayIn object and capture one frame to the selected file path.

Open the |display_in_poep4_example.m5f2| project in UiFlow2.

UiFlow2 Code Block:

    |init.png|

    |capture.png|

    |deinit.png|

MicroPython Example
-------------------

HDMI input
^^^^^^^^^^

This example captures one frame from the HDMI input and saves it as a JPEG file
in the device flash file system.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/addon/display_in/display_in_poep4_example.py
        :language: python
        :linenos:

**API**
-------

DisplayIn
^^^^^^^^^

.. autoclass:: addon.display_in.DisplayIn
    :members:
    :member-order: bysource
