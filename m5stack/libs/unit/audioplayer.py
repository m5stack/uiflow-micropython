# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import sys
import time
import machine

if sys.platform != "esp32":
    from typing import Literal


class AudioPlayerUnit:
    """Create an AudioPlayerUnit object.

    :param int id: The UART ID of the device. Default is 2.
    :param port: The UART port of the device.
    :type port: list | tuple
    :param bool verbose: The verbose mode of the device. Default is False.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import AudioPlayerUnit

            audio_player_0 = AudioPlayerUnit(2, port=(33, 32))
    """

    def __init__(self, id: Literal[0, 1, 2] = 2, port: list | tuple = None, verbose=False):
        self.uart = machine.UART(id, tx=port[1], rx=port[0])
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self.uart.irq(handler=self._handler, trigger=machine.UART.IRQ_RXIDLE)
        self.uart.read()
        self.verbose = verbose
        self.raw_message = ""
        self.command_num = 0
        self.is_recieved = False
        self.received_data = [False]
        self.play_status = None

    def _handler(self, uart) -> None:
        data = uart.read()
        if data is not None and len(data) > 5:
            self.verbose and print(
                "Received message:", " ".join(f"0x{byte:02X}" for byte in data).split()
            )
            # self.verbose and print(data[0] == self.command)
            # self.verbose and print(data[1] == (~self.command) & 0xFF)
            # if self.retun_value is not None:
            #     self.verbose and print(data[2:4] == bytes(self.retun_value))
            # else:
            #     self.verbose and print("True")
            # self.verbose and print(
            #     data[-1]
            #     == (
            #         self.command + ~self.command
            #         & 0xFF
            #         + sum(data[4:-1])
            #         + (0 if self.retun_value is None else sum(self.retun_value))
            #     )
            #     & 0xFF
            # )
            # self.verbose and print(
            #     (
            #         hex(
            #             self.command
            #             + (~self.command & 0xFF)
            #             + sum(data[4:-1])
            #             + (0 if self.retun_value is None else sum(self.retun_value))
            #             & 0xFF
            #         )
            #     )
            # )
            if (data[0] == 0x0A and self.command == 0x05) or (
                data[0] == self.command and data[1] == (~self.command & 0xFF)
            ):
                if (self.retun_value is None or data[2:4] == bytes(self.retun_value)) and data[
                    -1
                ] == (
                    self.command + ~self.command
                    & 0xFF
                    + sum(data[4:-1])
                    + (0 if self.retun_value is None else sum(self.retun_value))
                ) & 0xFF:
                    self.is_recieved = True
                    self.raw_message = " ".join(f"0x{byte:02X}" for byte in data)
                    self.received_data = data[4:-1]
                    self.verbose and print(
                        (
                            "Parsed Data:",
                            " ".join(f"0x{byte:02X}" for byte in self.received_data).split(),
                        )
                    )

                    # self.check_tick_callback()
            else:
                self.verbose and print("Invalid frame received: header/footer mismatch")
                uart.read()

    def _wait_for_message(self, time_out: int = 500):
        self.is_recieved = False
        self.received_data = [False]
        start_time = time.ticks_ms()
        while not self.is_recieved:
            if time.ticks_ms() - start_time > time_out:
                if self.verbose:
                    print(f"Message timeout after {time_out}ms")
                return [-1] * 11
            time.sleep_ms(10)
        return self.received_data

    def _send_message(self, command: int, data: list[int], retun_value=None) -> None:
        message = [command, (~command) & 0xFF, len(data)] + data
        sum = 0
        for i in message:
            sum += i

        sum = sum & 0xFF
        # print(f"Sum:0x{sum:02X}")
        message.append(sum & 0xFF)
        if len(message) > 32:
            raise ValueError("Message length is too long, max length is 32")
        self.command = command
        self.retun_value = retun_value
        self.verbose and print("--> ", " ".join(f"0x{byte:02X}" for byte in message))
        self.uart.write(bytes(message))

    def check_play_status(self):
        """Check the play status of the audio player.

        :returns: The play status of the audio player.
        :rtype: bool

        UiFlow2 Code Block:

            |check_play_status.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.check_play_status()
        """
        self._send_message(0x04, [0x00], [0x02, 0x00])
        return self._wait_for_message(500)[0]

    def play_audio(self) -> int:  # 可从暂停处开始播放
        """Play the audio.

        :returns: The play status of the audio player.
        :rtype: int

        UiFlow2 Code Block:

            |play_audio.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.play_audio()
        """
        self._send_message(0x04, [0x01], [0x02, 0x00])
        return self._wait_for_message(500)[0]

    def pause_audio(self) -> int:  # 暂停播放
        """Pause the audio.

        :returns: The play status of the audio player.
        :rtype: bool

        UiFlow2 Code Block:

            |pause_audio.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.pause_audio()
        """
        self._send_message(0x04, [0x02], [0x02, 0x00])
        return self._wait_for_message(500)[0]

    def stop_audio(self) -> int:  # 停止播放(从头开始)
        """Stop the audio.

        :returns: The play status of the audio player.
        :rtype: int

        UiFlow2 Code Block:

            |stop_audio.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.stop_audio()
        """
        self._send_message(0x04, [0x03], [0x02, 0x00])
        return self._wait_for_message(500)[0]

    def next_audio(self) -> int:
        """Play the next audio.

        :returns: Current play audio index.
        :rtype: int

        UiFlow2 Code Block:

            |next_audio.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.next_audio()
        """
        self._send_message(0x04, [0x05], [0x03, 0x0E])
        buf = self._wait_for_message(600)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def previous_audio(self) -> int:
        """Play the previous audio.

        :returns: Current play audio index.
        :rtype: int

        UiFlow2 Code Block:

            |previous_audio.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.previous_audio()
        """
        self._send_message(0x04, [0x04], [0x03, 0x0E])
        buf = self._wait_for_message(600)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def play_audio_by_index(self, index: int) -> int:
        """Play audio by index number.

        :param int index: The index of the audio to play.
        :returns: Current play audio index.
        :rtype: int

        UiFlow2 Code Block:

            |play_audio_by_index.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.play_audio_by_index(1)
        """
        index_high = (index >> 8) & 0xFF
        index_low = index & 0xFF
        self._send_message(0x04, [0x06, index_high, index_low], [0x03, 0x0E])
        buf = self._wait_for_message(500)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def play_audio_by_name(self, name: str) -> int:
        """Play audio by file name.

        :param str name: The name of the audio file to play.
        :returns: Current play audio index.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.play_audio_by_name("music.mp3")
        """
        hex_values = list(bytearray(name, "utf-8"))
        if len(hex_values) <= 27:
            self._send_message(0x04, [0x07] + hex_values, [0x03, 0x0E])
            return self._wait_for_message(500)[0]
        raise ValueError("Name length is too long, max length is 27")

    def get_current_online_device_type(self) -> int:
        """Get the current online device type.

        :returns: Device type code
        :rtype: int

            Device type:
                - 1: USB
                - 2: SD
                - 3: UDISK or SD
                - 4: Flash
                - 5: Flash or UDISK
                - 6: Flash or SD

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_current_online_device_type()
        """
        self._send_message(0x04, [0x08], [0x02, 0x08])
        return self._wait_for_message(500)[0]

    def get_current_play_device_type(self) -> int:
        """Get the current play device type.

        :returns: Device type code (0: USB, 1: SD, 2: SPI FLASH).
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_current_play_device_type()
        """
        self._send_message(0x04, [0x09], [0x02, 0x09])
        return self._wait_for_message(500)[0]

    def get_total_audio_number(self) -> int:
        """Get the total number of audio files available.

        :returns: The total number of audio files.
        :rtype: int

        UiFlow2 Code Block:

            |get_total_audio_number.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_total_audio_number()
        """
        self._send_message(0x04, [0x0D], [0x03, 0x0D])
        buf = self._wait_for_message(500)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def get_current_audio_number(self) -> int:
        """Get the current audio file number.

        :returns: The current audio file number.
        :rtype: int

        UiFlow2 Code Block:

            |get_current_audio_number.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_current_audio_number()
        """
        self._send_message(0x04, [0x0E], [0x03, 0x0E])
        buf = self._wait_for_message(500)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def play_current_audio_at_time(self, time_min: int, time_sec: int) -> None:
        """Play the current audio from a specific time position.

        :param int time_min: The minute position to start playing from.
        :param int time_sec: The second position to start playing from.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.play_current_audio_at_time(1, 30)
        """
        self._send_message(0x04, [0x0F, time_min, time_sec])
        time.sleep_ms(100)

    def play_audio_at_time(self, audio_index: int, time_min: int, time_sec: int) -> None:
        """Play a specific audio file from a specific time position.

        :param int audio_index: The index of the audio file to play.
        :param int time_min: The minute position to start playing from.
        :param int time_sec: The second position to start playing from.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.play_audio_at_time(1, 0, 30)
        """
        self._send_message(
            0x04, [0x10, (audio_index >> 8) & 0xFF, audio_index & 0xFF, time_min, time_sec]
        )
        time.sleep_ms(100)

    def next_directory(self) -> None:
        """Navigate to the next directory.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.next_directory()
        """
        self._send_message(0x04, [0x13], [0x03, 0x0E])
        time.sleep_ms(100)

    def previous_directory(self) -> None:
        """Navigate to the previous directory.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.previous_directory()
        """
        self._send_message(0x04, [0x12], [0x03, 0x0E])
        time.sleep_ms(100)

    def end_audio(self) -> None:
        """End playing the current audio.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.end_audio()
        """
        self._send_message(0x04, [0x14])
        time.sleep_ms(100)

    def get_file_name(self) -> list:
        """Get the name of the current audio file.

        :returns: The name of the current audio file as a list of bytes.
        :rtype: list

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_file_name()
        """
        self._send_message(0x04, [0x15], [0x0C, 0x15])
        return self._wait_for_message(500)[0:11]

    def select_audio_num(self, audio_num: int) -> int:
        """Select an audio file by number without playing it.

        :param int audio_num: The number of the audio file to select.
        :returns: The current selected audio file number.
        :rtype: int

        UiFlow2 Code Block:

            |select_audio_num.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.select_audio_num(1)
        """
        self._send_message(0x04, [0x16, (audio_num >> 8) & 0xFF, audio_num & 0xFF], [0x03, 0x0E])
        buf = self._wait_for_message(600)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def get_file_count(self) -> int:
        """Get the total number of files in the current directory.

        :returns: The total number of files.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_file_count()
        """
        self._send_message(0x04, [0x18], [0x03, 0x18])
        buf = self._wait_for_message(500)[0:2]
        return buf[0] & 0xFF << 8 | buf[1]

    def get_total_play_time(self) -> tuple:
        """Get the total play time of the current audio file.

        :returns: A tuple containing (hour, minute, second) of the total play time.
        :rtype: tuple

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_total_play_time()
        """
        self._send_message(0x05, [0x00], [0x04, 0x00])
        buf = self._wait_for_message(500)[0:3]
        return (buf[0], buf[1], buf[2])

    def decrease_volume(self) -> None:
        """Decrease the volume of the audio player.

        UiFlow2 Code Block:

            |decrease_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.decrease_volume()
        """
        self._send_message(0x06, [0x03])
        time.sleep_ms(100)

    def increase_volume(self) -> None:
        """Increase the volume of the audio player.

        UiFlow2 Code Block:

            |increase_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.increase_volume()
        """
        self._send_message(0x06, [0x02])
        time.sleep_ms(100)

    def get_volume(self) -> int:
        """Get the current volume level of the audio player.

        :returns: The current volume level.
        :rtype: int

        UiFlow2 Code Block:

            |get_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_volume()
        """
        self._send_message(0x06, [0x00], [0x02, 0x00])
        return self._wait_for_message(600)[0]

    def set_volume(self, volume: int) -> None:
        """Set the volume level of the audio player.

        :param int volume: The volume level to set (0-30).

        UiFlow2 Code Block:

            |set_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.set_volume(15)
        """
        self._send_message(0x06, [0x01, volume])
        time.sleep_ms(100)

    def repeat_at_time(self, start_min: int, start_sec: int, end_min: int, end_sec: int) -> None:
        """Set repeat playback between two time positions.

        :param int start_min: The start minute position.
        :param int start_sec: The start second position.
        :param int end_min: The end minute position.
        :param int end_sec: The end second position.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.repeat_at_time(0, 30, 1, 30)
        """
        self._send_message(0x08, [0x00, start_min, start_sec, end_min, end_sec])
        time.sleep_ms(100)

    def end_repeat(self) -> None:
        """End the repeat playback mode.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.end_repeat()
        """
        self._send_message(0x08, [0x01])
        time.sleep_ms(100)

    def get_play_mode(self) -> int:
        """Get the current play mode.

        :returns: The current play mode.
        :rtype: int

        UiFlow2 Code Block:

            |get_play_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.get_play_mode()
        """
        self._send_message(0x0B, [0x00], [0x02, 0x00])
        return self._wait_for_message(500)[0]

    def set_play_mode(self, mode: int) -> None:
        """Set the play mode.

        :param int mode: The play mode to set.

        UiFlow2 Code Block:

            |set_play_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.set_play_mode(1)
        """
        self._send_message(0x0B, [0x01, mode])
        time.sleep_ms(100)

    def start_combine_play(self, mode: int, data: list[int]) -> None:
        """Start combined play mode.

        :param int mode: The combined play mode.
        :param list[int] data: The data for combined play.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.start_combine_play(1, [1, 2, 3])
        """
        self._send_message(0x0C, [mode] + data)
        time.sleep_ms(100)

    def end_combine_play(self) -> None:
        """End the combined play mode.

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.end_combine_play()
        """
        self._send_message(0x0C, [0x02])
        time.sleep_ms(100)

    def into_sleep_mode(self) -> bool:
        """Put the audio player into sleep mode.

        :returns: True if the command was sent successfully.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                audio_player_0.into_sleep_mode()
        """
        self.uart.write(bytes([0x0D, 0xF3, 0x01, 0x01, 0x02]))
        return True
