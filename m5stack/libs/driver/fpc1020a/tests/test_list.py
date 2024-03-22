# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class int_t(int):
    _signed = True
    _size = 0

    def serialize(self, byteorder="big"):
        return self.to_bytes(self._size, byteorder)

    @classmethod
    def deserialize(cls, data, byteorder="big"):
        # Work around https://bugs.python.org/issue23640
        r = cls(int.from_bytes(data[: cls._size], byteorder))
        data = data[cls._size :]
        return r, data


class uint_t(int_t):
    _signed = False


class uint8_t(uint_t):
    _size = 1


class LVList(list):
    _item_type = None
    _length_type = uint8_t

    _getitem_kwargs = {"item_type": None, "length_type": uint8_t}

    _anonymous_classes = {}  # type:ignore[var-annotated]

    def serialize(self) -> bytes:
        assert self._item_type is not None
        return self._length_type(len(self)).serialize() + b"".join(
            [self._item_type(i).serialize() for i in self]
        )

    @classmethod
    def deserialize(cls, data: bytes):
        assert cls._item_type is not None
        length, data = cls._length_type.deserialize(data)
        r = cls()
        for i in range(length):
            item, data = cls._item_type.deserialize(data)
            r.append(item)
        return r, data

    def __new__(metaclass, name, bases, namespaces, **kwargs):
        cls_kwarg_attrs = namespaces.get("_getitem_kwargs", {})

        def __init_subclass__(cls, **kwargs):
            filtered_kwargs = kwargs.copy()

            for name, value in kwargs.items():
                if name in cls_kwarg_attrs:
                    setattr(cls, f"_{name}", filtered_kwargs.pop(name))

            super().__init_subclass__(**filtered_kwargs)

        if "__init_subclass__" not in namespaces:
            namespaces["__init_subclass__"] = __init_subclass__

        return type.__new__(metaclass, name, bases, namespaces, **kwargs)


r, d = LVList[uint8_t, uint8_t].deserialize(b"\x12\x34")
print(r)
print(d)
