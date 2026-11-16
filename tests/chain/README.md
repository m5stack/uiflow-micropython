# Chain sensor protocol tests

Run from the repository root with CPython:

```sh
python3 tests/chain/test_sensor_protocols.py
```

The tests cover DLight, ENV and IMU command bytes, units, range validation,
event callbacks, shared RGB and identity methods, and Chain frame checksums.
They use a simulated bus and do not require attached devices.

The existing Pedal implementation and examples are maintained by the base
branch and are outside this test suite. Hardware behavior requires device
testing.
