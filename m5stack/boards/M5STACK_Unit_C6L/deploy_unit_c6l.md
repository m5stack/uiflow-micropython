Program your board using the esptool.py program, found
[here](https://github.com/espressif/esptool).

To put the NanoC6 into 'update mode', hold the button while connecting the USB
cable. It can be released after the connection is made.

If you are putting MicroPython on your board for the first time then you should
first erase the entire flash using:

```bash
esptool.py --chip esp32c6 --port /dev/ttyUSB0 erase_flash
```

From then on program the firmware starting at address 0x0:

```bash
esptool.py --chip esp32c6 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x0 M5STACK_Unit_C6L-20250915-v1.25.0.bin
```

## Partition layout updates

Unit C6L uses `partitions_8mb_unit_c6l.csv`. The application partition is
`0x581000` bytes; the system filesystem starts at `0x591000` and has
`0x0c0000` bytes. The user filesystem retains its existing address
(`0x651000`) and size (`0x1ae000`).

When upgrading from the shared 8 MiB layout, flash a complete merged image
containing the updated partition table, application, and system filesystem.
Flashing only `micropython.bin` does not migrate the partition layout.
Use the image produced by `make BOARD=M5STACK_Unit_C6L pack` to retain an
existing user filesystem. The `pack_all` image includes an initialized user
filesystem and overwrites its contents when flashed.
