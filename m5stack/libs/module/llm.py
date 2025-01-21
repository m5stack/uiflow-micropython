# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import UART
import time
import ujson
from M5 import getBoard, BOARD
from collections import namedtuple


class ModuleComm:
    def __init__(self, uart):
        self._serial = uart

    def send_cmd(self, cmd):
        # print(f"[DEBUG] Sending command: {cmd}")
        self._serial.write(cmd)

    def get_response(self, timeout=5000):
        start_time = time.ticks_ms()
        response = ""

        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            if self._serial.any():
                try:
                    data = self._serial.read(1)
                    if data:
                        response += data.decode("utf-8")
                        if "\n" in response:
                            return {"time_out": False, "msg": response}
                        start_time = time.ticks_ms()
                except Exception:
                    pass

        if not response:
            return {"time_out": True, "msg": ""}
        return {"time_out": False, "msg": response}


class ModuleMsg:
    def __init__(self, module_comm):
        self._module_comm = module_comm
        self.response_msg_list = []

    def update(self):
        response = self._module_comm.get_response(50)
        if response["time_out"]:
            return
        self.add_msg_from_response(response["msg"])

    def add_msg_from_response(self, response):
        json_strings = response.strip().splitlines()
        for json_str in json_strings:
            try:
                # Try parse response
                doc = ujson.loads(json_str)
                # Push into resonse msg list
                self.response_msg_list.append(doc)
                # print(f"[DEBUG] Received message:\n{doc}")
            except ValueError:
                continue
        return

    def clear_msg(self, request_id):
        self.response_msg_list = [
            msg for msg in self.response_msg_list if msg["request_id"] != request_id
        ]

    def take_msg(self, request_id, on_msg):
        for msg in self.response_msg_list:
            if msg["request_id"] == request_id:
                on_msg(msg)  # 调用回调函数处理消息
                self.response_msg_list.remove(msg)  # 移除已处理的消息
                return True
        return False

    def wait_and_take_msg(self, request_id, on_msg, timeout=10000):
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            self.update()
            if self.take_msg(request_id, on_msg):
                return True
            time.sleep_ms(5)
        return False

    def send_cmd_and_wait_to_take_msg(self, cmd, request_id, on_msg, timeout=10000):
        self._module_comm.send_cmd(cmd)
        self.clear_msg(request_id)
        return self.wait_and_take_msg(request_id, on_msg, timeout)

    def send_cmd(self, cmd):
        self._module_comm.send_cmd(cmd)


class ApiSys:
    _MODULE_LLM_OK = 0
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97
    _MODULE_LLM_RESPONSE_PARSE_FAILED = -98

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None
        self._ret = self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def ping(self) -> int:
        cmd_ping = '{"request_id":"sys_ping","work_id":"sys","action":"ping","object":"None","data":"None"}'
        return self._send_cmd_and_wait(cmd_ping, "sys_ping", 2000)

    def version(self) -> int:
        cmd_version = '{"request_id":"sys_version","work_id":"sys","action":"version","object":"None","data":"None"}'
        return self._send_cmd_and_wait_verson(cmd_version, "sys_version", 2000)

    def lsmode(self) -> int:
        cmd_version = '{"request_id":"sys_lsmode","work_id":"sys","action":"lsmode","object":"None","data":"None"}'
        return self._send_cmd_and_wait_lsmode(cmd_version, "sys_lsmode", 2000)

    def rmmode(
        self,
        model=None,
        request_id="llm_rmmode",
    ) -> str:
        cmd = {
            "request_id": "sys_rmmode",
            "work_id": "sys",
            "action": "rmmode",
            "object": "sys.rmmode",
            "data": model if model is not None else "None",
        }
        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 20000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def reset(self, wait_reset_finish=True) -> int:
        cmd_reset = '{"request_id":"sys_reset","work_id":"sys","action":"reset","object":"None","data":"None"}'
        result = self._send_cmd_and_wait(cmd_reset, "sys_reset", 2000)

        if result != self._MODULE_LLM_OK or not wait_reset_finish:
            return result

        # Wait reset finish
        self._module_msg.clear_msg("0")
        if self._module_msg.wait_and_take_msg("0", self._set_ret_code, 15000):
            return self._ret
        return self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def reboot(self) -> int:
        cmd_reboot = '{"request_id":"sys_reboot","work_id":"sys","action":"reboot","object":"None","data":"None"}'
        return self._send_cmd_and_wait(cmd_reboot, "sys_reboot", 2000)

    def _send_cmd_and_wait(self, cmd, request_id, timeout):
        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            cmd, request_id, self._set_ret_code, timeout
        )
        return self._ret if success else self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def _send_cmd_and_wait_verson(self, cmd, request_id, timeout):
        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            cmd, request_id, self._set_data_code, timeout
        )
        return self._ret if success else self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def _send_cmd_and_wait_lsmode(self, cmd, request_id, timeout):
        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            cmd, request_id, self._set_mode_code, timeout
        )
        return self._ret if success else self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def _set_ret_code(self, msg):
        self._ret = (
            msg["error"]["code"]
            if "error" in msg and "code" in msg["error"]
            else self._MODULE_LLM_RESPONSE_PARSE_FAILED
        )

    def _set_data_code(self, msg):
        if "error" in msg and "code" in msg["error"]:
            code = msg["error"]["code"]
            if code == 0 and "data" in msg:
                self._ret = msg["data"]
            elif code == -3:
                self._ret = "v1.0"
            else:
                self._ret = code
        else:
            self._ret = self._MODULE_LLM_RESPONSE_PARSE_FAILED

    def _set_mode_code(self, msg):
        if "error" in msg and "code" in msg["error"]:
            code = msg["error"]["code"]
            if code == 0 and "data" in msg:
                self._ret = [
                    {"type": item["type"], "mode": item["mode"]}
                    for item in msg["data"]
                    if "type" in item and "mode" in item
                ]
            else:
                self._ret = code
        else:
            self._ret = self._MODULE_LLM_RESPONSE_PARSE_FAILED

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _free_temp(self):
        self._llm_work_id = None
        self._ret = self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT


class ApiLlm:
    _MODULE_LLM_OK = 0
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None
        self._is_msg_finish = None
        self._on_result = None

    def setup(
        self,
        prompt="",
        model="qwen2.5-0.5B-prefill-20e",
        response_format="llm.utf-8.stream",
        input="llm.utf-8.stream",
        enoutput=True,
        enkws=True,
        max_token_len=127,
        request_id="llm_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "llm",
            "action": "setup",
            "object": "llm.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
                "enkws": enkws,
                "max_token_len": max_token_len,
                "prompt": prompt,
            },
        }
        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 30000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def inference(self, work_id, input_data, request_id="llm_inference") -> str:
        cmd = {
            "request_id": request_id,
            "work_id": work_id,
            "action": "inference",
            "object": "llm.utf-8.stream",
            "data": {"delta": input_data, "index": 0, "finish": True},
        }
        self._module_msg.send_cmd(ujson.dumps(cmd))
        return self._MODULE_LLM_OK

    def inference_and_wait_result(
        self, work_id, input_data, on_result, timeout=5000, request_id="llm_inference"
    ) -> int:
        self.inference(work_id, input_data, request_id)
        self._is_msg_finish = False
        self._on_result = on_result

        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            self._module_msg.update()
            if self._module_msg.take_msg(request_id, self._on_inference_result):
                start_time = time.ticks_ms()

            if self._is_msg_finish:
                break

        self._free_temp()

        return self._MODULE_LLM_OK

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _on_inference_result(self, msg):
        if "data" in msg and "delta" in msg["data"]:
            if self._on_result:
                self._on_result(msg["data"]["delta"])
        if "data" in msg and "finish" in msg["data"]:
            self._is_msg_finish = msg["data"]["finish"]

    def _free_temp(self):
        self._llm_work_id = None
        self._is_msg_finish = None
        self._on_result = None


class ApiAudio:
    _MODULE_LLM_OK = 0
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._audio_work_id = None

    def setup(
        self,
        capcard=0,
        capdevice=0,
        cap_volume=0.5,
        playcard=0,
        playdevice=1,
        play_volume=0.15,
        request_id="audio_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "audio",
            "action": "setup",
            "object": "audio.setup",
            "data": {
                "capcard": capcard,
                "capdevice": capdevice,
                "capVolume": cap_volume,
                "playcard": playcard,
                "playdevice": playdevice,
                "playVolume": play_volume,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_audio_work_id, 5000
        )

        ret_work_id = self._audio_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def _set_audio_work_id(self, msg):
        if "work_id" in msg:
            self._audio_work_id = msg["work_id"]

    def _free_temp(self):
        self._audio_work_id = None


class ApiCamera:
    _MODULE_LLM_OK = 0
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._camera_work_id = None

    def setup(
        self,
        input="/dev/video0",
        frame_width=320,
        frame_height=320,
        enoutput=False,
        response_format="camera.raw",
        request_id="camera_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "camera",
            "action": "setup",
            "object": "camera.setup",
            "data": {
                "response_format": response_format,
                "input": input,
                "frame_width": frame_width,
                "frame_height": frame_height,
                "enoutput": enoutput,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_camera_work_id, 10000
        )

        ret_work_id = self._camera_work_id if success else ""
        self._free_temp()

        return ret_work_id

    def _set_camera_work_id(self, msg):
        if "work_id" in msg:
            self._camera_work_id = msg["work_id"]

    def _free_temp(self):
        self._camera_work_id = None


class ApiTts:
    _MODULE_LLM_OK = 0
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None
        self._ret = self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def setup(
        self,
        model="single_speaker_english_fast",
        response_format="sys.pcm",
        input="tts.utf-8.stream",
        enoutput=False,
        enkws=False,
        request_id="tts_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "tts",
            "action": "setup",
            "object": "tts.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
                "enkws": enkws,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 10000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def inference(self, work_id, input_data, timeout=0, request_id="tts_inference"):
        cmd = {
            "request_id": request_id,
            "work_id": work_id,
            "action": "inference",
            "object": "tts.utf-8.stream",
            "data": {"delta": input_data, "index": 0, "finish": True},
        }

        if timeout == 0:
            self._module_msg.send_cmd(ujson.dumps(cmd))
            return self._MODULE_LLM_OK

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_ret_code, timeout
        )

        return self._ret if success else self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _set_ret_code(self, msg):
        if "error" in msg and "code" in msg["error"]:
            self._ret = msg["error"]["code"]

    def _free_temp(self):
        self._llm_work_id = None
        self._ret = self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT


class ApiMelotts:
    _MODULE_LLM_OK = 0
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None
        self._ret = self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def setup(
        self,
        model="melotts_zh-cn",
        response_format="sys.pcm",
        input="tts.utf-8.stream",
        enoutput=False,
        request_id="melotts_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "melotts",
            "action": "setup",
            "object": "melotts.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 15000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def inference(self, work_id, input_data, timeout=0, request_id="tts_inference"):
        cmd = {
            "request_id": request_id,
            "work_id": work_id,
            "action": "inference",
            "object": "tts.utf-8.stream",
            "data": {"delta": input_data, "index": 0, "finish": True},
        }

        if timeout == 0:
            self._module_msg.send_cmd(ujson.dumps(cmd))
            return self._MODULE_LLM_OK

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_ret_code, timeout
        )

        return self._ret if success else self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _set_ret_code(self, msg):
        if "error" in msg and "code" in msg["error"]:
            self._ret = msg["error"]["code"]

    def _free_temp(self):
        self._llm_work_id = None
        self._ret = self._MODULE_LLM_WAIT_RESPONSE_TIMEOUT


class ApiKws:
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None

    def setup(
        self,
        kws="HELLO",
        model="sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01",
        response_format="kws.bool",
        input="sys.pcm",
        enoutput=True,
        enaudio=True,
        request_id="kws_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "kws",
            "action": "setup",
            "object": "kws.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
                "enwake_audio": enaudio,
                "kws": kws,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 30000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _free_temp(self):
        self._llm_work_id = None


class ApiAsr:
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None

    def setup(
        self,
        model="sherpa-ncnn-streaming-zipformer-20M-2023-02-17",
        response_format="asr.utf-8.stream",
        input="sys.pcm",
        enoutput=True,
        enkws=False,
        rule1=2.4,
        rule2=1.2,
        rule3=30.0,
        request_id="asr_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "asr",
            "action": "setup",
            "object": "asr.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
                "enkws": enkws,
                "rule1": rule1,
                "rule2": rule2,
                "rule3": rule3,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 10000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _free_temp(self):
        self._llm_work_id = None


class ApiVad:
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None

    def setup(
        self,
        model="silero-vad",
        response_format="vad.bool",
        input="sys.pcm",
        enoutput=True,
        request_id="vad_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "vad",
            "action": "setup",
            "object": "vad.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 30000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _free_temp(self):
        self._llm_work_id = None


class ApiWhisper:
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._llm_work_id = None

    def setup(
        self,
        model="whisper-tiny",
        response_format="asr.utf-8",
        input="sys.pcm",
        enoutput=True,
        language="en",
        request_id="whisper_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "whisper",
            "action": "setup",
            "object": "whisper.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "language": language,
                "enoutput": enoutput,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_llm_work_id, 30000
        )

        ret_work_id = self._llm_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def _set_llm_work_id(self, msg):
        if "work_id" in msg:
            self._llm_work_id = msg["work_id"]

    def _free_temp(self):
        self._llm_work_id = None


class ApiYolo:
    _MODULE_LLM_WAIT_RESPONSE_TIMEOUT = -97

    def __init__(self, module_msg):
        self._module_msg = module_msg
        self._yolo_work_id = None

    def setup(
        self,
        model="yolo11n",
        response_format="yolo.box.stream",
        input="yolo.jpg.base64",
        enoutput=True,
        request_id="yolo_setup",
    ) -> str:
        cmd = {
            "request_id": request_id,
            "work_id": "yolo",
            "action": "setup",
            "object": "yolo.setup",
            "data": {
                "model": model,
                "response_format": response_format,
                "input": input,
                "enoutput": enoutput,
            },
        }

        success = self._module_msg.send_cmd_and_wait_to_take_msg(
            ujson.dumps(cmd), request_id, self._set_yolo_work_id, 10000
        )

        ret_work_id = self._yolo_work_id if success else ""
        self._free_temp()
        return ret_work_id

    def _set_yolo_work_id(self, msg):
        if "work_id" in msg:
            self._yolo_work_id = msg["work_id"]

    def _free_temp(self):
        self._yolo_work_id = None


class LlmModule:
    def __init__(self, uart_id=1, tx=17, rx=16) -> None:
        self._uart = UART(
            uart_id,
            tx=tx,
            rx=rx,
            baudrate=115200,
            bits=8,
            parity=None,
            stop=1,
            rxbuf=1024,
        )

        # Create components
        self.comm = ModuleComm(self._uart)
        self.msg = ModuleMsg(self.comm)
        self.sys = ApiSys(self.msg)
        self.llm = ApiLlm(self.msg)
        self.audio = ApiAudio(self.msg)
        self.tts = ApiTts(self.msg)
        self.melotts = ApiMelotts(self.msg)
        self.kws = ApiKws(self.msg)
        self.asr = ApiAsr(self.msg)
        self.camera = ApiCamera(self.msg)
        self.yolo = ApiYolo(self.msg)
        self.vad = ApiVad(self.msg)
        self.whisper = ApiWhisper(self.msg)

        # Temp voice assistant callback setup
        self.on_keyword_detected = None
        self.on_asr_data_input = None
        self.on_llm_data_input = None

        # Latest work id and error code
        self.latest_llm_work_id = "llm"
        self.latest_audio_work_id = "audio"
        self.latest_tts_work_id = "tts"
        self.latest_melotts_work_id = "melotts"
        self.latest_kws_work_id = "kws"
        self.latest_asr_work_id = "asr"
        self.latest_camera_work_id = "camera"
        self.latest_yolo_work_id = "yolo"
        self.latest_vad_work_id = "vad"
        self.latest_whisper_work_id = "whisper"
        self.latest_error_code = 0
        self.version = 0

        # Voice assistant preset
        self._preset_va = None

    def update(self) -> None:
        """Update module."""
        self.msg.update()
        if self._preset_va:
            self._preset_va.update()

    def check_connection(self) -> bool:
        """

        Returns:
            bool: Is module connection ok
        """
        result = self.sys.ping() == 0
        self.version = self.sys.version()
        return result

    def get_version(self):
        return self.sys.version()

    def ls_mode(self):
        return self.sys.lsmode()

    def rm_mode(
        self,
        model=None,
    ) -> str:
        self.latest_error_code = self.sys.rmmode(model)
        return self.latest_error_code

    def get_response_msg_list(self) -> list:
        """

        Returns:
            list: Module's response message (dict) list.
        """
        return self.msg.response_msg_list

    def clear_response_msg_list(self) -> None:
        """Clear module's response message list."""
        self.msg.response_msg_list.clear()

    def sys_ping(self) -> int:
        self.latest_error_code = self.sys.ping()
        return self.latest_error_code

    def sys_reset(self, wait_reset_finish=True) -> int:
        self.latest_error_code = self.sys.reset(wait_reset_finish)
        return self.latest_error_code

    def sys_reboot(self) -> int:
        self.latest_error_code = self.sys.reboot()
        return self.latest_error_code

    def llm_setup(
        self,
        prompt="",
        model="qwen2.5-0.5B-prefill-20e",
        response_format="llm.utf-8.stream",
        input=None,
        enoutput=True,
        enkws=None,
        max_token_len=127,
        request_id="llm_setup",
    ) -> str:
        if self.version == "v1.0":
            model = "qwen2.5-0.5b"

        if input is None:
            input = "llm.utf-8.stream" if self.version == "v1.0" else ["llm.utf-8.stream"]

        if enkws:
            if self.version == "v1.0":
                enkws = True
            else:
                input.append(enkws)
        else:
            enkws = bool(enkws)

        self.latest_llm_work_id = self.llm.setup(
            prompt, model, response_format, input, enoutput, enkws, max_token_len, request_id
        )
        return self.latest_llm_work_id

    def llm_inference(self, work_id, input_data, request_id="llm_inference") -> str:
        self.latest_error_code = self.llm.inference(work_id, input_data, request_id)
        return self.latest_error_code

    def audio_setup(
        self,
        capcard=0,
        capdevice=0,
        cap_volume=0.5,
        playcard=0,
        playdevice=1,
        play_volume=0.15,
        request_id="audio_setup",
    ) -> str:
        self.latest_audio_work_id = self.audio.setup(
            capcard, capdevice, cap_volume, playcard, playdevice, play_volume, request_id
        )
        return self.latest_audio_work_id

    def camera_setup(
        self,
        request_id="camera_setup",
        input="/dev/video0",
        frame_width=320,
        frame_height=320,
        enoutput=False,
        response_format="camera.raw",
    ) -> str:
        self.latest_camera_work_id = self.camera.setup(
            input, frame_width, frame_height, enoutput, response_format, request_id
        )
        return self.latest_camera_work_id

    def yolo_setup(
        self,
        model="yolo11n",
        response_format="yolo.box.stream",
        input="camera.1000",
        enoutput=True,
        request_id="yolo_setup",
    ) -> str:
        self.latest_yolo_work_id = self.yolo.setup(
            model, response_format, input, enoutput, request_id
        )
        return self.latest_yolo_work_id

    def tts_setup(
        self,
        language="en_US",
        model="single_speaker_english_fast",
        response_format="sys.pcm",
        input=None,
        enoutput=False,
        enkws=None,
        request_id="tts_setup",
    ) -> str:
        if self.version == "v1.0":
            response_format = "tts.base64.wav"
        if language == "zh_CN":
            model = "single_speaker_fast"
        if input is None:
            input = "tts.utf-8.stream" if self.version == "v1.0" else ["tts.utf-8.stream"]

        if enkws:
            if self.version == "v1.0":
                enkws = True
            else:
                input.append(enkws)
        else:
            enkws = bool(enkws)

        self.latest_tts_work_id = self.tts.setup(
            model, response_format, input, enoutput, enkws, request_id
        )
        return self.latest_tts_work_id

    def tts_inference(self, work_id, input_data, timeout=0, request_id="tts_inference") -> int:
        self.latest_error_code = self.tts.inference(work_id, input_data, timeout, request_id)
        return self.latest_error_code

    def melotts_setup(
        self,
        language="en_US",
        model="melotts_zh-cn",
        response_format="sys.pcm",
        input=None,
        enoutput=False,
        enkws=None,
        request_id="tts_setup",
    ) -> str:
        if language == "zh_CN":
            model = "melotts_zh-cn"
        if input is None:
            input = ["tts.utf-8.stream"]

        if enkws:
            input.append(enkws)

        self.latest_melotts_work_id = self.melotts.setup(
            model, response_format, input, enoutput, request_id
        )
        return self.latest_melotts_work_id

    def melotts_inference(self, work_id, input_data, timeout=0, request_id="tts_inference") -> int:
        self.latest_error_code = self.melotts.inference(work_id, input_data, timeout, request_id)
        return self.latest_error_code

    def kws_setup(
        self,
        kws="HELLO",
        language="en_US",
        model="sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01",
        response_format="kws.bool",
        input="sys.pcm",
        enoutput=True,
        enaudio=True,
        request_id="kws_setup",
    ) -> str:
        if language == "zh_CN":
            model = "sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01"
        self.latest_kws_work_id = self.kws.setup(
            kws, model, response_format, input, enoutput, enaudio, request_id
        )
        return self.latest_kws_work_id

    def asr_setup(
        self,
        language="en_US",
        model="sherpa-ncnn-streaming-zipformer-20M-2023-02-17",
        response_format="asr.utf-8.stream",
        input=None,
        enoutput=True,
        enkws=None,
        rule1=2.4,
        rule2=1.2,
        rule3=30.0,
        request_id="asr_setup",
    ) -> str:
        if input is None:
            input = "sys.pcm" if self.version == "v1.0" else ["sys.pcm"]
        if language == "zh_CN":
            model = "sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23"
        if enkws:
            if self.version == "v1.0":
                enkws = True
            else:
                input.append(enkws)
        else:
            enkws = bool(enkws)

        self.latest_asr_work_id = self.asr.setup(
            model, response_format, input, enoutput, enkws, rule1, rule2, rule3, request_id
        )
        return self.latest_asr_work_id

    def vad_setup(
        self,
        model="silero-vad",
        response_format="kws.bool",
        input=None,
        enoutput=True,
        enkws=None,
        request_id="kws_setup",
    ) -> str:
        if input is None:
            input = ["sys.pcm"]
        if enkws:
            input.append(enkws)
        self.latest_vad_work_id = self.vad.setup(
            model, response_format, input, enoutput, request_id
        )
        return self.latest_vad_work_id

    def whisper_setup(
        self,
        language="en",
        model="whisper-tiny",
        response_format="asr.utf-8",
        input=None,
        enoutput=True,
        enkws=None,
        envad=None,
        request_id="asr_setup",
    ) -> str:
        if input is None:
            input = ["sys.pcm"]
        if enkws:
            input.append(enkws)
        if envad:
            input.append(envad)
        self.latest_whisper_work_id = self.whisper.setup(
            model, response_format, input, enoutput, language, request_id
        )
        return self.latest_whisper_work_id

    def get_latest_llm_work_id(self) -> str:
        return self.latest_llm_work_id

    def get_latest_audio_work_id(self) -> str:
        return self.latest_audio_work_id

    def get_latest_tts_work_id(self) -> str:
        return self.latest_tts_work_id

    def get_latest_melotts_work_id(self) -> str:
        return self.latest_melotts_work_id

    def get_latest_kws_work_id(self) -> str:
        return self.latest_kws_work_id

    def get_latest_asr_work_id(self) -> str:
        return self.latest_asr_work_id

    def get_latest_camera_work_id(self) -> str:
        return self.latest_camera_work_id

    def get_latest_yolo_work_id(self) -> str:
        return self.latest_yolo_work_id

    def get_latest_vad_work_id(self) -> str:
        return self.latest_vad_work_id

    def get_latest_whisper_work_id(self) -> str:
        return self.latest_whisper_work_id

    def get_latest_error_code(self) -> int:
        return self.latest_error_code

    def begin_voice_assistant(
        self,
        wake_up_keyword="HELLO",
        prompt="",
        language="en_US",
    ) -> bool:
        self._preset_va = PresetVoiceAssistant(self)
        self._preset_va.on_keyword_detected = self.on_keyword_detected
        self._preset_va.on_asr_data_input = self.on_asr_data_input
        self._preset_va.on_llm_data_input = self.on_llm_data_input
        return self._preset_va.begin(
            wake_up_keyword=wake_up_keyword, prompt=prompt, language=language
        )

    def set_voice_assistant_on_keyword_detected_callback(self, on_keyword_detected) -> None:
        """

        Args:
            on_keyword_detected (): e.g. on_keyword_detected()
        """
        self.on_keyword_detected = on_keyword_detected
        if self._preset_va:
            self._preset_va.on_keyword_detected = on_keyword_detected

    def set_voice_assistant_on_asr_data_input_callback(self, on_asr_data_input) -> None:
        """

        Args:
            on_asr_data_input (data: str, is_data_finish: bool, data_index: int): e.g. on_asr_data_input(data: str, is_data_finish: bool, data_index: int)
        """
        self.on_asr_data_input = on_asr_data_input
        if self._preset_va:
            self._preset_va.on_asr_data_input = on_asr_data_input

    def set_voice_assistant_on_llm_data_input_callback(self, on_llm_data_input) -> None:
        """

        Args:
            on_llm_data_input (data: str, is_data_finish: bool, data_index: int): e.g. on_llm_data_input(data: str, is_data_finish: bool, data_index: int)
        """
        self.on_llm_data_input = on_llm_data_input
        if self._preset_va:
            self._preset_va.on_llm_data_input = on_llm_data_input


class PresetVoiceAssistant:
    def __init__(self, module_llm) -> None:
        self._module_llm = module_llm
        self._work_id = {}
        self.on_keyword_detected = None
        self.on_asr_data_input = None
        self.on_llm_data_input = None
        self.version = None

    def begin(self, wake_up_keyword="HELLO", prompt="", language="en_US") -> bool:
        # Check connection
        print("[VoiceAssistant] Check connection..")
        if not self._module_llm.check_connection():
            return False

        self.version = self._module_llm.get_version()
        # Reset module
        print("[VoiceAssistant] Reset ModuleLLM..")
        self._module_llm.sys_reset(True)

        # Setup audio
        print("[VoiceAssistant] Setup module Audio..")
        self._work_id["audio"] = self._module_llm.audio_setup()
        if not self._work_id["audio"]:
            return False

        # Setup KWS
        print("[VoiceAssistant] Setup module KWS..")
        self._work_id["kws"] = self._module_llm.kws_setup(kws=wake_up_keyword, language=language)
        if not self._work_id["kws"]:
            return False

        # Setup ASR
        print("[VoiceAssistant] Setup module ASR..")
        if self.version == "v1.0":
            self._work_id["asr"] = self._module_llm.asr_setup(
                input="sys.pcm", enkws=True, language=language
            )
        else:
            self._work_id["asr"] = self._module_llm.asr_setup(
                input=["sys.pcm", self._work_id["kws"]], language=language
            )

        if not self._work_id["asr"]:
            return False

        # Setup LLM
        print("[VoiceAssistant] Setup module LLM..")
        if self.version == "v1.0":
            self._work_id["llm"] = self._module_llm.llm_setup(
                prompt=prompt, input=self._work_id["asr"], enkws=True
            )
        else:
            self._work_id["llm"] = self._module_llm.llm_setup(
                prompt=prompt, input=[self._work_id["asr"], self._work_id["kws"]]
            )
        if not self._work_id["llm"]:
            return False

        # Setup TTS
        print("[VoiceAssistant] Setup module TTS..")
        if self.version == "v1.0":
            self._work_id["tts"] = self._module_llm.tts_setup(
                input=self._work_id["llm"], enkws=True, language=language
            )
        else:
            self._work_id["tts"] = self._module_llm.melotts_setup(
                input=[self._work_id["llm"], self._work_id["kws"]], enkws=None, language=language
            )

        if not self._work_id["tts"]:
            return False

        print("[VoiceAssistant] Voice assistant ready")
        return True

    def update(self) -> None:
        for msg in self._module_llm.get_response_msg_list():
            # Handle KWS response
            if self.on_keyword_detected and msg["work_id"] == self._work_id["kws"]:
                self.on_keyword_detected()
                continue

            # Handle ASR response
            if self.on_asr_data_input and msg["work_id"] == self._work_id["asr"]:
                if msg["object"] == "asr.utf-8.stream":
                    self.on_asr_data_input(
                        msg["data"]["delta"], msg["data"]["finish"], msg["data"]["index"]
                    )
                continue

            # Handle LLM response
            if self.on_llm_data_input and msg["work_id"] == self._work_id["llm"]:
                if msg["object"] == "llm.utf-8.stream":
                    self.on_llm_data_input(
                        msg["data"]["delta"], msg["data"]["finish"], msg["data"]["index"]
                    )
                continue

        self._module_llm.clear_response_msg_list()
