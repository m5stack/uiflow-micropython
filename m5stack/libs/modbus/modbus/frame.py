# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT


class ModbusFrame:
    def __init__(
        self,
        func_code: int = 0,
        register: int = None,
        fr_type: str = "request",
        length: int = None,
        data: bytearray = None,
        error_code: int = None,
    ) -> None:
        """Init a generic modbus frame.

        :param int func_code: Function code (1-6,15,16). Defaults to 0.
        :param register: Register. Defaults to None.
        :type register: int or None
        :param fr_type: Frame type (request/response). Defaults to "request".
        :type fr_type: str or None
        :param length: Length of requested data. Defaults to None.
        :type length: int or None
        :param data: Payload. Defaults to None.
        :type data: bytearray or None
        :param error_code: Error Code. Defaults to None.
        :type error_code: int or None

        """

        self.type = fr_type

        if func_code not in [
            0x01,
            0x02,
            0x03,
            0x04,
            0x05,
            0x06,
            0x0F,
            0x10,
            0x81,
            0x82,
            0x83,
            0x84,
            0x85,
            0x86,
            0x8F,
            0x90,
        ]:
            raise ValueError("function code {} is not supported".format(func_code))
        self.func_code = func_code

        if fr_type == "request":
            if data is not None:
                if func_code not in [0x05, 0x06, 0x0F, 0x10]:
                    raise ValueError(
                        "data is not supported for {} with function code {}".format(
                            fr_type, func_code
                        )
                    )
        elif fr_type == "response":
            if data is not None:
                if func_code not in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]:
                    raise ValueError(
                        "data is not supported for {} with function code {}".format(
                            fr_type, func_code
                        )
                    )
        self.data = data

        if fr_type == "response":
            if register is not None:
                if func_code not in [0x05, 0x06, 0x0F, 0x10]:
                    raise ValueError(
                        "register is not supported for {} with function code {}".format(
                            fr_type, func_code
                        )
                    )
        self.register = register

        if fr_type == "request":
            if length is not None:
                if func_code not in [0x01, 0x02, 0x03, 0x04, 0x0F, 0x10]:
                    raise ValueError(
                        "length is not supported for {} with function code {}".format(
                            fr_type, func_code
                        )
                    )
        elif fr_type == "response":
            if length is not None:
                if func_code not in [0x0F, 0x10]:
                    raise ValueError(
                        "length is not supported for {} with function code {}".format(
                            fr_type, func_code
                        )
                    )
        self.length = length

        if fr_type == "response":
            if error_code is not None:
                if func_code not in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
                    raise ValueError(
                        "error_code is not supported for {} with function code {}".format(
                            fr_type, func_code
                        )
                    )
        self.error_code = error_code

        self.pdu = None
        self.frame = None

    def _create_pdu(self) -> None:
        self.pdu = bytearray([])
        self.pdu += bytearray([self.func_code])

        if self.type == "request":
            self.pdu += bytearray([self.register >> 8, self.register & 0xFF])
            if self.func_code in [0x01, 0x02, 0x03, 0x04, 0x0F, 0x10]:
                self.pdu += bytearray([self.length >> 8, self.length & 0xFF])
            if self.func_code in [0x0F, 0x10]:
                self.pdu += bytearray([len(self.data)])
            if self.func_code in [0x05, 0x06, 0x0F, 0x10]:
                self.pdu += self.data

        if self.type == "response":
            if self.func_code in [0x01, 0x02, 0x03, 0x04]:
                self.pdu += bytearray([len(self.data)])
            if self.func_code in [0x05, 0x06, 0x0F, 0x10]:
                self.pdu += bytearray([self.register >> 8, self.register & 0xFF])
            if self.func_code in [0x01, 0x02, 0x03, 0x04, 0x05, 0x06]:
                self.pdu += self.data
            if self.func_code in [0x0F, 0x10]:
                self.pdu += bytearray([self.length >> 8, self.length & 0xFF])
            if self.func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
                self.pdu += bytearray([self.error_code])

    def _create_frame(self) -> None:
        """Override in derived Class"""
        pass

    def get_frame(self) -> bytearray:
        if self.frame is None:
            self._create_frame()
        return self.frame


class ModbusRTUFrame(ModbusFrame):
    def __init__(self, device_addr: int = 0, verbose: bool = False, *args, **kwargs) -> None:
        """Create modbus rtu frame.

        :param int device_addr: Slave address. Defaults to 0.
        :param bool verbose: If True, print debug information. Defaults to False.
        :param int func_code: Function code (1-6,15,16). Defaults to 0.
        :param int register: Register. Defaults to None.
        :param str fr_type: Frame type (request/response). Defaults to "request".
        :param int length: Length of requested data. Defaults to None.
        :param bytes data: Payload. Defaults to None.
        """
        super(ModbusRTUFrame, self).__init__(*args, **kwargs)
        self._verbose = verbose
        self.device_addr = device_addr
        self.frame = None

    def _create_frame(self) -> None:
        self._create_pdu()
        self.frame = bytearray([self.device_addr]) + self.pdu
        crc = ModbusRTUFrame._crc16(self.frame)
        self.frame += bytearray([crc & 0xFF, crc >> 8])

    def __str__(self) -> str:
        return "<ModbusRTUFrame ({}): device: {}, func_code: {}, frame:{}>".format(
            self.type,
            self.device_addr,
            self.func_code,
            " ".join(["{:02x}".format(x) for x in self.get_frame()]),
        )

    @classmethod
    def _crc16(cls, data: bytearray) -> int:
        offset = 0
        length = len(data)
        if data is None or offset < 0 or offset > len(data) - 1 and offset + length > len(data):
            return 0
        crc = 0xFFFF
        for i in range(0, length):
            crc ^= data[offset + i]
            for j in range(0, 8):
                if (crc & 1) > 0:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc = crc >> 1
        return crc

    @classmethod
    def parse_frame(
        cls, frame: bytearray, fr_type: str = None, verbose: bool = False
    ) -> "ModbusRTUFrame":
        """Create a ModbusRTUFrame from bytearray.

        :param bytearray frame: The frame to parse.
        :param str fr_type: Type of frame, either "request", "response", or
                            None. If None, it will try to determine the type
                            automatically.
        :param bool verbose: If True, print debug information.
        :return: ModbusRTUFrame object if parsing was successful, None otherwise.
        :rtype: ModbusRTUFrame or None
        """

        verbose and print("Parsing RTU frame: " + " ".join(["{:02x}".format(x) for x in frame]))

        if len(frame) < 2:
            return

        device_addr = frame[0]
        func_code = frame[1]

        if cls._check_both(frame):
            verbose and print("frame is request or response")
            register = (frame[2] << 8) + frame[3]
            data = frame[4:6]
            f = ModbusRTUFrame(
                device_addr=device_addr,
                func_code=func_code,
                register=register,
                fr_type="request",
                data=data,
            )
            verbose and print(f)
            return f

        if cls._check_request(frame) and ((fr_type is None) or (fr_type == "request")):
            verbose and print("frame is request")
            register = (frame[2] << 8) + frame[3]
            length = (frame[4] << 8) + frame[5]
            data = None
            if func_code in [0x0F, 0x10]:
                bc = frame[6]
                data = frame[7 : 7 + bc]
            f = ModbusRTUFrame(
                device_addr=device_addr,
                func_code=func_code,
                register=register,
                fr_type="request",
                length=length,
                data=data,
            )
            verbose and print(f)
            return f

        if cls._check_response(frame) and ((fr_type is None) or (fr_type == "response")):
            verbose and print("frame is response")
            f = None
            if func_code in [0x01, 0x02, 0x03, 0x04]:
                bc = frame[2]
                data = frame[3 : 3 + bc]
                f = ModbusRTUFrame(
                    device_addr=device_addr, func_code=func_code, fr_type="response", data=data
                )
            if func_code in [0x0F, 0x10]:
                register = (frame[2] << 8) + frame[3]
                length = (frame[4] << 8) + frame[5]
                f = ModbusRTUFrame(
                    device_addr=device_addr,
                    func_code=func_code,
                    register=register,
                    fr_type="response",
                    length=length,
                )
            if func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
                error_code = frame[2]
                f = ModbusRTUFrame(
                    device_addr=device_addr,
                    func_code=func_code,
                    fr_type="response",
                    error_code=error_code,
                )

            if f is not None:
                print(f)
                return f

        # raise ValueError("Could not parse Frame " + " ".join(["{:02x}".format(x) for x in frame]))

    @classmethod
    def _check_both(cls, frame: bytearray) -> bool:
        """if func_code is 0x05 or 0x06, we can't decide if it is a request or a
        response. This method checks, if is a valid 0x05- or 0x06-frame.

        :param bytearray frame: The frame to check.

        :return: True, if it is a valid 0x05- or 0x06-frame.
        :rtype: bool
        """
        try:
            func_code = frame[1]
            if func_code not in [0x05, 0x06]:
                return False
            return cls._crc16(frame[0:6]) == (frame[7] << 8) + frame[6]
        except:
            return False

    @classmethod
    def _check_request(cls, frame: bytearray) -> bool:
        """This method checks, if is a valid request. It returns False,
        if the frame could be a request or a response.

        :param bytearray frame: The frame to check.
        :return: True, if it is a valid request.
        :rtype: bool
        """
        try:
            func_code = frame[1]
            if func_code in [0x01, 0x02, 0x03, 0x04]:
                return cls._crc16(frame[0:6]) == (frame[7] << 8) + frame[6]
            if func_code in [0x10, 0x0F]:
                bc = frame[6]
                if len(frame) >= 8 + bc:
                    return cls._crc16(frame[0 : 7 + bc]) == (frame[8 + bc] << 8) + frame[7 + bc]
                else:
                    return False
        except:
            return False

    @classmethod
    def _check_response(cls, frame: bytearray) -> bool:
        """This method checks, if is a valid response. It returns False,
        if the frame could be a request or a response.

        :param bytearray frame: The frame to check.
        :return: True, if it is a valid response.
        :rtype: bool
        """
        try:
            func_code = frame[1]
            if func_code in [0x01, 0x02, 0x03, 0x04]:
                bc = frame[2]
                if len(frame) >= bc + 5:
                    return cls._crc16(frame[0 : 3 + bc]) == (frame[4 + bc] << 8) + frame[3 + bc]
            if func_code in [0x10, 0x0F]:
                return cls._crc16(frame[0:6]) == (frame[7] << 8) + frame[6]
            if func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
                return cls._crc16(frame[0:3]) == (frame[4] << 8) + frame[3]
        except:
            return False

    @classmethod
    def transform_frame(cls, tcp_frame: "ModbusTCPFrame") -> "ModbusRTUFrame":
        """transform a tcp-frame to a rtu-frame and copy all data

        :param ModbusTCPFrame tcp_frame: tcp-frame to transform
        :return: ModbusRTUFrame object with data from tcp_frame
        :rtype: ModbusRTUFrame
        """
        frame = ModbusRTUFrame()
        frame.data = tcp_frame.data
        frame.device_addr = tcp_frame.unit_id
        frame.func_code = tcp_frame.func_code
        frame.length = tcp_frame.length
        frame.register = tcp_frame.register
        frame.type = tcp_frame.type
        return frame


class ModbusTCPFrame(ModbusFrame):
    def __init__(self, transaction_id: int = 0, unit_id: int = 0, *args, **kwargs) -> None:
        """Create modbus tcp frame.

        :param int transaction_id: Transaction ID. Defaults to 0.
        :param int unit_id: Unit address. Defaults to 0.
        :param int func_code: Function code (1-6,15,16). Defaults to 0.
        :param register: Register. Defaults to None.
        :type register: int or None
        :param fr_type: Frame type (request/response). Defaults to "request".
        :type fr_type: str or None
        :param length: Length of requested data. Defaults to None.
        :type length: int or None
        :param data: Payload. Defaults to None.
        :type data: bytearray or None
        """
        super(ModbusTCPFrame, self).__init__(*args, **kwargs)
        self.transaction_id = transaction_id
        self.unit_id = unit_id
        self.frame = None

    def _create_frame(self) -> None:
        self._create_pdu()
        self.frame = bytearray([self.transaction_id >> 8, self.transaction_id & 0xFF])
        self.frame += bytearray([0x00, 0x00])  # Protocol ID
        l = len(self.pdu) + 1
        self.frame += bytearray([l >> 8, l & 0xFF])
        self.frame += bytearray([self.unit_id])
        self.frame += self.pdu

    def __str__(self) -> str:
        return "<ModbusTCPFrame ({}): func_code: {}, frame:{}>".format(
            self.type, self.func_code, " ".join(["{:02x}".format(x) for x in self.get_frame()])
        )

    @classmethod
    def parse_frame(cls, frame: bytearray, verbose: bool = False) -> "ModbusTCPFrame":
        """Create a ModbusTCPFrame from bytearray.

        :param bytearray frame: The frame to parse.
        :param bool verbose: If True, print debug information.
        :return: ModbusTCPFrame object if parsing was successful, None otherwise.
        :rtype: ModbusTCPFrame or None
        """

        verbose and print("Parsing TCP frame: " + " ".join(["{:02x}".format(x) for x in frame]))

        if len(frame) < 8:
            return

        transaction_id = (frame[0] << 8) + frame[1]
        length = (frame[4] << 8) + frame[5]
        unit_id = frame[6]
        func_code = frame[7]

        if cls._check_both(frame, length):
            verbose and print("frame is request or response")
            register = (frame[8] << 8) + frame[9]
            data = frame[10:12]
            f = ModbusTCPFrame(
                transaction_id=transaction_id,
                unit_id=unit_id,
                func_code=func_code,
                register=register,
                fr_type="request",
                data=data,
            )
            verbose and print(f)
            return f

        if cls._check_request(frame, length):
            verbose and print("frame is request")
            register = (frame[8] << 8) + frame[9]
            d_length = (frame[10] << 8) + frame[11]
            data = None
            if func_code in [0x0F, 0x10]:
                bc = frame[12]
                data = frame[13 : 13 + bc]
            f = ModbusTCPFrame(
                transaction_id=transaction_id,
                unit_id=unit_id,
                func_code=func_code,
                register=register,
                fr_type="request",
                data=data,
                length=d_length,
            )
            verbose and print(f)
            return f

        f = None
        if cls._check_response(frame, length):
            verbose and print("frame is response")
            if func_code in [0x01, 0x02, 0x03, 0x04]:
                bc = frame[8]
                data = frame[9 : 9 + bc]
                f = ModbusTCPFrame(
                    transaction_id=transaction_id,
                    unit_id=unit_id,
                    func_code=func_code,
                    fr_type="response",
                    data=data,
                )
            if func_code in [0x0F, 0x10]:
                register = (frame[8] << 8) + frame[9]
                d_length = (frame[10] << 8) + frame[11]
                f = ModbusTCPFrame(
                    transaction_id=transaction_id,
                    unit_id=unit_id,
                    func_code=func_code,
                    fr_type="response",
                    register=register,
                    length=d_length,
                )
            if func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
                error_code = frame[8]
                f = ModbusTCPFrame(
                    transaction_id=transaction_id,
                    unit_id=unit_id,
                    func_code=func_code,
                    fr_type="response",
                    error_code=error_code,
                )
            if f is not None:
                verbose and print(f)
                return f

        # raise ValueError("Could not parse Frame " + " ".join(["{:02x}".format(x) for x in frame]))

    @classmethod
    def _check_both(cls, frame: bytearray, length: int) -> bool:
        """if func_code is 0x05 or 0x06, we can't decide if it is a
        request or a response. This method checks, if is a valid 0x05- or 0x06-frame.

        :param bytearray frame: The frame to check.
        :returns: True, if it is a valid 0x05- or 0x06-frame.
        :rtype: bool
        """
        try:
            func_code = frame[7]
            if func_code not in [0x05, 0x06]:
                return False
            return len(frame) == length + 6
        except:
            return False

    @classmethod
    def _check_request(cls, frame: bytearray, length: int) -> bool:
        """This method checks, if is a valid request. It returns False,
        if the frame could be a request or a response.

        :param bytearray frame: The frame to check.
        :returns: True, if it is a valid request.
        :rtype: bool
        """
        try:
            func_code = frame[7]
            if func_code in [0x01, 0x02, 0x03, 0x04]:
                if len(frame) == length + 6:
                    return length == 6
            if func_code in [0x10, 0x0F]:
                bc = frame[12]
                if len(frame) == bc + 13:
                    return len(frame) == length + 6
            return False
        except:
            return False

    @classmethod
    def _check_response(cls, frame: bytearray, length: int) -> bool:
        """This method checks, if is a valid response. It returns False,
        if the frame could be a request or a response.

        :param bytearray frame: The frame to check.
        :returns: True, if it is a valid response.
        :rtype: bool
        """
        try:
            func_code = frame[7]
            if func_code in [0x01, 0x02, 0x03, 0x04]:
                bc = frame[8]
                if len(frame) == bc + 9:
                    return len(frame) == length + 6
            if func_code in [0x10, 0x0F]:
                return len(frame) == length + 6
            if func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
                return length == 3
        except:
            return False
