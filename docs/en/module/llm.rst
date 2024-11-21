
Llm Module
==========

.. include:: ../refs/module.llm.ref

Micropython Example::

    from module import LlmModule

    def on_keyword_detected():
        print("[Keyword] detected")

    def on_asr_data_input(data: str, finish: bool, index: int):
        print(f"[ASR data] {data}")

    def on_llm_data_input(data: str, finish: bool, index: int):
        print(f"[LLM data] {data}")

    module_llm = LlmModule()
    module_llm.begin_voice_assistant()

    module_llm.set_voice_assistant_on_keyword_detected_callback(on_keyword_detected)
    module_llm.set_voice_assistant_on_asr_data_input_callback(on_asr_data_input)
    module_llm.set_voice_assistant_on_llm_data_input_callback(on_llm_data_input)

    while True:
        module_llm.update()

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |llm_voice_assistant.m5f2|


class LlmModule
---------------

Constructors
------------

.. class:: LlmModule()

    Initialize LlmModule and set up UART communication based on board type.

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: LlmModule.update() -> None

    Update ModuleLLM, receive response message.

    UIFLOW2:

        |update.png|

.. method:: LlmModule.check_connection() -> bool

    Check if the module connection is working properly.

    :return: True if module connection is OK, False otherwise.
    :rtype: bool

    UIFLOW2:

        |check_connection.png|

.. method:: LlmModule.get_response_msg_list() -> list

    Get the list of module's response messages.

    :return: List of response messages as dictionaries.
    :rtype: list

    UIFLOW2:

        |get_response_msg_list.png|

.. method:: LlmModule.clear_response_msg_list() -> None

    Clear the module's response message list.

    UIFLOW2:

        |clear_response_msg_list.png|

.. method:: LlmModule.sys_ping() -> int

    Send a ping to the system and get the response code.

    UIFLOW2:

        |sys_ping.png|

.. method:: LlmModule.sys_reset(wait_reset_finish=True) -> int

    Reset the system.

    :param bool wait_reset_finish: Whether to wait for reset completion.
    :return: Result of the reset command.
    :rtype: int

    UIFLOW2:

        |sys_reset.png|

.. method:: LlmModule.sys_reboot() -> int

    Reboot the system.

    :return: Result of the reboot command.
    :rtype: int

    UIFLOW2:

        |sys_reboot.png|

.. method:: LlmModule.llm_setup(prompt="", model="qwen2.5-0.5b", response_format="llm.utf-8.stream", input="llm.utf-8.stream", enoutput=True, enkws=True, max_token_len=127, request_id="llm_setup") -> str

    Set up the LLM module.

    :param str prompt: The prompt text.
    :param str model: The model name.
    :param str response_format: The response format.
    :param str input: The input format.
    :param bool enoutput: Enable output.
    :param bool enkws: Enable keyword spotting.
    :param int max_token_len: Maximum token length.
    :param str request_id: Request ID.
    :return: Result of the setup command.
    :rtype: str

    UIFLOW2:

        |llm_setup.png|

.. method:: LlmModule.llm_inference(work_id, input_data, request_id="llm_inference") -> str

    Perform inference with the LLM module.

    :param work_id: The work ID.
    :param input_data: The input data.
    :param str request_id: Request ID.
    :return: Result of the inference command.
    :rtype: str

    UIFLOW2:

        |llm_inference.png|

.. method:: LlmModule.audio_setup(capcard=0, capdevice=0, cap_volume=0.5, playcard=0, playdevice=1, play_volume=0.15, request_id="audio_setup") -> str

    Set up the audio module.

    :param int capcard: Capture card index.
    :param int capdevice: Capture device index.
    :param float cap_volume: Capture volume.
    :param int playcard: Playback card index.
    :param int playdevice: Playback device index.
    :param float play_volume: Playback volume.
    :param str request_id: Request ID.
    :return: Result of the setup command.
    :rtype: str

    UIFLOW2:

        |audio_setup.png|

.. method:: LlmModule.tts_setup(model="single_speaker_english_fast", response_format="tts.base64.wav", input="tts.utf-8.stream", enoutput=True, enkws=True, request_id="tts_setup") -> str

    Set up the TTS module.

    :param str model: TTS model name.
    :param str response_format: The response format.
    :param str input: The input format.
    :param bool enoutput: Enable output.
    :param bool enkws: Enable keyword spotting.
    :param str request_id: Request ID.
    :return: Result of the setup command.
    :rtype: str

    UIFLOW2:

        |tts_setup.png|

.. method:: LlmModule.kws_setup(kws="HELLO", model="sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01", response_format="kws.bool", input="sys.pcm", enoutput=True, request_id="kws_setup") -> str

    Set up the KWS module.

    :param str kws: Keyword to detect.
    :param str model: KWS model name.
    :param str response_format: The response format.
    :param str input: The input format.
    :param bool enoutput: Enable output.
    :param str request_id: Request ID.
    :return: Result of the setup command.
    :rtype: str

    UIFLOW2:

        |kws_setup.png|

.. method:: LlmModule.asr_setup(model="sherpa-ncnn-streaming-zipformer-20M-2023-02-17", response_format="asr.utf-8.stream", input="sys.pcm", enoutput=True, enkws=True, rule1=2.4, rule2=1.2, rule3=30.0, request_id="asr_setup") -> str

    Set up the ASR module.

    :param str model: ASR model name.
    :param str response_format: The response format.
    :param str input: The input format.
    :param bool enoutput: Enable output.
    :param bool enkws: Enable keyword spotting.
    :param float rule1: Rule 1 value.
    :param float rule2: Rule 2 value.
    :param float rule3: Rule 3 value.
    :param str request_id: Request ID.
    :return: Result of the setup command.
    :rtype: str

    UIFLOW2:

        |asr_setup.png|

.. method:: LlmModule.get_latest_llm_work_id() -> str

    Get latest LLM module work id.

    :return: Latest LLM module work id.
    :rtype: str

    UIFLOW2:

        |get_latest_llm_work_id.png|

.. method:: LlmModule.get_latest_audio_work_id() -> str

    Get latest Audio module work id.

    :return: Latest Audio module work id.
    :rtype: str

    UIFLOW2:

        |get_latest_audio_work_id.png|

.. method:: LlmModule.get_latest_tts_work_id() -> str

    Get latest TTS module work id.

    :return: Latest TTS module work id.
    :rtype: str

    UIFLOW2:

        |get_latest_tts_work_id.png|

.. method:: LlmModule.get_latest_kws_work_id() -> str

    Get latest KWS module work id.

    :return: Latest KWS module work id.
    :rtype: str

    UIFLOW2:

        |get_latest_kws_work_id.png|

.. method:: LlmModule.get_latest_asr_work_id() -> str

    Get latest ASR module work id.

    :return: Latest ASR module work id.
    :rtype: str

    UIFLOW2:

        |get_latest_asr_work_id.png|

.. method:: LlmModule.get_latest_error_code() -> int

    Get latest ModuleLLM response error code.

    :return: Latest ModuleLLM response error code.
    :rtype: int

    UIFLOW2:

        |get_latest_error_code.png|

.. method:: LlmModule.begin_voice_assistant(wake_up_keyword="HELLO", prompt="") -> bool

    Begin the voice assistant.

    :param str wake_up_keyword: The wake-up keyword.
    :param str prompt: The assistant prompt.
    :return: True if the voice assistant began successfully, False otherwise.
    :rtype: bool

    UIFLOW2:

        |begin_voice_assistant.png|

.. method:: LlmModule.set_voice_assistant_on_keyword_detected_callback(on_keyword_detected) -> None

    Set the callback for when the wake-up keyword is detected.

    :param on_keyword_detected: Callback function to be executed on keyword detection.

    UIFLOW2:

        |set_voice_assistant_on_keyword_detected_callback.png|

.. method:: LlmModule.set_voice_assistant_on_asr_data_input_callback(on_asr_data_input) -> None

    Set the callback for when ASR data is input.

    :param on_asr_data_input: Callback function to handle ASR data input.

    UIFLOW2:

        |set_voice_assistant_on_asr_data_input_callback.png|

.. method:: LlmModule.set_voice_assistant_on_llm_data_input_callback(on_llm_data_input) -> None

    Set the callback for when LLM data is input.

    :param on_llm_data_input: Callback function to handle LLM data input.

    UIFLOW2:

        |set_voice_assistant_on_llm_data_input_callback.png|