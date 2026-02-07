Audio Module
============

.. SKU: M144

.. include:: ../refs/module.audio.ref

The AudioModule class implements playback and recording functions and supports resampling.

It is used to play audio files and streams, record audio from the microphone, and convert between different sample rates.

Support the following products:

    |Audio Module|


UiFlow2 Example
---------------

Play WAV file
^^^^^^^^^^^^^

Open the |cores3_play_wav_example.m5f2| project in UiFlow2.

.. only:: builder_html

    :download:`66.wav <../../../examples/module/audio/66.wav>`

This example reads an audio file from the file system and plays it.

UiFlow2 Code Block:

    |cores3_play_wav_example.png|

Example output:

    None


Playback Controls
^^^^^^^^^^^^^^^^^

Open the |cores3_playback_controls_example.m5f2| project in UiFlow2.

.. only:: builder_html

    :download:`66.wav <../../../examples/module/audio/66.wav>`

This example demonstrates how to control playback using the AudioModule class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

UiFlow2 Code Block:

    |cores3_playback_controls_example.png|

Example output:

    None


Record Audio
^^^^^^^^^^^^

Open the |cores3_record_audio_example.m5f2| project in UiFlow2.

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

UiFlow2 Code Block:

    |cores3_record_audio_example.png|

Example output:

    None


MicroPython Example
-------------------

Play WAV file
^^^^^^^^^^^^^

This example reads an audio file from the file system and plays it.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/audio/cores3_playback_controls_example.py
        :language: python
        :linenos:

Example output:

    None


Playback Controls
^^^^^^^^^^^^^^^^^

This example demonstrates how to control playback using the AudioModule class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/audio/cores3_playback_controls_example.py
        :language: python
        :linenos:

Example output:

    None


Record Audio
^^^^^^^^^^^^

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/audio/cores3_record_audio_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

Class AudioModule
^^^^^^^^^^^^^^^^^

.. autoclass:: module.audio.AudioModule
    :members:
    :member-order: bysource
