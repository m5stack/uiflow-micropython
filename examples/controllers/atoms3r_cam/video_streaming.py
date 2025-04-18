# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import M5
from M5 import Display as dis
import camera as cam
import network
import time
import jpg
import socket
import struct
import code_scanner
import sys

M5.begin()

# Initialize camera
cam.init(pixformat=cam.RGB565, framesize=cam.QVGA)
cam.set_hmirror(False)

# Connect to existing WiFi and display IP
wlan = network.WLAN(network.STA_IF)
if wlan.isconnected():
    ip_info = wlan.ifconfig()
    ip_addr = ip_info[0]
    print("Local IP Address:", ip_addr)
    print("\nPlease open your browser and visit http://%s:8080 to view the stream.\n" % ip_addr)
else:
    print("WiFi not connected.")

# Create server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
s.bind(("0.0.0.0", 8080))
s.listen(2)
s.setblocking(True)


def start_streaming(s):
    print("Waiting for client connection...")
    client, addr = s.accept()
    client.settimeout(5.0)
    print("Connected: %s:%d" % (addr[0], addr[1]))

    # Receive HTTP request
    try:
        data = client.recv(1024)
        if not data:
            raise Exception("No HTTP request received")
    except:
        client.close()
        return

    # Send MJPEG HTTP response headers
    try:
        client.sendall(
            "HTTP/1.1 200 OK\r\n"
            "Server: AtomS3R-CAM\r\n"
            "Content-Type: multipart/x-mixed-replace;boundary=atoms3r_cam\r\n"
            "Cache-Control: no-cache\r\n"
            "Pragma: no-cache\r\n\r\n"
        )
    except:
        client.close()
        return

    # Main video streaming loop
    while True:
        try:
            img = cam.snapshot()
            if img is None:
                continue

            # QR code detection
            qrcode = code_scanner.find_qrcodes(img)
            if qrcode:
                payload = qrcode.payload()
                print("QR Code detected:", payload)
                img.draw_string(10, 10, "QRCode: %s" % payload, color=(0, 0, 255), scale=1)

            # Encode and send frame
            cframe = jpg.encode(img, 80)
            header = (
                "\r\n--atoms3r_cam\r\n"
                "Content-Type: image/jpeg\r\n"
                "Content-Length: %d\r\n\r\n" % cframe.size()
            )
            client.sendall(header)
            client.sendall(cframe.bytearray())

        except Exception as e:
            print("Streaming interrupted:", e)
            client.close()
            break


# Main server loop
while True:
    try:
        start_streaming(s)
    except Exception as e:
        print("Socket error:", e)
        time.sleep(2)
