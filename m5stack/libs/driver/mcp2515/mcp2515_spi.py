# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import time
import collections

from driver.mcp2515.mcp2515_param import *
from driver.mcp2515.can_frame import *

from machine import Pin, SPI

MCP_STDEXT = 0  # Standard and Extended        */
MCP_STD = 1  # Standard IDs ONLY            */
MCP_EXT = 2  # Extended IDs ONLY            */
MCP_ANY = 3


TXBnREGS = collections.namedtuple("TXBnREGS", "CTRL SIDH DATA")
RXBnREGS = collections.namedtuple("RXBnREGS", "CTRL SIDH DATA CANINTFRXnIF")


TXB = [
    TXBnREGS(REGISTER.MCP_TXB0CTRL, REGISTER.MCP_TXB0SIDH, REGISTER.MCP_TXB0DATA),
    TXBnREGS(REGISTER.MCP_TXB1CTRL, REGISTER.MCP_TXB1SIDH, REGISTER.MCP_TXB1DATA),
    TXBnREGS(REGISTER.MCP_TXB2CTRL, REGISTER.MCP_TXB2SIDH, REGISTER.MCP_TXB2DATA),
]

RXB = [
    RXBnREGS(
        REGISTER.MCP_RXB0CTRL,
        REGISTER.MCP_RXB0SIDH,
        REGISTER.MCP_RXB0DATA,
        CANINTF.CANINTF_RX0IF,
    ),
    RXBnREGS(
        REGISTER.MCP_RXB1CTRL,
        REGISTER.MCP_RXB1SIDH,
        REGISTER.MCP_RXB1DATA,
        CANINTF.CANINTF_RX1IF,
    ),
]

HSPI = 2


class MCP2515_CAN:
    def __init__(self):
        pass

    def mcp2515_spi_init(
        self, spi=HSPI, spi_baud=8000000, sclk=18, mosi=23, miso=19, cs=12, irq=15
    ) -> None:
        print(spi)
        self.hspi = SPI(
            spi,
            baudrate=spi_baud,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(sclk),
            mosi=Pin(mosi),
            miso=Pin(miso),
        )
        self.cs = Pin(cs, Pin.OUT)
        self.cs.on()
        self.irq = Pin(irq, Pin.IN)
        self.mcp2515_rx_index = 0
        self.extframe = False
        self.spi_start()
        if self.mcp2515_set_config_mode() != ERROR.ERROR_OK:
            raise Exception("Commu Module SPI init failed, maybe commu module is not connected")

        # add the some code

    def mcp2515_reset(self) -> int:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_RESET)
        self.spi_end()
        time.sleep_ms(10)  # type: ignore

    def mcp2515_set_config_mode(self) -> int:
        return self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_CONFIG)

    # def setListenOnlyMode(self) -> int:
    #     return self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_LISTENONLY)

    def mcp2515_set_sleep_mode(self) -> int:
        return self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_SLEEP)

    # def setLoopbackMode(self) -> int:
    #     return self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_LOOPBACK)

    def mcp2515_set_normal_mode(self) -> int:
        return self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_NORMAL)

    def mcp2515_set_mode(self, mode: int) -> int:
        return self.mcp2515_set_can_ctrl_mode(mode)

    def mcp2515_set_can_ctrl_mode(self, mode: int) -> int:
        self.mcp2515_modify_register(REGISTER.MCP_CANCTRL, CANCTRL_REQOP, mode)
        end_time = time.ticks_add(time.ticks_ms(), 200)  # type: ignore
        mode_match = False
        while time.ticks_diff(time.ticks_ms(), end_time) < 0:  # type: ignore
            newmode = self.mcp2515_read_register(REGISTER.MCP_CANSTAT)
            newmode &= CANSTAT_OPMOD
            mode_match = newmode == mode
            if mode_match:
                break
        return ERROR.ERROR_OK if mode_match else ERROR.ERROR_FAIL

    def mcp2515_config_rate(self, canSpeed: int, canClock: int = CAN_CLOCK.MCP_16MHZ) -> int:
        error = self.mcp2515_set_config_mode()
        if error != ERROR.ERROR_OK:
            return error
        set_ = 1
        try:
            cfg1, cfg2, cfg3 = CAN_CFGS[canClock][canSpeed]
        except KeyError:
            set_ = 0
        if set_:
            self.mcp2515_set_register(REGISTER.MCP_CNF1, cfg1)
            self.mcp2515_set_register(REGISTER.MCP_CNF2, cfg2)
            self.mcp2515_set_register(REGISTER.MCP_CNF3, cfg3)
            return ERROR.ERROR_OK
        return ERROR.ERROR_FAIL

    def mcp2515_init_can_buffers(self) -> None:
        self.mcp2515_write_id(REGISTER.MCP_RXM0SIDH, 1, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXM1SIDH, 1, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXF0SIDH, 1, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXF1SIDH, 0, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXF2SIDH, 1, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXF3SIDH, 0, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXF4SIDH, 1, 0x00)
        self.mcp2515_write_id(REGISTER.MCP_RXF5SIDH, 0, 0x00)
        a1 = REGISTER.MCP_TXB0CTRL
        a2 = REGISTER.MCP_TXB1CTRL
        a3 = REGISTER.MCP_TXB2CTRL
        for i in range(0, 14):
            self.mcp2515_set_register(a1, 0)
            self.mcp2515_set_register(a2, 0)
            self.mcp2515_set_register(a3, 0)
            a1 += 1
            a2 += 1
            a3 += 1
        self.mcp2515_set_register(REGISTER.MCP_RXB0CTRL, 0)
        self.mcp2515_set_register(REGISTER.MCP_RXB1CTRL, 0)

    def mcp2515_init(self, canIDMode: int, canSpeed: int, canClock: int) -> bool:
        self.mcp2515_reset()
        if self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_CONFIG) > 0:
            return False
        if self.mcp2515_config_rate(canSpeed, canClock) > 0:
            return False
        self.mcp2515_init_can_buffers()
        self.mcp2515_set_register(
            REGISTER.MCP_CANINTE, CANINTF.CANINTF_RX0IF | CANINTF.CANINTF_RX1IF
        )
        self.mcp2515_set_register(REGISTER.MCP_BFPCTRL, BxBFS_MASK | BxBFE_MASK)
        self.mcp2515_set_register(REGISTER.MCP_TXRTSCTRL, 0x00)
        if canIDMode == MCP_ANY:
            self.mcp2515_modify_register(
                REGISTER.MCP_RXB0CTRL,
                RXBnCTRL_RXM_MASK | RXB0CTRL_BUKT,
                RXBnCTRL_RXM_ANY | RXB0CTRL_BUKT,
            )
            self.mcp2515_modify_register(
                REGISTER.MCP_RXB1CTRL, RXBnCTRL_RXM_MASK, RXBnCTRL_RXM_ANY
            )
        if canIDMode == MCP_STDEXT:
            self.mcp2515_modify_register(
                REGISTER.MCP_RXB0CTRL,
                RXBnCTRL_RXM_MASK | RXB0CTRL_BUKT,
                RXBnCTRL_RXM_STDEXT | RXB0CTRL_BUKT,
            )
            self.mcp2515_modify_register(
                REGISTER.MCP_RXB1CTRL, RXBnCTRL_RXM_MASK, RXBnCTRL_RXM_STDEXT
            )
        if self.mcp2515_set_can_ctrl_mode(CANCTRL_REQOP_MODE.CANCTRL_REQOP_NORMAL) > 0:
            return False
        return True

    def mcp2515_write_id(self, mcp_addr: int, ext: int, id_: int) -> None:
        canid = id_ & 0xFFFF
        buffer = bytearray(CAN_IDLEN)
        if ext:
            buffer[MCP_EID0] = canid & 0xFF
            buffer[MCP_EID8] = canid >> 8
            canid = id_ >> 16
            buffer[MCP_SIDL] = canid & 0x03
            buffer[MCP_SIDL] += (canid & 0x1C) << 3
            buffer[MCP_SIDL] |= TXB_EXIDE_MASK
            buffer[MCP_SIDH] = canid >> 5
        else:
            buffer[MCP_SIDH] = canid >> 3
            buffer[MCP_SIDL] = (canid & 0x07) << 5
            buffer[MCP_EID0] = 0
            buffer[MCP_EID8] = 0
        self.mcp2515_set_registers(mcp_addr, buffer)

    def mcp2515_prepare_id(self, ext: int, id_: int) -> bytearray:
        canid = id_ & 0xFFFF
        buffer = bytearray(CAN_IDLEN)

        if ext:
            buffer[MCP_EID0] = canid & 0xFF
            buffer[MCP_EID8] = canid >> 8
            canid = id_ >> 16
            buffer[MCP_SIDL] = canid & 0x03
            buffer[MCP_SIDL] += (canid & 0x1C) << 3
            buffer[MCP_SIDL] |= TXB_EXIDE_MASK
            buffer[MCP_SIDH] = canid >> 5
        else:
            buffer[MCP_SIDH] = canid >> 3
            buffer[MCP_SIDL] = (canid & 0x07) << 5
            buffer[MCP_EID0] = 0
            buffer[MCP_EID8] = 0

        return buffer

    def mcp2515_read_can_message(self, rxbn: int = None):
        if rxbn is None:
            return self.mcp2515_read_message()

        rxb = RXB[rxbn]

        tbufdata = self.mcp2515_read_registers(rxb.SIDH, 1 + CAN_IDLEN)

        id_ = (tbufdata[MCP_SIDH] << 3) + (tbufdata[MCP_SIDL] >> 5)

        is_extended = False
        if (tbufdata[MCP_SIDL] & TXB_EXIDE_MASK) == TXB_EXIDE_MASK:
            id_ = (id_ << 2) + (tbufdata[MCP_SIDL] & 0x03)
            id_ = (id_ << 8) + tbufdata[MCP_EID8]
            id_ = (id_ << 8) + tbufdata[MCP_EID0]
            id_ |= CAN_EFF_FLAG
            is_extended = True

        dlc = tbufdata[MCP_DLC] & DLC_MASK
        if dlc > CAN_MAX_DLEN:
            return ERROR.ERROR_FAIL, None, None, None, None, None

        ctrl = self.mcp2515_read_register(rxb.CTRL)
        is_rtr = bool(ctrl & RXBnCTRL_RTR)
        if is_rtr:
            id_ |= CAN_RTR_FLAG

        fmi = 0xFF  # Assuming FMI is not used, set to a default value

        data = bytearray(self.mcp2515_read_registers(rxb.DATA, dlc))

        return ERROR.ERROR_OK, id_, is_extended, is_rtr, fmi, data

    def mcp2515_read_message(self) -> tuple[int, any]:
        rc = ERROR.ERROR_NOMSG, None

        stat = self.mcp2515_get_status()
        if stat & STAT.STAT_RX0IF and self.mcp2515_rx_index == 0:
            rc = self.mcp2515_read_can_message(RXBn.RXB0)
            if self.mcp2515_get_status() & STAT.STAT_RX1IF:
                self.mcp2515_rx_index = 1
            self.mcp2515_modify_register(REGISTER.MCP_CANINTF, RXB[RXBn.RXB0].CANINTFRXnIF, 0)
        elif stat & STAT.STAT_RX1IF:
            rc = self.mcp2515_read_can_message(RXBn.RXB1)
            self.mcp2515_rx_index = 0
            self.mcp2515_modify_register(REGISTER.MCP_CANINTF, RXB[RXBn.RXB1].CANINTFRXnIF, 0)

        return rc

    def mcp2515_send_can_message(self, extframe: bool, frame: any, txbn: int = None) -> int:
        self.extframe = extframe
        if txbn is None:
            return self.mcp2515_send_message(extframe, frame)

        if frame.dlc > CAN_MAX_DLEN:
            return ERROR.ERROR_FAILTX

        txbuf = TXB[txbn]
        # ext = frame.can_id & CAN_EFF_FLAG
        rtr = frame.can_id & CAN_RTR_FLAG
        id_ = frame.can_id & (CAN_EFF_MASK if self.extframe else CAN_SFF_MASK)
        data = self.mcp2515_prepare_id(self.extframe, id_)
        mcp_dlc = (frame.dlc | RTR_MASK) if rtr else frame.dlc

        data.extend(bytearray(1 + frame.dlc))
        data[MCP_DLC] = mcp_dlc
        data[MCP_DATA : MCP_DATA + frame.dlc] = frame.data
        self.mcp2515_set_registers(txbuf.SIDH, data)

        self.mcp2515_modify_register(
            txbuf.CTRL, TXBnCTRL.TXB_TXREQ, TXBnCTRL.TXB_TXREQ, spifastend=True
        )

        ctrl = self.mcp2515_read_register(txbuf.CTRL)
        if ctrl & (TXBnCTRL.TXB_ABTF | TXBnCTRL.TXB_MLOA | TXBnCTRL.TXB_TXERR):
            return ERROR.ERROR_FAILTX
        return ERROR.ERROR_OK

    def mcp2515_send_message(self, extframe: bool, frame: any) -> int:
        if frame.dlc > CAN_MAX_DLEN:
            return ERROR.ERROR_FAILTX

        tx_buffer = [TXBn.TXB0, TXBn.TXB1, TXBn.TXB2]

        for i in range(N_TXBUFFERS):
            txbuf = TXB[tx_buffer[i]]
            ctrlval = self.mcp2515_read_register(txbuf.CTRL)
            if (ctrlval & TXBnCTRL.TXB_TXREQ) == 0:
                return self.mcp2515_send_can_message(extframe, frame, tx_buffer[i])

        return ERROR.ERROR_ALLTXBUSY

    def mcp2515_check_receive(self) -> bool:
        res = self.mcp2515_get_status()
        if res & STAT_RXIF_MASK:
            return True
        return False

    def mcp2515_check_error(self) -> bool:
        eflg = self.mcp2515_get_error_flags()

        if eflg & EFLG_ERRORMASK:
            return True
        return False

    def mcp2515_get_error_flags(self) -> int:
        return self.mcp2515_read_register(REGISTER.MCP_EFLG)

    def mcp2515_clear_rxn_ovr_flags(self) -> None:
        self.mcp2515_modify_register(REGISTER.MCP_EFLG, EFLG.EFLG_RX0OVR | EFLG.EFLG_RX1OVR, 0)

    def mcp2515_get_interrupts(self) -> int:
        return self.mcp2515_read_register(REGISTER.MCP_CANINTF)

    def mcp2515_clear_interrupts(self) -> None:
        self.mcp2515_set_register(REGISTER.MCP_CANINTF, 0)

    def mcp2515_get_interrupt_mask(self) -> int:
        return self.mcp2515_read_register(REGISTER.MCP_CANINTE)

    def mcp2515_clear_tx_interrupts(self) -> None:
        self.mcp2515_modify_register(
            REGISTER.MCP_CANINTF,
            CANINTF.CANINTF_TX0IF | CANINTF.CANINTF_TX1IF | CANINTF.CANINTF_TX2IF,
            0,
        )

    def mcp2515_clear_rxn_ovr(self) -> None:
        eflg = self.mcp2515_get_error_flags()
        if eflg != 0:
            self.mcp2515_clear_rxn_ovr_flags()
            self.mcp2515_clear_interrupts()
            # mcp2515_modify_register(REGISTER.MCP_CANINTF, CANINTF.CANINTF_ERRIF, 0)

    def mcp2515_clear_merr(self) -> None:
        # self.mcp2515_modify_register(REGISTER.MCP_EFLG, EFLG.EFLG_RX0OVR | EFLG.EFLG_RX1OVR, 0)
        # self.mcp2515_clear_interrupts()
        self.mcp2515_modify_register(REGISTER.MCP_CANINTF, CANINTF.CANINTF_MERRF, 0)

    def mcp2515_clear_errif(self) -> None:
        # self.mcp2515_modify_register(REGISTER.MCP_EFLG, EFLG.EFLG_RX0OVR | EFLG.EFLG_RX1OVR, 0)
        # self.mcp2515_clear_interrupts()
        self.mcp2515_modify_register(REGISTER.MCP_CANINTF, CANINTF.CANINTF_ERRIF, 0)

    def mcp2515_read_register(self, reg: int) -> int:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_READ)
        self.spi_transfer_reg(reg)
        ret = self.spi_transfer_reg()
        self.spi_end()
        return ret

    def mcp2515_read_registers(self, reg: int, n: int) -> list[int]:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_READ)
        self.spi_transfer_reg(reg)
        # MCP2515 has auto-increment of address-pointer
        values = []
        for i in range(n):
            values.append(self.spi_transfer_reg())
        self.spi_end()
        return values

    def mcp2515_set_register(self, reg: int, value: int) -> None:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_WRITE)
        self.spi_transfer_reg(reg)
        self.spi_transfer_reg(value)
        self.spi_end()

    def mcp2515_set_registers(self, reg: int, values: bytearray) -> None:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_WRITE)
        self.spi_transfer_reg(reg)
        for v in values:
            self.spi_transfer_reg(v)
        self.spi_end()

    def mcp2515_modify_register(
        self, reg: int, mask: int, data: int, spifastend: bool = False
    ) -> None:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_BITMOD)
        self.spi_transfer_reg(reg)
        self.spi_transfer_reg(mask)
        self.spi_transfer_reg(data)
        if not spifastend:
            self.spi_end()
        else:
            self.cs.on()
            time.sleep_us(SPI_HOLD_US)  # type: ignore

    def mcp2515_get_status(self) -> int:
        self.spi_start()
        self.spi_transfer_reg(INSTRUCTION.INSTRUCTION_READ_STATUS)
        i = self.spi_transfer_reg()
        self.spi_end()
        return i

    def spi_transfer_reg(self, value=None):
        if value is None:
            response = bytearray(1)
            self.hspi.write_readinto(bytes([0x00]), response)
            return int.from_bytes(response, sys.byteorder)
        else:
            self.hspi.write(bytes([value]))
            return None

    def spi_start(self):
        self.cs.off()

    def spi_end(self):
        self.cs.on()
