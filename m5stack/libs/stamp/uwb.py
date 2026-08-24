# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
import math
import uwb as _uwb
from collections import namedtuple
from uwb import UWB as _UWB

from .f12 import StampF12


UWBIO = namedtuple("UWBIO", ["irq", "wakeup", "reset", "mosi", "miso", "clock", "cs", "sync"])

try:
    _f12 = StampF12()
except NotImplementedError:
    iomap = None
else:
    iomap = UWBIO(
        irq=_f12.pin(StampF12.IRQ),
        wakeup=_f12.pin(StampF12.BUSY),
        reset=_f12.pin(StampF12.RST),
        mosi=_f12.pin(StampF12.MOSI),
        miso=_f12.pin(StampF12.MISO),
        clock=_f12.pin(StampF12.CLK),
        cs=_f12.pin(StampF12.CS),
        sync=_f12.pin(StampF12.SW),  # QM33120 GP7/SYNC; unused by DS-TWR.
    )


class StampUWB:
    """QM33120/DW3720 UWB device configured for the current Stamp host.

    The PHY channel is fixed to channel 9. Only one active instance is allowed.
    Passing ``None`` for a pin uses the current board's default mapping.

    :param int irq: IRQ pin. Defaults are 21 on StampS3Mini and 0 on StampC6/C5.
    :param int wakeup: WAKEUP pin. Defaults are 39 on StampS3Mini, 18 on StampC6, and 24 on StampC5.
    :param int reset: RESET pin. Defaults are 40 on StampS3Mini, 19 on StampC6, and 25 on StampC5.
    :param int mosi: SPI MOSI pin. Defaults are 42 on StampS3Mini, 21 on StampC6, and 27 on StampC5.
    :param int miso: SPI MISO pin. Defaults are 41 on StampS3Mini, 20 on StampC6, and 26 on StampC5.
    :param int clock: SPI clock pin. Defaults are 44 on StampS3Mini, 23 on StampC6, and 12 on StampC5.
    :param int cs: SPI chip-select pin. Defaults are 43 on StampS3Mini, 22 on StampC6, and 11 on StampC5.

    MicroPython Code Block:

        .. code-block:: python

            from stamp import StampUWB

            radio = StampUWB()
    """

    CHANNEL = 9
    PREAMBLE_LENGTHS = (32, 64, 72, 128, 256, 512, 1024, 1536, 2048, 4096)
    PAC_SIZES = (4, 8, 16, 32)
    PREAMBLE_CODE_MIN = 9
    PREAMBLE_CODE_MAX = 12
    MAX_PAYLOAD = 125

    def __init__(
        self,
        irq=None,
        wakeup=None,
        reset=None,
        mosi=None,
        miso=None,
        clock=None,
        cs=None,
    ):
        provided = (irq, wakeup, reset, mosi, miso, clock, cs)
        if iomap is None and any(pin is None for pin in provided):
            raise ValueError(
                "irq, wakeup, reset, mosi, miso, clock, and cs are required " "for this Stamp host"
            )
        pins = {
            "irq": iomap.irq if irq is None and iomap is not None else irq,
            "wakeup": iomap.wakeup if wakeup is None and iomap is not None else wakeup,
            "reset": iomap.reset if reset is None and iomap is not None else reset,
            "mosi": iomap.mosi if mosi is None and iomap is not None else mosi,
            "miso": iomap.miso if miso is None and iomap is not None else miso,
            "clock": iomap.clock if clock is None and iomap is not None else clock,
            "cs": iomap.cs if cs is None and iomap is not None else cs,
        }
        self._device = _UWB(**pins)

    @staticmethod
    def _check_range(name, value, minimum, maximum):
        if not minimum <= value <= maximum:
            raise ValueError("%s must be in range %d-%d" % (name, minimum, maximum))
        return value

    @staticmethod
    def _check_choice(name, value, choices):
        if value not in choices:
            raise ValueError("invalid %s" % name)
        return value

    @staticmethod
    def _check_fixed(name, value, expected):
        if value != expected:
            raise ValueError("unsupported %s" % name)
        return value

    def configure(
        self,
        preamble_length=128,
        pac=8,
        tx_code=9,
        rx_code=9,
        sfd_type=_uwb.SFD_DW_8,
        data_rate=_uwb.BR_6M8,
        phr_mode=_uwb.PHR_STD,
        phr_rate=_uwb.PHR_RATE_STD,
        sfd_timeout=129,
    ):
        """Configure the channel 9 UWB PHY.

        :param int preamble_length: Preamble length in symbols. Allowed values are 32, 64, 72, 128, 256, 512, 1024, 1536, 2048, and 4096. Default is 128.
        :param int pac: Preamble acquisition chunk size. Allowed values are 4, 8, 16, and 32. Default is 8.
        :param int tx_code: Channel 9 TX preamble code, range 9-12. Default is 9.
        :param int rx_code: Channel 9 RX preamble code, range 9-12. Default is 9.
        :param int sfd_type: SFD type. Only ``uwb.SFD_DW_8`` is currently supported.
        :param int data_rate: PHY data rate. Only ``uwb.BR_6M8`` is currently supported.
        :param int phr_mode: PHR mode. Only ``uwb.PHR_STD`` is currently supported.
        :param int phr_rate: PHR rate. Only ``uwb.PHR_RATE_STD`` is currently supported.
        :param int sfd_timeout: SFD timeout in symbols, range 0-65535. Default is 129.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.configure(
                    preamble_length=128,
                    pac=8,
                    tx_code=9,
                    rx_code=9,
                    sfd_type=uwb.SFD_DW_8,
                    data_rate=uwb.BR_6M8,
                    phr_mode=uwb.PHR_STD,
                    phr_rate=uwb.PHR_RATE_STD,
                    sfd_timeout=129,
                )
        """
        return self._configure(
            preamble_length=preamble_length,
            pac=pac,
            tx_code=tx_code,
            rx_code=rx_code,
            sfd_type=sfd_type,
            data_rate=data_rate,
            phr_mode=phr_mode,
            phr_rate=phr_rate,
            sfd_timeout=sfd_timeout,
            sts_mode=_uwb.STS_OFF,
            sts_length=64,
            pdoa_mode=_uwb.PDOA_M0,
        )

    def _configure(
        self,
        preamble_length,
        pac,
        tx_code,
        rx_code,
        sfd_type,
        data_rate,
        phr_mode,
        phr_rate,
        sfd_timeout,
        sts_mode,
        sts_length,
        pdoa_mode,
    ):
        self._check_choice("preamble_length", preamble_length, self.PREAMBLE_LENGTHS)
        self._check_choice("pac", pac, self.PAC_SIZES)
        self._check_range("tx_code", tx_code, self.PREAMBLE_CODE_MIN, self.PREAMBLE_CODE_MAX)
        self._check_range("rx_code", rx_code, self.PREAMBLE_CODE_MIN, self.PREAMBLE_CODE_MAX)
        self._check_fixed("sfd_type", sfd_type, _uwb.SFD_DW_8)
        self._check_fixed("data_rate", data_rate, _uwb.BR_6M8)
        self._check_fixed("phr_mode", phr_mode, _uwb.PHR_STD)
        self._check_fixed("phr_rate", phr_rate, _uwb.PHR_RATE_STD)
        self._check_range("sfd_timeout", sfd_timeout, 0, 0xFFFF)
        return self._device.configure(
            channel=self.CHANNEL,
            preamble_length=preamble_length,
            pac=pac,
            tx_code=tx_code,
            rx_code=rx_code,
            sfd_type=sfd_type,
            data_rate=data_rate,
            phr_mode=phr_mode,
            phr_rate=phr_rate,
            sfd_timeout=sfd_timeout,
            sts_mode=sts_mode,
            sts_length=sts_length,
            pdoa_mode=pdoa_mode,
        )

    def configure_tx_rf(self, pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0):
        """Configure the channel 9 transmitter RF settings.

        :param int pg_delay: Pulse generator delay, range 0x00-0xFF. Default is 0x34.
        :param int tx_power: 32-bit TX power value, range 0x00000000-0xFFFFFFFF. Default is 0xFEFEFEFE.
        :param int pg_count: Pulse generator count, range 0x00-0xFF. Default is 0.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.configure_tx_rf(
                    pg_delay=0x34,
                    tx_power=0xFEFEFEFE,
                    pg_count=0,
                )
        """
        self._check_range("pg_delay", pg_delay, 0, 0xFF)
        self._check_range("tx_power", tx_power, 0, 0xFFFFFFFF)
        self._check_range("pg_count", pg_count, 0, 0xFF)
        return self._device.configure_tx_rf(
            pg_delay=pg_delay,
            tx_power=tx_power,
            pg_count=pg_count,
        )

    def set_antenna_delay(self, tx=16385, rx=16385):
        """Set the TX and RX antenna delays.

        :param int tx: TX antenna delay in device time units, range 0-65535. Default is 16385.
        :param int rx: RX antenna delay in device time units, range 0-65535. Default is 16385.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.set_antenna_delay(tx=16385, rx=16385)
        """
        self._check_range("tx", tx, 0, 0xFFFF)
        self._check_range("rx", rx, 0, 0xFFFF)
        return self._device.set_antenna_delay(tx=tx, rx=rx)

    def set_lna_pa(self, lna=True, pa=True):
        """Enable or disable the LNA and PA controls.

        :param bool lna: Enable the low-noise amplifier. Default is True.
        :param bool pa: Enable the power amplifier. Default is True.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.set_lna_pa(lna=True, pa=True)
        """
        return self._device.set_lna_pa(lna=lna, pa=pa)

    def set_rx_after_tx_delay(self, delay_uus=0):
        """Set the delay from TX completion to automatic RX enable.

        :param int delay_uus: Delay in UWB microseconds, range 0-4294967295. Default is 0.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.set_rx_after_tx_delay(0)
        """
        self._check_range("delay_uus", delay_uus, 0, 0xFFFFFFFF)
        return self._device.set_rx_after_tx_delay(delay_uus)

    def set_rx_timeout(self, timeout_uus=30000):
        """Set the RX frame timeout.

        :param int timeout_uus: Timeout in UWB microseconds, range 0-4294967295. Zero disables the timeout. Default is 30000.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.set_rx_timeout(timeout_uus=30000)
        """
        self._check_range("timeout_uus", timeout_uus, 0, 0xFFFFFFFF)
        return self._device.set_rx_timeout(timeout_uus)

    def set_preamble_timeout(self, timeout=0):
        """Set the preamble detection timeout.

        :param int timeout: Timeout in PAC units, range 0-65535. Zero disables the timeout. Default is 0.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.set_preamble_timeout(timeout=0)
        """
        self._check_range("timeout", timeout, 0, 0xFFFF)
        return self._device.set_preamble_timeout(timeout)

    def write_tx_frame(self, data, ranging=True):
        """Write a payload to the TX buffer.

        :param data: Bytes-like payload, range 0-125 bytes. Do not include the 2-byte FCS.
        :param bool ranging: Set the ranging bit in TX frame control. Default is True.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.write_tx_frame(b"hello")
        """
        if len(data) > self.MAX_PAYLOAD:
            raise ValueError("data must not exceed 125 bytes")
        return self._device.write_tx_frame(data, ranging=ranging)

    def set_delayed_trx_time(self, device_time):
        """Set the delayed TX/RX device time.

        :param int device_time: Low 32 bits of the 40-bit device timestamp shifted right by 8, range 0-4294967295.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                delayed_time = (radio.rx_timestamp() + 4500 * 63898) >> 8
                radio.set_delayed_trx_time(delayed_time)
        """
        self._check_range("device_time", device_time, 0, 0xFFFFFFFF)
        return self._device.set_delayed_trx_time(device_time)

    def start_tx(self, mode):
        """Start an immediate or delayed transmission.

        :param int mode: TX mode composed from ``uwb.TX_IMMEDIATE`` or ``uwb.TX_DELAYED`` and optional ``uwb.RESPONSE_EXPECTED``.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
        """
        return self._device.start_tx(mode)

    def rx_enable(self, mode=_uwb.RX_IMMEDIATE):
        """Enable the receiver.

        :param int mode: RX mode. Use ``uwb.RX_IMMEDIATE`` or ``uwb.RX_DELAYED`` and optionally combine delayed RX with ``uwb.IDLE_ON_DELAY_ERROR``. Default is ``uwb.RX_IMMEDIATE``.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.rx_enable()
        """
        return self._device.rx_enable(mode)

    def wait_status(self, mask, timeout_ms=-1):
        """Wait until any requested system status bit is set.

        :param int mask: Status mask, usually composed from ``uwb.STATUS_*`` constants.
        :param int timeout_ms: Software timeout in milliseconds, range -1-1073741823. Minus one waits indefinitely. Default is -1.
        :return: Raw 32-bit system status value.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                status = radio.wait_status(uwb.STATUS_RX_ALL, 50)
        """
        self._check_range("mask", mask, 0, 0xFFFFFFFF)
        self._check_range("timeout_ms", timeout_ms, -1, 0x3FFFFFFF)
        return self._device.wait_status(mask, timeout_ms)

    def read_status(self):
        """Read the low 32 bits of the system status register.

        :return: Raw 32-bit system status value.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                status = radio.read_status()
        """
        return self._device.read_status()

    def clear_status(self, mask):
        """Clear selected system status bits.

        :param int mask: Status mask, range 0x00000000-0xFFFFFFFF.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.clear_status(uwb.STATUS_TX_DONE)
        """
        self._check_range("mask", mask, 0, 0xFFFFFFFF)
        return self._device.clear_status(mask)

    def force_trx_off(self):
        """Force the transmitter and receiver to the idle state.

        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.force_trx_off()
        """
        return self._device.force_trx_off()

    def frame_length(self):
        """Get the last received frame length including the 2-byte FCS.

        :return: Received frame length in bytes, range 2-127.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                length = radio.frame_length()
        """
        return self._device.frame_length()

    def read_rx_frame(self):
        """Read the last received payload without the 2-byte FCS.

        :return: Received payload, range 0-125 bytes.
        :rtype: bytes

        MicroPython Code Block:

            .. code-block:: python

                frame = radio.read_rx_frame()
        """
        return self._device.read_rx_frame()

    def tx_timestamp(self):
        """Read the last TX timestamp.

        :return: Full 40-bit TX timestamp in device time units, range 0-(2**40 - 1).
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                timestamp = radio.tx_timestamp()
        """
        return self._device.tx_timestamp()

    def rx_timestamp(self):
        """Read the last RX timestamp.

        :return: Full 40-bit RX timestamp in device time units, range 0-(2**40 - 1).
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                timestamp = radio.rx_timestamp()
        """
        return self._device.rx_timestamp()

    def system_timestamp(self):
        """Read the current UWB system timestamp.

        :return: Full 40-bit system timestamp in device time units, range 0-(2**40 - 1).
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                timestamp = radio.system_timestamp()
        """
        return self._device.system_timestamp()

    def device_id(self):
        """Read the UWB device ID.

        :return: Device ID. QM33120/DW3720 returns 0xDECA0314.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                device_id = radio.device_id()
        """
        return self._device.device_id()

    def reset(self):
        """Reset, probe, and reinitialise the UWB device.

        PHY and RF settings must be configured again after reset.

        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.reset()
                radio.configure()
        """
        return self._device.reset()

    def wakeup(self):
        """Pulse the WAKEUP pin to wake the UWB device.

        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.wakeup()
        """
        return self._device.wakeup()

    def deinit(self):
        """Stop TX/RX and release the SPI and GPIO resources.

        This method is idempotent. Other methods raise ``OSError(ENODEV)`` after deinitialisation.

        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.deinit()
        """
        return self._device.deinit()


class StampUWBAngle(StampUWB):
    """Dual-antenna UWB angle device configured for the current Stamp host.

    The class uses channel 9, STS mode 1 with SDC, 256-symbol STS, and PDoA mode 3.
    Angle conversion requires the physical center-to-center antenna baseline and a product-specific
    zero-angle PDoA offset.

    :param float antenna_baseline_m: RX antenna center-to-center distance in metres. Default is 0.012.
    :param int pdoa_offset: Signed zero-angle raw PDoA offset, range -32768-32767. Default is 0.
    :param kwargs: Optional board pin overrides accepted by :class:`StampUWB`.

    MicroPython Code Block:

        .. code-block:: python

            from stamp import StampUWBAngle

            radio = StampUWBAngle(antenna_baseline_m=0.012, pdoa_offset=0)
            radio.configure()
    """

    CHANNEL_CENTER_HZ = 7987200000.0
    SPEED_OF_LIGHT = 299702547.0
    PDOA_RAW_PI = 6434
    PDOA_RAW_2PI = PDOA_RAW_PI * 2
    PDOA_RAW_SCALE = 1 << 11
    VALID_TDOA_LIMIT = _uwb.VALID_TDOA_LIMIT
    ANGLE_STS_MODE = _uwb.STS_MODE_1 | _uwb.STS_MODE_SDC
    ANGLE_STS_LENGTH = 256
    ANGLE_PDOA_MODE = _uwb.PDOA_M3

    def __init__(self, antenna_baseline_m=0.012, pdoa_offset=0, **kwargs):
        if antenna_baseline_m <= 0:
            raise ValueError("antenna_baseline_m must be greater than 0")
        self._check_range("pdoa_offset", pdoa_offset, -0x8000, 0x7FFF)
        self.antenna_baseline_m = antenna_baseline_m
        self.pdoa_offset = pdoa_offset
        super().__init__(**kwargs)

    def configure(
        self,
        preamble_length=128,
        pac=8,
        tx_code=9,
        rx_code=9,
        sfd_type=_uwb.SFD_DW_8,
        data_rate=_uwb.BR_6M8,
        phr_mode=_uwb.PHR_STD,
        phr_rate=_uwb.PHR_RATE_STD,
        sfd_timeout=129,
    ):
        """Configure the channel 9 dual-antenna Angle PHY.

        This method fixes STS to ``uwb.STS_MODE_1 | uwb.STS_MODE_SDC``, STS length to 256,
        and PDoA mode to ``uwb.PDOA_M3``. Remaining parameters use the same ranges as
        :meth:`StampUWB.configure`.

        :param int preamble_length: Preamble length in symbols. Default is 128.
        :param int pac: Preamble acquisition chunk size. Default is 8.
        :param int tx_code: Channel 9 TX preamble code, range 9-12. Default is 9.
        :param int rx_code: Channel 9 RX preamble code, range 9-12. Default is 9.
        :param int sfd_type: SFD type. Default is ``uwb.SFD_DW_8``.
        :param int data_rate: PHY data rate. Default is ``uwb.BR_6M8``.
        :param int phr_mode: PHR mode. Default is ``uwb.PHR_STD``.
        :param int phr_rate: PHR rate. Default is ``uwb.PHR_RATE_STD``.
        :param int sfd_timeout: SFD timeout in symbols, range 0-65535. Default is 129.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.configure()
        """
        return self._configure(
            preamble_length=preamble_length,
            pac=pac,
            tx_code=tx_code,
            rx_code=rx_code,
            sfd_type=sfd_type,
            data_rate=data_rate,
            phr_mode=phr_mode,
            phr_rate=phr_rate,
            sfd_timeout=sfd_timeout,
            sts_mode=self.ANGLE_STS_MODE,
            sts_length=self.ANGLE_STS_LENGTH,
            pdoa_mode=self.ANGLE_PDOA_MODE,
        )

    def read_pdoa(self):
        """Read the raw phase difference of arrival from the last RX frame."""
        return self._device.read_pdoa()

    def read_tdoa_pdoa(self, index=0):
        """Read one TDoA/PDoA diagnostic result from the last RX frame."""
        self._check_range("index", index, 0, 2)
        return self._device.read_tdoa_pdoa(index)

    def read_sts_quality(self):
        """Read STS validity and quality from the last RX frame."""
        return self._device.read_sts_quality()

    def set_pdoa_offset(self, offset=0):
        """Set the hardware PDoA correction offset."""
        self._check_range("offset", offset, 0, 0xFFFF)
        return self._device.set_pdoa_offset(offset)

    def read_pdoa_offset(self):
        """Read the hardware PDoA correction offset."""
        return self._device.read_pdoa_offset()

    def set_angle_calibration(self, pdoa_offset=0):
        """Set the software zero-angle PDoA calibration offset.

        Place the tag on the mechanical zero-angle axis, average multiple valid raw PDoA samples,
        and use that average as the offset. The value is applied by :meth:`read_angle`.

        :param int pdoa_offset: Signed raw PDoA offset, range -32768-32767. Default is 0.
        :return: None.
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                radio.set_angle_calibration(-120)
        """
        self._check_range("pdoa_offset", pdoa_offset, -0x8000, 0x7FFF)
        self.pdoa_offset = pdoa_offset

    def pdoa_to_angle(self, pdoa_raw):
        """Convert a raw PDoA sample to an arrival angle.

        The method subtracts the configured zero-angle offset, wraps the phase to ``[-pi, pi]``,
        and converts phase difference to angle using the configured antenna baseline and CH9
        wavelength. It returns None when the geometry is outside the physical ``asin`` range.

        :param int pdoa_raw: Signed raw PDoA value in s[1:-11] radians.
        :return: Arrival angle in degrees, or None when the sample is outside the physical range.
        :rtype: float

        MicroPython Code Block:

            .. code-block:: python

                angle = radio.pdoa_to_angle(pdoa_raw)
        """
        corrected = pdoa_raw - self.pdoa_offset
        while corrected > self.PDOA_RAW_PI:
            corrected -= self.PDOA_RAW_2PI
        while corrected < -self.PDOA_RAW_PI:
            corrected += self.PDOA_RAW_2PI
        phase = corrected / self.PDOA_RAW_SCALE
        wavelength = self.SPEED_OF_LIGHT / self.CHANNEL_CENTER_HZ
        sine = phase * wavelength / (2.0 * math.pi * self.antenna_baseline_m)
        if sine < -1.0 or sine > 1.0:
            return None
        return math.asin(sine) * 180.0 / math.pi

    def read_angle(self):
        """Read and validate the dual-antenna angle result from the last RX frame.

        Call immediately after ``uwb.STATUS_RX_GOOD`` and before any subsequent TX/RX operation.
        The sample is rejected when STS is invalid, TDoA exceeds :attr:`StampUWB.VALID_TDOA_LIMIT`,
        or the antenna geometry has no physical solution.

        :return: Tuple ``(angle_deg, pdoa_raw, tdoa, sts_quality)`` or None for an invalid sample.
        :rtype: tuple

        MicroPython Code Block:

            .. code-block:: python

                result = radio.read_angle()
                if result is not None:
                    angle, raw, tdoa, sts_quality = result
        """
        sts_valid, sts_quality = self.read_sts_quality()
        tdoa, pdoa_raw = self.read_tdoa_pdoa()
        if not sts_valid or abs(tdoa) > self.VALID_TDOA_LIMIT:
            return None
        angle = self.pdoa_to_angle(pdoa_raw)
        if angle is None:
            return None
        return angle, pdoa_raw, tdoa, sts_quality
