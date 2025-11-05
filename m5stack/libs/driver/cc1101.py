# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import machine
from micropython import const


class CC1101Packet:
    """CC1101 packet class to encapsulate received data"""

    def __init__(self, data, rssi=0, lqi=0, crc_ok=True):
        self.data = data
        self.rssi = rssi
        self.lqi = lqi
        self.crc_ok = crc_ok

    def decode(self):
        """Decode packet data to string"""
        try:
            return self.data.decode("utf-8")
        except:
            return str(self.data)

    def __str__(self):
        return f"CC1101Packet(data={self.data}, rssi={self.rssi}, lqi={self.lqi}, crc_ok={self.crc_ok})"


class CC1101:
    """CC1101 MicroPython implementation based on RadioLib C++ code"""

    # Constants from C++ implementation
    FIFO_BUFFER_SIZE = const(64)
    MAX_PACKET_LENGTH = const(61)  # 64 - 3 bytes for length and address

    # Transfer types
    WRITE_SINGLE_BYTE = const(0x00)
    WRITE_BURST = const(0x40)
    READ_SINGLE_BYTE = const(0x80)
    READ_BURST = const(0xC0)

    # Register types
    CONFIG_REGISTER = const(0x80)
    STATUS_REGISTER = const(0xC0)

    # FIFO and PATABLE addresses
    PATABLE = const(0x3E)
    FIFO = const(0x3F)

    # Configuration registers
    IOCFG2 = const(0x00)
    IOCFG1 = const(0x01)
    IOCFG0 = const(0x02)
    FIFOTHR = const(0x03)
    SYNC1 = const(0x04)
    SYNC0 = const(0x05)
    PKTLEN = const(0x06)
    PKTCTRL1 = const(0x07)
    PKTCTRL0 = const(0x08)
    ADDR = const(0x09)
    CHANNR = const(0x0A)
    FSCTRL1 = const(0x0B)
    FSCTRL0 = const(0x0C)
    FREQ2 = const(0x0D)
    FREQ1 = const(0x0E)
    FREQ0 = const(0x0F)
    MDMCFG4 = const(0x10)
    MDMCFG3 = const(0x11)
    MDMCFG2 = const(0x12)
    MDMCFG1 = const(0x13)
    MDMCFG0 = const(0x14)
    DEVIATN = const(0x15)
    MCSM2 = const(0x16)
    MCSM1 = const(0x17)
    MCSM0 = const(0x18)
    FOCCFG = const(0x19)
    BSCFG = const(0x1A)
    AGCCTRL2 = const(0x1B)
    AGCCTRL1 = const(0x1C)
    AGCCTRL0 = const(0x1D)
    WOREVT1 = const(0x1E)
    WOREVT0 = const(0x1F)
    WORCTRL = const(0x20)
    FREND1 = const(0x21)
    FREND0 = const(0x22)
    FSCAL3 = const(0x23)
    FSCAL2 = const(0x24)
    FSCAL1 = const(0x25)
    FSCAL0 = const(0x26)
    RCCTRL1 = const(0x27)
    RCCTRL0 = const(0x28)
    FSTEST = const(0x29)
    PTEST = const(0x2A)
    AGCTEST = const(0x2B)
    TEST2 = const(0x2C)
    TEST1 = const(0x2D)
    TEST0 = const(0x2E)

    # Status registers
    PARTNUM = const(0x30)
    VERSION = const(0x31)
    FREQEST = const(0x32)
    LQI = const(0x33)
    RSSI = const(0x34)
    MARCSTATE = const(0x35)
    WORTIME1 = const(0x36)
    WORTIME0 = const(0x37)
    PKTSTATUS = const(0x38)
    VCO_VC_DAC = const(0x39)
    TXBYTES = const(0x3A)
    RXBYTES = const(0x3B)
    RCCTRL1_STATUS = const(0x3C)
    RCCTRL0_STATUS = const(0x3D)

    # Command strobes
    SRES = const(0x30)
    SFSTXON = const(0x31)
    SXOFF = const(0x32)
    SCAL = const(0x33)
    SRX = const(0x34)
    STX = const(0x35)
    SIDLE = const(0x36)
    SAFC = const(0x37)
    SWOR = const(0x38)
    SPWD = const(0x39)
    SFRX = const(0x3A)
    SFTX = const(0x3B)
    SWORRST = const(0x3C)
    SNOP = const(0x3D)

    # MARC states
    MARCSTATE_IDLE = const(0x01)
    MARCSTATE_RX = const(0x0D)
    MARCSTATE_TX = const(0x13)
    MARCSTATE_TXFIFO_UNDERFLOW = const(0x16)
    MARCSTATE_RXFIFO_OVERFLOW = const(0x11)

    # Default values (matching C code defaults)
    DEFAULT_FREQ = 868.0  # CC1101_FREQ_MHZ
    DEFAULT_BITRATE = 2.4  # CC1101_BITRATE_KBPS
    DEFAULT_FREQ_DEV = 25.4  # CC1101_FREQ_DEV_KHZ
    DEFAULT_RX_BW = 58.0  # CC1101_BW_KHZ
    DEFAULT_POWER = 10  # 10 dBm
    DEFAULT_PREAMBLE = 16  # 16 bits
    DEFAULT_SYNC_H = 0x12  # Default sync word high (from ESP-IDF logic analyzer)
    DEFAULT_SYNC_L = 0xAD  # Default sync word low (from ESP-IDF logic analyzer)
    DEFAULT_RX_TIMEOUT = 500  # 500 ms (from C code)

    def __init__(self, spi, ss, gdo0, gdo2=None):
        """Initialize CC1101

        :param spi: SPI object
        :param ss: Chip select pin
        :param gdo0: GDO0 pin (interrupt pin)
        :param gdo2: GDO2 pin (optional)
        """
        self.spi = spi
        self.ss = machine.Pin(ss, mode=machine.Pin.OUT)
        self.gdo0 = machine.Pin(gdo0, mode=machine.Pin.IN)
        self.gdo2 = machine.Pin(gdo2, mode=machine.Pin.IN) if gdo2 else None

        # Deselect initially
        self.deselect()

        # Set up interrupt on GDO0 pin
        # GDO0 triggers on rising edge when packet is received
        self.gdo0.irq(self._radio_rx_isr, machine.Pin.IRQ_RISING)

        # Set up interrupt on GDO2 pin (if available)
        # GDO2 triggers on falling edge when packet is sent
        if self.gdo2:
            self.gdo2.irq(self._radio_tx_isr, machine.Pin.IRQ_FALLING)

        # Configuration parameters
        self.frequency = self.DEFAULT_FREQ
        self.bitrate = self.DEFAULT_BITRATE
        self.freq_dev = self.DEFAULT_FREQ_DEV
        self.rx_bw = self.DEFAULT_RX_BW
        self.power = self.DEFAULT_POWER
        self.preamble_length = self.DEFAULT_PREAMBLE
        self.sync_word_h = self.DEFAULT_SYNC_H
        self.sync_word_l = self.DEFAULT_SYNC_L

        # Internal state
        self.packet_length_queried = False
        self.packet_length = 0
        self.raw_rssi = 0
        self.raw_lqi = 0
        self.crc_on = True
        self.promiscuous = False

        # Callback mechanism
        self._rx_callback = None
        self._tx_callback = None
        self._last_rx_irq = None
        self._last_tx_irq = None

    def select(self):
        """Select CC1101 chip"""
        self.ss.value(0)

    def deselect(self):
        """Deselect CC1101 chip"""
        self.ss.value(1)

    def write_command(self, command):
        """Write command strobe"""
        buf = bytearray((command,))
        self.select()
        self.spi.write(buf)
        self.deselect()
        return buf[0]

    def write_register(self, address, data):
        """Write single byte to configuration register"""
        buf = bytearray(2)
        buf[0] = address | self.WRITE_SINGLE_BYTE
        buf[1] = data
        self.select()
        self.spi.write(buf)
        self.deselect()

    def set_register_value(self, address, value, msb, lsb):
        """Set specific bits in register (like RadioLib SPIsetRegValue)"""
        # Read current value
        current = self.read_register(address)

        # Create mask for the bits we want to change
        mask = 0
        for i in range(lsb, msb + 1):
            mask |= 1 << i

        # Clear the bits we want to change and set new value
        new_value = (current & ~mask) | (value & mask)

        # Write back
        self.write_register(address, new_value)

    def read_register(self, address, register_type=0x80):
        """Read value from configuration or status register"""
        read_buf = bytearray(2)
        write_buf = bytearray(2)
        write_buf[0] = address | register_type
        self.select()
        self.spi.write_readinto(write_buf, read_buf)
        self.deselect()
        return read_buf[1]

    def read_burst(self, address, length):
        """Read values from consecutive configuration registers"""
        buf = bytearray(length + 1)
        buf[0] = address | self.READ_BURST
        self.select()
        self.spi.write_readinto(buf, buf)
        self.deselect()
        return buf[1:]

    def write_burst(self, address, data):
        """Write data to consecutive registers"""
        buf = bytearray(1)
        buf[0] = address | self.WRITE_BURST
        buf.extend(data)
        self.select()
        self.spi.write(buf)
        self.deselect()

    def reset(self):
        """Reset CC1101 chip"""
        self.deselect()
        time.sleep_us(5)
        self.select()
        time.sleep_us(10)
        self.deselect()
        time.sleep_us(45)
        self.select()

        self.write_command(self.SRES)
        time.sleep_ms(10)
        self.deselect()

    def get_chip_version(self):
        """Get CC1101 chip version"""
        return self.read_register(self.VERSION, self.STATUS_REGISTER)

    def wait_for_idle(self):
        """Wait for CC1101 to enter idle state"""
        timeout = 1000  # 1 second timeout
        while timeout > 0:
            marc_state = self.read_register(self.MARCSTATE, self.STATUS_REGISTER) & 0x1F
            if marc_state == self.MARCSTATE_IDLE:
                return True
            time.sleep_ms(1)
            timeout -= 1
        return False

    def _radio_rx_isr(self, _):
        """Radio receive interrupt service routine"""
        self._last_rx_irq = time.ticks_ms()

        # Check if module is in RX state (not TX or IDLE)
        marc_state = self.read_register(self.MARCSTATE, self.STATUS_REGISTER) & 0x1F
        if marc_state != self.MARCSTATE_RX:
            return

        if self._rx_callback:
            # Check if packet is available
            if self.check_for_packet():
                # Read the packet
                result = self._read_data()
                if result and len(result) == 2:
                    packet_data, crc_ok = result
                    if packet_data:  # Check if we actually got data
                        # Create packet object
                        packet = CC1101Packet(packet_data, self.get_rssi(), self.get_lqi(), crc_ok)
                        # Call the callback
                        self._rx_callback(packet)
                # Note: _read_data() already restarts receive mode, so no need to do it here

    def _radio_tx_isr(self, _):
        """Radio transmit interrupt service routine"""
        self._last_tx_irq = time.ticks_ms()
        if self._tx_callback:
            self._tx_callback(_)

    def set_rx_callback(self, callback):
        """Set callback function for received packets

        :param callback: Function to call when packet is received
        """
        self._rx_callback = callback

    def set_tx_callback(self, callback):
        """Set callback function for transmitted packets

        :param callback: Function to call when packet is transmitted
        """
        self._tx_callback = callback

    def calculate_frequency_regs(self, freq_mhz):
        """Calculate frequency register values"""
        # CC1101 frequency calculation: f_carrier = (f(XOSC) / 2^16) * FREQ
        # where f(XOSC) = 26 MHz
        xosc_freq = 26.0  # MHz
        freq_reg = int((freq_mhz * (2**16)) / xosc_freq)

        freq2 = (freq_reg >> 16) & 0xFF
        freq1 = (freq_reg >> 8) & 0xFF
        freq0 = freq_reg & 0xFF

        return freq2, freq1, freq0

    def calculate_bitrate_regs(self, bitrate_kbps):
        """Calculate bitrate register values"""
        # Bitrate calculation: R_data = (((256 + DRATE_M) * 2^DRATE_E) / 2^28) * f(XOSC)
        xosc_freq = 26.0  # MHz
        target_rate = bitrate_kbps * 1000  # Convert to bps

        # Find best DRATE_E and DRATE_M combination
        best_error = float("inf")
        best_e = 0
        best_m = 0

        for e in range(16):  # DRATE_E: 0-15
            for m in range(256):  # DRATE_M: 0-255
                calculated_rate = ((256 + m) * (2**e)) / (2**28) * xosc_freq * 1000000
                error = abs(calculated_rate - target_rate)
                if error < best_error:
                    best_error = error
                    best_e = e
                    best_m = m

        return best_e, best_m

    def calculate_rx_bw_regs(self, rx_bw_khz):
        """Calculate receiver bandwidth register values"""
        # Bandwidth calculation: BW_channel = f(XOSC) / (8 * (4 + CHANBW_M) * 2^CHANBW_E)
        xosc_freq = 26.0  # MHz
        target_bw = rx_bw_khz * 1000  # Convert to Hz

        # Find best CHANBW_E and CHANBW_M combination
        best_error = float("inf")
        best_e = 0
        best_m = 0

        for e in range(4):  # CHANBW_E: 0-3
            for m in range(4):  # CHANBW_M: 0-3
                calculated_bw = xosc_freq * 1000000 / (8 * (4 + m) * (2**e))
                error = abs(calculated_bw - target_bw)
                if error < best_error:
                    best_error = error
                    best_e = e
                    best_m = m

        return best_e, best_m

    def calculate_freq_dev_regs(self, freq_dev_khz):
        """Calculate frequency deviation register values"""
        # Deviation calculation: f_dev = (f(XOSC) / 2^17) * (8 + DEVIATION_M) * 2^DEVIATION_E
        xosc_freq = 26.0  # MHz
        target_dev = freq_dev_khz * 1000  # Convert to Hz

        # Find best DEVIATION_E and DEVIATION_M combination
        best_error = float("inf")
        best_e = 0
        best_m = 0

        for e in range(8):  # DEVIATION_E: 0-7
            for m in range(8):  # DEVIATION_M: 0-7
                calculated_dev = (xosc_freq * 1000000 / (2**17)) * (8 + m) * (2**e)
                error = abs(calculated_dev - target_dev)
                if error < best_error:
                    best_error = error
                    best_e = e
                    best_m = m

        return best_e, best_m

    def get_power_table(self, power_dbm):
        """Get power amplifier table for given output power"""
        # Power table mapping based on frequency bands
        if self.frequency < 374.0:
            # 315 MHz
            f = 0
        elif self.frequency < 650.5:
            # 434 MHz
            f = 1
        elif self.frequency < 891.5:
            # 868 MHz
            f = 2
        else:
            # 915 MHz
            f = 3

        # Power table [power_dbm][frequency_band]
        pa_table = [
            [0x12, 0x12, 0x03, 0x03],  # -30 dBm
            [0x0D, 0x0E, 0x0F, 0x0E],  # -20 dBm
            [0x1C, 0x1D, 0x1E, 0x1E],  # -15 dBm
            [0x34, 0x34, 0x27, 0x27],  # -10 dBm
            [0x51, 0x60, 0x50, 0x8E],  # 0 dBm
            [0x85, 0x84, 0x81, 0xCD],  # 5 dBm
            [0xCB, 0xC8, 0xCB, 0xC7],  # 7 dBm
            [0xC2, 0xC0, 0xC2, 0xC0],  # 10 dBm
        ]

        power_levels = [-30, -20, -15, -10, 0, 5, 7, 10]

        for i, level in enumerate(power_levels):
            if power_dbm == level:
                return bytes([pa_table[i][f]])

        # Default to 10 dBm
        return bytes([pa_table[7][f]])

    def begin(self, freq=None, br=None, freq_dev=None, rx_bw=None, pwr=None, preamble_length=None):
        """Initialize CC1101 (like RadioLib begin method)

        :param freq: Frequency in MHz
        :param br: Bitrate in kbps
        :param freq_dev: Frequency deviation in kHz
        :param rx_bw: RX bandwidth in kHz
        :param pwr: Output power in dBm
        :param preamble_length: Preamble length in bits
        """
        # Update parameters if provided
        if freq is not None:
            self.frequency = freq
        if br is not None:
            self.bitrate = br
        if freq_dev is not None:
            self.freq_dev = freq_dev
        if rx_bw is not None:
            self.rx_bw = rx_bw
        if pwr is not None:
            self.power = pwr
        if preamble_length is not None:
            self.preamble_length = preamble_length

        # Check chip version first (like ESP-IDF)
        version = self.get_chip_version()

        # Reset the chip
        self.reset()
        time.sleep_ms(150)  # Wait for reset to complete
        valid_versions = [
            0x04,
            0x14,
            0x17,
            0x00,
            0x20,
        ]  # LEGACY, CURRENT, CLONE, and other variants
        if version not in valid_versions:
            raise RuntimeError(
                f"Unexpected CC1101 chip version 0x{version:02X} (expected one of {[hex(v) for v in valid_versions]}). Please check module connection."
            )

        # Configure basic settings
        self._config_basic_settings()

        # Configure frequency
        self._set_frequency(self.frequency)

        # Configure bitrate
        self._set_bitrate(self.bitrate)

        # Configure RX bandwidth
        self._set_rx_bandwidth(self.rx_bw)

        # Configure frequency deviation
        self._set_frequency_deviation(self.freq_dev)

        # Configure output power
        self._set_output_power(self.power)

        # Set variable packet length mode
        self._set_variable_packet_length()

        # Configure preamble length
        self._set_preamble_length(self.preamble_length)

        # Configure sync word
        self._set_sync_word(self.sync_word_h, self.sync_word_l)

        # Flush FIFOs
        self.write_command(self.SFRX)
        self.write_command(self.SFTX)

        return True

    def _config_basic_settings(self):
        """Configure basic CC1101 settings"""
        # Enter idle mode
        self.write_command(self.SIDLE)
        self.wait_for_idle()

        # MCSM0: Enable automatic frequency synthesizer calibration (matching RadioLib)
        # Set FS_AUTOCAL_IDLE_TO_RXTX (bits 5-4) and PIN_CTRL_OFF (bit 1)
        self.set_register_value(self.MCSM0, 0x10, 5, 4)  # FS_AUTOCAL_IDLE_TO_RXTX
        self.set_register_value(self.MCSM0, 0x00, 1, 1)  # PIN_CTRL_OFF

        # Set GDOs to Hi-Z initially (matching RadioLib)
        self.set_register_value(self.IOCFG0, 0x2E, 5, 0)  # GDOX_HIGH_Z
        self.set_register_value(self.IOCFG2, 0x2E, 5, 0)  # GDOX_HIGH_Z

        # Configure other basic settings
        # MCSM1: Set RXOFF_MODE to RX (0x0C) to stay in RX after packet reception
        # This is crucial for continuous receive mode
        self.set_register_value(self.MCSM1, 0x0C, 3, 2)  # RXOFF_RX
        self.write_register(self.MCSM2, 0x07)  # No RX timeout

        # AGC settings
        self.write_register(self.AGCCTRL2, 0x03)
        self.write_register(self.AGCCTRL1, 0x40)
        self.write_register(self.AGCCTRL0, 0x91)

        # Frontend settings
        self.write_register(self.FREND1, 0x56)
        self.write_register(self.FREND0, 0x10)

        # Frequency synthesizer settings
        self.write_register(self.FSCAL3, 0xE9)
        self.write_register(self.FSCAL2, 0x2A)
        self.write_register(self.FSCAL1, 0x00)
        self.write_register(self.FSCAL0, 0x1F)

        # Test settings
        self.write_register(self.TEST2, 0x81)
        self.write_register(self.TEST1, 0x35)
        self.write_register(self.TEST0, 0x09)

        # Calibrate frequency synthesizer
        self.write_command(self.SCAL)
        time.sleep_ms(1)
        self.wait_for_idle()

    def start_receive(self):
        """Start reception mode (like RadioLib startReceive)"""
        try:
            # Set mode to standby
            self.write_command(self.SIDLE)
            self.wait_for_idle()

            # Flush RX FIFO
            self.write_command(self.SFRX)

            # Set GDO0 mapping for packet received detection
            # Use GDOX_SYNC_WORD_SENT_OR_PKT_RECEIVED (0x06) for rising edge trigger
            self.write_register(self.IOCFG0, 0x06)

            # Start reception
            self.write_command(self.SRX)

            return True

        except Exception as e:
            print(f"Start receive error: {e}")
            return False

    def check_for_packet(self):
        """Check if a packet is available (non-blocking)"""
        try:
            # Check if GDO0 indicates packet received
            # GDO0 goes high when packet is received
            if self.gdo0.value() == 1:
                # Wait for packet to complete (with timeout to avoid blocking)
                timeout = 100  # 100ms timeout
                while self.gdo0.value() == 1 and timeout > 0:
                    time.sleep_ms(1)
                    timeout -= 1
                return True
            return False
        except Exception as e:
            print(f"Check packet error: {e}")
            return False

    def _set_frequency(self, freq_mhz):
        """Set CC1101 frequency"""
        freq2, freq1, freq0 = self.calculate_frequency_regs(freq_mhz)
        self.write_register(self.FREQ2, freq2)
        self.write_register(self.FREQ1, freq1)
        self.write_register(self.FREQ0, freq0)

    def _set_bitrate(self, bitrate_kbps):
        """Set CC1101 bitrate"""
        drate_e, drate_m = self.calculate_bitrate_regs(bitrate_kbps)
        # MDMCFG4: Set exponent part of data rate (matching RadioLib)
        self.set_register_value(self.MDMCFG4, drate_e, 3, 0)
        self.write_register(self.MDMCFG3, drate_m)

    def _set_rx_bandwidth(self, rx_bw_khz):
        """Set CC1101 RX bandwidth"""
        chanbw_e, chanbw_m = self.calculate_rx_bw_regs(rx_bw_khz)
        # Read current MDMCFG4 and update only bandwidth bits
        current_mdmcfg4 = self.read_register(self.MDMCFG4)
        new_mdmcfg4 = (chanbw_e << 6) | (chanbw_m << 4) | (current_mdmcfg4 & 0x0F)
        self.write_register(self.MDMCFG4, new_mdmcfg4)

    def _set_frequency_deviation(self, freq_dev_khz):
        """Set CC1101 frequency deviation"""
        dev_e, dev_m = self.calculate_freq_dev_regs(freq_dev_khz)
        self.write_register(self.DEVIATN, (dev_e << 4) | dev_m)

    def _set_output_power(self, power_dbm):
        """Set CC1101 output power"""
        power_table = self.get_power_table(power_dbm)
        self.write_burst(self.PATABLE, power_table)

    def _set_variable_packet_length(self):
        """Set CC1101 to variable packet length mode"""
        # PKTCTRL0: Variable packet length, enable CRC (matching RadioLib)
        self.set_register_value(self.PKTCTRL0, 0x00, 6, 4)  # WHITE_DATA_OFF | PKT_FORMAT_NORMAL
        self.set_register_value(self.PKTCTRL0, 0x05, 2, 0)  # CRC_ON | LENGTH_CONFIG_VARIABLE

        # PKTCTRL1: CRC_AUTOFLUSH_OFF | APPEND_STATUS_ON | ADR_CHK_NONE
        self.set_register_value(self.PKTCTRL1, 0x04, 3, 0)

    def _set_preamble_length(self, preamble_bits):
        """Set CC1101 preamble length"""
        preamble_map = {
            16: 0x00,
            24: 0x10,
            32: 0x20,
            48: 0x30,
            64: 0x40,
            96: 0x50,
            128: 0x60,
            192: 0x70,
        }
        preamble_reg = preamble_map.get(preamble_bits, 0x00)

        current_mdmcfg1 = self.read_register(self.MDMCFG1)
        new_mdmcfg1 = preamble_reg | (current_mdmcfg1 & 0x0F)
        self.write_register(self.MDMCFG1, new_mdmcfg1)

    def _set_sync_word(self, sync_h, sync_l):
        """Set CC1101 sync word (matching RadioLib)"""
        self.set_register_value(self.SYNC1, sync_h, 7, 0)
        self.set_register_value(self.SYNC0, sync_l, 7, 0)

    def transmit(self, data, addr=0):
        """Transmit data
        :param data: Data to transmit (string or bytes)
        :param addr: Address (optional)
        :return: True if successful, False otherwise
        """
        try:
            # Convert string to bytes if needed
            if isinstance(data, str):
                data_bytes = data.encode("utf-8")
            else:
                data_bytes = data

            if len(data_bytes) > self.MAX_PACKET_LENGTH:
                return False

            # Start transmission
            if not self._start_transmit(data_bytes, addr):
                return False

            # Wait for transmission using GDO2 edges if available (RadioLib style)
            timeout = 5 + int(((len(data_bytes) * 8) / self.bitrate) * 5)
            if timeout < 50:
                timeout = 50
            if self.gdo2 is not None:
                # Wait for TX start: GDO2 goes high
                start = time.ticks_ms()
                while self.gdo2.value() == 0:
                    if time.ticks_diff(time.ticks_ms(), start) > timeout:
                        self._finish_transmit()
                        return False
                    time.sleep_ms(1)
                # Wait for TX end: GDO2 goes low
                start = time.ticks_ms()
                while self.gdo2.value() == 1:
                    if time.ticks_diff(time.ticks_ms(), start) > timeout:
                        self._finish_transmit()
                        return False
                    time.sleep_ms(1)
            else:
                # Fallback: poll MARCSTATE - wait enter TX then leave TX
                enter_timeout = 50
                while enter_timeout > 0:
                    marc_state = self.read_register(self.MARCSTATE, self.STATUS_REGISTER) & 0x1F
                    if marc_state == self.MARCSTATE_TX:
                        break
                    time.sleep_ms(1)
                    enter_timeout -= 1
                leave_timeout = timeout
                while leave_timeout > 0:
                    marc_state = self.read_register(self.MARCSTATE, self.STATUS_REGISTER) & 0x1F
                    if marc_state != self.MARCSTATE_TX:
                        break
                    time.sleep_ms(1)
                    leave_timeout -= 1

            # Finish transmission
            self._finish_transmit()
            return True

        except Exception as e:
            print(f"Transmit error: {e}")
            return False

    def _start_transmit(self, data_bytes, addr=0):
        """Start transmission (like RadioLib startTransmit)"""
        try:
            # Set mode to standby
            self.write_command(self.SIDLE)
            self.wait_for_idle()

            # Flush TX FIFO
            self.write_command(self.SFTX)

            # Set GDO0 mapping for sync word sent or packet received (matching ESP-IDF)
            self.set_register_value(self.IOCFG0, 0x06, 5, 0)  # GDOX_SYNC_WORD_SENT_OR_PKT_RECEIVED

            # Set GDO2 mapping for TX completion interrupt (if GDO2 is available)
            if self.gdo2:
                self.set_register_value(
                    self.IOCFG2, 0x06, 5, 0
                )  # GDOX_SYNC_WORD_SENT_OR_PKT_RECEIVED

            # Write packet length (variable length mode)
            self.write_register(self.FIFO, len(data_bytes))

            # Write data to FIFO
            self.write_burst(self.FIFO, data_bytes)

            # Start transmission
            self.write_command(self.STX)

            return True

        except Exception as e:
            print(f"Start transmit error: {e}")
            return False

    def _finish_transmit(self):
        """Finish transmission (like RadioLib finishTransmit)"""
        try:
            # Set mode to standby
            self.write_command(self.SIDLE)
            self.wait_for_idle()

            # Flush TX FIFO
            self.write_command(self.SFTX)

            # Restart receive mode to be ready for next packet
            self._start_receive()

        except Exception as e:
            print(f"Finish transmit error: {e}")

    def receive(self, data=None, length=0):
        """Receive data (like RadioLib receive method) - BLOCKING

        :param data: Buffer to store received data (optional)
        :param length: Maximum length to receive (optional)
        :return: Received data as bytes, or empty bytes if no data
        """
        try:
            # Calculate timeout (500 ms + 400 full max-length packets at current bit rate)
            timeout = 500 + (1.0 / self.bitrate) * (self.MAX_PACKET_LENGTH * 400.0)

            # Start reception
            if not self._start_receive():
                return b""

            # Wait for packet start or timeout (GDO0 goes from low to high)
            start_time = time.ticks_ms()
            while self.gdo0.value() == 0:  # GDO0 low means waiting for packet
                if time.ticks_diff(time.ticks_ms(), start_time) > timeout:
                    self.standby()
                    self.write_command(self.SFRX)
                    return b""
                time.sleep_ms(1)

            # Wait for packet end or timeout (GDO0 goes from high to low)
            start_time = time.ticks_ms()
            while self.gdo0.value() == 1:  # GDO0 high means packet in progress
                if time.ticks_diff(time.ticks_ms(), start_time) > timeout:
                    self.standby()
                    self.write_command(self.SFRX)
                    return b""
                time.sleep_ms(1)

            # Read packet data
            return self._read_data(length)

        except Exception as e:
            print(f"Receive error: {e}")
            return b""

    def receive_polling(self, data=None, length=0):
        """Receive data in polling mode - NON-BLOCKING

        :param data: Buffer to store received data (optional)
        :param length: Maximum length to receive (optional)
        :return: Received data as bytes, or empty bytes if no data
        """
        try:
            # Just check if packet is available (non-blocking)
            if not self.check_for_packet():
                return b""

            # Read packet data
            return self._read_data(length)

        except Exception as e:
            print(f"Receive polling error: {e}")
            return b""

    def _start_receive(self):
        """Start reception (like RadioLib startReceive)"""
        try:
            # Set mode to standby
            if not self.standby():
                return False

            # Flush RX FIFO
            self.write_command(self.SFRX)

            # Set GDO0 mapping
            # GDO0 goes high when packet is received
            # Use GDOX_SYNC_WORD_SENT_OR_PKT_RECEIVED (0x06) for rising edge trigger
            self.write_register(self.IOCFG0, 0x06)

            # Set mode to receive
            self.write_command(self.SRX)

            return True

        except Exception as e:
            print(f"Start receive error: {e}")
            return False

    def _read_data(self, max_length=0):
        """Read received data (like RadioLib readData)"""
        try:
            # Get packet length
            packet_length = self._get_packet_length()
            if packet_length == 0:
                return b""

            # Limit length if specified
            if max_length > 0 and max_length < packet_length:
                packet_length = max_length

            # Check address filtering
            filter_val = (self.read_register(self.PKTCTRL1) >> 0) & 0x03
            if filter_val != 0:  # ADR_CHK_NONE
                self.read_register(self.FIFO)  # Skip address byte

            # Read packet data
            data = self.read_burst(self.FIFO, packet_length)

            # Check if status bytes are enabled (default: APPEND_STATUS_ON)
            is_append_status = ((self.read_register(self.PKTCTRL1) >> 2) & 0x01) == 1

            if is_append_status:
                # Read RSSI byte
                self.raw_rssi = self.read_register(self.FIFO)

                # Read LQI and CRC byte
                val = self.read_register(self.FIFO)
                self.raw_lqi = val & 0x7F

                # Check CRC
                if self.crc_on and (val & 0x80) == 0:  # CRC_ERROR (0x80 = CRC_OK bit)
                    self.packet_length_queried = False
                    # CRC error detected, will be returned in crc_ok flag

            # Clear internal flag so getPacketLength can return the new packet length
            self.packet_length_queried = False

            # Flush then standby according to RXOFF_MODE (default: RXOFF_IDLE)
            if ((self.read_register(self.MCSM1) >> 2) & 0x03) == 0:  # RXOFF_IDLE
                # Set mode to standby
                self.standby()
                # Flush Rx FIFO
                self.write_command(self.SFRX)

            # Return data and CRC status
            crc_ok = True
            if self.crc_on and (val & 0x80) == 0:  # CRC_ERROR
                crc_ok = False
            return data, crc_ok

        except Exception as e:
            print(f"Read data error: {e}")
            return b"", False

    def _rssi_to_dbm(self, raw_rssi):
        """Convert raw RSSI value to dBm"""
        if raw_rssi >= 128:
            return (raw_rssi - 256) / 2.0 - 74.0
        else:
            return raw_rssi / 2.0 - 74.0

    def get_rssi(self):
        """Get last received RSSI in dBm"""
        if hasattr(self, "raw_rssi"):
            return self._rssi_to_dbm(self.raw_rssi)
        return 0

    def get_lqi(self):
        """Get last received LQI"""
        if hasattr(self, "raw_lqi"):
            return self.raw_lqi
        return 0

    def get_marc_state(self):
        """Get current MARC state"""
        try:
            marc_state = self.read_register(self.MARCSTATE)
            return marc_state
        except Exception as e:
            print(f"MARC state error: {e}")
            return 0

    def _get_packet_length(self):
        """Get packet length from FIFO"""
        if not self.packet_length_queried:
            self.packet_length = self.read_register(self.FIFO)
            self.packet_length_queried = True
        return self.packet_length

    def standby(self):
        """Set module to standby mode"""
        try:
            self.write_command(self.SIDLE)
            self.wait_for_idle()
            # Clear IRQ flags when going to standby (like LoRa module)
            self._last_rx_irq = None
            self._last_tx_irq = None
            return True
        except Exception as e:
            print(f"Standby error: {e}")
            return False

    def rx_irq_triggered(self):
        """Returns True if the RX ISR has executed since the last time a send or a receive started"""
        return self._last_rx_irq is not None

    def tx_irq_triggered(self):
        """Returns True if the TX ISR has executed since the last time a send or a receive started"""
        return self._last_tx_irq is not None

    def get_status(self):
        """Get module status"""
        try:
            marc_state = self.read_register(self.MARCSTATE, self.STATUS_REGISTER) & 0x1F
            rssi = self.get_rssi()
            lqi = self.get_lqi()

            return {"marc_state": marc_state, "rssi": rssi, "lqi": lqi}
        except Exception as e:
            print(f"Status error: {e}")
            return {"marc_state": 0, "rssi": 0.0, "lqi": 0}
