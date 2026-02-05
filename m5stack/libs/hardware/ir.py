# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

try:
    import rmt_ir

    _HAS_RMT_IR_CMODULE = True
except ImportError:
    _HAS_RMT_IR_CMODULE = False
    from driver.ir.nec import NEC, NEC_8

import M5
import machine


class IR:
    def __init__(self) -> None:
        _pin_map = {
            # rx_pin, tx_pin
            M5.BOARD.M5AtomS3: (None, 4),
            M5.BOARD.M5AtomS3Lite: (None, 4),
            M5.BOARD.M5AtomS3U: (None, 12),
            M5.BOARD.M5Capsule: (None, 4),
            M5.BOARD.M5Cardputer: (None, 44),
            M5.BOARD.M5CardputerADV: (None, 44),
            M5.BOARD.M5StickCPlus: (None, 9),
            M5.BOARD.M5StickC: (None, 9),
            M5.BOARD.M5StickCPlus2: (None, 19),
            M5.BOARD.M5AtomU: (None, 12),
            M5.BOARD.M5Atom: (None, 12),
            M5.BOARD.M5AtomEcho: (None, 12),
            M5.BOARD.M5AtomEchoS3R: (None, 47),
            M5.BOARD.M5NanoC6: (None, 3),
            M5.BOARD.ArduinoNessoN1: (None, 9),
            M5.BOARD.M5StickS3: (42, 46),
            M5.BOARD.M5Unit_PoEP4: (None, 14),
        }
        (self._rx_pin, self._tx_pin) = _pin_map.get(M5.getBoard())
        self._receiver = None
        self._rmt_ir_instance = None
        self._user_callback = None
        if self._tx_pin:
            if _HAS_RMT_IR_CMODULE:
                self._transmitter = None  # will be initialized lazily
            else:
                self._transmitter = NEC(machine.Pin(self._tx_pin, machine.Pin.OUT, value=0))

    def tx(self, cmd, data):
        if self._tx_pin is None:
            raise NotImplementedError("IR transmitter is not supported on this board")
        # Clamp to range: 0~255
        cmd = max(0, min(255, cmd))
        data = max(0, min(255, data))
        if _HAS_RMT_IR_CMODULE:
            if self._rmt_ir_instance is None:
                rx_pin = self._rx_pin if self._rx_pin is not None else -1
                # NEC_8(rx_pin, tx_pin, callback)
                self._rmt_ir_instance = rmt_ir.NEC_8(rx_pin, self._tx_pin, None)
            self._rmt_ir_instance.send(cmd, data)
        elif self._transmitter:
            self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._rx_pin is None:
            raise NotImplementedError("IR receiver is not supported on this board")

        if self._receiver:
            if _HAS_RMT_IR_CMODULE:
                # ir_rx module doesn't have close(), just create new instance
                self._receiver = None
            else:
                self._receiver.close()

        self._user_callback = cb

        if _HAS_RMT_IR_CMODULE:
            # Use C module rmt_ir.NEC_8
            def _ir_rx_callback(_):
                """Adapter callback: read data and call user callback with (data, addr, ctrl)"""
                if self._rmt_ir_instance and self._user_callback:
                    result = self._rmt_ir_instance.read()
                    if result:
                        addr_16, cmd_16, is_repeat = result
                        # NEC_8: Extract 8-bit address and command (low 8 bits only)
                        addr_8 = addr_16 & 0xFF
                        cmd_8 = cmd_16 & 0xFF
                        # Convert to (data, addr, ctrl) format
                        # ctrl: 0=normal, -1=repeat (matching IR_RX.REPEAT)
                        ctrl = -1 if is_repeat else 0
                        self._user_callback(cmd_8, addr_8, ctrl)

            if self._tx_pin:
                self._rmt_ir_instance = rmt_ir.NEC_8(self._rx_pin, self._tx_pin, _ir_rx_callback)
            else:
                self._rmt_ir_instance = rmt_ir.NEC_8(self._rx_pin, _ir_rx_callback)
            self._receiver = self._rmt_ir_instance
        else:
            # Fallback to Python driver
            self._receiver = NEC_8(machine.Pin(self._rx_pin, machine.Pin.IN), cb)
