.. currentmodule:: audio

class Recorder
==============

.. include:: ../refs/system.audio.recorder.ref

The recorder can record audio from the microphone and encode the audio into wav or amr format.


class audio.Recorder
--------------------

Constructors
------------

.. class:: audio.Recorder(sample=8000, bits=16, stereo=False)

    Create a Recorder object.

    :param int sample: The sample rate of the audio data. The range is 8000-96000.
    :param int bits: The bits of the audio data.
    :param bool stereo: Whether the audio data is stereo.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Recorder.record(uri: str, time: int, sync=True)

    Record audio from microphone to file.

    :param str uri: The uri of the audio file. e.g. "file://flash/test.amr", "file:///sd/test.wav".
    :param int time: The duration of the recording, The unit is seconds.
    :param bool sync: Whether to record synchronously.

    UIFLOW2:

        |record.png|


.. method:: Recorder.record_into(buf, sample=8000, bits=16, stereo=False, sync=True)

    Play the raw audio data.

    :param bytes buf: Read into buf from the microphone.
    :param int sample: The sample rate of the audio data. The range is 8000-96000.
    :param int bits: The bits of the audio data.
    :param bool stereo: Whether the audio data is stereo.
    :param bool sync: Whether to record synchronously.

    UIFLOW2:

        |record_into.png|


.. method:: Recorder.pause()

    Pause the Recorder.

    UIFLOW2:

        |pause.png|


.. method:: Recorder.resume()

    Resume the Recorder.

    UIFLOW2:

        |resume.png|


.. method:: Recorder.stop()

    Stop the Recorder.

    UIFLOW2:

        |stop.png|


.. method:: Recorder.rms() -> float

    Get the root mean square of the audio data.

    :return: The root mean square of the audio data. The unit is dB.

    UIFLOW2:

        |rms.png|


.. method:: Recorder.volume() -> int

    Get the volume of the audio data.

    :return: The volume of the audio data. The range is 0-100.

    UIFLOW2:

        |volume.png|


.. method:: Recorder.is_recording() -> bool

    Check if the Recorder is recording.

    :return: True if the Recorder is recording, False otherwise.

    UIFLOW2:

        |is_recording.png|


.. method:: Recorder.config(sample=8000, bits=16, stereo=False) -> bool

    Configure the Recorder.

    :param int sample: The sample rate of the audio data. The range is 8000-96000.
    :param int bits: The bits of the audio data.
    :param bool stereo: Whether the audio data is stereo.

    UIFLOW2:

        |config.png|
