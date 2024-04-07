import bluetooth
from micropython import const
import struct
import gc
import time
import _thread

_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)
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
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)

event_strings = [
    "",
    "CENTRAL_CONNECT",
    "CENTRAL_DISCONNECT",
    "GATTS_WRITE",
    "GATTS_READ_REQUEST",
    "SCAN_RESULT",
    "SCAN_DONE",
    "PERIPHERAL_CONNECT",
    "PERIPHERAL_DISCONNECT",
    "GATTC_SERVICE_RESULT",
    "GATTC_SERVICE_DONE",
    "GATTC_CHARACTERISTIC_RESULT",
    "GATTC_CHARACTERISTIC_DONE",
    "GATTC_DESCRIPTOR_RESULT",
    "GATTC_DESCRIPTOR_DONE",
    "GATTC_READ_RESULT",
    "GATTC_READ_DONE",
    "GATTC_WRITE_DONE",
    "GATTC_NOTIFY",
    "GATTC_INDICATE",
    "GATTS_INDICATE_DONE",
    "MTU_EXCHANGED",
    "L2CAP_ACCEPT",
    "L2CAP_CONNECT",
    "L2CAP_DISCONNECT",
    "L2CAP_RECV",
    "L2CAP_SEND_READY",
    "CONNECTION_UPDATE",
    "ENCRYPTION_UPDATE",
    "GET_SECRET",
    "SET_SECRET",
]

_ADV_IND = const(0x00)
_ADV_DIRECT_IND = const(0x01)
_ADV_SCAN_IND = const(0x02)
_ADV_NONCONN_IND = const(0x03)

_FLAG_BROADCAST = const(0x0001)
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)
_FLAG_AUTHENTICATED_SIGNED_WRITE = const(0x0040)

_FLAG_AUX_WRITE = const(0x0100)
_FLAG_READ_ENCRYPTED = const(0x0200)
_FLAG_READ_AUTHENTICATED = const(0x0400)
_FLAG_READ_AUTHORIZED = const(0x0800)
_FLAG_WRITE_ENCRYPTED = const(0x1000)
_FLAG_WRITE_AUTHENTICATED = const(0x2000)
_FLAG_WRITE_AUTHORIZED = const(0x4000)

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)

_STATE_NOT_DISCOVERED = const(0)
_STATE_DISCOVERED = const(1)


# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)),
    )

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    # See org.bluetooth.characteristic.gap.appearance.xml
    if appearance:
        _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

    return payload


def decode_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2 : i + payload[i] + 1])
        i += 1 + payload[i]
    return result


def decode_name(payload):
    n = decode_field(payload, _ADV_TYPE_NAME)
    return str(n[0], "utf-8") if n else ""


def decode_services(payload):
    services = []
    for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<h", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<d", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(u))
    return services


class Queue:
    def __init__(self):
        self.queue = []
        self.lock = _thread.allocate_lock()

    def put(self, item):
        with self.lock:
            self.queue.append(item)

    def get(self):
        with self.lock:
            if len(self.queue) == 0:
                return 0
            return self.queue.pop(0)


class Server:
    def __init__(self, parent, name, buf_size, verbose=False) -> None:
        self._verbose = verbose
        self._ble = parent._ble
        self._parent = parent
        self._connected_devices = set()
        self._rx_buffer = bytearray()
        self._payload = advertising_payload(name=name, appearance=_ADV_APPEARANCE_GENERIC_COMPUTER)
        self._buf_size = buf_size
        self._services = []
        self._value_handles = ()
        self._value_handle_map = {}
        self._recv_cb = None
        self._connected_cb = None
        self._disconnected_cb = None

    def clear_services(self):
        self._services.clear()

    def add_service(self, uuid, characteristics: list | tuple = None):
        self._services.append((bluetooth.UUID(uuid), characteristics))

    def create_characteristic(self, uuid, read=False, write=False, notify=False):
        return (
            bluetooth.UUID(uuid),
            bluetooth.FLAG_READ * read
            + bluetooth.FLAG_WRITE * write
            + bluetooth.FLAG_NOTIFY * notify,
        )

    def start(self, interval_us=500000):
        self._verbose and print(self._services)
        self._value_handles = self._ble.gatts_register_services(self._services)

        for i in range(len(self._services)):
            for j in range(len(self._services[i][1])):
                self._value_handle_map[self._services[i][1][j][0]] = self._value_handles[i][j]
        self._verbose and print(self._value_handle_map)

        self._start_advertising(interval_us)

    def on_receive(self, callback):
        self._recv_cb = callback

    def on_connected(self, callback):
        self._connected_cb = callback

    def on_disconnected(self, callback):
        self._disconnected_cb = callback

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, addr_type, addr = data
            client = self.Client(self, conn_handle, addr_type, addr)
            self._connected_devices.add(client)
            self._verbose and print("Device connected")
            try:
                self._parent._start_async_task(self._connected_cb, self, client)
            except:
                pass
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, addr_type, addr = data
            for client in self._connected_devices:
                if client.connect_handle == conn_handle:
                    self._verbose and print("Device disconnected")
                    self._connected_devices.remove(client)
                    try:
                        self._parent._start_async_task(self._disconnected_cb, self, client)
                    except:
                        pass
                    self._start_advertising()
                    break

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            for client in self._connected_devices:
                if client.connect_handle != conn_handle:
                    continue
                client._recv(value_handle)
                try:
                    self._parent._start_async_task(self._recv_cb, self, client)
                except:
                    pass
                break

    def get_client(self, index):
        return self._connected_devices[index]

    def get_clients(self):
        return self._connected_devices

    def _start_advertising(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    class Client:
        def __init__(self, server, connect_handle, addr_type, addr) -> None:
            self.connect_handle = connect_handle
            self.addr_type = addr_type
            self.addr = addr
            self.rx_buffers = {}
            self._server = server

        def _recv(self, handle):
            self.rx_buffers[handle] = self.rx_buffers.get(
                handle, b""
            ) + self._server._ble.gatts_read(handle)
            self._server._verbose and print(
                "Received data: ", self.rx_buffers[handle], " from ", handle
            )

        def _get_value_handle(self, uuid):
            value_handle = self._server._value_handle_map[bluetooth.UUID(uuid)]
            if not value_handle:
                self._verbose and print("Characteristic uuid ", uuid, " not found")
                raise ValueError("Characteristic uuid ", uuid, " not found")
            return value_handle

        def any(self, uuid):
            value_handle = self._get_value_handle(uuid)
            return len(self.rx_buffers.get(value_handle, b""))

        def read(self, uuid, sz=None):
            value_handle = self._get_value_handle(uuid)
            if not self.rx_buffers[value_handle]:
                return b""
            if not sz:
                sz = len(self.rx_buffers[value_handle])
            result = self.rx_buffers[value_handle][0:sz]
            self.rx_buffers[value_handle] = self.rx_buffers[value_handle][sz:]
            return result

        def write(self, data, uuid):
            value_handle = self._get_value_handle(uuid)
            self._server._ble.gatts_notify(self.connect_handle, value_handle, data)

        def close(self):
            self._server._ble.gap_disconnect(self.connect_handle)


class Client:
    def __init__(self, parent, verbose=False) -> None:
        self._verbose = verbose
        self._ble = parent._ble
        self._parent = parent
        self._scan_results = []
        self._reset()

    def _reset(self):
        self._server_conn_handle = None
        self._server_addr_type = None
        self._server_addr = None
        self._service_handle_map = {}
        self._discovering_uuid = None
        self.rx_buffers = {}
        self._current_service_uuid = None

    def on_connected(self, callback):
        self._connected_cb = callback

    def on_disconnected(self, callback):
        self._disconnected_cb = callback

    def on_server_found(self, callback):
        self._server_found_cb = callback

    def on_scan_finished(self, callback):
        self._scan_finished_cb = callback

    def on_read_complete(self, callback):
        self._read_complete_cb = callback

    def on_notify(self, callback):
        self._notify_cb = callback

    def scan(
        self, timeout=2000, connect_on_found=True, target_name_prefix="M5UiFlow", target_uuid=None
    ):
        self._target_name_prefix = target_name_prefix
        self._target_uuid = target_uuid
        self._connect_on_found = connect_on_found
        self._scan_results = []
        self._ble.gap_scan(timeout, 30000, 30000)

    def connect(self, addr_type, addr):
        self._server_addr_type = addr_type
        self._server_addr = bytes(addr)
        self._ble.gap_connect(addr_type, addr)

    def _extract_uuid_items(self, original_dict):
        extracted_items = {}
        for service_uuid, characteristics in original_dict.items():
            filtered_characteristics = {
                char_uuid: value
                for char_uuid, value in characteristics.items()
                if char_uuid not in ["start", "end", "state"] and char_uuid.startswith("UUID")
            }
            if filtered_characteristics:  # 如果有符合条件的特征，才添加到最终字典
                extracted_items[service_uuid] = filtered_characteristics
        return extracted_items

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type in (_ADV_IND, _ADV_DIRECT_IND):
                if self._target_name_prefix:
                    if not decode_name(adv_data).startswith(self._target_name_prefix):
                        return
                self._verbose and print(
                    "Found device %s at rssi %d, adv_type %d"
                    % (decode_name(adv_data), rssi, adv_type)
                )
                self._scan_results.append(
                    (decode_name(adv_data), addr_type, addr, adv_type, rssi, adv_data)
                )
                if self._connect_on_found:
                    self._ble.gap_scan(None)
                    self.connect(addr_type, addr)
                try:
                    self._parent._start_async_task(
                        self._server_found_cb, self, self._scan_results[-1]
                    )
                except:
                    pass

        elif event == _IRQ_SCAN_DONE:
            try:
                self._parent._start_async_task(self._scan_finished_cb, self, self._scan_results)
            except:
                pass

        elif event == _IRQ_PERIPHERAL_CONNECT:
            # A successful gap_connect().
            conn_handle, addr_type, addr = data
            if addr_type == self._server_addr_type and addr == self._server_addr:
                self._verbose and print("Connected to device, handle", conn_handle)
                self._server_conn_handle = conn_handle
                self._ble.gattc_discover_services(self._server_conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Disconnect (either initiated by us or the remote end).
            self._verbose and print("Device disconnect")
            conn_handle, addr_type, addr = data
            if conn_handle == self._server_conn_handle:
                try:
                    self._parent._start_async_task(
                        self._disconnected_cb, self, conn_handle, addr_type, addr
                    )
                except:
                    pass
                self._reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            self._verbose and print("GATTC service result")
            # Connected device returned a service.
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._server_conn_handle:
                self._verbose and print("Service found: ", uuid)
                self._service_handle_map[str(uuid)] = {
                    "start": start_handle,
                    "end": end_handle,
                    "state": _STATE_NOT_DISCOVERED,
                }

        elif event == _IRQ_GATTC_SERVICE_DONE:
            # Service query complete.
            self._verbose and print("GATTC service done")
            for key in self._service_handle_map:
                service = self._service_handle_map[key]
                if service["state"] == _STATE_NOT_DISCOVERED:
                    service["state"] = _STATE_DISCOVERED
                    self._discovering_uuid = key
                    self._ble.gattc_discover_characteristics(
                        self._server_conn_handle, service["start"], service["end"]
                    )
                    return

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Connected device returned a characteristic.
            conn_handle, def_handle, value_handle, properties, uuid = data
            self._verbose and print("Characteristic found: ", uuid, properties)
            self._service_handle_map[self._discovering_uuid][str(uuid)] = value_handle
            if properties & _FLAG_NOTIFY:
                self.rx_buffers[value_handle] = b""

        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            for key in self._service_handle_map:  # start discover again
                service = self._service_handle_map[key]
                if service["state"] == _STATE_NOT_DISCOVERED:
                    service["state"] = _STATE_DISCOVERED
                    self._discovering_uuid = key
                    self._ble.gattc_discover_characteristics(
                        self._server_conn_handle, service["start"], service["end"]
                    )
                    return
            # all characteristics discovered
            self._service_handle_map = self._extract_uuid_items(self._service_handle_map)
            try:
                self._parent._start_async_task(self._connected_cb, self)
            except:
                pass

        elif event == _IRQ_GATTC_READ_RESULT:
            # A read completed successfully.
            conn_handle, value_handle, char_data = data
            if conn_handle == self._server_conn_handle:
                try:
                    self._parent._start_async_task(
                        self._read_complete_cb, self, conn_handle, value_handle, char_data
                    )
                except:
                    pass

        elif event == _IRQ_GATTC_READ_DONE:
            # Read completed (no-op).
            conn_handle, value_handle, status = data

        elif event == _IRQ_GATTC_NOTIFY:
            # The ble_temperature.py demo periodically notifies its value.
            conn_handle, value_handle, notify_data = data
            self._verbose and print("GATTC notify %d" % value_handle)
            if conn_handle == self._server_conn_handle:
                self.rx_buffers[value_handle] = (
                    self.rx_buffers.get(value_handle, b"") + notify_data
                )
                try:
                    self._parent._start_async_task(self._notify_cb, self)
                except:
                    pass

    def _get_value_handle(self, character_uuid, service_uuid=None):
        if not service_uuid:
            service_uuid = self._current_service_uuid
        if not service_uuid:
            raise ValueError("Service not set")

        try:
            value_handle = self._service_handle_map[str(bluetooth.UUID(service_uuid))][
                str(bluetooth.UUID(character_uuid))
            ]
            if not value_handle:
                raise ValueError("Characteristic not found")
        except:
            raise ValueError("Characteristic not found")
        return value_handle

    def set_current_service_uuid(self, service_uuid):
        self._current_service_uuid = service_uuid

    def any(self, uuid, service_uuid=None):
        value_handle = self._get_value_handle(uuid, service_uuid)
        return len(self.rx_buffers.get(value_handle, b""))

    def read(self, uuid, service_uuid=None, sz=None):
        value_handle = self._get_value_handle(uuid, service_uuid)
        if not self.rx_buffers[value_handle]:
            return b""
        if not sz:
            sz = len(self.rx_buffers[value_handle])
        result = self.rx_buffers[value_handle][0:sz]
        self.rx_buffers[value_handle] = self.rx_buffers[value_handle][sz:]
        return result

    def write(self, data, uuid, service_uuid=None):
        value_handle = self._get_value_handle(uuid, service_uuid)
        self._ble.gattc_write(self._server_conn_handle, value_handle, data)

    def close(self):
        if not self._server_conn_handle:
            return
        self._ble.gap_disconnect(self._server_conn_handle)
        self._reset()

    def get_services(self):
        return self._service_handle_map.keys()

    def get_characteristics(self, service_uuid):
        return self._service_handle_map[service_uuid].keys()

    def set_mtu(self, mtu):
        self._ble.config(mtu=mtu)
        self._ble.gattc_exchange_mtu(self._server_conn_handle)


class Device:
    def __init__(self, name="M5UiFlow", buf_size=100, verbose=False) -> None:
        self._verbose = verbose
        self._ble = self._ble = bluetooth.BLE()
        self.client = Client(self, verbose)
        self.server = Server(self, name, buf_size, verbose)
        self._ble.active(True)
        self._mtu = self._ble.config("mtu")
        self._ble.irq(self._ble_irq)

        self._cb_queue = Queue()
        self._async_worker_run = True
        self._async_worker_exit_flag = False
        _thread.start_new_thread(self._async_worker, ())

    def _ble_irq(self, event, data):
        self._verbose and print("event: (%d)%s" % (event, event_strings[event]))

        if event == _IRQ_MTU_EXCHANGED:
            # ATT MTU exchange complete (either initiated by us or the remote device).
            conn_handle, mtu = data
            self._verbose and print("MTU exchanged: %d" % mtu)
            self._mtu = mtu

        else:
            self.server._irq(event, data)
            self.client._irq(event, data)

    def get_mtu(self):
        return self._mtu

    def deinit(self):
        self._stop_async_worker()
        self._ble.active(False)

    def _start_async_task(self, callback, *args, **kwargs):
        if callback is None:
            return
        self._cb_queue.put((callback, args, kwargs))

    def _stop_async_worker(self):
        self._async_worker_exit_flag = False
        self._async_worker_run = False
        self._cb_queue.put(None)  # Ensure the worker loop can exit if it's waiting on the queue.
        while not self._async_worker_exit_flag:  # Wait for the worker to exit
            time.sleep(0.1)

    def _async_worker(self):
        while self._async_worker_run:
            task = self._cb_queue.get()
            if task == 0:
                time.sleep(0.1)
                continue
            if task is None:
                self._verbose and print("Exiting async worker")
                # None is used as a signal to stop the worker
                break
            callback, args, kwargs = task
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print("Error executing task:", e)
        gc.collect()
        self._async_worker_exit_flag = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()
