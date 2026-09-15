# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import camera
from easysocket import EasyTCPServer
import socket
import network
import code_scanner
import time
import image
import jpg


tcps = None
wlan_sta = None
stamp_addon_cam0308_0 = None


stream_info = None
client = None
request = None
ssid = None
pwd = None
cam_img = None
code_result = None
frame = None


def setup():
    global \
        tcps, \
        wlan_sta, \
        stamp_addon_cam0308_0, \
        stream_info, \
        client, \
        request, \
        ssid, \
        pwd, \
        cam_img, \
        code_result, \
        frame

    M5.begin()
    camera.init(pixformat=camera.RGB565, framesize=camera.FRAME_QVGA)
    camera.set_hmirror(False)
    camera.set_vflip(False)
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    ssid = "your-wifi-ssid"
    pwd = "your-wifi-pwd"
    print((str("Connecting to Wi-Fi: ") + str(ssid)))
    wlan_sta.connect(ssid, pwd)
    while not (wlan_sta.isconnected()):
        time.sleep_ms(100)
    tcps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcps.bind(("0.0.0.0", 8080))
    tcps.listen(1)
    print(
        (str("Open http://") + str((str((wlan_sta.ifconfig()[0])) + str(":8080/ in a browser"))))
    )


def loop():
    global \
        tcps, \
        wlan_sta, \
        stamp_addon_cam0308_0, \
        stream_info, \
        client, \
        request, \
        ssid, \
        pwd, \
        cam_img, \
        code_result, \
        frame
    M5.update()
    try:
        M5.update()
        stream_info = tcps.accept()
        client = stream_info[0]
        request = client.recv(1024)
        client.send(
            (
                str(
                    (
                        str(
                            (
                                str(
                                    (
                                        str(
                                            (
                                                str(
                                                    (
                                                        str(
                                                            (
                                                                str("HTTP/1.1 200 OK")
                                                                + str((chr(13)))
                                                            )
                                                        )
                                                        + str((chr(10)))
                                                    )
                                                )
                                                + str(
                                                    "Content-Type: multipart/x-mixed-replace; boundary=cam0308"
                                                )
                                            )
                                        )
                                        + str((chr(13)))
                                    )
                                )
                                + str((chr(10)))
                            )
                        )
                        + str((chr(13)))
                    )
                )
                + str((chr(10)))
            )
        )
        while True:
            cam_img = camera.snapshot()
            code_result = code_scanner.find_qrcodes(cam_img)
            if code_result:
                print(code_result.payload())
                cam_img.draw_string(8, 8, str(code_result.payload()), color=0x0000FF, scale=1)
            frame = jpg.encode(cam_img, 80)
            client.send(
                (
                    str(
                        (
                            str(
                                (
                                    str(
                                        (
                                            str(
                                                (
                                                    str(
                                                        (
                                                            str(
                                                                (
                                                                    str(
                                                                        (
                                                                            str(
                                                                                (
                                                                                    str((chr(13)))
                                                                                    + str(
                                                                                        (chr(10))
                                                                                    )
                                                                                )
                                                                            )
                                                                            + str("--cam0308")
                                                                        )
                                                                    )
                                                                    + str((chr(13)))
                                                                )
                                                            )
                                                            + str((chr(10)))
                                                        )
                                                    )
                                                    + str("Content-Type: image/jpeg")
                                                )
                                            )
                                            + str((chr(13)))
                                        )
                                    )
                                    + str((chr(10)))
                                )
                            )
                            + str((chr(13)))
                        )
                    )
                    + str((chr(10)))
                )
            )
            client.send(frame.bytearray())
    except:
        try:
            client.close()
        except:
            pass

        tcps.close()
        stream_info = tcps.accept()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
