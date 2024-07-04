# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# espnow module for MicroPython on ESP32
# MIT license; Copyright (c) 2022 Glenn Moloney @glenn20
#
# SPDX-License-Identifier: MIT

from _espnow import *
import network
import binascii
import struct

AP = 0
STA = 1


class M5ESPNow(ESPNowBase):
    # Static buffers for alloc free receipt of messages with ESPNow.irecv().
    _data = [None, bytearray(MAX_DATA_LEN)]
    _none_tuple = (None, None)

    def __init__(self, wifi_ch=0) -> None:
        super().__init__()
        # Initialize Wi-Fi in STA and AP mode
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.wlan_ap = network.WLAN(network.AP_IF)
        self.wlan_sta.active(True)
        self.wlan_ap.active(True)
        self.wifi_channel = wifi_ch
        # Initialize ESP-NOW
        self.active(True)
        self.peer_list = [None] * 20
        self.broadcast = False

    def set_add_peer(self, peer_mac, peer_id=1, ifidx=0, encrypt=False, lmk=None):
        peer_mac = binascii.unhexlify(peer_mac)
        self.peer_list[peer_id - 1] = peer_mac
        self.add_peer(peer_mac, channel=self.wifi_channel, ifidx=ifidx, encrypt=encrypt, lmk=lmk)

    def set_delete_peer(self, peer_id) -> None:
        peer = self.peer_list[peer_id - 1]
        if bytes(peer) is bytes:
            self.del_peer(peer)

    def send_data(self, peer_id, msg) -> None:
        peer = self.peer_list[peer_id - 1]
        msg = self.convert_to_bytes(msg)
        self.send(peer, msg)

    def broadcast_data(self, msg) -> None:
        msg = self.convert_to_bytes(msg)
        peer = b"\xff\xff\xff\xff\xff\xff"
        if self.broadcast is False:
            self.add_peer(peer)
            self.broadcast = True
        self.send(peer, msg)

    def set_pmk_encrypt(self, pmk) -> None:
        self.set_pmk(pmk)

    def set_irq_callback(self, callback) -> None:
        super().irq(callback, self)

    def recv_data(self, timeout_ms=0) -> bytes:
        n = self.recvinto(self._data, timeout_ms)
        return [bytes(x) for x in self._data] if n else self._none_tuple

    def get_peer_list(self, encrypt=0) -> list:
        peer_lst = []
        for i in range(0, self.peer_count()[encrypt]):
            peer_lst.append(self._bytes_to_hex_str(self.get_peers()[i][0]))
        return peer_lst

    def get_mac(self, mode=0) -> str:
        return self.wlan_ap.config("mac") if mode else self.wlan_sta.config("mac")

    def get_remote_mac(self, select, ssid):
        scan_detail = self.wlan_sta.scan()
        for i in range(0, len(scan_detail)):
            try:
                if scan_detail[i][0].decode("utf-8") == ssid:
                    return scan_detail[i][1] if select else scan_detail[i][2]
            except:
                return None

    def set_deinit(self):
        self.active(False)
        self.wlan_sta.active(False)
        self.wlan_ap.active(False)

    def convert_to_bytes(self, msg):
        if isinstance(msg, list):
            msg = bytes(msg)
        elif isinstance(msg, int):
            msg = msg.to_bytes(4, "little")
        elif isinstance(msg, float):
            msg = struct.pack(">d", msg)
        return msg

    def _bytes_to(self, payload, format=0):
        return (
            struct.unpack(">d", payload)[0]
            if format
            else int.from_bytes(payload, byteorder="little")
        )

    def _bytes_to_hex_str(self, bytes):
        return binascii.hexlify(bytes).decode().upper()

    def _hex_str_to_bytes(self, hexStr):
        return binascii.unhexlify(hexStr)

    def _to_bytes(self, list):
        return bytes(list)
