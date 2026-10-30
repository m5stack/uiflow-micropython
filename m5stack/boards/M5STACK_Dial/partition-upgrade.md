# Dial partition layout upgrade

Dial uses `partitions_8mb_dial.csv`: the application has `0x660000` bytes,
and the system filesystem starts at `0x670000` with `0x0d0000` bytes.
The user filesystem stays at `0x740000` with `0x0c0000` bytes.

Upgrade with a complete merged firmware containing the partition table,
application and system filesystem. Flashing only `micropython.bin` does
not migrate the layout. Use `make BOARD=M5STACK_Dial pack` to generate an
upgrade image that leaves the existing user filesystem untouched.
`pack_all` includes a new user filesystem and overwrites existing files.
