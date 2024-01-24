Speaker
=======

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.speaker.ref

Speaker 用于控制主机内部集成的按键。以下是主机的 Speaker 支持详细：

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+---------+
    |Controller       | NS4168  | AW88298 |
    +=================+=========+=========+
    | AtomS3          |         |         |
    +-----------------+---------+---------+
    | AtomS3 Lite     |         |         |
    +-----------------+---------+---------+
    | AtomS3U         |         |         |
    +-----------------+---------+---------+
    | StampS3         |         |         |
    +-----------------+---------+---------+
    | CoreS3          |         | |S|     |
    +-----------------+---------+---------+
    | Core2           | |S|     |         |
    +-----------------+---------+---------+
    | TOUGH           | |S|     |         |
    +-----------------+---------+---------+

.. |S| unicode:: U+2714

Micropython Example::

    pass

UIFLOW2 Example::

    pass

class Speaker
-------------

.. important::

    Speaker Class的方法重度依赖 ``M5.begin()`` |M5.begin.svg| 和 ``M5.update()`` |M5.update.svg|。

    调用 Speaker 对象的所有方法，需要放在 ``M5.begin()`` |M5.begin.svg| 的后面，
    并在 主循环中调用 ``M5.update()`` |M5.update.svg|。

Methods
-------

.. method:: Speaker.config([cfg])
            Speaker.config('param')
            Speaker.config(param=value)

    获取或者设置 Speaker 对象的参数。

    UIFLOW2:

        读取属性：

            ==================  ===========  ===========
            Parameter           Type         Description
            ==================  ===========  ===========
            pin_data_out        (integer)    I2S 的串行数据线，用二进制补码表示的音频数据。
            pin_bck             (integer)    I2S 的串行时钟线，对应数字音频的每一位数据。
            pin_ws              (integer)    I2S 的帧时钟，用于切换左右声道的数据。
            sample_rate         (integer)    音频输出的采样率。
            stereo              (boolean)    使用双声道输出。
            buzzer              (boolean)    使用单GPIO蜂鸣器。
            use_dac             (boolean)    使用DAC音箱。
            dac_zero_level      (integer)    使用DAC时的零电平参考值。
            magnification       (integer)    输入值的乘数。
            dma_buf_len         (integer)    I2S 的DMA缓冲区长度。
            dma_buf_count       (integer)    I2S 的DMA缓冲区数量。
            task_priority       (integer)    后台任务优先级。
            task_pinned_core    (integer)    后台任务使用的CPU。
            i2s_port            (integer)    I2S端口。
            ==================  ===========  ===========

            Python::

                Speaker.config("pin_data_in")

            |config.svg|

        设置属性：

            Python::

                Speaker.config(pin_data_in=1)

            |config1.svg|

.. method:: Speaker.begin() -> bool

    启动 Speaker 功能。执行成功返回 True 。

    UIFLOW2:

        |begin.svg|

.. method:: Speaker.end() -> None

    禁用 Speaker 。

    UIFLOW2:

        Python::

            Speaker.end()

        |end.svg|

.. method:: Speaker.isRunning() -> bool

    获取 Speaker 是否处于运行状态， 返回bool类型。

    UIFLOW2:

        |isRunning.svg|

.. method:: Speaker.isEnabled() -> bool

    获取 Speaker 是否处于使能状态， 返回bool类型。

    UIFLOW2:

        |isEnabled.svg|

.. method:: Speaker.isPlaying([channel]) -> bool

    获取 Speaker 是否处于声音输出状态， 返回bool类型。

    传入参数 ``channel`` 时，获取指定通道的播放状态。``channel`` 接受的值是 0 ~ 7 。

    UIFLOW2:

        |isPlaying.svg|

.. method:: Speaker.getPlayingChannels() -> int

    获取正在播放的频道数。

    UIFLOW2:

        |getPlayingChannels.svg|

.. method:: Speaker.setVolume(volume: int) -> None

    设置声音的输出主音量。``volume`` 接受 0 ~ 255 的音量等级。

    UIFLOW2:

        |setVolume.svg|

.. method:: Speaker.getVolume() -> int

    获取声音的输出主音量。返回 0 ~ 255 的音量等级。

    UIFLOW2:

        |getVolume.svg|

.. method:: Speaker.setVolumePercentage(percentage: float) -> None

    设置声音的输出主音量百分比。``percentage`` 是 0% ~ 100% 的音量等级。

    UIFLOW2:

        Python::

            Speaker.getVolumePercentage(0.5) # 50%

        |setVolumePercentage.svg|

.. method:: Speaker.getVolumePercentage() -> float

    获取声音的输出主音量百分比。返回 0% ~ 100% 的音量等级。

    UIFLOW2:

        |getVolumePercentage.svg|

.. method:: Speaker.setAllChannelVolume(volume: int) -> None

    设置所有虚拟通道的声音输出音量。``volume`` 接受 0 ~ 255 的音量等级。

    UIFLOW2:

        uiflow2 的需要做成无返回值的块。

        Python::

            Speaker.setAllChannelVolume(128)

        |setAllChannelVolume.svg|

.. method:: Speaker.setChannelVolume(channel: int, volume: int) -> None

    设置指定虚拟通道的声音输出音量。

    参数如下：

        - ``volume`` 接受 0 ~ 255 的音量等级。
        - ``channel`` 是播放的通道，范围是 0 ~ 7 。

    UIFLOW2:

        uiflow2的需要做成无返回值的块。

        |setChannelVolume.svg|

.. method:: Speaker.getChannelVolume(channel) -> int

    获取指定虚拟通道的声音输出音量。``channel`` 是虚拟通道，范围是 0 ~ 7 。

    UIFLOW2:

        |getChannelVolume.svg|

.. method:: Speaker.stop([channel]) -> None

    停止声音输出。当不使用 ``channel`` 时，停止所有通道的声音输出。``channel`` 接受的值是 0 ~ 7 。

    UIFLOW2:

        |stop.svg|

.. method:: Speaker.tone(frequency, duration[, channel[, stop_current_sound]]) -> None

    播放简单的音调声音。

    参数是：

        - ``frequency`` 是音调的频率，单位是 Hz。
        - ``duration`` 是音调的持续时间，单位是毫秒。
        - ``channel`` 是播放的通道，范围是 0 ~ 7 ，默认填 -1 ，使用可用的通道播放。
        - ``stop_current_sound`` 用于控制是否等待之前的音频播放完成，为 True 时，无需等待当前输出完成即可开始新的输出。

    UIFLOW2:

        |tone.svg|

.. method:: Speaker.playRaw(wav_data: bytes|bytearray[, sample_rate: int[, stereo: bool[, repeat: int[, channel: int[, stop_current_sound: bool]]]]]) -> bool

    播放 PCM 的数据。

    参数是：

        - ``wav_data`` 是音频数据的 buffer。
        - ``sample_rate`` 是设置音频数据的采样率。
        - ``stereo`` 是设置音频为双声道。
        - ``repeat`` 是音频播放的次数，默认是 1 。
        - ``channel`` 是播放的通道，范围是 0 ~ 7 ，默认填 -1 ，使用可用的通道播放。
        - ``stop_current_sound`` 用于控制是否等待之前的音频播放完成，为 True 时，无需等待当前输出完成即可开始新的输出。

    UIFLOW2:

        |playRaw.svg|

.. method:: Speaker.playWav(wav_data: bytes|bytearray[, repeat: int[, channel: int[, stop_current_sound: bool]]]) -> None

    播放 wave 格式的音频数据。要求传入整个音频文件的原始数据。

    参数是：

        - ``wav_data`` 是音频数据的 buffer。
        - ``repeat`` 是音频播放的次数，默认是 1 。
        - ``channel`` 是播放的通道，范围是 0 ~ 7 ，默认填 -1 ，使用可用的通道播放。
        - ``stop_current_sound`` 用于控制是否等待之前的音频播放完成，为 True 时，无需等待当前输出完成即可开始新的输出。

    UIFLOW2:

        |playWav.svg|
