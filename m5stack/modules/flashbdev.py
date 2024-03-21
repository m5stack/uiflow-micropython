# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from esp32 import Partition

sys_bdev = Partition.find(Partition.TYPE_DATA, label="sys")
sys_bdev = sys_bdev[0] if sys_bdev else None

vfs_bdev = Partition.find(Partition.TYPE_DATA, label="vfs")
vfs_bdev = vfs_bdev[0] if vfs_bdev else None
