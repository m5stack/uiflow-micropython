# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import importlib
import pathlib
import sys
import types
import unittest


LIBS_PATH = pathlib.Path(__file__).parents[2] / "m5stack" / "libs"
sys.path.insert(0, str(LIBS_PATH))


class FakeBoard:
    M5StampC5 = 1
    M5StampC6 = 2
    M5StampS3Mini = 3


fake_m5 = types.ModuleType("M5")
fake_m5.BOARD = FakeBoard
fake_m5.current_board = FakeBoard.M5StampC5
fake_m5.getBoard = lambda: fake_m5.current_board


class FakePin:
    IN = 0
    OUT = 1
    instances = []

    def __init__(self, number, mode=None, value=None):
        self.number = number
        self.mode = mode
        self.value = value
        self.instances.append(self)


class FakeSPI:
    instances = []

    def __init__(self, spi_id, **kwargs):
        self.spi_id = spi_id
        self.kwargs = kwargs
        self.instances.append(self)


fake_machine = types.ModuleType("machine")
fake_machine.Pin = FakePin
fake_machine.SPI = FakeSPI


class FakeRxPacket:
    pass


class FakeSX1262:
    instances = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.calls = []
        self.callback = None
        self.instances.append(self)

    def configure(self, config):
        self.calls.append(("configure", config))

    def send(self, packet, tx_at_ms):
        self.calls.append(("send", packet, tx_at_ms))
        return 123

    def recv(self, timeout_ms, rx_length, rx_packet):
        self.calls.append(("recv", timeout_ms, rx_length, rx_packet))
        return rx_packet

    def start_recv(self, continuous):
        self.calls.append(("start_recv", continuous))

    def set_irq_callback(self, callback):
        self.callback = callback

    def poll_recv(self):
        return "packet"

    def standby(self):
        self.calls.append(("standby",))

    def sleep(self):
        self.calls.append(("sleep",))

    def irq_triggered(self):
        return True


fake_lora = types.ModuleType("lora")
fake_lora.RxPacket = FakeRxPacket
fake_lora.SX1262 = FakeSX1262

fake_micropython = types.ModuleType("micropython")
fake_micropython.scheduled = []
fake_micropython.schedule = lambda callback, arg: fake_micropython.scheduled.append(
    (callback, arg)
)


class FakeUWB:
    instances = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.instances.append(self)


fake_uwb = types.ModuleType("uwb")
fake_uwb.UWB = FakeUWB
fake_uwb.SFD_DW_8 = 1
fake_uwb.BR_6M8 = 2
fake_uwb.PHR_STD = 3
fake_uwb.PHR_RATE_STD = 4
fake_uwb.RX_IMMEDIATE = 5
fake_uwb.STS_MODE_1 = 0x10
fake_uwb.STS_MODE_SDC = 0x20
fake_uwb.STS_OFF = 0
fake_uwb.PDOA_M0 = 0
fake_uwb.PDOA_M3 = 3
fake_uwb.VALID_TDOA_LIMIT = 100


class StampSupportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.modules["M5"] = fake_m5
        sys.modules["machine"] = fake_machine
        sys.modules["lora"] = fake_lora
        sys.modules["micropython"] = fake_micropython
        sys.modules["uwb"] = fake_uwb

    def setUp(self):
        FakePin.instances.clear()
        FakeSPI.instances.clear()
        FakeSX1262.instances.clear()
        FakeUWB.instances.clear()
        fake_micropython.scheduled.clear()
        for name in ("stamp.uwb", "stamp.lora1262", "stamp.f12", "stamp"):
            sys.modules.pop(name, None)

    def test_f12_maps_signal_positions_for_all_supported_hosts(self):
        f12_module = importlib.import_module("stamp.f12")
        expected = {
            FakeBoard.M5StampC5: (23, 0, 24, 25, 26, 27, 11, 12),
            FakeBoard.M5StampC6: (8, 0, 18, 19, 20, 21, 22, 23),
            FakeBoard.M5StampS3Mini: (38, 21, 39, 40, 41, 42, 43, 44),
        }
        positions = (
            f12_module.StampF12.SW,
            f12_module.StampF12.IRQ,
            f12_module.StampF12.BUSY,
            f12_module.StampF12.RST,
            f12_module.StampF12.MISO,
            f12_module.StampF12.MOSI,
            f12_module.StampF12.CS,
            f12_module.StampF12.CLK,
        )

        for board, pins in expected.items():
            fake_m5.current_board = board
            f12 = f12_module.StampF12()
            self.assertEqual(tuple(f12.pin(position) for position in positions), pins)

    def test_f12_rejects_non_gpio_positions_and_unsupported_hosts(self):
        f12_module = importlib.import_module("stamp.f12")
        fake_m5.current_board = FakeBoard.M5StampC5
        f12 = f12_module.StampF12()
        for position in (0, 1, 2, 7, 11, 13):
            with self.assertRaises(ValueError):
                f12.pin(position)

        fake_m5.current_board = 99
        with self.assertRaises(NotImplementedError):
            f12_module.StampF12()

    def test_lora_uses_c6_f12_defaults_and_tcxo_voltage(self):
        fake_m5.current_board = FakeBoard.M5StampC6
        lora_module = importlib.import_module("stamp.lora1262")
        radio = lora_module.StampLoRa1262()

        self.assertEqual(radio._sw.number, 8)
        self.assertEqual((radio._sw.mode, radio._sw.value), (FakePin.OUT, 1))
        self.assertEqual(radio._spi.spi_id, 1)
        self.assertEqual(radio._spi.kwargs["sck"].number, 23)
        self.assertEqual(radio._spi.kwargs["mosi"].number, 21)
        self.assertEqual(radio._spi.kwargs["miso"].number, 20)
        self.assertEqual(radio.modem.kwargs["reset"].number, 19)
        self.assertEqual(radio.modem.kwargs["cs"].number, 22)
        self.assertEqual(radio.modem.kwargs["busy"].number, 18)
        self.assertEqual(radio.modem.kwargs["dio1"].number, 0)
        self.assertEqual(radio.modem.kwargs["dio3_tcxo_millivolts"], 3000)
        self.assertEqual(radio.modem.kwargs["lora_cfg"]["freq_khz"], 868000)

    def test_lora_allows_complete_custom_pin_mapping(self):
        fake_m5.current_board = 99
        lora_module = importlib.import_module("stamp.lora1262")
        radio = lora_module.StampLoRa1262(
            sw=1,
            irq=2,
            busy=3,
            reset=4,
            miso=5,
            mosi=6,
            cs=7,
            clock=8,
            spi_id=2,
        )

        self.assertEqual(radio._sw.number, 1)
        self.assertEqual(radio._spi.spi_id, 2)
        self.assertEqual(radio._spi.kwargs["sck"].number, 8)
        with self.assertRaises(ValueError):
            lora_module.StampLoRa1262(sw=1)

    def test_lora_validates_and_delegates_high_level_api(self):
        fake_m5.current_board = FakeBoard.M5StampC5
        lora_module = importlib.import_module("stamp.lora1262")
        radio = lora_module.StampLoRa1262()

        radio.set_freq(923000)
        radio.set_sf(12)
        radio.set_bw("125")
        radio.set_coding_rate(5)
        radio.set_syncword(0x34)
        radio.set_preamble_len(20)
        radio.set_output_power(22)
        self.assertEqual(
            radio.modem.calls[:7],
            [
                ("configure", {"freq_khz": 923000}),
                ("configure", {"sf": 12}),
                ("configure", {"bw": "125"}),
                ("configure", {"coding_rate": 5}),
                ("configure", {"syncword": 0x34}),
                ("configure", {"preamble_len": 20}),
                ("configure", {"output_power": 22}),
            ],
        )
        self.assertEqual(radio.send("hello"), 123)
        self.assertIn(("send", b"hello", None), radio.modem.calls)

        packet = FakeRxPacket()
        self.assertIs(radio.recv(100, 16, packet), packet)
        radio.start_recv()
        self.assertTrue(radio.irq_triggered())
        radio.standby()
        radio.deinit()

        callback = lambda received: received
        radio.set_irq_callback(callback)
        radio.modem.callback()
        self.assertEqual(fake_micropython.scheduled, [(callback, "packet")])

        with self.assertRaises(ValueError):
            radio.set_freq(923001)
        with self.assertRaises(ValueError):
            radio.set_bw("100")
        with self.assertRaises(ValueError):
            radio.set_output_power(23)

    def test_uwb_compatibility_iomap_comes_from_f12(self):
        expected = {
            FakeBoard.M5StampC5: (0, 24, 25, 27, 26, 12, 11, 23),
            FakeBoard.M5StampC6: (0, 18, 19, 21, 20, 23, 22, 8),
            FakeBoard.M5StampS3Mini: (21, 39, 40, 42, 41, 44, 43, 38),
        }
        for board, pins in expected.items():
            fake_m5.current_board = board
            sys.modules.pop("stamp.uwb", None)
            uwb_module = importlib.import_module("stamp.uwb")
            self.assertEqual(tuple(uwb_module.iomap), pins)
            radio = uwb_module.StampUWB()
            self.assertEqual(
                radio._device.kwargs,
                {
                    "irq": pins[0],
                    "wakeup": pins[1],
                    "reset": pins[2],
                    "mosi": pins[3],
                    "miso": pins[4],
                    "clock": pins[5],
                    "cs": pins[6],
                },
            )

        custom_pins = {
            "irq": 1,
            "wakeup": 2,
            "reset": 3,
            "mosi": 4,
            "miso": 5,
            "clock": 6,
            "cs": 7,
        }
        custom_radio = uwb_module.StampUWB(**custom_pins)
        self.assertEqual(custom_radio._device.kwargs, custom_pins)


if __name__ == "__main__":
    unittest.main()
