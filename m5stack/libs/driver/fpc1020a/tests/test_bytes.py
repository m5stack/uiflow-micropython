from os.path import abspath, dirname
import sys


TESTS = dirname(abspath(__file__))
sys.path.insert(0, dirname(TESTS))

from fpc1020a import types as t

data = t.serialize([0, 0, 0, b'\x12\x34\x56\x78'], (t.uint8_t, t.uint8_t, t.uint8_t, t.Bytes,))
print(data)