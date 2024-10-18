# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from micropython import const
import time
import machine


class LoRaWAN868Module:
    """

    note:
        cn: COM.LoRaWAN是M5Stack堆叠模块系列中的LoRaWAN通信模块，支持节点到节点或LoRaWAN通信。
        en: COM.LoRaWAN is a LoRaWAN communication module in the M5Stack stackable module series, supporting node-to-node or LoRaWAN communication.

    details:
        color: "#0FE6D7"
        link: https://docs.m5stack.com/en/module/comx_lorawan
        image: https://static-cdn.m5stack.com/resource/docs/products/module/comx_lorawan/comx_lorawan_01.webp
        category: Module

    example:
        - ../../../examples/module/lorawan868_example_tx.py
        - ../../../examples/module/lorawan868_example_rx.py

    m5f2:
        - module/lorawan868_example_tx.m5f2
        - module/lorawan868_example_rx.m5f2

    """

    """
    constant: LoRa band frequency
    """
    BAND_470 = const("470000000")
    BAND_868 = const("868000000")
    BAND_915 = const("915000000")

    """
    constant: LoRa Mode
    """
    MODE_LORA = const("0")
    MODE_LORAWAN = const("1")

    def __init__(self, id=1, port=None, band=BAND_868):
        """
        note:
            en: Initialize the LoRaWANModule.
            cn: 初始化LoRaWANModule。

        params:
            id:
                note: The UART ID to use for communication.
            port:
                note: The UART port to use for communication, specified as a tuple of (rx, tx) pins.
            timeout:
                note: The timeout for the UART communication.
            band:
                note: The frequency to use for LoRa communication
                options:
                    470MHz: LoRaWANModule.BAND_470
                    868MHz: LoRaWANModule.BAND_868
                    915MHz: LoRaWANModule.BAND_915
        """
        self.band = band
        self.uart = machine.UART(id, tx=port[1], rx=port[0])
        self.uart.init(115200, bits=0, parity=None, stop=1, rxbuf=1024)

        self.wake_up()
        self.set_mode(self.MODE_LORA)
        self.set_parameters(self.band, 10, 7, 0, 1, 8, 1, 0, 0)
        ret = self.at_cmd("PrintMode", "0")  # String Output Mode

        if not ret:
            raise Exception("LoRaWAN module not detected")
        self.flush()

    def set_mode(self, mode):
        """
        note:
            en: Set the mode of the LoRaWAN module.
            cn: 设置LoRaWAN模块的模式。

        params:
            mode:
                note: The mode to set.
                options:
                    LoRa: LoRaWANModule.MODE_LORA
                    LoRaWAN: LoRaWANModule.MODE_LORAWAN

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("LORAWAN", mode)

    def set_parameters(self, freq, power, sf, bw, cr, preamble, crc, iq_inv, save):
        """
        note:
            en: Set the parameters of the LoRaWAN module.
            cn: 设置LoRaWAN模块的参数。

        params:
            freq:
                note: Set LoRa listening/sending frequency in Hz.
            power:
                note: LoRa signal output power in dBm;
            sf:
                note: Spreading factor, from 5~12
            bw:
                note: Bandwidth 0 – 125K, 1 – 250K, 2 – 500K;
            cr:
                note: 1 – 4/5, 2 – 4/6, 3 – 4/7, 4 – 4/8;
            preamble:
                note: Preamble Length from 8~65535 bit;
            crc:
                note: 0 – disable CRC check, 1 – enable CRC check;
            iq_inv:
                note: 0 -- not inverted, 1 – inverted;
            save:
                note: Save parameters to FLASH, 0 – not save, 1 – save.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd(
            "LoraSet",
            "{},{},{},{},{},{},{},{},{}".format(
                freq, power, sf, bw, cr, preamble, crc, iq_inv, save
            ),
        )

    def wake_up(self):
        """
        note:
            en: Wake up the device through a serial port interrupt. After resetting, the device is in sleep state.
                In theory, sending any data through the serial port can trigger the interrupt and wake up the device.
            cn: 通过串口中断唤醒设备。设备重置后进入睡眠状态，通过串口发送任意数据即可唤醒设备。

        example:
            Send any string like "ABC" to wake up the device.
        """
        self.at_cmd("XXX")  # XXX可以是任意数据，比如"ABC"

    def sleep(self):
        """
        note:
            en: Put the device into low-power mode.
            cn: 将设备置于低功耗模式。

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("LPM", 1)

    def reset(self):
        """
        note:
            en: Reset the device.
            cn: 重置设备。
        """
        self.at_cmd("RESET", 1)

    def restore_factory_settings(self):
        """
        note:
            en: Restore the device to factory settings. The parameters will reset and the device will enter sleep mode after response ends.
            cn: 恢复设备至出厂设置。恢复后，设备将重置参数并在响应结束后进入睡眠模式。

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("DefaultSet", 1)

    def set_copyright(self, enable=True):
        """
        note:
            en: Enable or disable copyright information print when boot loader mode begins. Default is enable.
            cn: 启用或禁用在启动加载器模式下的版权信息打印。默认启用。

        params:
            enable:
                note: Set True to enable, False to disable.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("Copyright", 1 if enable else 0)

    def set_auto_low_power(self, enable=True):
        """
        note:
            en: Enable or disable automatic low-power mode. Default is enable.
            cn: 启用或禁用自动低功耗模式。默认启用。

        params:
            enable:
                note: Set True to enable, False to disable.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("AutoLPM", 1 if enable else 0)

    def query_chip_id(self):
        """
        note:
            en: Query the unique ID of the chip, which can be used to query the corresponding serial number.
            cn: 查询芯片的唯一ID，可用于查询相应的序列号。

        returns: |
            The unique chip ID.
        """
        return self.at_query("ChipID")

    def enable_rx(self, timeout=0):
        """
        note:
            en: Enable the LoRaWAN module to receive data.
            cn: 启用LoRaWAN模块接收数据。

        params:
            timeout:
                note: The timeout for the receive operation.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("RX", str(timeout))

    def set_deveui(self, deveui=None):
        """
        note:
            en: Set or query the DevEui. DevEui must be 16 hex characters (0-9, A-F).
            cn: 设置或查询DevEui。DevEui必须是16位十六进制字符（0-9, A-F）。

        params:
            deveui:
                note: The DevEui to set. If None, query the current DevEui.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("DevEui", deveui)

    def set_appeui(self, appeui=None):
        """
        note:
            en: Set or query the AppEui. AppEui must be 16 hex characters (0-9, A-F).
            cn: 设置或查询AppEui。AppEui必须是16位十六进制字符（0-9, A-F）。

        params:
            appeui:
                note: The AppEui to set. If None, query the current AppEui.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("AppEui", appeui)

    def set_appkey(self, appkey=None):
        """
        note:
            en: Set or query the AppKey. AppKey must be 32 hex characters (0-9, A-F).
            cn: 设置或查询AppKey。AppKey必须是32位十六进制字符（0-9, A-F）。

        params:
            appkey:
                note: The AppKey to set. If None, query the current AppKey.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("AppKey", appkey)

    def set_nwkskey(self, nwkskey=None):
        """
        note:
            en: Set or query the NwkSKey. NwkSKey must be 32 hex characters (0-9, A-F).
            cn: 设置或查询NwkSKey。NwkSKey必须是32位十六进制字符（0-9, A-F）。

        params:
            nwkskey:
                note: The NwkSKey to set. If None, query the current NwkSKey.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("NwkSKey", nwkskey)

    def set_appskey(self, appskey=None):
        """
        note:
            en: Set or query the AppSKey. AppSKey must be 32 hex characters (0-9, A-F).
            cn: 设置或查询AppSKey。AppSKey必须是32位十六进制字符（0-9, A-F）。

        params:
            appskey:
                note: The AppSKey to set. If None, query the current AppSKey.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("AppSKey", appskey)

    def set_devaddr(self, devaddr=None):
        """
        note:
            en: Set or query the DevAddr. DevAddr must be 8 hex characters (0-9, A-F).
            cn: 设置或查询DevAddr。DevAddr必须是8位十六进制字符（0-9, A-F）。

        params:
            devaddr:
                note: The DevAddr to set. If None, query the current DevAddr.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("DevAddr", devaddr)

    def set_otaa_mode(self, enable=True):
        """
        note:
            en: Set or query the OTAA mode. 1 for OTAA mode, 0 for ABP mode.
            cn: 设置或查询OTAA模式。1表示OTAA模式，0表示ABP模式。

        params:
            enable:
                note: Set True for OTAA mode, False for ABP mode.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("OTAA", 1 if enable else 0)

    def set_adr(self, enable=True):
        """
        note:
            en: Enable or disable the ADR (Adaptive Data Rate) function. Default is enabled.
            cn: 启用或禁用ADR（自适应数据速率）功能。默认启用。

        params:
            enable:
                note: Set True to enable ADR, False to disable.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("ADR", 1 if enable else 0)

    def set_channel_mask(self, mask):
        """
        note:
            en: Set or query the LoRaWAN working channel mask.
            cn: 设置或查询LoRaWAN的工作频道掩码。

        params:
            mask:
                note: The channel mask in hexadecimal format, e.g., 0000000000000000000000FF for channels 0~7.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("ChMask", mask)

    def join_network(self):
        """
        note:
            en: Join the network using OTAA (Over-The-Air Activation). This command triggers the join process.
            cn: 使用OTAA（空中激活）加入网络。该命令触发入网过程。

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("Join", 1)

    def set_duty_cycle(self, cycle):
        """
        note:
            en: Set or query the communication cycle in milliseconds. For example, 60000 means communication every 60 seconds.
            cn: 设置或查询通信周期，单位为毫秒。例如，60000表示每60秒通信一次。

        params:
            cycle:
                note: The communication cycle in milliseconds.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("DutyCycle", cycle)

    def set_class_mode(self, mode):
        """
        note:
            en: Set or query the device's communication mode. Only Class A or Class C are valid.
            cn: 设置或查询设备的通信模式。只能设置为Class A或Class C。

        params:
            mode:
                note: Set "A" for Class A or "C" for Class C.

        rreturns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("Class", mode)

    def set_ack(self, enable=True):
        """
        note:
            en: Enable or disable the ACK receipt function. If enabled, the device waits for acknowledgment from the gateway.
            cn: 启用或禁用ACK确认功能。如果启用，设备将等待网关的确认。

        params:
            enable:
                note: Set True to enable ACK, False to disable.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("IsTxConfirmed", 1 if enable else 0)

    def set_app_port(self, port):
        """
        note:
            en: Set or query the application port (fport) for upstream data. Valid range is 0~255.
            cn: 设置或查询上行数据端口（fport）。有效范围是0~255。

        params:
            port:
                note: The application port to set.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("AppPort", port)

    def set_retransmission_count(self, count=None):
        """
        note:
            en: Set or query the number of retransmissions if communication fails. The valid range is 3~8.
            cn: 设置或查询在通信失败时的重传次数。有效范围是3~8。

        params:
            count:
                note: The number of retransmissions to set. If None, query the current setting.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("ConfirmedNbTrials", count)

    def send_hex(self, hex_data):
        """
        note:
            en: Send hex data in LoRaWAN or LoRa mode. Hex characters must be in pairs (e.g., "AABB").
            cn: 在LoRaWAN或LoRa模式下发送十六进制数据。十六进制字符必须成对出现（例如："AABB"）。

        params:
            hex_data:
                note: The hex data to send, up to 64 bytes.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("SendHex", hex_data)

    def send_string(self, string_data):
        """
        note:
            en: Send string data in LoRaWAN or LoRa mode. The string must consist of ASCII characters.
            cn: 在LoRaWAN或LoRa模式下发送字符串数据。字符串必须由ASCII字符组成。

        params:
            string_data:
                note: The string data to send, up to 64 bytes.

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("SendStr", string_data)

    def query_lorawan_mode(self):
        """
        note:
            en: Query if the device is in LoRaWAN or normal LoRa mode.
            cn: 查询设备是处于LoRaWAN模式还是普通LoRa模式。

        returns: |
            +LORAWAN: 1 if in LoRaWAN mode, 0 if in normal LoRa mode.
        """
        return self.at_query("LORAWAN")

    def save_parameters_to_flash(self):
        """
        note:
            en: Save the current LoRa parameters to FLASH memory.
            cn: 将当前LoRa参数保存到FLASH存储中。

        returns:
            True if the command is successful, False if not.
        """
        return self.at_cmd("SaveToFLASH", 1)

    def at_cmd(self, cmd, data=None):
        """
        note:
            en: Send an AT command to the LoRaWAN module.
            cn: 向LoRaWAN模块发送AT命令。

        params:
            cmd:
                note: The AT command to send.
            data:
                note: The data to send with the AT command.

        returns: |
            note: True if the command is successful, False if not.
        """
        if data:
            self.uart.write("AT+{}={}".format(cmd, str(data)))
        else:
            self.uart.write("AT+{}".format(cmd))
        time.sleep(0.1)
        ret = self.uart.read()
        if "ERROR" in ret:
            return False
        return True

    def at_query(self, cmd):
        """
        note:
            en: Query the current settings of the LoRaWAN module.
            cn: 查询LoRaWAN模块的当前设置。

        params:
            cmd:
                note: The AT command to query.

        returns: |
            note: The response from the LoRaWAN module.
        """
        self.uart.write("AT+{}=?".format(cmd))
        time.sleep(0.1)
        return self.uart.read()

    def at_receive(self):
        """
        note:
            en: Receive a response from the LoRaWAN module.
            cn: 从LoRaWAN模块接收响应。

        returns: |
            note: The response from the LoRaWAN module.
        """
        return self.uart.read()

    def flush(self):
        """
        note:
            en: Clear the UART buffer.
            cn: 清空UART缓冲区。
        """
        self.uart.flush()

    def any(self):
        """
        note:
            en: Check if there is any data in the UART buffer.
            cn: 检查UART缓冲区是否有数据。

        returns: |
            note: True if there is data, False if not.
        """
        return self.uart.any()

    def receive_data(self):
        """
        note:
            en: Receive data from the LoRaWAN module.
            cn: 从LoRaWAN模块接收数据。

        returns: |
            note: The received data.
        """
        return self.uart.read()
