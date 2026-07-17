
# class Recorder

The recorder can record audio from the microphone and encode the audio into wav or amr format.

## class audio.Recorder

## Constructors

### `class audio.Recorder(sample=8000, bits=16, stereo=False)`

    Create a Recorder object.

    - Parameter `sample` (`int`): The sample rate of the audio data. The range is 8000-96000.
    - Parameter `bits` (`int`): The bits of the audio data.
    - Parameter `stereo` (`bool`): Whether the audio data is stereo.

## Methods

### `Recorder.record(uri: str, time: int, sync=True)`

    Record audio from microphone to file.

    - Parameter `uri` (`str`): The uri of the audio file. e.g. "file://flash/test.amr", "file://sd/test.wav".
    - Parameter `time` (`int`): The duration of the recording, The unit is seconds.
    - Parameter `sync` (`bool`): Whether to record synchronously.

### `Recorder.create_pcm_buf(time) -> bytearray`

    Create a buffer to store the audio data. The audio data is in PCM format.

    The length of the data buffer is :math:`sample * bits * time / 8`

    - Parameter `time` (`int`): The duration of the recording, The unit is seconds.

    - Returns: The buffer to store the audio data.

### `Recorder.record_into(buf, sample=8000, bits=16, stereo=False, sync=True)`

    Play the raw audio data.

    - Parameter `buf` (`bytes`): Read into buf from the microphone.
    - Parameter `sample` (`int`): The sample rate of the audio data. The range is 8000-96000.
    - Parameter `bits` (`int`): The bits of the audio data.
    - Parameter `stereo` (`bool`): Whether the audio data is stereo.
    - Parameter `sync` (`bool`): Whether to record synchronously.

### `Recorder.pause()`

    Pause the Recorder.

### `Recorder.resume()`

    Resume the Recorder.

### `Recorder.stop()`

    Stop the Recorder.

### `Recorder.rms() -> float`

    Get the root mean square of the audio data.

    - Returns: The root mean square of the audio data. The unit is dB.

### `Recorder.volume() -> int`

    Get the volume of the audio data.

    - Returns: The volume of the audio data. The range is 0-100.

### `Recorder.is_recording() -> bool`

    Check if the Recorder is recording.

    - Returns: True if the Recorder is recording, False otherwise.

### `Recorder.config(sample=8000, bits=16, stereo=False) -> bool`

    Configure the Recorder.

    - Parameter `sample` (`int`): The sample rate of the audio data. The range is 8000-96000.
    - Parameter `bits` (`int`): The bits of the audio data.
    - Parameter `stereo` (`bool`): Whether the audio data is stereo.
