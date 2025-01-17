# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from micropython import const
from machine import Pin
import time


# registers
SE0 = 0
SE1 = 1
FSHOST = 2
LSHOST = 3

# MAX3421E command byte format: rrrrr0wa where 'r' is register number

# MAX3421E Registers in HOST mode.
rRCVFIFO = const(0x08)  # 1<<3
rSNDFIFO = const(0x10)  # 2<<3
rSUDFIFO = const(0x20)  # 4<<3
rRCVBC = const(0x30)  # 6<<3
rSNDBC = const(0x38)  # 7<<3

rUSBIRQ = const(0x68)  # 13<<3
# USBIRQ Bits
bmVBUSIRQ = const(0x40)  # b6
bmNOVBUSIRQ = const(0x20)  # b5
bmOSCOKIRQ = const(0x01)  # b0

rUSBIEN = const(0x70)  # 14<<3
# USBIEN Bits
bmVBUSIE = const(0x40)  # b6
bmNOVBUSIE = const(0x20)  # b5
bmOSCOKIE = const(0x01)  # b0

rUSBCTL = const(0x78)  # 15<<3
# USBCTL Bits
bmCHIPRES = const(0x20)  # b5
bmPWRDOWN = const(0x10)  # b4

rCPUCTL = const(0x80)  # 16<<3
# CPUCTL Bits
bmPUSLEWID1 = const(0x80)  # b7
bmPULSEWID0 = const(0x40)  # b6
bmIE = const(0x01)  # b0

rPINCTL = const(0x88)  # 17<<3
# PINCTL Bits
bmFDUPSPI = const(0x10)  # b4
bmINTLEVEL = const(0x08)  # b3
bmPOSINT = const(0x04)  # b2
bmGPXB = const(0x02)  # b1
bmGPXA = const(0x01)  # b0
# GPX pin selections
GPX_OPERATE = const(0x00)
GPX_VBDET = const(0x01)
GPX_BUSACT = const(0x02)
GPX_SOF = const(0x03)

rREVISION = const(0x90)  # 18<<3

rIOPINS1 = const(0xA0)  # 20<<3

# IOPINS1 Bits
bmGPOUT0 = const(0x01)
bmGPOUT1 = const(0x02)
bmGPOUT2 = const(0x04)
bmGPOUT3 = const(0x08)
bmGPIN0 = const(0x10)
bmGPIN1 = const(0x20)
bmGPIN2 = const(0x40)
bmGPIN3 = const(0x80)

rIOPINS2 = const(0xA8)  # 21<<3
# IOPINS2 Bits
bmGPOUT4 = const(0x01)
bmGPOUT5 = const(0x02)
bmGPOUT6 = const(0x04)
bmGPOUT7 = const(0x08)
bmGPIN4 = const(0x10)
bmGPIN5 = const(0x20)
bmGPIN6 = const(0x40)
bmGPIN7 = const(0x80)

rGPINIRQ = const(0xB0)  # 22<<3
# GPINIRQ Bits
bmGPINIRQ0 = const(0x01)
bmGPINIRQ1 = const(0x02)
bmGPINIRQ2 = const(0x04)
bmGPINIRQ3 = const(0x08)
bmGPINIRQ4 = const(0x10)
bmGPINIRQ5 = const(0x20)
bmGPINIRQ6 = const(0x40)
bmGPINIRQ7 = const(0x80)

rGPINIEN = const(0xB8)  # 23<<3
# GPINIEN Bits
bmGPINIEN0 = const(0x01)
bmGPINIEN1 = const(0x02)
bmGPINIEN2 = const(0x04)
bmGPINIEN3 = const(0x08)
bmGPINIEN4 = const(0x10)
bmGPINIEN5 = const(0x20)
bmGPINIEN6 = const(0x40)
bmGPINIEN7 = const(0x80)

rGPINPOL = const(0xC0)  # 24<<3
# GPINPOL Bits
bmGPINPOL0 = const(0x01)
bmGPINPOL1 = const(0x02)
bmGPINPOL2 = const(0x04)
bmGPINPOL3 = const(0x08)
bmGPINPOL4 = const(0x10)
bmGPINPOL5 = const(0x20)
bmGPINPOL6 = const(0x40)
bmGPINPOL7 = const(0x80)

rHIRQ = const(0xC8)  # 25<<3
# HIRQ Bits
bmBUSEVENTIRQ = const(0x01)  # indicates BUS Reset Done or BUS Resume
bmRWUIRQ = const(0x02)
bmRCVDAVIRQ = const(0x04)
bmSNDBAVIRQ = const(0x08)
bmSUSDNIRQ = const(0x10)
bmCONDETIRQ = const(0x20)
bmFRAMEIRQ = const(0x40)
bmHXFRDNIRQ = const(0x80)

rHIEN = const(0xD0)  # 26<<3

# HIEN Bits
bmBUSEVENTIE = const(0x01)
bmRWUIE = const(0x02)
bmRCVDAVIE = const(0x04)
bmSNDBAVIE = const(0x08)
bmSUSDNIE = const(0x10)
bmCONDETIE = const(0x20)
bmFRAMEIE = const(0x40)
bmHXFRDNIE = const(0x80)

rMODE = const(0xD8)  # 27<<3

# MODE Bits
bmHOST = const(0x01)
bmLOWSPEED = const(0x02)
bmHUBPRE = const(0x04)
bmSOFKAENAB = const(0x08)
bmSEPIRQ = const(0x10)
bmDELAYISO = const(0x20)
bmDMPULLDN = const(0x40)
bmDPPULLDN = const(0x80)

rPERADDR = const(0xE0)  # 28<<3

rHCTL = const(0xE8)  # 29<<3 #
# HCTL Bits
bmBUSRST = const(0x01)
bmFRMRST = const(0x02)
bmSAMPLEBUS = const(0x04)
bmSIGRSM = const(0x08)
bmRCVTOG0 = const(0x10)
bmRCVTOG1 = const(0x20)
bmSNDTOG0 = const(0x40)
bmSNDTOG1 = const(0x80)

rHXFR = const(0xF0)  # 30<<3
# Host transfer token values for writing the HXFR register (R30)
# OR this bit field with the endpoint number in bits 3:0
tokSETUP = const(0x10)  # HS=0, ISO=0, OUTNIN=0, SETUP=1
tokIN = const(0x00)  # HS=0, ISO=0, OUTNIN=0, SETUP=0
tokOUT = const(0x20)  # HS=0, ISO=0, OUTNIN=1, SETUP=0
tokINHS = const(0x80)  # HS=1, ISO=0, OUTNIN=0, SETUP=0
tokOUTHS = const(0xA0)  # HS=1, ISO=0, OUTNIN=1, SETUP=0
tokISOIN = const(0x40)  # HS=0, ISO=1, OUTNIN=0, SETUP=0
tokISOOUT = const(0x60)  # HS=0, ISO=1, OUTNIN=1, SETUP=0

rHRSL = const(0xF8)  # 31<<3

# HRSL Bits
bmRCVTOGRD = const(0x10)
bmSNDTOGRD = const(0x20)
bmKSTATUS = const(0x40)
bmJSTATUS = const(0x80)
bmSE0 = const(0x00)  # SE0 - disconnect state
bmSE1 = const(0xC0)  # SE1 - illegal state

# Host error result codes, the 4 LSB's in the HRSL register
hrSUCCESS = const(0x00)
hrBUSY = const(0x01)
hrBADREQ = const(0x02)
hrUNDEF = const(0x03)
hrNAK = const(0x04)
hrSTALL = const(0x05)
hrTOGERR = const(0x06)
hrWRONGPID = const(0x07)
hrBADBC = const(0x08)
hrPIDERR = const(0x09)
hrPKTERR = const(0x0A)
hrCRCERR = const(0x0B)
hrKERR = const(0x0C)
hrJERR = const(0x0D)
hrTIMEOUT = const(0x0E)
hrBABBLE = const(0x0F)

MODE_FS_HOST = bmDPPULLDN | bmDMPULLDN | bmHOST | bmSOFKAENAB
MODE_LS_HOST = bmDPPULLDN | bmDMPULLDN | bmHOST | bmLOWSPEED | bmSOFKAENAB


class Max3421e:
    def __init__(self, spi, cs, irq):
        self.spi = spi
        self.cs = cs
        self.cs.on()
        self.irq = irq
        self.irq.irq(self.irq_cb, Pin.IRQ_FALLING)
        self.vbusState = None
        self.max3421e_config()

    def irq_cb(self, _):
        self.host_interrupt_handler()

    def max3421e_config(self):
        self.write_register(rPINCTL, (bmFDUPSPI))
        if self.max3421e_softreset() == 0:
            return False
        self.write_register(rMODE, bmDPPULLDN | bmDMPULLDN | bmHOST)
        self.write_register(rHIEN, bmCONDETIE | bmFRAMEIE)
        # check if device is connected
        self.write_register(rHCTL, bmSAMPLEBUS)
        while not (self.read_register(rHCTL) & bmSAMPLEBUS):
            pass
        self.bus_probe()
        self.write_register(rHIRQ, bmCONDETIRQ)
        self.write_register(rCPUCTL, 0x01)
        return True

    def bus_probe(self):
        bus_sample = self.read_register(rHRSL)
        bus_sample &= bmJSTATUS | bmKSTATUS

        if bus_sample == bmJSTATUS:
            if (self.read_register(rMODE) & bmLOWSPEED) == 0:
                self.write_register(rMODE, MODE_FS_HOST)
                self.vbusState = FSHOST
            else:
                self.write_register(rMODE, MODE_LS_HOST)
                self.vbusState = LSHOST

        elif bus_sample == bmKSTATUS:
            if (self.read_register(rMODE) & bmLOWSPEED) == 0:
                self.write_register(rMODE, MODE_LS_HOST)
                self.vbusState = LSHOST
            else:
                self.write_register(rMODE, MODE_FS_HOST)
                self.vbusState = FSHOST

        elif bus_sample == bmSE1:
            self.vbusState = SE1

        elif bus_sample == bmSE0:
            self.write_register(rMODE, (bmDPPULLDN | bmDMPULLDN | bmHOST | bmSEPIRQ))
            self.vbusState = SE0

    def read_gpin(self, pin):
        val = self.read_register(rIOPINS2) & 0xF0
        val |= self.read_register(rIOPINS1) >> 4
        return (val >> pin) & 0x01

    def write_gpout(self, pin, value):
        if pin < 0 or pin > 7:
            raise ValueError("Invalid pin number, must be between 0 and 7.")

        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1.")

        gpout1 = self.read_register(rIOPINS1)
        gpout2 = self.read_register(rIOPINS2)

        if pin < 4:
            if value == 1:
                gpout1 |= 1 << pin
            else:
                gpout1 &= ~(1 << pin)
            self.write_register(rIOPINS1, gpout1)
        else:
            pin -= 4
            if value == 1:
                gpout2 |= 1 << pin
            else:
                gpout2 &= ~(1 << pin)
            self.write_register(rIOPINS2, gpout2)

    def read_gpin_value(self):
        gpin = self.read_register(rIOPINS2)
        gpin &= 0xF0
        gpin |= self.read_register(rIOPINS1) >> 4
        return gpin

    def write_gpout_value(self, data):
        self.write_register(rIOPINS1, data)
        data >>= 4
        self.write_register(rIOPINS2, data)

    def max3421e_get_VbusState(self):  # noqa: N802
        return self.vbusState

    def max3421e_task(self):
        pinvalue = self.irq.value()
        rcode = 0
        if pinvalue == 0:
            rcode = self.host_interrupt_handler()
        return rcode

    def host_interrupt_handler(self):
        HIRQ_sendback = 0x00  # noqa: N806
        HIRQ = self.read_register(rHIRQ)  # noqa: N806  # determine interrupt source
        if HIRQ & bmCONDETIRQ:
            self.bus_probe()
            HIRQ_sendback |= bmCONDETIRQ  # noqa: N806
        # End HIRQ interrupts handling, clear serviced IRQs
        self.write_register(rHIRQ, HIRQ_sendback)
        return HIRQ_sendback

    def max3421e_softreset(self):
        i = 0
        self.write_register(rUSBCTL, bmCHIPRES)
        self.write_register(rUSBCTL, 0x00)
        while True:
            if self.read_register(rUSBIRQ) & bmOSCOKIRQ:
                i += 1
                break
        return i

    # single read register of MAX3421E
    def read_register(self, address, byteorder="big", signed=False):
        # print("regRd: {}\n".format(address))
        response = self.transfer_reg(address)
        return int.from_bytes(response, byteorder, signed)

    # single write register of MAX3421E
    def write_register(self, address, value):
        self.transfer_reg(address | 0x02, value)

    # spi read & write of MAX3421E
    def transfer_reg(self, address, value=0x00):
        response = bytearray(1)
        self.cs.off()
        self.spi.write(bytes([address]))
        self.spi.write_readinto(bytes([value]), response)
        self.cs.on()
        return response

    # multi read register of MAX3421E
    def read_multi_bytes(self, address, nbytes):
        response = []
        self.cs.off()
        self.spi.write(bytes([address]))
        response = list(self.spi.read(nbytes))
        self.cs.on()
        return response

    # multi write register of MAX3421E
    def write_multi_bytes(self, address, value):
        nbytes = len(value)
        for i in range(0, nbytes):
            self.write_register((address + i), value[i])

    def deinit(self):
        pass
