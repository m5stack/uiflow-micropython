
# LLM Module

Micropython Example:
```python
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
```

## class LlmModule

## Constructors

### `class LlmModule()`

    Initialize LlmModule and set up UART communication based on board type.

## Methods

### `LlmModule.update() -> None`

    Update ModuleLLM, receive response message.

### `LlmModule.check_connection() -> bool`

    Check if the module connection is working properly.

    - Returns: True if module connection is OK, False otherwise.
    - Return type: bool

### `LlmModule.get_response_msg_list() -> list`

    Get the list of module's response messages.

    - Returns: List of response messages as dictionaries.
    - Return type: list

### `LlmModule.clear_response_msg_list() -> None`

    Clear the module's response message list.

### `LlmModule.sys_ping() -> int`

    Send a ping to the system and get the response code.

### `LlmModule.sys_reset(wait_reset_finish=True) -> int`

    Reset the system.

    - Parameter `wait_reset_finish` (`bool`): Whether to wait for reset completion.
    - Returns: Result of the reset command.
    - Return type: int

### `LlmModule.sys_reboot() -> int`

    Reboot the system.

    - Returns: Result of the reboot command.
    - Return type: int

### `LlmModule.llm_setup(prompt="", model="qwen2.5-0.5b", response_format="llm.utf-8.stream", input="llm.utf-8.stream", enoutput=True, enkws=True, max_token_len=127, request_id="llm_setup") -> str`

    Set up the LLM module.

    - Parameter `prompt` (`str`): The prompt text.
    - Parameter `model` (`str`): The model name.
    - Parameter `response_format` (`str`): The response format.
    - Parameter `input` (`str`): The input format.
    - Parameter `enoutput` (`bool`): Enable output.
    - Parameter `enkws` (`bool`): Enable keyword spotting.
    - Parameter `max_token_len` (`int`): Maximum token length.
    - Parameter `request_id` (`str`): Request ID.
    - Returns: Result of the setup command.
    - Return type: str

### `LlmModule.llm_inference(work_id, input_data, request_id="llm_inference") -> str`

    Perform inference with the LLM module.

    - Parameter `work_id`: The work ID.
    - Parameter `input_data`: The input data.
    - Parameter `request_id` (`str`): Request ID.
    - Returns: Result of the inference command.
    - Return type: str

### `LlmModule.audio_setup(capcard=0, capdevice=0, cap_volume=0.5, playcard=0, playdevice=1, play_volume=0.15, request_id="audio_setup") -> str`

    Set up the audio module.

    - Parameter `capcard` (`int`): Capture card index.
    - Parameter `capdevice` (`int`): Capture device index.
    - Parameter `cap_volume` (`float`): Capture volume.
    - Parameter `playcard` (`int`): Playback card index.
    - Parameter `playdevice` (`int`): Playback device index.
    - Parameter `play_volume` (`float`): Playback volume.
    - Parameter `request_id` (`str`): Request ID.
    - Returns: Result of the setup command.
    - Return type: str

### `LlmModule.tts_setup(model="single_speaker_english_fast", response_format="tts.base64.wav", input="tts.utf-8.stream", enoutput=True, enkws=True, request_id="tts_setup") -> str`

    Set up the TTS module.

    - Parameter `model` (`str`): TTS model name.
    - Parameter `response_format` (`str`): The response format.
    - Parameter `input` (`str`): The input format.
    - Parameter `enoutput` (`bool`): Enable output.
    - Parameter `enkws` (`bool`): Enable keyword spotting.
    - Parameter `request_id` (`str`): Request ID.
    - Returns: Result of the setup command.
    - Return type: str

### `LlmModule.kws_setup(kws="HELLO", model="sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01", response_format="kws.bool", input="sys.pcm", enoutput=True, request_id="kws_setup") -> str`

    Set up the KWS module.

    - Parameter `kws` (`str`): Keyword to detect.
    - Parameter `model` (`str`): KWS model name.
    - Parameter `response_format` (`str`): The response format.
    - Parameter `input` (`str`): The input format.
    - Parameter `enoutput` (`bool`): Enable output.
    - Parameter `request_id` (`str`): Request ID.
    - Returns: Result of the setup command.
    - Return type: str

### `LlmModule.asr_setup(model="sherpa-ncnn-streaming-zipformer-20M-2023-02-17", response_format="asr.utf-8.stream", input="sys.pcm", enoutput=True, enkws=True, rule1=2.4, rule2=1.2, rule3=30.0, request_id="asr_setup") -> str`

    Set up the ASR module.

    - Parameter `model` (`str`): ASR model name.
    - Parameter `response_format` (`str`): The response format.
    - Parameter `input` (`str`): The input format.
    - Parameter `enoutput` (`bool`): Enable output.
    - Parameter `enkws` (`bool`): Enable keyword spotting.
    - Parameter `rule1` (`float`): Rule 1 value.
    - Parameter `rule2` (`float`): Rule 2 value.
    - Parameter `rule3` (`float`): Rule 3 value.
    - Parameter `request_id` (`str`): Request ID.
    - Returns: Result of the setup command.
    - Return type: str

### `LlmModule.get_latest_llm_work_id() -> str`

    Get latest LLM module work id.

    - Returns: Latest LLM module work id.
    - Return type: str

### `LlmModule.get_latest_audio_work_id() -> str`

    Get latest Audio module work id.

    - Returns: Latest Audio module work id.
    - Return type: str

### `LlmModule.get_latest_tts_work_id() -> str`

    Get latest TTS module work id.

    - Returns: Latest TTS module work id.
    - Return type: str

### `LlmModule.get_latest_kws_work_id() -> str`

    Get latest KWS module work id.

    - Returns: Latest KWS module work id.
    - Return type: str

### `LlmModule.get_latest_asr_work_id() -> str`

    Get latest ASR module work id.

    - Returns: Latest ASR module work id.
    - Return type: str

### `LlmModule.get_latest_error_code() -> int`

    Get latest ModuleLLM response error code.

    - Returns: Latest ModuleLLM response error code.
    - Return type: int

### `LlmModule.begin_voice_assistant(wake_up_keyword="HELLO", prompt="") -> bool`

    Begin the voice assistant.

    - Parameter `wake_up_keyword` (`str`): The wake-up keyword.
    - Parameter `prompt` (`str`): The assistant prompt.
    - Returns: True if the voice assistant began successfully, False otherwise.
    - Return type: bool

### `LlmModule.set_voice_assistant_on_keyword_detected_callback(on_keyword_detected) -> None`

    Set the callback for when the wake-up keyword is detected.

    - Parameter `on_keyword_detected`: Callback function to be executed on keyword detection.

### `LlmModule.set_voice_assistant_on_asr_data_input_callback(on_asr_data_input) -> None`

    Set the callback for when ASR data is input.

    - Parameter `on_asr_data_input`: Callback function to handle ASR data input.

### `LlmModule.set_voice_assistant_on_llm_data_input_callback(on_llm_data_input) -> None`

    Set the callback for when LLM data is input.

    - Parameter `on_llm_data_input`: Callback function to handle LLM data input.
