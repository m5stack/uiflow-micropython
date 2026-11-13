:mod:`audio` --- player and recorder
=====================================

.. module:: audio
    :synopsis: player and recorder

.. include:: ../refs/system.audio.ref

This module implements player and recorder

- player: encapsulates the ADF esp_audio, support local and online resources.
- recorder: record and encoding the voice into file.

Create the recording directory and upload playback files before use.
See `Resource Files and Paths <../quick-reference/resource-files.html>`_
for ADF URI syntax. On StickS3, use ``M5.Mic`` and ``M5.Speaker`` for WAV
recording and playback; the ADF path may hang during codec/I2S initialization.

Below is the detailed audio support for the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+--------+--------+-------------+---------+
    |                 | AW88298 | ES7210 | ES8311 | I2S Philips | I2S PDM |
    +=================+=========+========+========+=============+=========+
    | CoreS3          | |S|     | |S|    |        |             |         |
    +-----------------+---------+--------+--------+-------------+---------+
    | BOX3            |         | |S|    | |S|    |             |         |
    +-----------------+---------+--------+--------+-------------+---------+

.. |S| unicode:: U+2714


Micropython Example:

    .. literalinclude:: ../../../examples/system/audio/cores3_audio_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_audio_example.m5f2|


Classes
-------

.. toctree::
    :maxdepth: 1

    audio.player.rst
    audio.recorder.rst
