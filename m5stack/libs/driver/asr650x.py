# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time
import binascii

AT_RESPONED_OK = "OK\r\n"
AT_RESPONED_ERROR = "ERROR\r\n"
AT_RECV_OK = "OK+RECV:"


class LoRaWAN_Asr650x(object):
    def __init__(self, tx, rx, debug=False):
        self.__uart = machine.UART(1, tx=tx, rx=rx)
        self.__uart.init(115200, bits=0, parity=None, stop=1)
        self.debug = debug
        self.set_work_mode(2)
        self._downlink_buffer = []
        self._downlink_buffer_size = 50
        self._join_status = False

    def get_product_serial_number(self):
        """
        AT+CGSN?
        """
        result, error = self.__at_cmd("AT+CGSN?")
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][6:]

    def reset_module_to_default(self):
        """
        Reset module to default config.
        Parameter:
            None
        Return:
            True
            False
        """
        pass

    def get_DevAddr(self):
        """
        Get Device address.
        Parameter:
            None
        Return:
            DevAddr: xxxxxxxx  4 bytes
        """
        cmd = "AT+CDEVADDR?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][10:]

    def set_DevAddr(self, devaddr):
        """
        Set Device address.
        Parameter:
            devaddr: xx:xx:xx:xx  4 bytes
        Return:
            True
            False
        """
        cmd = "AT+CDEVADDR=" + str(devaddr)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_DevEui(self):
        """
        Get Device EUI.
        Parameter:
            None
        Return:
            DevEui: xxxxxxxxxxxxxxxx 8 byte
        """
        cmd = "AT+CDEVEUI?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][9:]

    def set_DevEui(self, deveui):
        """
        Set Device EUI.
        Parameter:
            deveui: xxxxxxxxxxxxxxxx 8 bytes
        Return:
            True
            False
        """
        cmd = "AT+CDEVEUI=" + str(deveui)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_AppEui(self):
        """
        Get Application EUI.
        Parameter:
            None
        Return:
            AppEui: xxxxxxxxxxxxxxxx 8 bytes
        """
        cmd = "AT+CAPPEUI?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][9:]

    def set_AppEui(self, appeui):
        """
        Set Application EUI.
        Parameter:
            appeui: xxxxxxxxxxxxxxxx 8 bytes
        Return:
            True
            False
        """
        cmd = "AT+CAPPEUI=" + str(appeui)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_AppKey(self):
        """
        get App Key.
        Parameter:
            None
        Return:
            key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
            False
        """
        cmd = "AT+CAPPKEY?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][9:]

    def set_AppKey(self, key):
        """
        Set App Key.
        Parameter:
            None
        Return:
            key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
            False
        """
        cmd = "AT+CAPPKEY=" + str(key)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_APPSKEY(self):
        """
        Set App Session Key.
        Parameter:
            AppSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
        Return:
            True
            False
        """
        cmd = "AT+CAPPSKEY?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][10:]

    def set_APPSKEY(self, AppSKEY):
        """
        Set App Session Key.
        Parameter:
            AppSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
        Return:
            True
            False
        """
        cmd = "AT+CAPPSKEY=" + str(AppSKEY)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_NWKSKEY(self):
        """
        Get Network Session Key.
        Parameter:
            None
        Return:
            NWKSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
            False
        """
        cmd = "AT+CNWKSKEY?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][10:]

    def set_NWKSKEY(self, NWKSKEY):
        """
        Set Network Session Key.
        Parameter:
            NWKSKEY: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx 16 bytes
        Return:
            True
            False
        """
        cmd = "AT+CNWKSKEY=" + str(NWKSKEY)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_join_mode(self):
        """
        Set LoRaWAN Mode.
        Parameter:
            None
        Return:
            True
            False
        """
        cmd = "AT+CJOINMODE?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        if result[1][11:] == "1":
            return "ABP"
        else:
            return "OTAA"

    def set_join_mode(self, mode):
        """
        Set LoRaWAN Mode.
        Parameter:
            OTAA 0
            ABP  1
        Return:
            True
            False
        """
        cmd = "AT+CJOINMODE=" + str(mode)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_frequency_band_mask(self):
        """
        Get frequency band mask.
        Parameter:
            None
        Return:
            mask
        """
        cmd = "AT+CFREQBANDMASK?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][15:]

    def set_frequency_band_mask(self, mask):
        """
        Get frequency band mask.
        Parameter:
            mask
        Return:
            True
            False
        """
        cmd = "AT+CFREQBANDMASK=" + str(mask)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_uplink_downlink_mode(self):
        """
        Get uplink and downlink mode.
        Parameter:
            None
        Return:
            mode:
                1 Same frequency mode
                2 Inter-frequency mode
        """
        cmd = "AT+CULDLMODE?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][11:]

    def set_uplink_downlink_mode(self, mode):
        """
        Get uplink and downlink mode.
        Parameter:
            mode:
                1 Same frequency mode
                2 Inter-frequency mode
        Return:
            True
            False
        """
        cmd = "AT+CULDLMODE=" + str(mode)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_work_mode(self):
        """
        Get model work mode.
        Parameter:
            None
        Return:
            mode
            False
        """
        cmd = "AT+CWORKMODE?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][11:]

    def set_work_mode(self, mode):
        """
        Get model work mode.
        Parameter:
            mode
                only support 2
        Return:
            True
            False
        """
        cmd = "AT+CWORKMODE=" + str(mode)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_class_mode(self):
        """
        Get class mode.
        Parameter:
            None
        Return:
            class mode:
                0 classA
                1 classB
                2 classB
            False
        """
        cmd = "AT+CCLASS?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        return result[1][8:]

    def set_class_mode(
        self, class_mode, branch=None, para1=None, para2=None, para3=None, para4=None
    ):
        """
        Set class mode with params.
        Parameter:
            class_mode:
                0 classA
                1 classB
                2 classC
            branch:
            para1:
            para2:
            para3:
            para4:
        Return:
            True
            False
        """
        cmd = "AT+CCLASS=" + str(class_mode)
        if (
            branch is None
            and para1 is not None
            and para2 is not None
            and para3 is not None
            and para4 is not None
        ):
            cmd = "{},{},{},{},{},{}".format(cmd, branch, para1, para2, para3, para4)
        result, error = self.__at_cmd(cmd)
        return not error

    def get_status(self):
        """
        Get status.
        Parameter:
            None
        Return:
            status:
                0
                1
                2
                3
                4
                5
                6
                7
                8
            False
        """
        pass

    def join(self, para1, para2=None, para3=None, para4=None):
        """
        Join LoRaWAN network.
        Parameter:
            para1:
                0 stop join
                1 start join
            para2:
                0 close auto join
                1 open auto join
            para3:
                7 ~ 255
            para4:
                1 ~ 256
        Return:
            True
            False
        """
        cmd = "AT+CJOIN=" + str(para1)
        if para2 is not None and para3 is not None and para4 is not None:
            cmd = "{},{},{},{}".format(cmd, para2, para3, para4)
        result, error = self.__at_cmd(cmd, timeout=500)
        return not error

    def send_data(self, payload, confirm=None, nbtrials=None):
        """
        Send data.
        Parameter:
            confirm:
                0
                1
            nbtrials:
                1 ~ 15
            payload:
                xxxxxx  HEX format string
        Return:
            True
            False
        """
        data = self._BytesToHexStr(payload.encode())
        if confirm is not None and nbtrials is not None:
            cmd = "AT+DTRX={},{},{},{}".format(confirm, nbtrials, int(len(data) / 2), data)
            result, error = self.__at_cmd(cmd, timeout=500, keyword="OK+RECV:")
        else:
            cmd = "AT+DTRX={},{}".format(int(len(data) / 2), data)
            result, error = self.__at_cmd(cmd, timeout=500, keyword="OK+SENT:")
        return not error

    def receive_data(self):
        """
        Receive downlink data if have.
        Parameter:
            None
        Return:
            data
            False
        """
        cmd = "AT+DRX?"
        result, error = self.__at_cmd(cmd)
        if error:
            return False
        result = self.__message_recv_data(result)
        try:
            index = result.index("+DRX:")
            if result[index][5] == "0":
                return None
            else:
                return result[index].split(",")[1]
        except ValueError:
            return False

    def set_uplink_confirm_mode(self, mode):
        """
        Set uplink confirmed mode, setting before send data.
        Parameter:
            mode:
                0 unconfirmed mode
                1 confirmed
        Return:
            True
            False
        """
        cmd = "AT+CCONFIRM=" + str(mode)
        result, error = self.__at_cmd(cmd)
        return not error

    def set_uplink_app_port(self, port):
        """
        Set uplink app port, setting before send data.
        Parameter:
            port 1 ~ 233
        Return:
            True
            False
        """
        cmd = "AT+CAPPPORT=" + str(port)
        result, error = self.__at_cmd(cmd)
        return not error

    def set_datarate(self, rate):
        """
        Set datarate.
        Parameter:
            rate:
                0 SF12 BW125
                1 SF11 BW125
                2 SF10 BW125
                3 SF9  BW125
                4 SF8  BW125
                5 SF7  BW125
        Return:
            True
            False
        """
        cmd = "AT+CDATARATE=" + str(rate)
        result, error = self.__at_cmd(cmd)
        return not error

    def set_report_mode(self, mode, interval=None):
        """
        Set report mode and report interval.
        Parameter:
            mode:
                0
                1
            interval:  s
        Return:
            True
            False
        """
        cmd = "AT+CRM={},{}".format(mode, interval)
        result, error = self.__at_cmd(cmd)
        return not error

    def set_tx_power(self, power):
        """
        Set tx power dBm.
        Parameter:
            power:
                0 17dBm
                1 15dBm
                2 13dBm
                3 11dBm
                4 9dBm
                5 7dBm
                6 5dBm
                7 3dBm
        Return:
            True
            False
        """
        # AT command not current.
        pass

    def enable_adaptive_datarate(self, status):
        """
        Set adaptive datarate status.
        Parameter:
            status:
                0 disable
                1 enable
        Return:
            True
            False
        """
        cmd = "AT+CADR=" + str(status)
        result, error = self.__at_cmd(cmd)
        return not error

    def set_rx_window_param(self, rx1_offset, rx2_dr, rx2_freq):
        """
        Set receive window param.
        Parameter:
            rx1_offset:
            rx2_dr:
                0 SF12 BW125
                1 SF11 BW125
                2 SF10 BW125
                3 SF9  BW125
                4 SF8  BW125
                5 SF7  BW125
            rx2_freq:  int hz
        Return:
            True
            False
        """
        cmd = "AT+CRXP={},{},{}".format(rx1_offset, rx2_dr, rx2_freq)
        result, error = self.__at_cmd(cmd)
        return not error

    def set_rx1_delay_time(self, delay):
        """
        Set receive window param.
        Parameter:
            delay
        Return:
            True
            False
        """
        cmd = "AT+CRX1DELAY={}".format(delay)
        result, error = self.__at_cmd(cmd)
        return not error

    ##############################################################################
    def __at_cmd(self, cmd, timeout=500, keyword=AT_RESPONED_OK):
        command = str(cmd) + str("\r\n")
        if self.debug:
            print("T: " + command[:-2])
        self.__uart.write(command)
        return self.__wait_ok(timeout, keyword)

    def __wait_ok(self, timeout, keyword=AT_RESPONED_OK):
        error = True
        msgs = []
        time.sleep(0.1)
        while self.__uart.any():
            time.sleep_ms(100)
            line = self.__uart.readline()
            if line is not None:
                line = line.decode()
                msgs.append(line)
                if keyword in line:
                    error = False
                elif line == AT_RESPONED_ERROR:
                    error = True
                    msgs.remove(line)

                if "ERR+SENT" in line:
                    error = True
                    msgs.remove(line)
                elif "ERR+SEND" in line:
                    error = True
                    msgs.remove(line)
                elif "+CME ERROR" in line:
                    error = True
                    msgs.remove(line)
                elif "OK+RECV:" in line:
                    if "02,00,00" not in line:  # special case
                        if len(self._downlink_buffer) < self._downlink_buffer_size:
                            self._downlink_buffer.append(line[8:-2])
                        else:
                            self._downlink_buffer.pop(0)
                            self._downlink_buffer.append(line[8:-2])
                elif "+CJOIN:OK" in line:
                    self._join_status = True
                elif "+CJOIN:FAIL" in line:
                    self._join_status = False
                else:
                    pass

        if self.debug:
            print("R: {}".format(msgs))
        return (msgs, error)

    def __message_recv_data(self, msgs):
        respon = []
        for i in msgs:
            if i != "\r\n" and i != "ASR6501:~# ":
                if len(i) > 2 and i[-2:] == "\r\n":
                    i = i[:-2]
                if len(i) >= 4 and i == "OK\r\n":
                    continue
                respon.append(i)
        return respon

    def _flatten(self, _list):
        return sum(([x] if not isinstance(x, list) else self._flatten(x) for x in _list), [])

    def _BytesToHexStr(self, bins):
        return "".join(["%02X" % x for x in bins]).strip()

    def _HexStrToBytes(self, hexStr):
        return binascii.unhexlify(hexStr)


class LoRaWAN_470(LoRaWAN_Asr650x):
    def __init__(self, tx, rx, debug=False):
        """
        Parameter:

        Return:
            True
            False
        """
        super(LoRaWAN_470, self).__init__(tx, rx, debug)

    def config_ABP(self, devaddr, appskey, nwkskey):
        """
        Config the ABP join mode information.
        Parameter:
        Return:
            None
        """
        self.set_DevAddr(devaddr)
        self.set_APPSKEY(appskey)
        self.set_NWKSKEY(nwkskey)
        self.set_join_mode(1)

    def get_ABP_config(self):
        """
        Get the ABP join mode information.
        Parameter:
            self
        Return:
            (devaddr, appskey, newskey)
        """
        return (self.get_DevAddr(), self.get_APPSKEY(), self.get_NWKSKEY())

    def config_OTAA(self, deveui, appeui, appkey):
        """
        Config the OTAA join mode information.
        Parameter:

        Return:
            True
            False
        """
        self.set_DevEui(deveui)
        self.set_AppEui(appeui)
        self.set_AppKey(appkey)
        self.set_join_mode(0)

    def get_OTAA_config(self):
        """
        Get the OTAA join mode information.
        Parameter:
        Return:
            (deveui, appeui, appkey)
        """
        return (self.get_DevEui(), self.get_AppEui(), self.get_AppKey())

    def check_join_status(self):
        """
        Check the LoRaWAN network join status.
        Parameter:
        Return:
            True   join OK
            False  join fail
        """
        if self._join_status:
            return self._join_status
        else:
            cmd = "AT+CSTATUS?"
            result, error = self.__at_cmd(cmd)
            result = self.__message_recv_data(result)
            for item in range(len(result)):
                try:
                    if result[item].index("+CSTATUS:") == 0:
                        if result[item].split(":")[1] == "05":
                            return False
                        elif result[item].split(":")[1] == "03":
                            return True
                        elif result[item].split(":")[1] == "04":
                            return True
                        elif result[item].split(":")[1] == "07":
                            return True
                        elif result[item].split(":")[1] == "08":
                            return True
                        else:
                            return False
                except:
                    pass

    def check_uplink_status(self):
        """
        Check data uplink status.
        Parameter:
        Return:
            True   success
            False  failed
        """
        cmd = "AT+CSTATUS?"
        result, error = self.__at_cmd(cmd)
        result = self.__message_recv_data(result)
        for item in range(len(result)):
            try:
                if result[item].index("+CSTATUS:") == 0:
                    if result[item].split(":")[1] == "05":
                        return False
                    elif result[item].split(":")[1] == "03":
                        return True
                    elif result[item].split(":")[1] == "04":
                        return True
                    elif result[item].split(":")[1] == "07":
                        return True
                    elif result[item].split(":")[1] == "08":
                        return True
                    else:
                        return False
            except:
                pass

    def check_downlink_data(self, timeout=10):
        """
        Check downlink data, dta will receive after uplink data.
        Parameter:
        Return:
            false
            data
        """
        msgs = []
        now_time = time.time()
        wait_time = now_time + timeout
        line = self.__uart.readline()
        while wait_time > time.time():
            while (wait_time > time.time()) and (line is None):
                line = self.__uart.readline()
            if line is not None:
                if AT_RECV_OK in line:
                    line = line.decode()
                    msgs.append(line[8:-2])
                    return msgs
                else:
                    line = None
        return False


class LoRaWAN_915(LoRaWAN_470):
    def __init__(self, tx, rx, debug=False):
        """
        Parameter:

        Return:
            True
            False
        """
        super(LoRaWAN_915, self).__init__(tx, rx, debug)


class LoRaWAN_868(LoRaWAN_470):
    def __init__(self, tx, rx, debug=False):
        """
        Parameter:

        Return:
            True
            False
        """
        super(LoRaWAN_868, self).__init__(tx, rx, debug)


"""
if __name__ == "__main__":

    lora = LoRaWAN_470(tx=17, rx=16, debug=True)

    # print(lora.get_ABP_config())

    lora.config_OTAA("0037CAE1FC3542B9", "70B3D57ED003B699", "67FA4ED1075A20573BCDD7594C458698")

    lora.set_rx_window_param(0, 0, 505300000)
    lora.set_frequency_band_mask("0400")
    lora.set_class_mode(2)
    lora.set_uplink_downlink_mode(2)
    lora.join(1, 0, 10, 8)
    while not lora.check_join_status():
        pass
    print("joined")
    lora.send_data("ABCDEF", confirm=1, nbtrials=10)
"""
