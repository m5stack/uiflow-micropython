PDM Unit
==========

.. sku: U089

.. include:: ../refs/unit.pdm.ref

This is the driver library of PDM Unit, which is provides a set of methods to control the PDM microphone. Through the
I2S interface, the module can record audio data and save it as WAV files.

Support the following products:

    |PDM|


UiFlow2 Example
---------------

record voice and play voice
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the |pdm_cores3_example.m5f2| project in UiFlow2.

This example records voice and plays voice.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

record voice and play voice
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example records voice and plays voice.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/pdm/pdm_cores3_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

PDMUnit
^^^^^^^^^

.. autoclass:: unit.pdm.PDMUnit
    :members:

    .. py:method:: begin()

        Initialize the PDM microphone.

        :return: Returns True if initialization was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |begin.png|

        MicroPython Code Block:

            .. code-block:: python

                pdm.begin()

    .. py:method:: end()

        Stop the PDM microphone.

        UiFlow2 Code Block:

            |end.png|

        MicroPython Code Block:

            .. code-block:: python

                pdm.end()

    .. py:method:: record(buffer, sample_rate=16000, stereo=False)

        Record audio data into the provided buffer.

        :param bytearray buffer: Buffer to store the recorded audio data
        :param int sample_rate: Sample rate in Hz (default: 16000)
        :param bool stereo: True for stereo recording, False for mono (default: False)
        :return: True if recording started successfully
        :rtype: bool

        UiFlow2 Code Block:

            |record.png|

        MicroPython Code Block:

            .. code-block:: python

                rec_data = bytearray(16000 * 5)  # 5 seconds buffer
                pdm.record(rec_data, 16000, False)

    .. py:method:: isRecording()

        Check if recording is in progress.

        :return: Returns the number of bytes recorded.
        
            * ``0`` - Not recording
            * ``1`` - Recording (Queue has available space)
            * ``2`` - Recording (Queue is full) 

        :rtype: int

        UiFlow2 Code Block:

            |isRecording.png|

        MicroPython Code Block:

            .. code-block:: python

                pdm.isRecording()

    .. py:method:: recordWavFile(path, rate=16000, time=5, stereo=False)

        Record audio directly to a WAV file.

        :param str path: Path to save the WAV file
        :param int rate: Sample rate in Hz (default: 16000)
        :param int time: Recording duration in seconds (default: 5)
        :param bool stereo: True for stereo recording, False for mono (default: False)
        :return: True if recording was successful
        :rtype: bool

        UiFlow2 Code Block:

            |recordWavFile.png|

        MicroPython Code Block:

            .. code-block:: python

                pdm.recordWavFile("/sd/test.wav", 16000, 5, False)

    .. py:method:: config(**kwargs)

        Configure the PDM microphone parameters.

        :param kwargs: Configuration parameters

            - pin_data_in: Data input pin
            - pin_ws: Word select pin
            - sample_rate: Sample rate in Hz
            - stereo: Stereo mode
            - over_sampling: Over sampling rate
            - noise_filter_level: Noise filter level
            - magnification: Audio magnification
            - dma_buf_len: DMA buffer length
            - dma_buf_count: DMA buffer count
            - task_priority: Task priority
            - task_pinned_core: Task core pinning
            - i2s_port: I2S port number

        UiFlow2 Code Block:

            |get_config_boolean.png|

            |get_config_int.png|

            |set_config_boolean.png|

            |set_config_int.png|

        MicroPython Code Block:

            .. code-block:: python

                pdm.config(
                    dma_buf_count=3,
                    dma_buf_len=256,
                    over_sampling=2,
                    noise_filter_level=0,
                    sample_rate=16000,
                    pin_data_in=1,
                    pin_ws=2,
                    pin_bck=-1,
                    pin_mck=-1,
                    use_adc=False,
                    stereo=False,
                    magnification=1,
                    task_priority=2,
                    task_pinned_core=255,
                    i2s_port=i2s_port,
                )
