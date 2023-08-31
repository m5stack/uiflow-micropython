Mic
===

.. include:: ../refs/system.ref
.. include:: ../refs/hardware.mic.ref

Mic 用于控制主机内部集成的按键。以下是主机的 Mic 支持详细：

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+--------+
    |Controller       | SPM1423 | ES7210 |
    +=================+=========+========+
    | AtomS3          |         |        |
    +-----------------+---------+--------+
    | AtomS3 Lite     |         |        |
    +-----------------+---------+--------+
    | AtomS3U         | |S|     |        |
    +-----------------+---------+--------+
    | StampS3         |         |        |
    +-----------------+---------+--------+
    | CoreS3          |         | |S|    |
    +-----------------+---------+--------+
    | Core2           | |S|     |        |
    +-----------------+---------+--------+
    | TOUGH           |         |        |
    +-----------------+---------+--------+

.. |S| unicode:: U+2714

Micropython Example::

    pass

UIFLOW2 Example::

    pass

class Mic
---------

.. important::

    Mic Class的方法重度依赖 ``M5.begin()`` |M5.begin.svg| 和 ``M5.update()`` |M5.update.svg|。

    调用 Mic 对象的所有方法，需要放在 ``M5.begin()`` |M5.begin.svg| 的后面，并在 主循环中调用 ``M5.update()`` |M5.update.svg|。

Methods
-------

.. method:: Mic.config([cfg:mic_config_t])
            Mic.config('param')
            Mic.config(param=value)

    获取或者设置 Mic 对象的参数。

    当不传入任何参数时，会返回 :py:class:`mic_config_t` 的对象。
    当传入一个 :py:class:`mic_config_t` 的对象， Mic 会设置 Mic 的所有支持的参数。

    当传入下表中的参数， Mic 会对传入的参数进行获取或者设置。

    以下是支持的参数:

        ==================  ===========  ===========
        Parameter           Type         Description
        ==================  ===========  ===========
        pin_data_in         (integer)    I2S 的串行数据线，用二进制补码表示的音频数据。
        pin_bck             (integer)    I2S 的串行时钟线，对应数字音频的每一位数据。
        pin_mck             (integer)    I2S 的主时钟线。一般为了使系统间能够更好地同步时增加MCLK信号，MCLK的频率 = 256 * 采样频率。
        pin_ws              (integer)    I2S 的帧时钟，用于切换左右声道的数据。
        sample_rate         (integer)    输入音频的目标采样率。
        stereo              (boolean)    使用双声道输出。
        over_sampling       (integer)    求平均值的采样次数。
        magnification       (integer)    输入值的乘数。
        noise_filter_level  (integer)    先前值的系数，用于噪声过滤。
        use_adc             (boolean)    使用模拟输入麦克风（仅需要 pin_data_in ）。
        dma_buf_len         (integer)    I2S 的DMA缓冲区长度。
        dma_buf_count       (integer)    I2S 的DMA缓冲区数量。
        task_priority       (integer)    后台任务优先级。
        task_pinned_core    (integer)    后台任务使用的CPU。
        i2s_port            (integer)    I2S端口。
        ==================  ===========  ===========

    UIFLOW2:

        读取属性：

            Python::

                Mic.config("pin_data_in")

            |config.svg|

        设置属性：

            Python::

                Mic.config(pin_data_in=1)

            |config1.svg|

.. method:: Mic.begin() -> bool

    启动 Mic 功能。执行成功返回 True 。

    UIFLOW2:

        uiflow2 的需要做成两种块， 一种忽略返回值的块， 一种有返回值（ 返回bool类型 ）的块。
        有返回值的块放到 Advanced 栏中。

        Python::

            Mic.begin()

        |begin.svg|

.. method:: Mic.end() -> bool

    描述

    UIFLOW2:

        uiflow2 的需要做成两种块， 一种忽略返回值的块， 一种有返回值（ 返回bool类型 ）的块。
        有返回值的块放到 Advanced 栏中。

        Python::

            Mic.end()

        |end.svg|

.. method:: Mic.isRunning() -> bool

    描述

    UIFLOW2:

        获取 Mic 是否处于运行状态， 返回bool类型。
        uiflow2的需要做成有返回值的块。

        Python::

            Mic.isRunning()

        |isRunning.svg|

.. method:: Mic.isEnabled() -> bool

    描述

    UIFLOW2:

        获取 Mic 是否处于使能状态， 返回bool类型。
        uiflow2的需要做成有返回值的块。

        Python::

            Mic.isEnabled()

        |isEnabled.svg|

.. method:: Mic.isRecording() -> int

    描述

    UIFLOW2:

        获取 Mic 是否处于录音状态， 返回int类型。

        返回值：
            - 0=not recording
            - 1=recording (There's room in the queue)
            - 2=recording (There's no room in the queue.)

        uiflow2的需要做成有返回值的块。

        Python::

            Mic.isRecording()

        |isRecording.svg|

.. method:: Mic.setSampleRate(sample_rate) -> None

    描述

    UIFLOW2:

        设置采样率， uiflow2 的需要做成无返回值的块。
        参数 sample_rate 一般有 8000 ， 11025 ，22050 ，32000 ，44100

        |setSampleRate.svg|

.. method:: Mic.record(rec_data[, rate[, stereo]]) -> bool

    描述。

    UIFLOW2:

        uiflow2 的需要做成两种块， 一种忽略返回值的块， 一种有返回值（ 返回bool类型 ）的块。
        有返回值的块放到 Advanced 栏中。

        参数 rec_data 要求传入一个buffer，。
        参数 rate 一般有 8000， 11025，22050，32000，44100， 默认填8000。
        参数 stereo 传入True或者False。

        |record.svg|

class mic_config_t
------------------

.. py:attribute:: mic_config_t.pin_data_in
    :type: int

    I2S 的串行数据线，用二进制补码表示的音频数据。

.. py:attribute:: mic_config_t.pin_bck
    :type: int

    I2S 的串行时钟线，对应数字音频的每一位数据。

.. py:attribute:: mic_config_t.pin_mck
    :type: int

    I2S 的主时钟线。一般为了使系统间能够更好地同步时增加MCLK信号，MCLK的频率 = 256 * 采样频率。

.. py:attribute:: mic_config_t.pin_ws
    :type: int

    I2S 的帧时钟，用于切换左右声道的数据。

.. py:attribute:: mic_config_t.sample_rate
    :type: int

    输入音频的目标采样率。

.. py:attribute:: mic_config_t.stereo
    :type: bool

    使用双声道输出。

.. .. py:attribute:: mic_config_t.input_offset
    :type: int

    已弃用。

.. py:attribute:: mic_config_t.over_sampling
    :type: int

    求平均值的采样次数。

.. py:attribute:: mic_config_t.magnification
    :type: int

    输入值的乘数。

.. py:attribute:: mic_config_t.noise_filter_level
    :type: int

    先前值的系数，用于噪声过滤。

.. py:attribute:: mic_config_t.use_adc
    :type: bool

    使用模拟输入麦克风（仅需要 pin_data_in ）。

.. py:attribute:: mic_config_t.dma_buf_len
    :type: int

    I2S 的DMA缓冲区长度。

.. py:attribute:: mic_config_t.dma_buf_count
    :type: int

    I2S 的DMA缓冲区数量。

.. py:attribute:: mic_config_t.task_priority
    :type: int

    后台任务优先级。

.. py:attribute:: mic_config_t.task_pinned_core
    :type: int

    后台任务使用的CPU。

.. py:attribute:: mic_config_t.i2s_port
    :type: int

    I2S端口。
