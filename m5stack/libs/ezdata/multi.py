import time
import os


class MultiPartForm:
    def __init__(self) -> None:
        self.fields = []
        self.files = []
        self.boundary = str(time.time())

    def content_type(self):
        return "multipart/form-data; boundary=%s" % self.boundary

    def add_field(self, name, value):
        self.fields.append((name, value))

    def add_file(self, field, filename, mimetype=None):
        file_size = os.stat(filename)[6]
        if mimetype is None:
            mimetype = "application/octet-stream"
        self.files.append((field, filename, mimetype, file_size))

    def content_length(self):
        res = 0
        part_boundary = ("--" + self.boundary).encode()
        needs_CLRF = False
        for name, value in self.fields:
            if needs_CLRF:
                res += len(b"\r\n")
            needs_CLRF = True

            block = [
                part_boundary,
                ('Content-Disposition: form-data; name="%s"' % name).encode(),
                b"Content-Type: multipart/form-data",
                b"",
                value.encode(),
            ]
            res += len(b"\r\n".join(block))

        for field, filename, content_type, file_size in self.files:
            if needs_CLRF:
                res += len(b"\r\n")
            needs_CLRF = True

            block = [
                part_boundary,
                (
                    'Content-Disposition: form-data; name="%s"; filename="%s"' % (field, filename)
                ).encode(),
                ("Content-Type: %s" % content_type).encode(),
                b"",
            ]

            res += len(b"\r\n".join(block))
            res += len(b"\r\n")
            res += file_size
        res += len("\r\n--" + self.boundary + "--\r\n")
        return res

    def content(self):
        data = b""
        part_boundary = ("--" + self.boundary).encode()

        needs_CLRF = False
        for name, value in self.fields:
            if needs_CLRF:
                data += b"\r\n"
            needs_CLRF = True

            block = [
                part_boundary,
                ('Content-Disposition: form-data; name="%s"' % name).encode(),
                b"Content-Type: multipart/form-data",
                b"",
                value.encode(),
            ]

            data += b"\r\n".join(block)

        for field, filename, content_type, _ in self.files:
            if needs_CLRF:
                data += b"\r\n"
            needs_CLRF = True

            block = [
                part_boundary,
                (
                    'Content-Disposition: form-data; name="%s"; filename="%s"' % (field, filename)
                ).encode(),
                ("Content-Type: %s" % content_type).encode(),
                b"",
            ]

            data += b"\r\n".join(block)
            data += b"\r\n"

            with open(filename, "rb") as f:
                while True:
                    ch = f.read(1024)
                    if not ch:
                        break
                    data += ch

        data += ("\r\n--" + self.boundary + "--\r\n").encode()
        return data
