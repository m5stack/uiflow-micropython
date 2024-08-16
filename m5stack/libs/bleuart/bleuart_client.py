# Copyright (c) 2024 M5Stack Technology CO LTD

import bluetooth
from micropython import const
from .ble_advertising import decode_services, decode_name

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_WRITE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLEUARTClient:
    def __init__(self, verbose=False):
        self._verbose = verbose
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._rx_buffer = bytearray()
        self._reset()

    def _reset(self):
        # Cached name and address from a successful scan.
        self._name = None
        self._addr_type = None
        self._addr = None

        # Cached value (if we have one)
        self._value = None

        # Callbacks for completion of various operations.
        # These reset back to None after being invoked.
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None

        # Persistent callback for when new data is notified from the device.
        self._handler = None

        # Connected device.
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._rx_handle = None
        self._tx_handle = None

    def irq(self, handler):
        self._handler = handler

    def _irq(self, event, data):
        self._verbose and print(event)
        if event == _IRQ_SCAN_RESULT:
            self._verbose and print("Scan result")
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND) and decode_name(adv_data) == self._name:
                # Found a potential device, remember it and stop scanning.
                self._addr_type = addr_type
                self._addr = bytes(
                    addr
                )  # Note: addr buffer is owned by caller so need to copy it.
                self._name = decode_name(adv_data) or "?"
                self._ble.gap_scan(None)

        elif event == _IRQ_SCAN_DONE:
            self._verbose and print("Scan done")
            # if self._scan_callback:
            if self._addr:
                # Found a device during the scan (and the scan was explicitly stopped).
                # self._scan_callback(self._addr_type, self._addr, self._name)
                # self._scan_callback = None
                self._ble.gap_connect(self._addr_type, self._addr)
            else:
                # Scan timed out.
                # self._scan_callback(None, None, None)
                pass

        elif event == _IRQ_PERIPHERAL_CONNECT:
            # Connect successful.
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Disconnect (either initiated by us or the remote end).
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                # If it was initiated by us, it'll already be reset.
                self._reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            self._verbose and print("GATTC service result")
            # Connected device returned a service.
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._conn_handle and uuid == _UART_UUID:
                self._start_handle, self._end_handle = start_handle, end_handle

        elif event == _IRQ_GATTC_SERVICE_DONE:
            self._verbose and print("GATTC service done")
            # Service query complete.
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )
            else:
                self._verbose and print("Failed to find nordic uart service.")

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Connected device returned a characteristic.
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _UART_RX_UUID:
                self._rx_handle = value_handle
            if conn_handle == self._conn_handle and uuid == _UART_TX_UUID:
                self._tx_handle = value_handle

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            # Characteristic query complete.
            if self._rx_handle:
                # We've finished connecting and discovering device, fire the connect callback.
                if self._conn_callback:
                    self._conn_callback()
            else:
                self._verbose and print("Failed to find temperature characteristic.")

        elif event == _IRQ_GATTC_READ_RESULT:
            # A read completed successfully.
            conn_handle, value_handle, char_data = data
            if conn_handle == self._conn_handle and value_handle == self._rx_handle:
                self._update_value(char_data)
                if self._read_callback:
                    self._read_callback(self._value)
                    self._read_callback = None

        elif event == _IRQ_GATTC_READ_DONE:
            # Read completed (no-op).
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            self._verbose and print("GATTC notify")
            # The ble_temperature.py demo periodically notifies its value.
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle and value_handle == self._tx_handle:
                self._rx_buffer += notify_data
                if self._handler:
                    self._handler(self._value)

    # Returns true if we've successfully connected and discovered characteristics.
    def is_connected(self):
        return (
            self._conn_handle is not None
            and self._rx_handle is not None
            and self._tx_handle is not None
        )

    # Find a device advertising the environmental sensor service.
    # def scan(self, callback=None):
    #     self._addr_type = None
    #     self._addr = None
    #     self._scan_callback = callback
    #     self._ble.gap_scan(2000, 30000, 30000)

    # # Connect to the specified device (otherwise use cached address from a scan).
    # def connect(self, addr_type=None, addr=None, callback=None):
    #     self._addr_type = addr_type or self._addr_type
    #     self._addr = addr or self._addr
    #     self._conn_callback = callback
    #     if self._addr_type is None or self._addr is None:
    #         return False
    #     self._ble.gap_connect(self._addr_type, self._addr)
    #     return True

    def connect(self, name, timeout=2000):
        self._name = name
        self._addr_type = None
        self._addr = None
        self._ble.gap_scan(timeout, 30000, 30000)

    def any(self):
        return len(self._rx_buffer)

    def read(self, sz=None):
        if not sz:
            sz = len(self._rx_buffer)
        result = self._rx_buffer[0:sz]
        self._rx_buffer = self._rx_buffer[sz:]
        return result

    def readline(self, max_size=-1):
        if max_size == -1:
            max_size = 16
        while True:
            if b"\n" in self._rx_buffer:
                pos = self._rx_buffer.index(b"\n") + 1
                result = self._rx_buffer[0:pos]
                self._rx_buffer = self._rx_buffer[pos:]
                return result
            if len(self._rx_buffer) >= max_size:
                result = self._rx_buffer[0:max_size]
                self._rx_buffer = self._rx_buffer[max_size:]
                return result

    def write(self, data):
        if not self.is_connected():
            return
        self._ble.gattc_write(self._conn_handle, self._rx_handle, data)

    # Disconnect from current device.
    def close(self):
        if not self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    def deinit(self):
        self._ble.active(False)
