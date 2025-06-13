# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.mcp2515.mcp2515_spi import MCP2515_CAN
from driver.mcp2515.can_frame import CANFrame
import machine
import time

ERROR_OK = 0
ERROR_FAIL = 1
ERROR_ALLTXBUSY = 2
ERROR_FAILINIT = 3
ERROR_FAILTX = 4
ERROR_NOMSG = 5

CAN_SFF_MASK = 0x000007FF  # standard frame format (SFF)
CAN_EFF_MASK = 0x1FFFFFFF  # extended frame format (EFF)

import M5
from collections import namedtuple

MBusIO = namedtuple("MBusIO", ["cs", "int", "sck", "mosi", "miso"])
iomap = {
    M5.BOARD.M5Stack: MBusIO(12, 15, 18, 23, 19),
    M5.BOARD.M5StackCore2: MBusIO(27, 2, 18, 23, 38),
    M5.BOARD.M5StackCoreS3: MBusIO(6, 13, 36, 37, 35),
    M5.BOARD.M5Tough: MBusIO(27, 2, 18, 23, 38),
    M5.BOARD.M5Tab5: MBusIO(2, 47, 5, 18, 19),
}.get(M5.getBoard())


class CommuModuleCAN(MCP2515_CAN):
    """Create an CommuModuleCAN object

    :param int mode: The CAN mode to use(NORMAL, LISTEN_ONLY), Default is NORMAL.

        Options:
            - ``NORMAL``: Normal mode
            - ``LISTEN_ONLY``: Listen only mode

    :param int baudrate: The baudrate to use, Default is CAN_1000KBPS.

        Options:
            - ``CAN_5KBPS``: 5Kbps
            - ``CAN_10KBPS``: 10Kbps
            - ``CAN_20KBPS``: 20Kbps
            - ``CAN_31K25BPS``: 31.25Kbps
            - ``CAN_33KBPS``: 33Kbps
            - ``CAN_40KBPS``: 40Kbps
            - ``CAN_50KBPS``: 50Kbps
            - ``CAN_80KBPS``: 80Kbps
            - ``CAN_83K3BPS``: 83.33Kbps
            - ``CAN_95KBPS``: 95Kbps
            - ``CAN_100KBPS``: 100Kbps
            - ``CAN_125KBPS``: 125Kbps
            - ``CAN_200KBPS``: 200Kbps
            - ``CAN_250KBPS``: 250Kbps
            - ``CAN_500KBPS``: 500Kbps
            - ``CAN_1000KBPS``: 1Mbps


    :param int spi_baud: The SPI baudrate to use, Default is 8000000.
    :param int canIDMode: The CAN ID mode to use(MCP_STDEXT, MCP_EXTDONLY), Default is MCP_STDEXT.

        Options:
            - ``MCP_STDEXT``: Standard and Extended
            - ``MCP_EXTDONLY``: Extended only

    :param bool debug: Whether to enable debug mode, Default is False.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import CommuModuleCAN

            commu = CommuModuleCAN(CommuModule.NORMAL, baudrate=16)

    """

    NORMAL = 0x00
    LISTEN_ONLY = 0x60

    MCP_STDEXT = 0  # Standard and Extended
    MCP_8MHZ = 3

    CAN_5KBPS = 1
    CAN_10KBPS = 2
    CAN_20KBPS = 3
    CAN_31K25BPS = 4
    CAN_33KBPS = 5
    CAN_40KBPS = 6
    CAN_50KBPS = 7
    CAN_80KBPS = 8
    CAN_83K3BPS = 9
    CAN_95KBPS = 10
    CAN_100KBPS = 11
    CAN_125KBPS = 12
    CAN_200KBPS = 13
    CAN_250KBPS = 14
    CAN_500KBPS = 15
    CAN_1000KBPS = 16

    def __init__(
        self,
        mode: int = NORMAL,
        baudrate: int = CAN_1000KBPS,
        spi_baud=8000000,
        canIDMode: int = MCP_STDEXT,
        debug=False,
    ):
        super().__init__()
        self.debug = debug
        self.mcp2515_spi_init(
            spi_baud=spi_baud,
            sclk=iomap.sck,
            mosi=iomap.mosi,
            miso=iomap.miso,
            cs=iomap.cs,
            irq=iomap.int,
        )

        mode = self.mcp2515_set_mode(mode)
        if self.debug:
            print("CAN Mode Function Error Message Code: {}  \r\n".format(mode))
        if self.mcp2515_init(canIDMode, baudrate, canClock=self.MCP_8MHZ) is not True:
            raise Exception("Commu Module init failed")
        self.commu_can_id = None
        self.error = ERROR_OK

    def info(self):
        """Get the state of error information.

        :returns: The current error information.
        :rtype: str

        UiFlow2 Code Block:

            |info.png|

        MicroPython Code Block:

            .. code-block:: python

                commu.info()
        """
        return self.error

    def reset(self) -> None:
        self.mcp2515_reset()

    def get_irq_state(self) -> bool:
        return bool(not self.irq.value())

    def any(self) -> bool:
        """Check if any message is available.

        :returns: The current message availability.
        :rtype: bool

        UiFlow2 Code Block:

            |any.png|

        MicroPython Code Block:

            .. code-block:: python

                commu.any()
        """
        return self.mcp2515_check_receive()

    def clear_interrupts(self):
        self.mcp2515_clear_interrupts()

    def recv(self, fifo=0, list=None, timeout=5000):
        """Read a message from the CAN bus.

        :param int fifo: The fifo is an integer, it can be any number and compatible with Pyb.CAN
        :param list list: list is an optional list object to be used as the return value.
        :param int timeout: timeout is the timeout in milliseconds to wait for the receive.
        :returns: Tuple containing (can_id, is_extended, is_rtr, fmi, data)
        :rtype: tuple

            - The id of the message.
            - A boolean that indicates if the message ID is standard or extended.
            - A boolean that indicates if the message is an RTR message.
            - The FMI (Filter Match Index) value.
            - An array containing the data.

        UiFlow2 Code Block:

            |recv_message.png|

            |recv_message_into.png|

        MicroPython Code Block:

            .. code-block:: python

                commu.recv(0)

                buf = bytearray(8)
                lst = [0, 0, 0, 0, memoryview(buf)]
                # No heap memory is allocated in the following call
                commu.recv(0, lst)
        """

        start_time = time.ticks_ms()

        while time.ticks_ms() - start_time < timeout:
            self.error, can_id, is_extended, is_rtr, fmi, data = self.mcp2515_read_can_message()
            if self.debug:
                print(
                    "CAN Read Data Packet Function Error Message Code: {}  \r\n".format(self.error)
                )
            if self.error == ERROR_OK:
                self.commu_can_id = can_id & (CAN_EFF_MASK if self.extframe else CAN_SFF_MASK)
                if list is None:
                    return [can_id, is_extended, is_rtr, fmi, bytes(data)]
                else:
                    list[:] = [can_id, is_extended, is_rtr, fmi, bytes(data)]
                    return True
            time.sleep(0.01)

        return None

    def send(self, data: str, can_id: int, extframe: bool = False) -> int:
        """Send a message to the CAN bus.

        :param str data: The message data.
        :param int can_id: The CAN ID.
        :param bool extframe: Whether to use extended frame format.
        :returns: The message data.
        :rtype: str

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                commu.send('uiflow2', 0, extframe=False)
        """
        can_frame = CANFrame(can_id, bytes(data.encode()))
        send = self.mcp2515_send_can_message(extframe, can_frame)
        if self.debug:
            print("CAN Send Data Packet Function Error Message Code: {}  \r\n".format(send))
        return send

    def commu_can_debug(self, enable=True) -> None:
        self.debug = enable

    def deinit(self):
        pass
        # self.hspi.deinit()

    def commu_can_config_rate(self, canSpeed: int, canClock: int = 3) -> int:
        config = self.mcp2515_config_rate(canSpeed, canClock)
        if self.debug:
            print("CAN Configure Function Error Message Code: {}  \r\n".format(config))
        return config


class CommuModuleRS485:
    def __new__(
        cls,
        id,
        **kwargs,
    ):
        return machine.UART(
            id,
            **kwargs,
        )


class CommuModuleI2C:
    def __new__(
        cls,
        id,
        **kwargs,
    ):
        return machine.I2C(
            id,
            **kwargs,
        )
