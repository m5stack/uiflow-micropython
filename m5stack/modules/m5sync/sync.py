# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""
HOW TO USE:

import sync
sync.run()

This module will download files from res.json and save them to /flash/res.
It will also create a record.json to record the files it has downloaded.
Included a simple GUI to show the progress.

If a file in record.json is not in res.json, it will be deleted.
If a file in res.json is not in record.json, it will be downloaded.
If a file in res.json is in record.json, it will be skipped.
"""

import json
import os
import time
import hashlib
import requests
from collections import namedtuple
import network
import M5
from hardware import RGB
from widgets.label import Label

# Log control
WARN = True
INFO = True
DEBUG = False

ViewInfo = namedtuple(
    "ViewInfo", ["title_x", "title_y", "title_font", "text_x", "text_y", "text_font"]
)


def file_exists(file_path):
    try:
        with open(file_path, "r"):
            return True
    except OSError:
        return False


def calculate_md5(file_path):
    md5_hash = hashlib.md5()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.digest().hex()


def open_or_create_chche(file_path):
    if file_exists(file_path):
        root = None
        with open(file_path, "r") as f:
            root = json.load(f)
            return root["fileList"]
    return []


def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump({"time": time.mktime(time.localtime()), "fileList": data}, f)


def wait_key(timeout=5000):
    start = time.time()
    while time.time() - start < timeout:
        M5.update()
        if M5.Touch.getCount() > 0:
            return
        if M5.BtnA.wasClicked() or M5.BtnB.wasClicked() or M5.BtnC.wasClicked():
            return
        if M5.BtnPWR.wasPressed():
            return
    return


class DownloadView:
    COLOR_RED = 0xFF0000
    COLOR_YELLOW = 0xFFFF00
    COLOR_BLUE = 0x0000FF
    COLOR_GREEN = 0x00FF00
    COLOR_BLACK = 0x000000

    view_info_table = {
        M5.BOARD.M5Stack: ViewInfo(
            title_x=160,
            title_y=71,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=160,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu24,
        ),
        M5.BOARD.M5StackCore2: ViewInfo(
            title_x=160,
            title_y=71,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=160,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5StickC: ViewInfo(
            title_x=40,
            title_y=58,
            title_font=M5.Lcd.FONTS.DejaVu18,
            text_x=40,
            text_y=80,
            text_font=M5.Lcd.FONTS.DejaVu12,
        ),
        M5.BOARD.M5StickCPlus: ViewInfo(
            title_x=67,
            title_y=91,
            title_font=M5.Lcd.FONTS.DejaVu24,
            text_x=67,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5StickCPlus2: ViewInfo(
            title_x=67,
            title_y=91,
            title_font=M5.Lcd.FONTS.DejaVu24,
            text_x=67,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5StackCoreInk: ViewInfo(
            title_x=100,
            title_y=51,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=100,
            text_y=100,
            text_font=M5.Lcd.FONTS.DejaVu24,
        ),
        M5.BOARD.M5Paper: ViewInfo(
            title_x=280,
            title_y=412,
            title_font=M5.Lcd.FONTS.DejaVu56,
            text_x=280,
            text_y=480,
            text_font=M5.Lcd.FONTS.DejaVu40,
        ),
        M5.BOARD.M5Tough: ViewInfo(
            title_x=160,
            title_y=71,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=160,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu24,
        ),
        M5.BOARD.M5Station: ViewInfo(
            title_x=120,
            title_y=39,
            title_font=M5.Lcd.FONTS.DejaVu24,
            text_x=120,
            text_y=68,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5StackCoreS3: ViewInfo(
            title_x=160,
            title_y=71,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=160,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu24,
        ),
        M5.BOARD.M5AtomS3: ViewInfo(
            title_x=64,
            title_y=35,
            title_font=M5.Lcd.FONTS.DejaVu24,
            text_x=64,
            text_y=64,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5Dial: ViewInfo(
            title_x=120,
            title_y=71,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=120,
            text_y=120,
            text_font=M5.Lcd.FONTS.DejaVu24,
        ),
        M5.BOARD.M5DinMeter: ViewInfo(
            title_x=120,
            title_y=39,
            title_font=M5.Lcd.FONTS.DejaVu24,
            text_x=120,
            text_y=68,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5Cardputer: ViewInfo(
            title_x=120,
            title_y=39,
            title_font=M5.Lcd.FONTS.DejaVu24,
            text_x=120,
            text_y=68,
            text_font=M5.Lcd.FONTS.DejaVu18,
        ),
        M5.BOARD.M5AirQ: ViewInfo(
            title_x=100,
            title_y=51,
            title_font=M5.Lcd.FONTS.DejaVu40,
            text_x=100,
            text_y=100,
            text_font=M5.Lcd.FONTS.DejaVu24,
        ),
    }

    def __init__(self) -> None:
        board_id = M5.getBoard()
        self.view_info = self.view_info_table.get(board_id, None)

    def on_view(self):
        if self.view_info:
            M5.Lcd.clear(0xFFFFFF)
            self.title_label = Label(
                "Sync...",
                self.view_info.title_x,
                self.view_info.title_y,
                w=M5.Lcd.width(),
                h=M5.Lcd.height(),
                font_align=Label.CENTER_ALIGNED,
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=self.view_info.title_font,
            )
            self.title_label.set_text("Sync...")

            self.progress_label = Label(
                "0%",
                self.view_info.text_x,
                self.view_info.text_y,
                w=M5.Lcd.width(),
                h=M5.Lcd.height(),
                font_align=Label.CENTER_ALIGNED,
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=self.view_info.text_font,
            )
            self.progress_label.set_text("0%")
        else:
            self.rgb = RGB()
            self.rgb.set_color(0, self.COLOR_YELLOW)

    def set_total_size(self, size):
        self.total_size = size
        self.downloaded_size = 0

    def update_progress(self, size):
        self.downloaded_size += size
        percent = int(self.downloaded_size / self.total_size * 100)
        if self.view_info:
            self.progress_label.set_text(f"{percent}%")
        else:
            self.rgb.set_color(0, self.COLOR_BLACK)
            time.sleep(0.02)
            self.rgb.set_color(0, self.COLOR_BLUE)
            time.sleep(0.02)

    def on_success(self):
        if self.view_info:
            self.title_label.set_text("Success")
        else:
            self.rgb.set_color(0, self.COLOR_GREEN)
        time.sleep(1)

    def on_failed(self):
        if self.view_info:
            self.title_label.set_text("Failed")
        else:
            self.rgb.set_color(0, self.COLOR_RED)

    def on_exit(self):
        if self.view_info:
            M5.Lcd.clear(0x000000)
            M5.Lcd.setTextColor(0xFFFFFF, 0)


class M5Sync:
    RECORD_JSON_PATH = "/flash/res/record.json"
    SYNC_JSON_PATH = "/flash/res/res.json"

    def __init__(self) -> None:
        self._view = DownloadView()

    def run(self):
        # STEP1: create or open record.json
        cache_records = open_or_create_chche(self.RECORD_JSON_PATH)
        DEBUG and print("[DEBUG] record.json:", cache_records)

        # STEP2: open res.json
        file_records = []
        total_size = 0
        if not file_exists(self.SYNC_JSON_PATH):
            return
        else:
            with open(self.SYNC_JSON_PATH, "r") as f:
                sync = json.load(f)
            DEBUG and print("[DEBUG] res.json:", sync)
            file_records = sync["fileList"]
            total_size = sync["totalSize"]

        if len(cache_records) == 0 and len(file_records) == 0:
            INFO and print("[INFO] No files to sync.")
            return  # no files to sync

        # STEP3: init lcd or led
        self._view.set_total_size(total_size)
        self._view.on_view()

        # STEP4: process files
        err = self.process_files(cache_records, file_records)

        if len(err) > 0:
            self._view.on_failed()
        else:
            self._view.on_success()

        # STEP5: save record, remove res.json
        save_json(self.RECORD_JSON_PATH, cache_records)
        if len(err) > 0:
            wait_key()

        self._view.on_exit()
        del self._view
        INFO and print("[INFO] Sync finished.")
        return

    def process_files(self, record, sync):
        # TODO
        err = ""

        # 检查sync文件中的记录在不在record中，不在就删除
        for old_file in record:
            no_exist = True
            for file in sync:
                if file["devicePath"] == old_file["devicePath"]:
                    no_exist = False
                    break
            if no_exist:
                try:
                    os.remove(old_file["devicePath"])
                    INFO and print("[INFO] Deleted file:", old_file["devicePath"])
                except OSError as e:
                    WARN and print(f"[WARN] Error deleting file {old_file['devicePath']}: {e}")
                record.remove(old_file)
                continue  # 继续下一个循环，不增加索引

        # 检查record文件中的记录在不在sync中，不在就下载
        for file in sync:
            # update_info(f"{i+1}/{file_num}")
            if file_exists(file["devicePath"]):
                # 如果文件存在，检查md5
                if calculate_md5(file["devicePath"]) == file["md5"]:
                    INFO and print(f"[INFO] File {file['devicePath']} already downloaded.")
                    self._view.update_progress(file["size"])
                    for index in range(len(record)):
                        if record[index]["devicePath"] == file["devicePath"]:
                            record.pop(index)
                            break
                    record.append(file)
                    continue

            # 如果文件不存在或者md5不匹配，下载文件
            INFO and print(f"[INFO] MD5 mismatch for file: {file['name']}")
            for _ in range(3):
                if self.download_file(file["url"], file["devicePath"]) is False:
                    INFO and print(f"[INFO] Failed to download file: {file['devicePath']}")
                    continue
                if calculate_md5(file["devicePath"]) == file["md5"]:
                    INFO and print(f"[INFO] Downloaded and verified file: {file['devicePath']}")
                    for index in range(len(record)):
                        if record[index]["devicePath"] == file["devicePath"]:
                            record.pop(index)
                            break
                    record.append(file)
                    break
        return err

    def download_file(self, url, save_path, retry=3):
        def _download_file(url, save_path):
            # 发送GET请求
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                length = int(response.headers["Content-Length"])
                block_len = 4096
                source = response.raw
                read = 0
                with open(save_path, "wb") as file:
                    # 逐块读取数据
                    while read < length:
                        to_read = block_len if (length - read) >= block_len else length - read
                        buf = source.read(to_read)
                        read += len(buf)
                        DEBUG and print(f"[DEBUG] {read}/{length}; LEN = {len(buf)}", end="\r")
                        file.write(buf)
                        # update_progress(0, read / length)
                        self._view.update_progress(len(buf))
                        # update_info(f"{read}/{length}")
                        # time.sleep(0.1) #emulate slow connection
                    INFO and print(f"[INFO] File {url} downloaded successfully.")
                response.close()
                return True
            else:
                WARN and print("[WARN] Failed to download file. code = %d" % response.status_code)
                response.close()
                return False

        for i in range(retry):
            if _download_file(url, save_path):
                return True
            WARN and print(f"[WARN] Retry {i+1}...")


def run():
    INFO and print("[INFO] Syncing resources...")

    wlan = network.WLAN(network.STA_IF)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if not wlan.isconnected():
        WARN and print("[WARN] WiFi not connected.")
        WARN and print("[WARN] quit sync.")
        return

    INFO and print("[INFO] WiFi connected!")
    sync = M5Sync()
    sync.run()
    del sync
