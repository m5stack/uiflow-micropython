# Memory Budget and MemoryError

## Measure Available Heap

Available Python heap depends on firmware version, enabled modules, PSRAM,
UI objects and network/audio buffers. Source file size and line count do
not determine an application's memory limit. Parsing and compiling source
also require temporary memory.

Read the heap before imports, after UI setup, after networking starts and
after switching features:

```python
import gc
import os
import sys

def heap_checkpoint(stage):
    gc.collect()
    print(stage, "free:", gc.mem_free(), "allocated:", gc.mem_alloc())

print(os.uname())
print(sys.implementation)
heap_checkpoint("before application setup")
```
`gc.mem_free()` measures Python GC heap; it does not include every native
allocation or guarantee one contiguous allocation of that size. Where the
firmware provides it, `micropython.mem_info()` helps inspect the heap.
Reserve memory for the largest expected payload and temporary allocations
during reconnects and page changes.

## Common Allocation Traps

| Expensive pattern | Prefer |
| --- | --- |
| Images/audio/base64 embedded in large source literals | Files under `/flash/res` or a mounted SD card, read in bounded chunks. |
| `open(...).read()` or large response/JSON copies | Streaming or a bounded input size; close files/responses promptly. |
| New frame buffers or large bytearray slices in every frame | One reusable buffer; `readinto` and memoryview where supported. |
| Unlimited samples/logs in a list or dictionary | A fixed-size ring buffer, bounded history, or streamed logging. |
| Large string concatenations / formatting / temporary containers | Small status updates and bounded chunks; avoid whole-payload copies. |
| Recursive navigation or repeated page construction | A state machine, reused pages and bounded feature state. |

A raw RGB565 buffer needs at least `width * height * 2` bytes: 135 x 240
uses 64,800 bytes, 320 x 240 uses 153,600 bytes and 480 x 480 uses 460,800
bytes. Double buffering doubles this payload; descriptors, alignment,
decoders and the UI library need additional memory. Compressed file size
does not describe the size of a decoded image.

## Bounded File Copy

Use a new destination filename; opening it with `wb` replaces existing
contents. This example allocates one 1 KiB buffer rather than the entire file:

```python
def copy_resource(source, destination):
    buffer = bytearray(1024)
    view = memoryview(buffer)
    with open(source, "rb") as src, open(destination, "wb") as dst:
        while True:
            count = src.readinto(buffer)
            if not count:
                break
            dst.write(view[:count])
```
## Structure a Multi-feature Application

Avoid constructing a Wi-Fi manager, SSH client, sensor UI and their large
buffers together at import time. Split code by feature with a small shared
state/controller, create only the active feature's expensive resources, and
close them before switching. For example:

```text
main.py          # event loop and bounded application state
wifi_page.py     # connection UI; reuse the system's existing STA connection
ssh_page.py      # session lifecycle, bounded receive buffer, explicit close
level_page.py    # sensor sampling and reusable display state
res/             # image/audio/font files, not Python string literals
```
Moving code to several files helps organization and can reduce peak compiler
memory when loading one feature at a time. Importing every file at startup
still retains its modules and globals. Matching `.mpy` files can avoid
on-device source compilation but must match the firmware's MicroPython
version/architecture; they do not eliminate runtime allocations. Frozen
modules require a firmware build.

Release unused large references and close native resources before calling
`gc.collect()`. Collection cannot free objects still referenced by a page,
callback, global or `sys.modules`, and cannot fix an allocation failure
that occurs before `main.py` begins execution. Reduce peak allocations
and the amount of data kept in memory.

See [Resource Files and Paths](resource-files.md) and
[Board Capabilities](board-capabilities.md) before selecting resources
and optional modules.
