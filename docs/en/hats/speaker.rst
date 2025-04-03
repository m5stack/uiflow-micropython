Speaker Hat
===========

.. sku: U055

.. include:: ../refs/hat.speaker.ref

The following products are supported:

    |Speaker Hat|

Below is the detailed support for Speaker on the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+-------------------+
    |Controller       | Speaker Hat       |
    +=================+===================+
    | CoreInk         | |S|               |
    +-----------------+-------------------+
    | StickC          | |S|               |
    +-----------------+-------------------+
    | StickC PLUS     | |S|               |
    +-----------------+-------------------+
    | StickC PLUS2    | |S|               |
    +-----------------+-------------------+

.. |S| unicode:: U+2705
.. |N| unicode:: U+274C

Micropython Example:

    .. literalinclude:: ../../../examples/hat/speaker/stickc_plus2_speaker_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_speaker_example.m5f2|

    :download:`poweron_2_5s.wav <../../../examples/hardware/speaker/poweron_2_5s.wav>`

class SpeakerHat
----------------

Constructors
------------

.. class:: SpeakerHat(*args, **kwargs)

    Create an SpeakerHat object.

    UIFLOW2:

        |init.png|

    SpeakerHat class inherits M5.Speaker class, See :ref:`hardware.Speaker.Methods <hardware.Speaker.Methods>` for more details.
