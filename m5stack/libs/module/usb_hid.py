# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver import max3421e
from driver.max3421e import Max3421e
from .usb_class import *
import time


USB_STATE_MASK = 0xF0

USB_STATE_DETACHED = 0x10
USB_DETACHED_SUBSTATE_INITIALIZE = 0x11
USB_DETACHED_SUBSTATE_WAIT_FOR_DEVICE = 0x12
USB_DETACHED_SUBSTATE_ILLEGAL = 0x13
USB_ATTACHED_SUBSTATE_SETTLE = 0x20
USB_ATTACHED_SUBSTATE_RESET_DEVICE = 0x30
USB_ATTACHED_SUBSTATE_WAIT_RESET_COMPLETE = 0x40
USB_ATTACHED_SUBSTATE_WAIT_SOF = 0x50
USB_ATTACHED_SUBSTATE_WAIT_RESET = 0x51
USB_ATTACHED_SUBSTATE_GET_DEVICE_DESCRIPTOR_SIZE = 0x60
USB_STATE_ADDRESSING = 0x70
USB_STATE_CONFIGURING = 0x80
USB_STATE_RUNNING = 0x90
USB_STATE_ERROR = 0xA0


USB_XFER_TIMEOUT = 5000
USB_NAK_LIMIT = 32000
USB_RETRY_LIMIT = 3
USB_SETTLE_DELAY = 200
USB_NAK_NOWAIT = 1

###################### START USB CHAPTER 9 ######################
# Standard Device Requests
USB_REQUEST_GET_STATUS = 0
USB_REQUEST_CLEAR_FEATURE = 1
USB_REQUEST_SET_FEATURE = 3
USB_REQUEST_SET_ADDRESS = 5
USB_REQUEST_GET_DESCRIPTOR = 6
USB_REQUEST_SET_DESCRIPTOR = 7
USB_REQUEST_GET_CONFIGURATION = 8
USB_REQUEST_SET_CONFIGURATION = 9
USB_REQUEST_GET_INTERFACE = 10
USB_REQUEST_SET_INTERFACE = 11
USB_REQUEST_SYNCH_FRAME = 12

# USB descriptors
USB_DESCRIPTOR_DEVICE = 0x01
USB_DESCRIPTOR_CONFIGURATION = 0x02
USB_DESCRIPTOR_STRING = 0x03
USB_DESCRIPTOR_INTERFACE = 0x04
USB_DESCRIPTOR_ENDPOINT = 0x05
USB_DESCRIPTOR_DEVICE_QUALIFIER = 0x06
USB_DESCRIPTOR_OTHER_SPEED = 0x07
USB_DESCRIPTOR_INTERFACE_POWER = 0x08
USB_DESCRIPTOR_OTG = 0x09

# HID constants
HID_REQUEST_GET_REPORT = 0x01
HID_REQUEST_GET_IDLE = 0x02
HID_REQUEST_GET_PROTOCOL = 0x03
HID_REQUEST_SET_REPORT = 0x09
HID_REQUEST_SET_IDLE = 0x0A
HID_REQUEST_SET_PROTOCOL = 0x0B

# Class Descriptor Types
HID_DESCRIPTOR_HID = 0x21
HID_DESCRIPTOR_REPORT = 0x22
HID_DESRIPTOR_PHY = 0x23

USB_SETUP_HOST_TO_DEVICE = 0x00
USB_SETUP_DEVICE_TO_HOST = 0x80
USB_SETUP_TYPE_STANDARD = 0x00
USB_SETUP_TYPE_CLASS = 0x20
USB_SETUP_TYPE_VENDOR = 0x40
USB_SETUP_RECIPIENT_DEVICE = 0x00
USB_SETUP_RECIPIENT_INTERFACE = 0x01
USB_SETUP_RECIPIENT_ENDPOINT = 0x02
USB_SETUP_RECIPIENT_OTHER = 0x03


###################### END USB CHAPTER 9 ######################

# Common setup data constant combinations
bmREQ_GET_DESCR = USB_SETUP_DEVICE_TO_HOST | USB_SETUP_TYPE_STANDARD | USB_SETUP_RECIPIENT_DEVICE
bmREQ_SET = USB_SETUP_HOST_TO_DEVICE | USB_SETUP_TYPE_STANDARD | USB_SETUP_RECIPIENT_DEVICE
bmREQ_CL_GET_INTF = USB_SETUP_DEVICE_TO_HOST | USB_SETUP_TYPE_CLASS | USB_SETUP_RECIPIENT_INTERFACE

# HID requests
bmREQ_HIDOUT = USB_SETUP_HOST_TO_DEVICE | USB_SETUP_TYPE_CLASS | USB_SETUP_RECIPIENT_INTERFACE
bmREQ_HIDIN = USB_SETUP_DEVICE_TO_HOST | USB_SETUP_TYPE_CLASS | USB_SETUP_RECIPIENT_INTERFACE
bmREQ_HIDREPORT = (
    USB_SETUP_DEVICE_TO_HOST | USB_SETUP_TYPE_STANDARD | USB_SETUP_RECIPIENT_INTERFACE
)


HID_PROTOCOL_NONE = 0x00
HID_PROTOCOL_KEYBOARD = 0x01
HID_PROTOCOL_MOUSE = 0x02


# Configuration Descriptor (CD)
CD_bLength_Pos = 0
CD_bDescriptorType_Pos = 1
CD_wTotalLengthLSB_Pos = 2
CD_wTotalLengthMSB_Pos = 3
CD_bNumInterfaces_Pos = 4
CD_bConfigurationValue_Pos = 5
CD_iConfiguration_Pos = 6
CD_bmAttributes_Pos = 7
CD_MaxPower_Pos = 8

# Interface Descriptor (ID)
ID_bLength_Pos = 9
ID_bDescriptorType_Pos = 10
ID_bInterfaceNumber_Pos = 11
ID_bAlternateSetting_Pos = 12
ID_bNumEndpoints_Pos = 13
ID_bInterfaceClass_Pos = 14
ID_bInterfaceSubClass_Pos = 15
ID_bInterfaceProtocol_Pos = 16
ID_iInterface_Pos = 17

# HID Descriptor (HD)
HD_bLength_Pos = 18
HD_bDescriptorType_Pos = 19
HD_bcdHIDLSB_Pos = 20
HD_bcdHIDMSB_Pos = 21
HD_bCountryCode_Pos = 22
HD_bNumDescriptors_Pos = 23
HD_bDescriptorType_Pos = 24
HD_wItemLengthLSB_Pos = 25
HD_wItemLengthMSB_Pos = 26

# Endpoint Descriptor (ED)
ED_bLength_Pos = 27
ED_bDescriptorType_Pos = 28
ED_bEndpointAddress_Pos = 29
ED_bmAttributes_Pos = 30
ED_wMaxPacketSizeLSB_Pos = 31
ED_wMaxPacketSizeMSB_Pos = 32
ED_bInterval_Pos = 33

AVG_LENGTH = 34


USB_SETTLE_DELAY = 200
USB_NUMDEVICES = 2


class UsbHID(Max3421e):
    def __init__(self, spi, cs, irq):
        super().__init__(spi, cs, irq)
        self.usb_task_state = USB_DETACHED_SUBSTATE_INITIALIZE
        self.usb_error = None
        self.delay_ms = 0

    def usbhost_init(self):
        self.devtable = [None] * (USB_NUMDEVICES + 1)
        for i in range(0, (USB_NUMDEVICES + 1)):
            self.devtable[i] = DEV_RECORD()
        self.dev0ep = EP_RECORD()
        for i in range(0, (USB_NUMDEVICES + 1)):
            self.devtable[i].epinfo = None
            self.devtable[i].devclass = 0
        self.devtable[0].epinfo = self.dev0ep
        self.dev0ep = self.devtable[0].epinfo
        self.dev0ep.sndToggle = max3421e.bmSNDTOG0
        self.dev0ep.rcvToggle = max3421e.bmRCVTOG0
        self.new_dev_addr = None
        self.dev_endpoint = 0

    def usbhost_task(self):  # noqa: C901
        rcode = bytes
        self.lowspeed = False
        buf = USB_DEVICE_DESCRIPTOR()
        tmpdata = self.max3421e_get_VbusState()

        # modify USB task state if Vbus changed
        if tmpdata == max3421e.SE1:
            self.usb_task_state = USB_DETACHED_SUBSTATE_ILLEGAL
            self.lowspeed = False
        elif tmpdata == max3421e.SE0:
            if (self.usb_task_state & USB_STATE_MASK) != USB_STATE_DETACHED:
                self.usb_task_state = USB_DETACHED_SUBSTATE_INITIALIZE
                self.lowspeed = False
        elif tmpdata == max3421e.FSHOST or tmpdata == max3421e.LSHOST:
            if tmpdata == max3421e.LSHOST:
                self.lowspeed = True
            if (self.usb_task_state & USB_STATE_MASK) == USB_STATE_DETACHED:
                self.delay_ms = time.ticks_ms() + USB_SETTLE_DELAY
                self.usb_task_state = USB_ATTACHED_SUBSTATE_SETTLE

        for i in range(0, USB_NUMDEVICES):
            pass

        if self.usb_task_state == USB_DETACHED_SUBSTATE_INITIALIZE:
            self.usbhost_init()
            self.usb_task_state = USB_DETACHED_SUBSTATE_WAIT_FOR_DEVICE

        elif self.usb_task_state == USB_DETACHED_SUBSTATE_WAIT_FOR_DEVICE:
            pass

        elif self.usb_task_state == USB_DETACHED_SUBSTATE_ILLEGAL:
            pass

        elif self.usb_task_state == USB_ATTACHED_SUBSTATE_SETTLE:
            if self.delay_ms < time.ticks_ms():
                self.usb_task_state = USB_ATTACHED_SUBSTATE_RESET_DEVICE

        elif self.usb_task_state == USB_ATTACHED_SUBSTATE_RESET_DEVICE:
            self.write_register(max3421e.rHCTL, max3421e.bmBUSRST)
            self.usb_task_state = USB_ATTACHED_SUBSTATE_WAIT_RESET_COMPLETE

        elif self.usb_task_state == USB_ATTACHED_SUBSTATE_WAIT_RESET_COMPLETE:
            if (self.read_register(max3421e.rHCTL) & max3421e.bmBUSRST) == 0:
                tmpdata = self.read_register(max3421e.rMODE) | max3421e.bmSOFKAENAB
                self.write_register(max3421e.rMODE, tmpdata)
                self.usb_task_state = USB_ATTACHED_SUBSTATE_WAIT_SOF
                self.delay_ms = time.ticks_ms() + 20

        elif self.usb_task_state == USB_ATTACHED_SUBSTATE_WAIT_SOF:
            if self.read_register(max3421e.rHIRQ) & max3421e.bmFRAMEIRQ:
                if self.delay_ms < time.ticks_ms():
                    self.usb_task_state = USB_ATTACHED_SUBSTATE_GET_DEVICE_DESCRIPTOR_SIZE

        elif self.usb_task_state == USB_ATTACHED_SUBSTATE_GET_DEVICE_DESCRIPTOR_SIZE:
            self.devtable[0].epinfo.MaxPktSize = 8
            rcode, data = self.usbhost_get_dev_descr(0, 0, 18, buf)
            if rcode == 0:
                self.devtable[0].epinfo.MaxPktSize = data[7]
                buff8 = [0] * 8
                rcode, data = self.usbhost_get_dev_descr(0, 0, 8, buff8)
            else:
                print("Error in Get Dev18 Descr1 Rcode: {}\n".format(rcode))
                self.usb_error = USB_ATTACHED_SUBSTATE_GET_DEVICE_DESCRIPTOR_SIZE
                self.usb_task_state = USB_STATE_ERROR

            if rcode == 0:
                self.usb_task_state = USB_STATE_ADDRESSING
            else:
                print("Error in Get Dev8 Descr1 Rcode: {}\n".format(rcode))
                self.usb_error = USB_ATTACHED_SUBSTATE_GET_DEVICE_DESCRIPTOR_SIZE
                self.usb_task_state = USB_STATE_ERROR

        elif self.usb_task_state == USB_STATE_ADDRESSING:
            for i in range(1, USB_NUMDEVICES):
                if self.devtable[i].epinfo == None:  # noqa: E711
                    self.devtable[i].epinfo = self.devtable[0].epinfo
                    rcode, data = self.usbhost_set_addr(0, 0, i)
                    self.new_dev_addr = i
                    if rcode == 0:
                        self.usb_task_state = USB_STATE_CONFIGURING

                    else:
                        self.usb_error = USB_STATE_ADDRESSING
                        self.usb_task_state = USB_STATE_ERROR

            if self.usb_task_state == USB_STATE_ADDRESSING:
                self.usb_error = 0xFE
                self.usb_task_state = USB_STATE_ERROR

        elif self.usb_task_state == USB_STATE_CONFIGURING:
            rcode, data = self.usbhost_get_dev_descr(self.new_dev_addr, 0, 18, buf)
            if rcode:
                print("Error in Get Dev18 Descr2 Rcode: {}\n".format(rcode))
                self.usb_error = USB_STATE_CONFIGURING
                self.usb_task_state = USB_STATE_ERROR

            elif rcode == 0:
                buff9 = [0] * 9
                rcode, data = self.usbhost_get_conf_descr(self.new_dev_addr, 0, 9, 1, buff9)
            if rcode:
                print("Error in Get Config Descr Rcode: {}\n".format(rcode))
                self.usb_error = USB_STATE_CONFIGURING
                self.usb_task_state = USB_STATE_ERROR

            elif rcode == 0:
                pkt_size = data[CD_wTotalLengthMSB_Pos] << 8 | data[CD_wTotalLengthLSB_Pos]
                buffi = [0] * pkt_size
                rcode, data = self.usbhost_ctrl_req(
                    self.new_dev_addr,
                    0,
                    bmREQ_GET_DESCR,
                    USB_REQUEST_GET_DESCRIPTOR,
                    1,
                    USB_DESCRIPTOR_CONFIGURATION,
                    0x0000,
                    pkt_size,
                    buffi,
                    nak_limit=USB_NAK_LIMIT,
                )
            if rcode:
                print("Error in Control Req Rcode: {}\n".format(rcode))
                self.usb_error = USB_STATE_CONFIGURING
                self.usb_task_state = USB_STATE_ERROR

            self.devtable[self.new_dev_addr].epinfo = self.devtable[0].epinfo
            self.devtable[self.new_dev_addr].epinfo.MaxPktSize = 5
            self.devtable[self.new_dev_addr].epinfo.sndToggle = max3421e.bmSNDTOG0
            self.devtable[self.new_dev_addr].epinfo.rcvToggle = max3421e.bmRCVTOG0

            if rcode == 0:
                descr_len = data[CD_wTotalLengthMSB_Pos] << 8 | data[CD_wTotalLengthLSB_Pos]
                pkt_size = data[HD_wItemLengthMSB_Pos] << 8 | data[HD_wItemLengthLSB_Pos]
                Next = 0  # noqa: N806
                while True:
                    print("HID: ", data[ID_bInterfaceProtocol_Pos + Next])
                    if (
                        descr_len
                        >= AVG_LENGTH & data[ID_bInterfaceProtocol_Pos + Next]
                        == HID_PROTOCOL_MOUSE
                    ):
                        self.dev_endpoint = int(data[ED_bEndpointAddress_Pos + Next] & 0x0F)
                        print("End point: {0}, Next: {1}\n".format(self.dev_endpoint, Next))
                        break
                    if (
                        descr_len
                        >= AVG_LENGTH & data[ID_bInterfaceProtocol_Pos + Next]
                        == HID_PROTOCOL_KEYBOARD
                    ):
                        self.dev_endpoint = int(data[ED_bEndpointAddress_Pos + Next] & 0x0F)
                        print("KB End point: {0}, Next: {1}\n".format(self.dev_endpoint, Next))
                        break
                    elif (Next + AVG_LENGTH) > descr_len:
                        print("Error in EndPoint Address\n")
                        break
                    Next += 25  # noqa: N806
                rcode, data = self.usbhost_set_conf(self.new_dev_addr, 0, 1)

            if rcode:
                print("Error in Set Config Rcode: {}\n".format(rcode))
                self.usb_error = USB_STATE_CONFIGURING
                self.usb_task_state = USB_STATE_ERROR

            elif rcode == 0:
                rcode, data = self.usbhost_set_protocol(self.new_dev_addr, 0, 0, 0)
            if rcode:
                print("Error in Set Protocol Rcode: {}\n".format(rcode))
                self.usb_error = USB_STATE_CONFIGURING
                self.usb_task_state = USB_STATE_ERROR

            rcode, data = self.usbhost_set_idle(self.new_dev_addr, 0, 0, 0, 0)
            if rcode:
                print("Error in Set Idle Rcode: {}\n".format(rcode))

            buffi = [0] * pkt_size
            rcode, data = self.usbhost_get_report_descr(self.new_dev_addr, 0, pkt_size, buffi)
            if rcode:
                print("Error in Get Report Descr Rcode: {}\n".format(rcode))
                self.usb_error = USB_STATE_CONFIGURING
                self.usb_task_state = USB_STATE_ERROR

            if self.usb_task_state == USB_STATE_CONFIGURING:
                self.usb_task_state = USB_STATE_RUNNING

        elif self.usb_task_state == USB_STATE_RUNNING:
            pass
        elif self.usb_task_state == USB_STATE_ERROR:
            pass

    def get_usbtaskstate(self):
        return self.usb_task_state

    def set_usbtaskstate(self, state):
        self.usb_task_state = state

    def usbhost_get_devtable_entry(self, addr, ep):
        ptr = self.devtable[addr].epinfo
        ptr += ep
        return ptr

    def usbhost_set_devtable_entry(self, addr, ep_ptr):
        self.devtable[addr].epinfo = ep_ptr

    def usbhost_get_dev_descr(self, addr, ep, nbytes, dataptr, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_GET_DESCR,
            USB_REQUEST_GET_DESCRIPTOR,
            0x00,
            USB_DESCRIPTOR_DEVICE,
            0x0000,
            nbytes,
            dataptr,
            nak_limit,
        )

    def usbhost_get_conf_descr(self, addr, ep, nbytes, conf, dataptr, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_GET_DESCR,
            USB_REQUEST_GET_DESCRIPTOR,
            conf,
            USB_DESCRIPTOR_CONFIGURATION,
            0x0000,
            nbytes,
            dataptr,
            nak_limit,
        )

    def usbhost_get_str_descr(self, addr, ep, nbytes, index, langid, dataptr, nak_limit):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_GET_DESCR,
            USB_REQUEST_GET_DESCRIPTOR,
            index,
            USB_DESCRIPTOR_CONFIGURATION,
            langid,
            nbytes,
            dataptr,
            nak_limit,
        )

    def usbhost_set_addr(self, oldaddr, ep, newaddr, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            oldaddr,
            ep,
            bmREQ_SET,
            USB_REQUEST_SET_ADDRESS,
            newaddr,
            0x00,
            0x0000,
            0x0000,
            None,
            nak_limit,
        )

    def usbhost_set_conf(self, addr, ep, conf_value, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_SET,
            USB_REQUEST_SET_CONFIGURATION,
            conf_value,
            0x00,
            0x0000,
            0x0000,
            None,
            nak_limit,
        )

    def usbhost_set_protocol(self, addr, ep, interface, protocol, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDOUT,
            HID_REQUEST_SET_PROTOCOL,
            protocol,
            0x00,
            interface,
            0x0000,
            None,
            nak_limit,
        )

    def usbhost_get_protocol(self, addr, ep, interface, dataptr, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDIN,
            HID_REQUEST_GET_PROTOCOL,
            0x00,
            0x00,
            interface,
            0x0001,
            dataptr,
            nak_limit,
        )

    def usbhost_get_report_descr(self, addr, ep, nbytes, dataptr, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDREPORT,
            USB_REQUEST_GET_DESCRIPTOR,
            0x00,
            HID_DESCRIPTOR_REPORT,
            0x0000,
            nbytes,
            dataptr,
            nak_limit,
        )

    def usbhost_set_report(
        self, addr, ep, nbytes, interface, report_type, report_id, dataptr, nak_limit=USB_NAK_LIMIT
    ):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDOUT,
            HID_REQUEST_SET_REPORT,
            report_id,
            report_type,
            interface,
            nbytes,
            dataptr,
            nak_limit,
        )

    def usbhost_get_report(
        self, addr, ep, nbytes, interface, report_type, report_id, dataptr, nak_limit=USB_NAK_LIMIT
    ):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDIN,
            HID_REQUEST_GET_REPORT,
            report_id,
            report_type,
            interface,
            nbytes,
            dataptr,
            nak_limit,
        )

    def usbhost_get_idle(self, addr, ep, interface, reportID, dataptr, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDIN,
            HID_REQUEST_GET_IDLE,
            reportID,
            0,
            interface,
            0x0001,
            dataptr,
            nak_limit,
        )

    def usbhost_set_idle(self, addr, ep, interface, reportID, duration, nak_limit=USB_NAK_LIMIT):
        return self.usbhost_ctrl_req(
            addr,
            ep,
            bmREQ_HIDOUT,
            HID_REQUEST_SET_IDLE,
            reportID,
            duration,
            interface,
            0x0000,
            None,
            None,
        )

    def usbhost_ctrl_req(
        self, addr, ep, bmReqType, bRequest, wValLo, wValHi, wInd, nbytes, dataptr, nak_limit
    ):
        direction = False
        rcode = bytes
        setup_pkt = []
        data = 0

        self.write_register(max3421e.rPERADDR, addr)
        mode = self.read_register(max3421e.rMODE)
        self.write_register(
            max3421e.rMODE,
            (mode | max3421e.bmLOWSPEED) if self.lowspeed else (mode & ~(max3421e.bmLOWSPEED)),
        )

        if bmReqType & 0x80:
            direction = True

        setup_pkt.append(bmReqType)
        setup_pkt.append(bRequest)
        setup_pkt.append(wValLo)
        setup_pkt.append(wValHi)
        setup_pkt.append((wInd & 0xFF))
        setup_pkt.append(((wInd >> 8) & 0xFF))
        setup_pkt.append((nbytes & 0xFF))
        setup_pkt.append(((nbytes >> 8) & 0xFF))

        self.write_multi_bytes(max3421e.rSUDFIFO, setup_pkt)
        rcode = self.usbhost_dispatch_Pkt(max3421e.tokSETUP, ep, nak_limit)
        if rcode:
            return rcode, 0

        if dataptr != None:  # noqa: E711
            rcode, data = self.usbhost_ctrl_data(addr, ep, nbytes, dataptr, direction)
            # print(data)
        if rcode:
            return rcode, 0

        rcode = self.usbhost_ctrl_status(ep, direction)
        return rcode, data

    def usbhost_ctrl_status(self, ep, direction, nak_limit=USB_NAK_LIMIT):
        if direction:
            rcode = self.usbhost_dispatch_Pkt(max3421e.tokOUTHS, ep, nak_limit)
        else:
            rcode = self.usbhost_dispatch_Pkt(max3421e.tokINHS, ep, nak_limit)
        return rcode

    def usbhost_ctrl_data(self, addr, ep, nbytes, dataptr, direction, nak_limit=USB_NAK_LIMIT):
        if direction:
            self.devtable[addr].epinfo.rcvToggle = max3421e.bmRCVTOG1
            rcode, data = self.usbhost_in_transfer(addr, ep, nbytes, dataptr, nak_limit)
            return rcode, data
        else:
            self.devtable[addr].epinfo.sndToggle = max3421e.bmSNDTOG1
            rcode = self.usbhost_out_transfer(addr, ep, nbytes, dataptr, nak_limit)
            return rcode, 0

    def usbhost_in_transfer(self, addr, ep, nbytes, data, nak_limit=USB_NAK_LIMIT):
        maxpktsize = self.devtable[addr].epinfo.MaxPktSize
        xfrlen = 0
        data_lst = []
        self.write_register(max3421e.rHCTL, self.devtable[addr].epinfo.rcvToggle)
        while True:
            rcode = self.usbhost_dispatch_Pkt(max3421e.tokIN, ep, nak_limit)
            if rcode == max3421e.hrTOGERR:
                bmRcvToggle = (  # noqa: N806
                    0 if (self.read_register(max3421e.rHRSL) & max3421e.bmRCVTOGRD) else 1
                )
                self.write_register(
                    max3421e.rHCTL, max3421e.bmRCVTOG1 if bmRcvToggle else max3421e.bmRCVTOG0
                )
                continue

            if rcode:
                if rcode == 4:
                    pass
                else:
                    return rcode, 0

            if (self.read_register(max3421e.rHIRQ) & max3421e.bmRCVDAVIRQ) == 0:
                return 0xF0, 0

            pktsize = self.read_register(max3421e.rRCVBC)
            if pktsize > nbytes:
                pktsize = nbytes
            mem_left = nbytes - xfrlen
            if mem_left < 0:
                mem_left = 0

            data_lst += self.read_multi_bytes(
                max3421e.rRCVFIFO, mem_left if pktsize > mem_left else pktsize
            )
            self.write_register(max3421e.rHIRQ, max3421e.bmRCVDAVIRQ)
            xfrlen += pktsize
            if (pktsize < maxpktsize) or (xfrlen >= nbytes):
                if self.read_register(max3421e.rHRSL) & max3421e.bmRCVTOGRD:
                    self.devtable[addr].epinfo.rcvToggle = max3421e.bmRCVTOG1
                else:
                    self.devtable[addr].epinfo.rcvToggle = max3421e.bmRCVTOG0
                return 0, data_lst

    def usbhost_out_transfer(self, addr, ep, nbytes, data, nak_limit=USB_NAK_LIMIT):
        data_p = data
        bytes_left = nbytes
        start_byte = 0
        maxpktsize = self.devtable[addr].epinfo.MaxPktSize
        timeout = time.ticks_ms() + USB_XFER_TIMEOUT

        if not maxpktsize:
            return 0xFE

        self.write_register(max3421e.rHCTL, self.devtable[addr].epinfo.sndToggle)
        while bytes_left:
            nak_count = 0
            retry_count = 0
            bytes_tosend = maxpktsize if (bytes_left >= maxpktsize) else bytes_left
            self.write_multi_bytes(
                max3421e.rSNDFIFO, data_p[start_byte : (start_byte + bytes_tosend)]
            )
            self.write_register(max3421e.rSNDBC, bytes_tosend)
            self.write_register(max3421e.rHXFR, (max3421e.tokOUT | ep))
            while not (self.read_register(max3421e.rHIRQ) & max3421e.bmHXFRDNIRQ):
                pass
            self.write_register(max3421e.rHIRQ, max3421e.bmHXFRDNIRQ)
            rcode = self.read_register(max3421e.rHRSL) & 0x0F
            while rcode and timeout > time.ticks_ms():
                if rcode == max3421e.hrNAK:
                    nak_count += 1
                    if nak_limit and (nak_count == USB_NAK_LIMIT):
                        return rcode
                elif rcode == max3421e.hrTIMEOUT:
                    retry_count += 1
                    if retry_count == USB_RETRY_LIMIT:
                        return rcode
                else:
                    return rcode

                self.write_register(max3421e.rSNDBC, 0)
                self.write_register(max3421e.rSNDFIFO, data_p[bytes_tosend])
                self.write_register(max3421e.rSNDBC, bytes_tosend)
                self.write_register(max3421e.rHXFR, (max3421e.tokOUT | ep))
                while not (self.read_register(max3421e.rHIRQ) & max3421e.bmHXFRDNIRQ):
                    pass
                self.write_register(max3421e.rHIRQ, max3421e.bmHXFRDNIRQ)
                rcode = self.read_register(max3421e.rHRSL) & 0x0F
            bytes_left -= bytes_tosend
            start_byte += bytes_tosend
        self.devtable[addr].epinfo.sndToggle = (
            max3421e.bmSNDTOG1
            if (self.read_register(max3421e.rHRSL) & max3421e.bmSNDTOGRD)
            else max3421e.bmSNDTOG0
        )
        return rcode

    def usbhost_dispatch_Pkt(self, token, ep, nak_limit=USB_NAK_LIMIT):  # noqa: N802
        nak_count = 0
        retry_count = 0
        timeout = time.ticks_ms() + USB_XFER_TIMEOUT

        while timeout > time.ticks_ms():
            self.write_register(max3421e.rHXFR, (token | ep))
            rcode = 0xFF
            while timeout > time.ticks_ms():
                tmpdata = self.read_register(max3421e.rHIRQ)
                if tmpdata & max3421e.bmHXFRDNIRQ:
                    self.write_register(max3421e.rHIRQ, max3421e.bmHXFRDNIRQ)
                    rcode = 0x00
                    break
            if rcode != 0x00:
                return rcode
            rcode = self.read_register(max3421e.rHRSL) & 0x0F
            if rcode == max3421e.hrNAK:
                nak_count += 1
                if nak_limit and (nak_count == nak_limit):
                    return rcode
            elif rcode == max3421e.hrTIMEOUT:
                retry_count += 1
                if retry_count == USB_RETRY_LIMIT:
                    return rcode
            else:
                return rcode
