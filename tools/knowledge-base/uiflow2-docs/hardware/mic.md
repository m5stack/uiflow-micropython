<!-- .. _hardware.Mic: -->

# Mic

<!-- .. include:: ../refs/system.ref -->
<!-- .. include:: ../refs/hardware.mic.ref -->

Mic is used to control the built-in microphone inside the host device. Below is
the detailed Mic support for the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | SPM1423 | ES7210 |

###### | AtomS3          |         |        |

###### | AtomS3 Lite     |         |        |

###### | AtomS3U         | |S|     |        |

###### | StampS3         |         |        |

###### | CoreS3          |         | |S|    |

###### | Core2           | |S|     |        |

###### | TOUGH           |         |        |

<!-- .. |S| unicode:: U+2714 -->

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time

label0 = None

rec_data = None

def setup():
    global label0, rec_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 123, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.end()
    Mic.begin()
    rec_data = bytearray(8000 * 5)
    label0.setText(str("rec..."))
    Mic.record(rec_data, 8000, False)
    while Mic.isRecording():
        time.sleep_ms(500)
    Mic.end()
    Speaker.begin()
    label0.setText(str("play..."))
    Speaker.playRaw(rec_data, 8000)
    while Speaker.isPlaying():
        time.sleep_ms(500)
    label0.setText(str("done"))

def loop():
    global label0, rec_data
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |cores3_mic_example.m5f2|

## class Mic

<!-- .. important:: -->

    Methods of the Mic Class heavily rely on ``M5.begin()``  and ``M5.update()`` .

    All calls to methods of Mic objects should be placed after ``M5.begin()`` , and ``M5.update()``  should be called in the main loop.

<!-- .. note:: -->

    Mic is registered in the ``M5`` module, **not** in the ``hardware``
    module. Use ``from M5 import *`` to make ``Mic`` available. Do not
    write ``from hardware import Mic``.

<!-- .. _hardware.Mic.Methods: -->

## Methods

<!-- .. method:: Mic.config([cfg:mic_config_t]) -->
            Mic.config('param')
            Mic.config(param=value)

    Get or set the parameters of the Mic object.

    When no parameters are passed, it returns an object of :py:class:`mic_config_t`.
    When a :py:class:`mic_config_t` object is passed, Mic sets all supported parameters of the Mic.

    When passing parameters from the table below, Mic will get or set the passed parameters.

    The following parameters are supported:

        ==================  ===========  ===========
        Parameter           Type         Description
        ==================  ===========  ===========
        pin_data_in         (integer)    Serial data line of I2S, representing audio data in binary complement.
        pin_bck             (integer)    Serial clock line of I2S, corresponding to each bit of digital audio data.
        pin_mck             (integer)    Master clock line of I2S. Generally, to better synchronize between systems, increase the MCLK signal, MCLK frequency = 256 * sampling frequency.
        pin_ws              (integer)    Frame clock of I2S, used to switch left and right channel data.
        sample_rate         (integer)    Target sampling rate of input audio.
        stereo              (boolean)    Use stereo output.
        over_sampling       (integer)    Number of times to average the sampling.
        magnification       (integer)    Multiplier of the input value.
        noise_filter_level  (integer)    Coefficient of the previous value used for noise filtering.
        use_adc             (boolean)    Use analog input microphone (only pin_data_in is needed).
        dma_buf_len         (integer)    DMA buffer length of I2S.
        dma_buf_count       (integer)    Number of DMA buffers of I2S.
        task_priority       (integer)    Priority of background tasks.
        task_pinned_core    (integer)    CPU used by background tasks.
        i2s_port            (integer)    I2S port.
        ==================  ===========  ===========

    UIFLOW2:

        Read property:

            Python::

                Mic.config("pin_data_in")

        Set property:

            Python::

                Mic.config(pin_data_in=1)

<!-- .. method:: Mic.begin() -> bool -->

    Start the Mic function. Returns True if successful.

    UIFLOW2:

<!-- .. method:: Mic.end() -> bool -->

    Stop the Mic function. Returns True if successful.

    UIFLOW2:

<!-- .. method:: Mic.isRunning() -> bool -->

    Check if Mic is running. Returns a boolean value.

    UIFLOW2:

<!-- .. method:: Mic.isEnabled() -> bool -->

    Check if Mic is enabled. Returns a boolean value.

    UIFLOW2:

<!-- .. method:: Mic.isRecording() -> int -->

    Check if Mic is recording. Returns an integer value.

    Return values:

        - 0=not recording
        - 1=recording (There's room in the queue)
        - 2=recording (There's no room in the queue.)

    UIFLOW2:

<!-- .. method:: Mic.setSampleRate(sample_rate) -> None -->

    Set the sampling rate. The parameter sample_rate generally includes 8000, 11025, 22050, 32000, 44100.

    UIFLOW2:

<!-- .. method:: Mic.record(rec_data[, rate[, stereo]]) -> bool -->

    Record audio data.

    The parameter rec_data requires passing a buffer.
    The parameter rate generally includes 8000, 11025, 22050, 32000, 44100, with a default of 8000.
    The parameter stereo is passed as True or False.

    UIFLOW2:

## class mic_config_t

<!-- .. py:attribute:: mic_config_t.pin_data_in -->
    :type: int

    Serial data line of I2S, representing audio data in binary complement.

<!-- .. py:attribute:: mic_config_t.pin_bck -->
    :type: int

    Serial clock line of I2S, corresponding to each bit of digital audio data.

<!-- .. py:attribute:: mic_config_t.pin_mck -->
    :type: int

    Master clock line of I2S. Generally, to better synchronize between systems,
    increase the MCLK signal, MCLK frequency = 256 * sampling frequency.

<!-- .. py:attribute:: mic_config_t.pin_ws -->
    :type: int

    Frame clock of I2S, used to switch left and right channel data.

<!-- .. py:attribute:: mic_config_t.sample_rate -->
    :type: int

    Target sampling rate of input audio.

<!-- .. py:attribute:: mic_config_t.stereo -->
    :type: bool

    Use stereo output.

<!-- .. .. py:attribute:: mic_config_t.input_offset -->
    :type: int

    Deprecated.

<!-- .. py:attribute:: mic_config_t.over_sampling -->
    :type: int

    Number of times to average the sampling.

<!-- .. py:attribute:: mic_config_t.magnification -->
    :type: int

    Multiplier of the input value.

<!-- .. py:attribute:: mic_config_t.noise_filter_level -->
    :type: int

    Coefficient of the previous value used for noise filtering.

<!-- .. py:attribute:: mic_config_t.use_adc -->
    :type: bool

    Use analog input microphone (only pin_data_in is needed).

<!-- .. py:attribute:: mic_config_t.dma_buf_len -->
    :type: int

    DMA buffer length of I2S.

<!-- .. py:attribute:: mic_config_t.dma_buf_count -->
    :type: int

    Number of DMA buffers of I2S.

<!-- .. py:attribute:: mic_config_t.task_priority -->
    :type: int

    Priority of background tasks.

<!-- .. py:attribute:: mic_config_t.task_pinned_core -->
    :type: int

    CPU used by background tasks.

<!-- .. py:attribute:: mic_config_t.i2s_port -->
    :type: int

    I2S port.
