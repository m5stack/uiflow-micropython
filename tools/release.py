# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
from collections import namedtuple
import glob
import logging
import json

logging.basicConfig(level=logging.INFO)

try:
    import requests

    logging.debug("Successfully imported 'requests'.")
except ImportError:
    logging.warning("'requests' module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

    logging.info("'requests' has been successfully installed.")


FirewareInfo = namedtuple("FirewareInfo", ["board", "fid", "suffix"])

fireware_info_table = (
    FirewareInfo("M5STACK_AirQ", "9b14de127a34084d5c8aaedc7e762547", ""),
    FirewareInfo("M5STACK_Atom_Echo", None, "ATOM-ECHO"),
    FirewareInfo("M5STACK_Atom_Lite", "be2520992ff600ec2b8cf1e79d0229d5", "ATOM-LITE"),
    FirewareInfo("M5STACK_Atom_Matrix", "be2520992ff600ec2b8cf1e79d0229d5", "ATOM-Matrix"),
    FirewareInfo("M5STACK_AtomS3", "b5dcd270f671956482a8f8a363dc5f7d", "ATOMS3"),
    FirewareInfo("M5STACK_AtomS3_Lite", "b5dcd270f671956482a8f8a363dc5f7d", "ATOMS3-LITE"),
    FirewareInfo("M5STACK_AtomS3U", "b5dcd270f671956482a8f8a363dc5f7d", "ATOMS3U"),
    FirewareInfo("M5STACK_AtomU", "be2520992ff600ec2b8cf1e79d0229d5", "ATOMU"),
    FirewareInfo("M5STACK_Basic", "3ca95a4ce9c2c94514a97573962e43c2", "16MB"),
    FirewareInfo("M5STACK_Basic_4MB", "3ca95a4ce9c2c94514a97573962e43c2", "4MB"),
    FirewareInfo("M5STACK_Capsule", "36d3ea31ed0a039b0efa1a2ff102d93b", ""),
    FirewareInfo("M5STACK_Cardputer", "375d772b179c54d6a3f61f20be574235", ""),
    FirewareInfo("M5STACK_Core2", "ffadcb704115b88ca9fd149e567c73f5", "CORE2"),
    FirewareInfo("M5STACK_CoreInk", "737cc4a5469a3db81ed66e086f467ef5", ""),
    FirewareInfo("M5STACK_CoreS3", "94163f815781c124742a0ea26f22509c", ""),
    FirewareInfo("M5STACK_Dial", "431644329f5431d5ea36bec9ab94f664", ""),
    FirewareInfo("M5STACK_DinMeter", "42e62514d351731e7bcb6ce032789e00", ""),
    FirewareInfo("M5STACK_Fire", "fb3bf2d6484fcc25ae5c962a4245e88a", ""),
    FirewareInfo("M5STACK_Paper", "a003515b05be5c2aba5282630ecb3a51", ""),
    FirewareInfo("M5STACK_Stamp_PICO", "d3b966b3ff9b1f1bd29225cc307a0d78", ""),
    FirewareInfo("M5STACK_StampS3", "017e0eef047afb70eb8b9fc1fbccefe0", ""),
    FirewareInfo("M5STACK_Station", "6f1b78c29bfdfc5fbabfcf5614ab2042", ""),
    FirewareInfo("M5STACK_StickC", "a44718de7ac2c0879b75cd56db8c667e", ""),
    FirewareInfo("M5STACK_StickC_PLUS", "e012605c9ebfebb7159fff2ac35f79c8", ""),
    FirewareInfo("M5STACK_StickC_PLUS2", "39d70217ff0b53c368b0efbfbf2a11af", ""),
    FirewareInfo("M5STACK_Tough", "ffadcb704115b88ca9fd149e567c73f5", "TOUGH"),
)

third_party_info_table = (
    FirewareInfo("SEEED_STUDIO_XIAO_ESP32S3", "375ae5281d0de5a7dba8296fac53f832", ""),
)


def get_version():
    version = None
    with open("./m5stack/version.txt", "r") as file:
        version = file.read()
    return version.lower()


def get_online_version():
    url = "https://m5burner-api.m5stack.com/api/firmware/uiflow2/latest"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        logging.debug(data)
        return data
    else:
        logging.error("status: %d", response.status_code)
        logging.error("text: %s", response.text)


def check_version_exists(infos, fid, version):
    for info in infos:
        if info["fid"] == fid:
            for item in info["versions"]:
                if item["version"] == version:
                    return False
    return True


def upload(fid, version, file_path):
    logging.info(f"Uploading {file_path}")
    url = f"http://m5burner-api.m5stack.com/api/admin/firmware/{fid}/version"
    headers = {}
    payload = {"version": version}
    files = [("firmware", ("file.bin", open(file_path, "rb"), "application/octet-stream"))]
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    logging.info(response.text)


def remove(fid, version, file_path):
    logging.info(f"Remove {file_path}")
    url = f"http://m5burner-api.m5stack.com/api/admin/firmware/remove/{fid}"
    headers = {"Content-Type": "application/json"}
    payload = {"version": version}
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    logging.info(response.text)


def main():
    version = get_version()
    logging.info(f"Current version: {version}")
    online_version_infos = get_online_version()

    for info in fireware_info_table:
        if info.fid is None:
            logging.warning(f"Skipping {info.board}")
            continue

        full_version = None
        if len(info.suffix):
            full_version = version + "-" + info.suffix
        else:
            full_version = version
        if check_version_exists(online_version_infos, info.fid, full_version):
            pattern = f"./m5stack/build-{info.board}/uiflow-*-*.bin"
            matching_files = glob.glob(pattern)
            if matching_files:
                upload(info.fid, full_version, matching_files[0])
        else:
            logging.warning(f"Version {full_version} already exists.")

    for info in third_party_info_table:
        if info.fid is None:
            logging.warning(f"Skipping {info.board}")
            continue

        full_version = None
        if len(info.suffix):
            full_version = version + "-" + info.suffix
        else:
            full_version = version
        if check_version_exists(online_version_infos, info.fid, full_version):
            pattern = f"./third-party/build-{info.board}/uiflow-*-*.bin"
            matching_files = glob.glob(pattern)
            if matching_files:
                upload(info.fid, full_version, matching_files[0])
        else:
            logging.warning(f"Version {full_version} already exists.")

    logging.info("Done.")


if __name__ == "__main__":
    main()
