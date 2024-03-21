# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os
import sys
from os.path import abspath, dirname, exists, join, isdir, isfile
import unittest

TESTS = dirname(abspath(__file__))
sys.path.insert(0, dirname(TESTS))

import fpc1020a

f = open("data/add_mode/succuss", "r")
fpc = fpc1020a.FPC1020A(f)
print(fpc.get_add_mode())

# class TestFPC1020A(unittest.TestCase):

#     def tes_get_add_mode(self):
#         f = open("data/add_mode/succuss", "r")
#         fpc = fpc1020a.FPC1020A(f)
#         print(fpc.get_add_mode())
#         self.assertEqual(fpc.get_add_mode(), 1)

# if __name__ == '__main__':
#     unittest.main()
