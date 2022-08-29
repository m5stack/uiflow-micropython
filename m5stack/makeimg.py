# Combine bootloader, partition table and application into a final binary.

from datetime import date
import os, sys

sys.path.append(os.getenv("IDF_PATH") + "/components/partition_table")

import gen_esp32part

OFFSET_BOOTLOADER_DEFAULT = 0x1000
OFFSET_PARTITIONS_DEFAULT = 0x8000


def load_sdkconfig_value(filename, value, default):
    value = "CONFIG_" + value + "="
    with open(filename, "r") as f:
        for line in f:
            if line.startswith(value):
                return line.split("=", 1)[1]
    return


def load_sdkconfig_hex_value(filename, value, default):
    value = "CONFIG_" + value + "="
    with open(filename, "r") as f:
        for line in f:
            if line.startswith(value):
                return int(line.split("=", 1)[1], 16)
    return default


def load_sdkconfig_spiram_value(filename):
    value = "CONFIG_ESP32_SPIRAM_SUPPORT="
    with open(filename, "r") as f:
        for line in f:
            if line.startswith(value):
                if line.split("=", 1)[1][0] == "y":
                    return "SPIRAM-"
    return ""


def load_sdkconfig_flash_size_value(filename):
    value = "CONFIG_ESPTOOLPY_FLASHSIZE="
    with open(filename, "r") as f:
        for line in f:
            if line.startswith(value):
                return str(line.split("_")[-1].split("=", 1)[1][1:-2])
    return "4MB"


def load_sdkconfig_str_value(filename, value, default):
    value = load_sdkconfig_value(filename, value, None)
    if value is None:
        return default
    return value.strip().strip('"')


def load_partition_table(filename):
    with open(filename, "rb") as f:
        return gen_esp32part.PartitionTable.from_binary(f.read())


# Extract command-line arguments.
arg_sdkconfig = sys.argv[1]
arg_bootloader_bin = sys.argv[2]
arg_partitions_bin = sys.argv[3]
arg_nvs_bin = sys.argv[4]
arg_application_bin = sys.argv[5]
arg_filesystem_bin = sys.argv[6]
arg_output_bin = sys.argv[7]
arg_output_uf2 = sys.argv[8]

# Load required sdkconfig values.
idf_target = load_sdkconfig_str_value(arg_sdkconfig, "IDF_TARGET", "").upper()
offset_bootloader = load_sdkconfig_hex_value(
    arg_sdkconfig, "BOOTLOADER_OFFSET_IN_FLASH", OFFSET_BOOTLOADER_DEFAULT
)
offset_partitions = load_sdkconfig_hex_value(
    arg_sdkconfig, "PARTITION_TABLE_OFFSET", OFFSET_PARTITIONS_DEFAULT
)

# Load the partition table.
partition_table = load_partition_table(arg_partitions_bin)

max_size_bootloader = offset_partitions - offset_bootloader
max_size_partitions = 0
offset_nvs = 0
max_size_nvs = 0
offset_application = 0
max_size_application = 0
offset_filesystem = 0
max_size_filesystem = 0

# Inspect the partition table to find offsets and maximum sizes.
for part in partition_table:
    if part.name == "nvs":
        max_size_partitions = part.offset - offset_partitions
        offset_nvs = part.offset
        max_size_nvs = part.size
    elif part.type == gen_esp32part.APP_TYPE and offset_application == 0:
        offset_application = part.offset
        max_size_application = part.size
    elif part.type == gen_esp32part.DATA_TYPE and part.name == "vfs":
        offset_filesystem = part.offset
        max_size_filesystem = part.size


# Define the input files, their location and maximum size.
files_in = [
    ("bootloader", offset_bootloader, max_size_bootloader, arg_bootloader_bin),
    ("partitions", offset_partitions, max_size_partitions, arg_partitions_bin),
    ("nvs", offset_nvs, max_size_nvs, arg_nvs_bin),
    ("application", offset_application, max_size_application, arg_application_bin),
    ("filesystem", offset_filesystem, max_size_filesystem, arg_filesystem_bin),
]

file_out = arg_output_bin

# Write output file with combined firmware.
cur_offset = offset_bootloader
with open(file_out, "wb") as fout:
    for name, offset, max_size, file_in in files_in:
        assert offset >= cur_offset
        fout.write(b"\xff" * (offset - cur_offset))
        cur_offset = offset
        with open(file_in, "rb") as fin:
            data = fin.read()
            fout.write(data)
            cur_offset += len(data)
            print(
                "%-12s@0x%06x % 9d  (% 8d remaining)"
                % (name, offset, len(data), max_size - len(data))
            )
            if len(data) > max_size:
                print(
                    "ERROR: %s overflows allocated space of %d bytes by %d bytes"
                    % (name, max_size, len(data) - max_size)
                )
                sys.exit(1)
    print("%-23s% 8d  (% 8.1f MB)" % ("total", cur_offset, (cur_offset / 1024 / 1024)))
    print(
        "\r\nWrote 0x%x bytes to file %s, ready to flash to offset 0x%x.\r\n"
        "Example command:\r\n"
        "    1. make flash\r\n"
        "    2. esptool.py --chip %s --port /dev/ttyUSBx --baud 1500000 write_flash 0x%x %s"
        % (cur_offset, file_out, offset_bootloader, idf_target, offset_bootloader, file_out)
    )

# Generate .uf2 file if the SoC has native USB.
if idf_target in ("ESP32S2", "ESP32S3"):
    sys.path.append(os.path.join(os.path.dirname(__file__), "../micropython/tools"))
    import uf2conv

    families = uf2conv.load_families()
    uf2conv.appstartaddr = 0
    uf2conv.familyid = families[idf_target]
    with open(arg_application_bin, "rb") as fin, open(arg_output_uf2, "wb") as fout:
        fout.write(uf2conv.convert_to_uf2(fin.read()))

# uiflow-[git describe]-[target]-<feature_str->[flash size]-[date]
today = date.today()
feature_str = ""
if idf_target == "ESP32C3":
    if load_sdkconfig_str_value(arg_sdkconfig, "ESP_CONSOLE_USB_SERIAL_JTAG", "").upper() == "Y":
        feature_str = "usb-"
else:
    feature_str = load_sdkconfig_spiram_value(arg_sdkconfig).lower()

release_file_out = "{}-{}-{}{}-{}.bin".format(
    file_out.split(".bin")[0],
    idf_target.lower(),
    feature_str.lower(),
    load_sdkconfig_flash_size_value(arg_sdkconfig).lower(),
    today.strftime("%Y%m%d"),
)
os.system("cp {} {}".format(file_out, release_file_out))
