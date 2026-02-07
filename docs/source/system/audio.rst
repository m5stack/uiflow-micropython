:mod:`audio` --- player and recorder
=====================================

.. module:: audio
    :synopsis: player and recorder

.. include:: ../refs/system.audio.ref

This module implements player and recorder

- player: encapsulates the ADF esp_audio, support local and online resources.
- recorder: record and encoding the voice into file.

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
