# Combine bootloader, partition table and application into a final binary.

import cmd
import os, sys

sys.path.append(os.getenv("IDF_PATH") + "/components/partition_table")

import gen_esp32part


def load_partition_table(filename):
    with open(filename, "rb") as f:
        return gen_esp32part.PartitionTable.from_binary(f.read())


# Extract command-line arguments.
arg_littlefs2_exec = sys.argv[1]
arg_board_type_in = sys.argv[2]
arg_filesystem_in = sys.argv[3]
arg_filesystem_out = sys.argv[4]
arg_partitions_bin = sys.argv[5]

# Load the partition table.
partition_table = load_partition_table(arg_partitions_bin)

# Inspect the partition table to find offsets and maximum sizes.
for part in partition_table:
    if part.type == gen_esp32part.DATA_TYPE and part.name == "vfs":
        max_size_filesystem = part.size

# print("fs partition size: 0x%x bytes" % max_size_filesystem)

cmd_line = "{} -c -b {} -i {} -o {} -s {}".format(
    arg_littlefs2_exec,
    arg_board_type_in,
    arg_filesystem_in,
    arg_filesystem_out,
    hex(max_size_filesystem),
)

os.system(cmd_line)
