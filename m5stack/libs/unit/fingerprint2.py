# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import machine


class FingerprintPacket:
    START_CODE = b"\xEF\x01"
    default_address = b"\xFF\xFF\xFF\xFF"

    def __init__(self, pkt_type, payload=b""):
        self.type = pkt_type
        self.payload = payload[:64]
        self.address = FingerprintPacket.default_address

    @staticmethod
    def set_default_address(addr_bytes):
        if not isinstance(addr_bytes, (bytes, bytearray)) or len(addr_bytes) != 4:
            raise ValueError("Address must be 4 bytes")
        FingerprintPacket.default_address = bytes(addr_bytes)

    def checksum(self):
        length = len(self.payload) + 2
        total = self.type + ((length >> 8) & 0xFF) + (length & 0xFF)
        total += sum(self.payload)
        return total & 0xFFFF

    def build_packet(self):
        length = len(self.payload) + 2
        packet = bytearray()
        packet += self.START_CODE
        packet += self.address
        packet.append(self.type)
        packet += length.to_bytes(2, "big")
        packet += self.payload
        packet += self.checksum().to_bytes(2, "big")
        return packet


class SerialCmdHelper:
    def __init__(self, serial, debug=False):
        self.serial = serial
        self.debug = debug

    def _log_debug(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    def _format_bytes(self, data):
        return " ".join(f"{b:02X}" for b in data)

    def _flush(self):
        while self.serial.any():
            self.serial.read()

    def cmd(self, pkt: FingerprintPacket, timeout_ms=1000):
        self._flush()
        data = pkt.build_packet()
        self._log_debug(f"TX: {self._format_bytes(data)}")
        self.serial.write(data)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
            if self.serial.any() >= 12:
                time.sleep_ms(5)
                rx = self.serial.read()
                self._log_debug(f"RX: {self._format_bytes(rx)}")
                return rx
            time.sleep_ms(1)
        self._log_debug("RX Timeout")
        return None


class Fingerprint2Unit:
    def __init__(self, id: int = 2, port: list | tuple = None, debug=False):
        if id not in (0, 1, 2):
            raise ValueError("Parameter 'id' must be 0, 1, or 2.")
        self.id = id
        self.serial = machine.UART(self.id, baudrate=115200, tx=port[1], rx=port[0], rxbuf=2048)
        self.helper = SerialCmdHelper(self.serial, debug=debug)
        self.debug = debug
        self.max_id = 99  # 最大指纹容量 100 枚，范围 0 ~ 99

    def _log_debug(self, message):
        if self.debug:
            print(f"[DEBUG] {message}")

    def _format_bytes(self, data):
        return " ".join(f"{b:02X}" for b in data)

    def _parse_response(self, rx):
        if rx is None:
            return False
        if len(rx) < 12:
            return False
        if rx[0] != 0xEF or rx[1] != 0x01:
            return False
        return rx[9] == 0x00

    def send_cmd(self, cmd_bytes, timeout_ms=1000):
        pkt = FingerprintPacket(0x01, cmd_bytes)
        return self.helper.cmd(pkt, timeout_ms)

    def get_verify_image(self) -> bool:
        """Capture fingerprint image for verification.

        :return: True if the fingerprint image was successfully captured, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_verify_image.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.get_verify_image()
        """
        rx = self.send_cmd(b"\x01")
        return self._parse_response(rx)

    def get_enroll_image(self) -> bool:
        """Capture fingerprint image for enrollment.

        :return: True if the fingerprint image was successfully captured, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_enroll_image.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.get_enroll_image()
        """
        rx = self.send_cmd(b"\x29")
        return self._parse_response(rx)

    def gen_feature(self) -> bool:
        """Generate fingerprint feature.

        Converts the original fingerprint image stored in the image buffer into a feature file,
        which is then stored in the template buffer.

        :return: True if the fingerprint feature was successfully generate, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |gen_feature.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.gen_feature()
        """
        rx = self.send_cmd(b"\x02")
        return self._parse_response(rx)

    def gen_template(self) -> bool:
        """Merge fingerprint features to generate a template.

        Combines two fingerprint feature files into one fingerprint template.

        :return: True if the fingerprint template was successfully generate, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |gen_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.gen_template()
        """
        rx = self.send_cmd(b"\x05")
        return self._parse_response(rx)

    def store_template(self, id) -> bool:
        """Store fingerprint template into flash memory.

        Stores the generated fingerprint template into flash memory at the specified ID.

        :param int id: Storage location ID (range: 0 ~ 99)
        :return: True if storage successful False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |store_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.store_template(id)
        """
        if not (0 <= id <= self.max_id):
            raise ValueError(f"ID out of range. Must be between 0 and {self.max_id}.")
        rx = self.send_cmd(b"\x06" + b"\x01" + id.to_bytes(2, "big"))
        return self._parse_response(rx)

    def load_template(self, id) -> bool:
        """Load fingerprint template from flash memory.

        Loads the fingerprint template with the specified ID from flash memory
        into the template buffer.

        :param int id: ID of the fingerprint template to load

        :return: True if load template succcessful.
        :rtype: bool

        UiFlow2 Code Block:

            |load_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.load_template(id)
        """
        rx = self.send_cmd(b"\x07" + b"\x02" + id.to_bytes(2, "big"))
        return self._parse_response(rx)

    def delete_template(self, id) -> bool:
        """Delete fingerprint template from flash memory.

        Deletes the fingerprint template with the specified ID from the flash storage.

        :param int id: ID of the fingerprint template to delete
        :return: True if deletion successful, False otherwise
        :rtype: bool

        UiFlow2 Code Block:

            |delete_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.delete_template(id)
        """
        if not (0 <= id <= self.max_id):
            raise ValueError(f"ID out of range. Must be between 0 and {self.max_id}.")
        rx = self.send_cmd(b"\x0C" + id.to_bytes(2, "big") + b"\x00\x01")
        return self._parse_response(rx)

    def delete_all_template(self) -> bool:
        """Clear the fingerprint database.

        Deletes all fingerprint templates stored in the fingerprint database.

        :return: True if deletion successful, False otherwise
        :rtype: bool

        UiFlow2 Code Block:

            |delete_all_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.delete_all_template()
        """
        rx = self.send_cmd(b"\x0D")
        return self._parse_response(rx)

    def upload_template(self, save_path="template.tzh", log=False) -> bool:
        """Upload fingerprint template and save to specified path

        Uploads the template stored in the template buffer to the host controller.

        :param str path: File path to save the uploaded template
        :return: True if upload template successful.
        :rtype: bool

        UiFlow2 Code Block:

            |upload_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.upload_template(path)
        """
        size = 0
        off = 0
        ra = 0
        with open(save_path, "wb") as f:
            for i in range(1, 9):
                if i < 8:
                    size = 1000
                else:
                    size = 262  # 第8包
                cmd_bytes = b"\x7A" + off.to_bytes(2, "big") + size.to_bytes(2, "big")
                off += size
                pkt = FingerprintPacket(0x01, cmd_bytes)
                self.serial.read()
                data = pkt.build_packet()
                self._log_debug(f"TX: {self._format_bytes(data)}")
                self.serial.write(data)
                start = time.ticks_ms()
                ack_len = 12
                while time.ticks_diff(time.ticks_ms(), start) < 500:
                    if self.serial.any() >= ack_len:
                        time.sleep_ms(100)  # 确保完整接收
                        rx = self.serial.read()
                        self._log_debug(f"RX: {self._format_bytes(rx[:14])}")
                        if rx[9] == 0x00:  # 确认码成功
                            break
                        else:
                            print("rx error")
                            return False
                else:
                    print("Timeout waiting for response")
                    return False
                # 提取模板数据部分
                template_size = (rx[10] << 8) | rx[11]
                payload = rx[12:-2]  # 去除校验和
                f.write(payload)
                ra += template_size
                print("Block %d: size %d   total: %d\n" % (i, template_size, ra))
                time.sleep_ms(100)
        print(f"template upload success, save to {save_path}")
        return True

    def download_template(self, filepath="template.tzh"):
        """Download template.

        Reads the fingerprint template from the file system and downloads it to the fingerprint module.

        :param str path: Path to the fingerprint template file
        :return: True if download template successful.
        :rtype: bool

        UiFlow2 Code Block:

            |download_template.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.download_template(path)
        """

        def _format_bytes(data):
            return " ".join(f"{b:02X}" for b in data)

        def _send_packet(dev_addr: int, offset: int, chunk: bytes):
            header = b"\xEF\x01"
            addr = dev_addr.to_bytes(4, "big")
            pid = b"\x01"  # 数据包
            cmd = b"\x7B"  # 下载模板指令
            off = offset.to_bytes(2, "big")
            size = len(chunk).to_bytes(2, "big")
            content = cmd + off + size + chunk
            plen = len(chunk) + 7  # len(content).to_bytes(2, 'big')
            body = pid + plen.to_bytes(2, "big") + content
            checksum = sum(body) & 0xFFFF
            packet = header + addr + body + checksum.to_bytes(2, "big")
            self.serial.write(packet)
            print(f"Send {len(packet)} bytes at offset {offset}\n")

        dev_addr = 0xFFFFFFFF
        try:
            with open(filepath, "rb") as f:
                offset = 0
                while True:
                    chunk = f.read(1000)  # 模板数据 = 最大128B - 指令码1B - 偏移2B - 大小2B
                    if not chunk:
                        break
                    _send_packet(dev_addr, offset, chunk)
                    offset += len(chunk)
                    # wait for ack
                    time.sleep_ms(260)
                    self.serial.read(128)
        except OSError:
            print("File not found: %s" % filepath)
            return False
        return True

    def upload_image(self, to_rgb565=True, byte_order=True) -> bytearray | None:
        """Upload fingerprint image from module.

        Uploads the 4-bit grayscale fingerprint image from the module (size: 80x208).
        Optionally, converts the raw image to RGB565 format suitable for display.

        :param bool to_rgb565: Whether to convert raw image to RGB565 (default True)
        :param bool byte_order: If converting to RGB565, set True for little-endian byte order, or False for big-endian. Default is True.
        :return: Fingerprint image data as bytearray. Returns None on failure.
        :rtype: bytearray | None

        UiFlow2 Code Block:

            |upload_image.png|

        MicroPython Code Block:

            .. code-block:: python

                img_buf = unit_fp2_0.upload_image(to_rgb565=True, byte_order=True)
        """
        width = 80
        height = 208
        pkt = FingerprintPacket(0x01, b"\x0A")
        data = pkt.build_packet()
        self.serial.read()  # flush rx buffer
        self._log_debug(f"TX: {self._format_bytes(data)}")
        self.serial.write(data)
        image_data = []
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 300:
            if self.serial.any() >= 12:
                rx = self.serial.read(12)
                self._log_debug(f"RX: {self._format_bytes(rx[:12])}")
                if rx[9] != 0x00:
                    print("Module returned error confirmation code:", hex(rx[9]))
                    return None
                print("Acknowledged, preparing to receive image data")
                while True:
                    # Wait for packet header
                    while self.serial.any() < 9:
                        pass
                    rx = self.serial.read(9)
                    packet_type = rx[6]
                    data_len = (rx[7] << 8) | rx[8]
                    # Wait for full packet body
                    while self.serial.any() < data_len:
                        pass
                    data = self.serial.read(data_len)
                    image_data += data[:-2]  # remove 2-byte checksum
                    if packet_type == 0x08:  # last data packet
                        print("Image reception complete, length:", len(image_data))
                        break
                    else:
                        print(f"Received data packet, length: {data_len}")
                # Convert to RGB565 if requested
                if to_rgb565:
                    rgb_buf = bytearray()
                    pixel_count = width * height
                    for i in range(pixel_count // 2):
                        byte = image_data[i]
                        high_gray = (byte >> 4) & 0x0F
                        low_gray = byte & 0x0F
                        for gray4 in (high_gray, low_gray):
                            gray8 = (gray4 << 4) | gray4
                            r = gray8 >> 3
                            g = gray8 >> 2
                            b = gray8 >> 3
                            rgb565 = (r << 11) | (g << 5) | b
                            if byte_order:
                                rgb_buf.append(rgb565 & 0xFF)
                                rgb_buf.append((rgb565 >> 8) & 0xFF)
                            else:
                                rgb_buf.append((rgb565 >> 8) & 0xFF)
                                rgb_buf.append(rgb565 & 0xFF)
                    return rgb_buf
                else:
                    return bytearray(image_data)
        print("Timeout waiting for image upload")
        return None

    def get_valid_template_num(self) -> int:
        """Get the number of valid fingerprint templates.

        Returns the count of fingerprint templates currently stored in the fingerprint database.

        :return: Number of valid fingerprint templates
        :rtype: int

        UiFlow2 Code Block:

            |get_valid_template_num.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.get_valid_template_num()
        """
        rx = self.send_cmd(b"\x1D")
        valid_templates = 0
        if len(rx) >= 12 and rx[6] == 0x07 and rx[9] == 0x00:
            valid_templates = int.from_bytes(rx[10:12], "big")
        return valid_templates

    def get_stored_template_id(self) -> list[int] | None:
        """Get the list of stored fingerprint template IDs from the fingerprint sensor.

        This function queries the fingerprint sensor for its template index map,
        which represents the occupied (used) template slots in the database,
        and returns the list of those occupied IDs.

        :return: A list of occupied fingerprint template IDs, or None if retrieval fails.
        :rtype: list[int] | None

        UiFlow2 Code Block:

            |get_stored_template_id.png|

        MicroPython Code Block:

            .. code-block:: python

                stored_ids = get_stored_template_id(sensor)
        """
        rx = self.send_cmd(b"\x1F\x00")
        total_bits = self.max_id
        total_bytes = (total_bits + 7) // 8  # 向上取整所需字节数
        if rx and len(rx) >= 10 + total_bytes and rx[9] == 0x00:
            data = rx[10 : 10 + total_bytes]
            bits = []
            for byte in data:
                for i in range(8):
                    bits.append(bool((byte >> i) & 0x01))
            return tuple(bits[:total_bits])
        else:
            return tuple(False for _ in range(total_bits))

    def find_match(self):
        """Search for a matching fingerprint in the database.

        Compares the fingerprint features stored in the template buffer
        with the stored templates in the database.

        :return:
            - (id, score): A tuple of the matched fingerprint ID and match score.
            - None: If no matching fingerprint is found.

        UiFlow2 Code Block:

            |find_match.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.find_match()
        """
        start_page = 0
        page_num = self.max_id
        rx = self.send_cmd(
            b"\x04" + b"\x01" + start_page.to_bytes(2, "big") + page_num.to_bytes(2, "big")
        )
        if rx and len(rx) == 16 and rx[0] == 0xEF and rx[1] == 0x01 and rx[6] == 0x07:
            if rx[9] == 0x00:
                page_id = int.from_bytes(rx[10:12], "big")
                match_score = int.from_bytes(rx[12:14], "big")
                return (page_id, match_score)
        else:
            return None

    def match(self) -> int:
        """Precisely match two fingerprint features.

        Compares two fingerprint feature files and returns the result and score.

        :return: Similarity score of the match
        :rtype: int

        UiFlow2 Code Block:

            |match.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.match()
        """
        score = 0
        rx = self.send_cmd(b"\x03")
        if rx and len(rx) == 14 and rx[0] == 0xEF and rx[1] == 0x01 and rx[6] == 0x07:
            score = int.from_bytes(rx[10:12], "big")
            if rx[9] == 0x00:
                return (True, score)
            else:
                return (False, score)
        else:
            return (False, 0)

    def is_connected(self) -> bool:
        """Check whether the fingerprint module is connected.

        :return: True if the module is connected, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |is_connected.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.is_connected()
        """
        rx = self.send_cmd(b"\x35")
        if rx and rx[0] == 0xEF and rx[1] == 0x01 and len(rx) == 12:
            return True
        else:
            return False

    def activate_module(self) -> None:
        """Activate the module.

        UiFlow2 Code Block:

            |activate_module.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.activate_module()
        """
        rx = self.send_cmd(b"\xD4")
        return self._parse_response(rx)

    def set_work_mode(self, mode: int = 0, save: bool = False) -> None:
        """Set the working mode.

        :param int mode: Working mode (0: Auto sleep, 1: Always-on).
        :param bool save: Whether to save the setting to the device. Default is False.

        UiFlow2 Code Block:

            |set_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.set_work_mode(mode, save)
        """
        self.send_cmd(b"\xD2" + bytearray([mode]))
        if save:
            self.send_cmd(b"\xD6" + bytearray([1]))

    def get_work_mode(self) -> int:
        """Get the current working mode.

        Returns the module's current working mode:
            - 0: Auto sleep mode
            - 1: Always-on mode

        :return: Current working mode
        :rtype: int

        UiFlow2 Code Block:

            |get_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = unit_fp2_0.get_work_mode()
        """
        rx = self.send_cmd(b"\xD3")
        return rx[-3]

    def set_auto_sleep_time(self, time_s: int = 10, save: bool = False) -> None:
        """Set the sleep timeout.

        This parameter is only effective in "Auto Sleep Mode".
        It determines how long the fingerprint module waits without receiving any command
        before it enters sleep mode and starts monitoring for fingerprint press.

        :param int time_s: Auto sleep timeout in seconds. Range: 10~254.
        :param bool save: Whether to save this configuration to flash.

        UiFlow2 Code Block:

            |set_auto_sleep_time.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_fp2_0.set_auto_sleep_time(30, save=True)
        """
        time_s = min(max(time_s, 10), 254)
        self.send_cmd(b"\xD0" + bytearray([time_s]))
        if save:
            self.send_cmd(b"\xD6" + bytearray([0]))

    def get_auto_sleep_time(self) -> int:
        """Get auto sleep time.

        This value is only valid in "Timed Sleep Mode". It indicates how long the module will wait
        without receiving commands before entering sleep state.

        :return: Auto sleep time in seconds
        :rtype: int

        UiFlow2 Code Block:

            |get_auto_sleep_time.png|

        MicroPython Code Block:

            .. code-block:: python

                sleep_time = unit_fp2_0.get_auto_sleep_time()
        """
        rx = self.send_cmd(b"\xD1")
        if rx[-4] == 0x00:
            return rx[-3]

    def get_work_status(self) -> bool:
        """Get fingerprint module work status.

        :return: True if active, False otherwise
        :rtype: bool

        UiFlow2 Code Block:

            |get_work_status.png|

        MicroPython Code Block:

            .. code-block:: python

                status = unit_fp2_0.get_work_status()
        """
        rx = self.send_cmd(b"\xD5")
        if rx and len(rx) == 13 and rx[-4] == 0x00:
            return rx[-3] == 0x01
        return False

    def get_firmware_version(self) -> int:
        """Get firmware version.

        :return: Firmware version number
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                version = unit_fp2_0.get_firmware_version()
        """
        rx = self.send_cmd(b"\xD7")
        return rx[-3]

    def set_led_breath(self, start_color: int, end_color: int, repeat: int) -> bool:
        """Set LED breathing mode.

        :param int start_color: Start color (bit0: blue, bit1: green, bit2: red)
        :param int end_color: End color (bit0: blue, bit1: green, bit2: red)
        :param int repeat: Number of cycles (0=infinite)
        :return: True if command successful, False otherwise
        :rtype: bool

        Color codes:
            - 0x00: All off
            - 0x01: Blue
            - 0x02: Green
            - 0x03: Cyan (blue + green)
            - 0x04: Red
            - 0x05: Magenta (red + blue)
            - 0x06: Yellow (red + green)
            - 0x07: White (red + green + blue)

        UiFlow2 Code Block:

            |set_led_breath.png|

        MicroPython Code Block:

            .. code-block:: python

                # Blue breathing light, 5 cycles
                unit_fp2_0.set_led_breath(0x01, 0x01, 5)

                # Red to white breathing light, infinite cycles
                unit_fp2_0.set_led_breath(0x04, 0x07, 0)
        """
        cmd_bytes = b"\x3C" + bytes([1, start_color, end_color, repeat])
        rx = self.send_cmd(cmd_bytes)
        return self._parse_response(rx)

    def set_led_color(self, color: int) -> bool:
        """Set LED color.

        :param int color: LED color (0: always off, other values: always on with specified color)
        :return: True if command successful, False otherwise
        :rtype: bool

        Color codes:
            - 0x00: Always off
            - 0x01: Blue
            - 0x02: Green
            - 0x03: Cyan (blue + green)
            - 0x04: Red
            - 0x05: Magenta (red + blue)
            - 0x06: Yellow (red + green)
            - 0x07: White (red + green + blue)

        UiFlow2 Code Block:

            |set_led_color.png|

        MicroPython Code Block:

            .. code-block:: python

                # Always on white light
                unit_fp2_0.set_led_color(0x07)

                # Always off (turn off all LEDs)
                unit_fp2_0.set_led_color(0x00)

                # Always on red light
                unit_fp2_0.set_led_color(0x04)
        """
        if color == 0:
            cmd_bytes = b"\x3C" + bytes([4, 0, 0, 0])
        else:
            cmd_bytes = b"\x3C" + bytes([3, color, color, 0])
        rx = self.send_cmd(cmd_bytes)
        return self._parse_response(rx)
