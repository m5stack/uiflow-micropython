Atomic Echo Base
================

.. sku: A149

.. include:: ../refs/base.echo.ref

The following products are supported:

    |Atomic Echo Base|

Below is the detailed support for Atomic Echo Base on the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+-------------------+
    |Controller       | Atomic Echo Base  |
    +=================+===================+
    | Atom Echo       | |O|               |
    +-----------------+-------------------+
    | Atom Lite       | |S|               |
    +-----------------+-------------------+
    | Atom Matrix     | |S|               |
    +-----------------+-------------------+
    | AtomS3          | |S|               |
    +-----------------+-------------------+
    | AtomS3 Lite     | |S|               |
    +-----------------+-------------------+
    | AtomS3R         | |S|               |
    +-----------------+-------------------+
    | AtomS3R-CAM     | |S|               |
    +-----------------+-------------------+
    | AtomS3R-Ext     | |S|               |
    +-----------------+-------------------+

.. |S| unicode:: U+2705
.. |O| unicode:: U+2B55


UiFlow2 Example
---------------

Play WAV file
^^^^^^^^^^^^^

Open the |atoms3_play_wav_example.m5f2| project in UiFlow2.

.. only:: builder_html

    :download:`66.wav <../../../examples/module/audio/66.wav>`

This example reads an audio file from the file system and plays it.

UiFlow2 Code Block:

    |atoms3_play_wav_example.png|

Example output:

    None


Playback Controls
^^^^^^^^^^^^^^^^^

Open the |atoms3_playback_controls_example.m5f2| project in UiFlow2.

.. only:: builder_html

    :download:`66.wav <../../../examples/module/audio/66.wav>`

This example demonstrates how to control playback using the AtomicEchoBase class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

UiFlow2 Code Block:

    |atoms3_playback_controls_example.png|

Example output:

    None


Record Audio
^^^^^^^^^^^^

Open the |atoms3_record_audio_example.m5f2| project in UiFlow2.

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

UiFlow2 Code Block:

    |atoms3_record_audio_example.png|

Example output:

    None


MicroPython Example
-------------------

Play WAV file
^^^^^^^^^^^^^

This example reads an audio file from the file system and plays it.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/echo/atoms3_playback_controls_example.py
        :language: python
        :linenos:

Example output:

    None


Playback Controls
^^^^^^^^^^^^^^^^^

This example demonstrates how to control playback using the AtomicEchoBase class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/echo/atoms3_playback_controls_example.py
        :language: python
        :linenos:

Example output:

    None


Record Audio
^^^^^^^^^^^^

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/echo/atoms3_record_audio_example.py
        :language: python
        :linenos:

Example output:

    None


AtomicEchoBase
^^^^^^^^^^^^^^

.. autoclass:: base.echo.AtomicEchoBase
    :members:
    :member-order: bysource
