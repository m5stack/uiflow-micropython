def deserialize(data, schema):
    result = []
    for type_ in schema:
        # value, data = type_.deserialize(data)
        if data:
            value, data = type_.deserialize(data)
        else:
            value = None
        result.append(value)
    return result, data

def serialize(data, schema):
    return b''.join(t(v).serialize() for t, v in zip(schema, data))

class Bytes(bytes):
    def serialize(self):
        return self

    @classmethod
    def deserialize(cls, data):
        return cls(data), b''

class int_t(int):
    _signed = True
    _size = 0

    def serialize(self, byteorder='big'):
        return self.to_bytes(self._size, byteorder)

    @classmethod
    def deserialize(cls, data, byteorder='big'):
        # Work around https://bugs.python.org/issue23640
        r = cls(int.from_bytes(data[:cls._size], byteorder))
        data = data[cls._size:]
        return r, data

class uint_t(int_t):
    _signed = False

class uint8_t(uint_t):
    _size = 1

class uint16_t(uint_t):
    _size = 2
