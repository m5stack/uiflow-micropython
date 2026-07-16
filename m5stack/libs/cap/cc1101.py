# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from collections import namedtuple

import M5
import machine
import micropython
from driver.cc1101 import CC1101 as CC1101Driver, CC1101Packet
from driver.st25r3916 import ST25R3916
from unit.nfc import NFCUnit


PortDescriptor = namedtuple(
    "PortDescriptor",
    [
        "power_en",
        "spi_sck",
        "spi_mosi",
        "spi_miso",
        "spi_cs",
        "gdo0",
        "rf_sw0",
        "nfc_cs",
        "nfc_irq",
    ],
)

_port_table = {
    M5.BOARD.M5CardputerADV: PortDescriptor(
        power_en=3,
        spi_sck=40,
        spi_mosi=14,
        spi_miso=39,
        spi_cs=5,
        gdo0=15,
        rf_sw0=13,
        nfc_cs=6,
        nfc_irq=4,
    ),
}


class _CC1101CapSubGHz:
    PREAMBLE_LENGTHS = (16, 24, 32, 48, 64, 96, 128, 192)

    def __init__(
        self,
        pin_cs,
        pin_gdo0,
        pin_gdo2,
        freq_khz,
        bitrate_kbps,
        freq_dev_khz,
        rx_bw_khz,
        output_power,
        preamble_length,
        sync_word_h,
        sync_word_l,
        spi,
        select_bus=None,
        set_rf_switch=None,
    ):
        self._validate_range(preamble_length, 16, 192)
        self._validate_range(sync_word_h, 0, 0xFF)
        self._validate_range(sync_word_l, 0, 0xFF)
        self._validate_range(output_power, -30, 10)

        self._select_bus = select_bus
        self._select()
        self.driver = CC1101Driver(spi=spi, ss=pin_cs, gdo0=pin_gdo0, gdo2=pin_gdo2)
        self.frequency = freq_khz
        self.bitrate = bitrate_kbps
        self.freq_dev = freq_dev_khz
        self.rx_bw = rx_bw_khz
        self.power = output_power
        self.preamble_length = preamble_length
        self.sync_word_h = sync_word_h
        self.sync_word_l = sync_word_l
        self.rx_irq_callback = None
        self.tx_irq_callback = None
        self._in_rx = False
        self._set_rf_switch = set_rf_switch

        self.driver.sync_word_h = sync_word_h
        self.driver.sync_word_l = sync_word_l
        self.driver.begin(
            freq=freq_khz / 1000.0,
            br=bitrate_kbps,
            freq_dev=freq_dev_khz,
            rx_bw=rx_bw_khz,
            pwr=output_power,
            preamble_length=preamble_length,
        )

    def _select(self):
        if self._select_bus:
            self._select_bus()

    def _validate_range(self, value, min_val, max_val):
        if value < min_val or value > max_val:
            raise ValueError("Value {} out of range {} to {}".format(value, min_val, max_val))

    def set_freq(self, freq_khz=868000):
        self._select()
        valid = (
            315000 <= freq_khz <= 348000
            or 415000 <= freq_khz <= 464000
            or 830000 <= freq_khz <= 928000
        )
        if not valid:
            raise ValueError(
                "Frequency {} kHz not in valid ranges "
                "(315000-348000, 415000-464000, 830000-928000)".format(freq_khz)
            )
        if self._set_rf_switch:
            self._set_rf_switch(freq_khz)
        self.frequency = freq_khz
        self.driver._set_frequency(freq_khz / 1000.0)

    def set_bitrate(self, bitrate_kbps):
        self._select()
        self._validate_range(bitrate_kbps, 0.6, 6.0)
        self.bitrate = bitrate_kbps
        self.driver._set_bitrate(bitrate_kbps)

    def set_freq_dev(self, freq_dev_khz):
        self._select()
        self._validate_range(freq_dev_khz, 1.6, 380)
        self.freq_dev = freq_dev_khz
        self.driver._set_frequency_deviation(freq_dev_khz)

    def set_rx_bw(self, rx_bw_khz):
        self._select()
        self._validate_range(rx_bw_khz, 58, 812)
        self.rx_bw = rx_bw_khz
        self.driver._set_rx_bandwidth(rx_bw_khz)

    def set_output_power(self, output_power):
        self._select()
        self._validate_range(output_power, -30, 10)
        self.power = output_power
        self.driver._set_output_power(output_power)

    def set_preamble_length(self, preamble_length):
        self._select()
        if preamble_length not in self.PREAMBLE_LENGTHS:
            raise ValueError(
                "Invalid preamble length {}, must be one of {}".format(
                    preamble_length, self.PREAMBLE_LENGTHS
                )
            )
        self.preamble_length = preamble_length
        self.driver._set_preamble_length(preamble_length)

    def set_sync_word(self, sync_word_h, sync_word_l):
        self._select()
        self._validate_range(sync_word_h, 0, 0xFF)
        self._validate_range(sync_word_l, 0, 0xFF)
        self.sync_word_h = sync_word_h
        self.sync_word_l = sync_word_l
        self.driver._set_sync_word(sync_word_h, sync_word_l)

    def send(self, packet):
        self._select()
        if isinstance(packet, str):
            packet = bytes(packet, "utf-8")
        elif isinstance(packet, (list, tuple)):
            packet = bytes(packet)
        elif isinstance(packet, int):
            packet = bytes((packet,))

        ok = self.driver.transmit(packet)
        if ok:
            self.start_recv()
        return ok

    def recv(self, timeout_ms=None):
        self._select()
        if not self._in_rx:
            self.start_recv()

        if timeout_ms is not None:
            result = self.driver.receive(timeout_ms=timeout_ms)
            self._in_rx = False
            if result and len(result) == 2:
                data, crc_ok = result
                if data:
                    packet = CC1101Packet(
                        data, self.driver.get_rssi(), self.driver.get_lqi(), crc_ok
                    )
                    self.start_recv()
                    return packet
            self.start_recv()
            return None

        if self.driver.check_for_packet():
            result = self.driver._read_data()
            self._in_rx = False
            if result and len(result) == 2:
                data, crc_ok = result
                if data:
                    packet = CC1101Packet(
                        data, self.driver.get_rssi(), self.driver.get_lqi(), crc_ok
                    )
                    self.start_recv()
                    return packet
            self.start_recv()
        return None

    def start_recv(self):
        self._select()
        self._in_rx = True
        self.driver.start_receive()

    def set_rx_irq_callback(self, callback):
        self._select()
        self.rx_irq_callback = callback

        def _rx_irq_callback(packet):
            if self.rx_irq_callback:
                micropython.schedule(self.rx_irq_callback, packet)

        self.driver.set_rx_callback(_rx_irq_callback)

    def set_tx_irq_callback(self, callback):
        self._select()
        self.tx_irq_callback = callback

        def _tx_irq_callback(_):
            if self.tx_irq_callback:
                micropython.schedule(self.tx_irq_callback, None)

        self.driver.set_tx_callback(_tx_irq_callback)

    def standby(self):
        self._select()
        self._in_rx = False
        self.driver.standby()

    def rx_irq_triggered(self):
        self._select()
        return self.driver.rx_irq_triggered()

    def tx_irq_triggered(self):
        self._select()
        return self.driver.tx_irq_triggered()

    def get_rssi(self):
        return self.driver.get_rssi()

    def get_lqi(self):
        return self.driver.get_lqi()

    def get_status(self):
        self._select()
        return self.driver.get_status()


class NFCCap(NFCUnit):
    """Create an NFCCap object for the ST25R3916 on CC1101Cap hardware.

    The CC1101Cap board contains both a CC1101 Sub-GHz radio and an ST25R3916
    NFC reader. Use ``NFCCap`` when working with NFC cards; use ``CC1101Cap``
    when working with Sub-GHz radio.

    MicroPython Code Block:

        .. code-block:: python

            from cap import NFCCap

            nfc = NFCCap()
            card = nfc.detect()
    """

    def __init__(self):
        self._port = _port_table.get(M5.getBoard())
        if self._port is None:
            raise NotImplementedError("NFC CAP is not supported on this board")

        self._power_en = machine.Pin(self._port.power_en, machine.Pin.OUT, value=1)
        self._cc1101_cs = machine.Pin(self._port.spi_cs, machine.Pin.OUT, value=1)
        self._nfc_cs = machine.Pin(self._port.nfc_cs, machine.Pin.OUT, value=1)
        self._spi = machine.SPI(
            1,
            baudrate=2000000,
            polarity=0,
            phase=1,
            sck=machine.Pin(self._port.spi_sck),
            mosi=machine.Pin(self._port.spi_mosi),
            miso=machine.Pin(self._port.spi_miso),
        )
        self._chip = ST25R3916(
            spi=self._spi,
            cs=self._nfc_cs,
            irq=self._port.nfc_irq,
        )
        super().__init__(chip=self._chip)


class CC1101Cap:
    """Create a CC1101Cap object.

    :param float freq_khz: CC1101 RF frequency in kHz.
    :param float bitrate_kbps: Data rate in kbps, range from 0.6 to 6.0 kbps.
    :param float freq_dev_khz: Frequency deviation in kHz, range from 1.6 to 380 kHz.
    :param float rx_bw_khz: Receiver bandwidth in kHz, range from 58 to 812 kHz.
    :param int output_power: Output power in dBm, range from -30 to 10 dBm.
    :param int preamble_length: Preamble length in bits, options: 16, 24, 32, 48, 64, 96, 128, 192.
    :param int sync_word_h: High byte of sync word (0x00 to 0xFF).
    :param int sync_word_l: Low byte of sync word (0x00 to 0xFF).

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from cap import CC1101Cap

            cap_cc1101_0 = CC1101Cap(868000.0, 2.4, 25.4, 58.0, 10, 16, 0x12, 0xAD)
    """

    # CC1101 hardware bands supported by the Cap RF matching network.
    _FREQ_RANGES = (
        (315000, 348000),
        (415000, 464000),
        (830000, 928000),
    )

    _GDO2_FORCE_LOW = 0x2F
    _GDO2_FORCE_HIGH = 0x6F

    def __init__(
        self,
        freq_khz: float = 868000.0,
        bitrate_kbps: float = 2.4,
        freq_dev_khz: float = 25.4,
        rx_bw_khz: float = 58.0,
        output_power: int = 10,
        preamble_length: int = 16,
        sync_word_h: int = 0x12,
        sync_word_l: int = 0xAD,
    ):
        self._port = _port_table.get(M5.getBoard())
        if self._port is None:
            raise NotImplementedError("CC1101 CAP is not supported on this board")

        self._validate_freq(freq_khz)

        self._power_en = machine.Pin(self._port.power_en, machine.Pin.OUT, value=1)
        self._rf_sw0 = machine.Pin(self._port.rf_sw0, machine.Pin.OUT)
        self._subghz_spi = machine.SPI(
            1,
            baudrate=1000000,
            polarity=0,
            phase=0,
            sck=machine.Pin(self._port.spi_sck),
            mosi=machine.Pin(self._port.spi_mosi),
            miso=machine.Pin(self._port.spi_miso),
        )

        self._select_subghz_spi()
        self._set_rf_sw0(freq_khz)
        time.sleep_ms(10)

        self.subghz = _CC1101CapSubGHz(
            pin_cs=self._port.spi_cs,
            pin_gdo0=self._port.gdo0,
            pin_gdo2=None,
            freq_khz=freq_khz,
            bitrate_kbps=bitrate_kbps,
            freq_dev_khz=freq_dev_khz,
            rx_bw_khz=rx_bw_khz,
            output_power=output_power,
            preamble_length=preamble_length,
            sync_word_h=sync_word_h,
            sync_word_l=sync_word_l,
            spi=self._subghz_spi,
            select_bus=self._select_subghz_spi,
            set_rf_switch=self._set_rf_switch,
        )
        self._set_rf_switch(freq_khz)

    def __getattr__(self, attr):
        return getattr(self.subghz, attr)

    def _validate_freq(self, freq_khz):
        for low, high in self._FREQ_RANGES:
            if low <= freq_khz <= high:
                return
        raise ValueError("Frequency must be in 315000-348000, 415000-464000, or 830000-928000 kHz")

    def _switch_state(self, freq_khz):
        if freq_khz < 374000:
            return 0, 1
        if freq_khz < 650500:
            return 1, 0
        return 1, 1

    def _set_rf_sw0(self, freq_khz):
        sw0, _ = self._switch_state(freq_khz)
        self._rf_sw0.value(sw0)

    def _select_subghz_spi(self):
        self._subghz_spi.init(
            baudrate=1000000,
            polarity=0,
            phase=0,
            sck=machine.Pin(self._port.spi_sck),
            mosi=machine.Pin(self._port.spi_mosi),
            miso=machine.Pin(self._port.spi_miso),
        )

    def _set_rf_switch(self, freq_khz):
        self._select_subghz_spi()
        sw0, sw1 = self._switch_state(freq_khz)
        self._rf_sw0.value(sw0)
        self.subghz.driver.write_register(
            self.subghz.driver.IOCFG2, self._GDO2_FORCE_HIGH if sw1 else self._GDO2_FORCE_LOW
        )

    def set_freq(self, freq_khz: int = 868000) -> None:
        """Set frequency in kHz.

        :param int freq_khz: Frequency in kHz. Valid ranges: 315000-348000, 415000-464000, 830000-928000.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                cap_cc1101_0.set_freq(868000.0)
        """
        self._validate_freq(freq_khz)
        self.subghz.set_freq(freq_khz)
