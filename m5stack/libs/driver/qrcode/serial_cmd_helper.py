# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time


class CmdStatus:
    SUCCESS = 0
    INVALID_PARAM = 1
    TIMEOUT = 2
    ACK_MISMATCH = 3


class SerialCmdHelper:
    def __init__(self, serial, debug: bool = False):
        self.serial = serial
        self.debug = debug

    def _log_debug(self, message: str):
        if self.debug:
            print(f"\n[DEBUG] {message}")

    def _format_bytes(self, data: bytes) -> str:
        return " ".join(f"{b:02X}" for b in data)

    def cmd(self, cmd, cmd_ack=None, timeout_ms: int = 1000) -> CmdStatus:
        """
        发送串口命令并处理响应。
        :param cmd: 要发送的命令。
        :param cmd_ack: 期望的响应 (None 表示不期望响应)。
        :param timeout_ms: 等待响应的超时时间 (仅在 cmd_ack 不为 None 时生效)。
        :return: 执行状态。
        """
        tmp = self.serial.read()  # flush rx buffer
        self._log_debug(f"TX: {self._format_bytes(cmd)}")
        self.serial.write(cmd)
        if cmd_ack is None:
            return CmdStatus.SUCCESS
        ack_length = len(cmd_ack)
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < timeout_ms:
            if self.serial.any() >= ack_length:
                rx = self.serial.read(ack_length)
                self._log_debug(f"RX: {self._format_bytes(rx)}")
                if rx == cmd_ack:
                    return CmdStatus.SUCCESS
                else:
                    return CmdStatus.ACK_MISMATCH
            time.sleep_ms(1)
        return CmdStatus.TIMEOUT

    def cmd_retry(
        self,
        cmd: bytes,
        cmd_ack: bytes,
        timeout_ms: int = 1000,
        retries: int = 3,
        retry_delay_ms: int = 100,
    ) -> CmdStatus:
        """
        发送命令并进行重试。
        :param retries: 重试次数。
        :param retry_delay_ms: 每次重试之间的延迟时间 (毫秒)。
        :return: 执行状态。
        """
        for attempt in range(retries):
            self._log_debug(f"Attempt {attempt + 1}/{retries}")
            status = self.cmd(cmd, cmd_ack, timeout_ms)
            if status == CmdStatus.SUCCESS:
                return CmdStatus.SUCCESS
            self._log_debug(f"Retry after {retry_delay_ms} ms")
            time.sleep_ms(retry_delay_ms)
        return status
