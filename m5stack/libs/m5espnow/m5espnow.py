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


class M5ESPNow(ESPNowBase):
    # Static buffers for alloc free receipt of messages with ESPNow.irecv().
    _data = [None, bytearray(MAX_DATA_LEN)]
    _none_tuple = (None, None)
    AP = 0
    STA = 1

    def __init__(self, wifi_ch=0) -> None:
        # Initialize Wi-Fi in STA and AP mode
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.wlan_ap = network.WLAN(network.AP_IF)
        self.wlan_sta.active(True)
        self.wlan_ap.active(True)
        self.wifi_channel = wifi_ch
        # Initialize ESP-NOW
        super().__init__()
        self.active(True)
        self.peer_list = [None] * 20
        self.broadcast = False

    def set_add_peer(self, peer_mac, peer_id=1, ifidx=0, encrypt=False, lmk=None):
        #! Add/register the provided mac address as a peer.
        peer_mac = binascii.unhexlify(peer_mac)
        self.peer_list[peer_id - 1] = peer_mac
        self.add_peer(peer_mac, channel=self.wifi_channel, ifidx=ifidx, encrypt=encrypt, lmk=lmk)

    def set_delete_peer(self, peer_id) -> None:
        #! Deregister the peer associated with the provided peer_mac address.
        peer = self.peer_list[peer_id - 1]
        if isinstance(peer, bytes):
            self.del_peer(peer)
            self.peer_list[peer_id - 1] = None

    def send_data(self, peer_id, msg) -> None:
        #! Send the data in msg to the stored peer ID peer_id with the given network.
        peer = self.peer_list[peer_id - 1]
        msg = self.convert_to_bytes(msg)
        if peer is not None:
            self.send(peer, msg)

    def broadcast_data(self, msg) -> None:
        #! All devices will also receive messages sent to the broadcast MAC address
        msg = self.convert_to_bytes(msg)
        peer = b"\xff\xff\xff\xff\xff\xff"
        if self.broadcast is False:
            self.add_peer(peer)
            self.broadcast = True
        self.send(peer, msg)

    def set_pmk_encrypt(self, pmk) -> None:
        #! Set the Primary Master Key (PMK) which is used to encrypt the Local Master Keys (LMK) for encrypting messages.
        self.set_pmk(pmk)

    def set_irq_callback(self, callback) -> None:
        #! Set a callback function to be called as soon as possible after a message has been received from another ESPNow device.
        super().irq(callback, self)

    def recv_data(self, timeout_ms=0) -> bytes:
        #! The callback function will be called with the ESPNow instance object as an argument.
        n = self.recvinto(self._data, timeout_ms)
        return [bytes(x) for x in self._data] if n else self._none_tuple

    def get_peer_list(self, encrypt=0) -> list:
        #! Get the parameters for all the registered peers (as a list).
        peer_lst = []
        for i in range(0, self.peer_count()[encrypt]):
            peer_lst.append(self._bytes_to_hex_str(self.get_peers()[i][0]))
        return peer_lst

    def get_mac(self, mode=0) -> str:
        #! Get the device network MAC address.
        return self.wlan_ap.config("mac") if mode else self.wlan_sta.config("mac")

    def get_remote_mac(self, select, ssid) -> None | bytes:
        #! To find remote mac by remote ssid.
        scan_detail = self.wlan_sta.scan()
        for i in range(0, len(scan_detail)):
            try:
                if scan_detail[i][0].decode("utf-8") == ssid:
                    return scan_detail[i][1] if select else scan_detail[i][2]
            except:
                return None

    def set_ap_ssid(self, ssid) -> None:
        #! Set the SSID configure in AP mode.
        self.wlan_ap.config(essid=ssid)

    def deinit(self) -> None:
        #! De-initialise the ESP-NOW software stack, disable callbacks, deallocate the recv data buffer and deregister all peers.
        self.active(False)

    def convert_to_bytes(self, msg) -> bytes:
        if isinstance(msg, list):
            msg = bytes(msg)
        elif isinstance(msg, int):
            msg = msg.to_bytes(4, "little")
        elif isinstance(msg, float):
            msg = struct.pack(">f", msg)
        return msg

    def _bytes_to(self, bytes, format=0) -> int | float:
        return struct.unpack(">f", bytes)[0] if format else int.from_bytes(bytes, "little")

    def _bytes_to_hex_str(self, bytes) -> str:
        #! To get a hex string from a bytes string.
        return binascii.hexlify(bytes).decode().upper()

    def _hex_str_to_bytes(self, hexstr) -> bytes:
        #! To get a bytes string from a hex string.
        return binascii.unhexlify(hexstr)

    def _to_bytes(self, variable) -> bytes:
        #! Get the current actual IP address, subnet mask and gateway of the module.
        return self.convert_to_bytes(variable)
