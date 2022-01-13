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

micropython.alloc_emergency_exception_buf(256)
