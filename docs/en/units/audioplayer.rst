AudioPlayer Unit
==================

.. sku:U197

.. include:: ../refs/unit.audioplayer.ref

This is the driver library of AudioPlayer Unit, which is used to play audio files.

Support the following products:

    |AudioPlayer|

UiFlow2 Example
---------------

play audio
^^^^^^^^^^^^^^^

Open the |audioplayer_core2_example.m5f2| project in UiFlow2.

This example plays the audio file on the AudioPlayer Unit.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

play audio
^^^^^^^^^^^^^^^

This example plays the audio file on the AudioPlayer Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/audioplayer/audioplayer_core2_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

AudioPlayerUnit
^^^^^^^^^^^^^^^

.. autoclass:: unit.audioplayer.AudioPlayerUnit
    :members:
    :member-order: bysource