import gc
import uos as os
from flashbdev import bdev

uiflow_str = """
       _  __ _               
 _   _(_)/ _| | _____      __
| | | | | |_| |/ _ \ \ /\ / /
| |_| | |  _| | (_) \ V  V / 
 \__,_|_|_| |_|\___/ \_/\_/  
"""
print(uiflow_str)
del uiflow_str

# monut flash file system
try:
    if bdev:
        vfs = os.VfsLfs2(bdev, progsize=32, readsize=128, lookahead=128)
        os.mount(vfs, "/flash")
except OSError:
    import inisetup

    vfs = inisetup.setup()

gc.collect()
gc.threshold(56 * 1024)

import micropython
import sys

micropython.alloc_emergency_exception_buf(256)
# system path
sys.path.append("/flash/libs")
sys.path.append("/flash/libs/micropython")
# change directory to "/flash"
os.chdir("/flash")

# copy OTA update file to main.py
# main_ota_temp.py this file name is fixed
try:
    s = open("main_ota_temp.py", "rb")
    f = open("main.py", "wb")
    f.write(s.read())
    s.close()
    f.close()
    os.remove("main_ota_temp.py")
except:
    pass
