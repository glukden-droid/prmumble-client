# Dumps PRMumble 1.3 shortcuts from HKCU\SOFTWARE\Project Reality\PR Mumble\shortcuts
# (what the PR launcher reads). Values are Qt QSettings "@Variant(...)" strings,
# stored as REG_BINARY UTF-16 when they contain zero bytes; inside is a
# QDataStream (Qt_4_0) QVariant.
#   python pr_shortcuts.py
import struct
import sys
import winreg

KEY = r"SOFTWARE\Project Reality\PR Mumble\shortcuts"


def variant_bytes(raw):
    if isinstance(raw, bytes):
        s = raw.decode("utf-16-le")
    else:
        s = raw
    if not s.startswith("@Variant(") or not s.endswith(")"):
        return None
    return s[9:-1].encode("latin-1")


class Reader:
    def __init__(self, b):
        self.b, self.o = b, 0

    def take(self, n):
        v = self.b[self.o:self.o + n]
        self.o += n
        return v

    def u8(self):
        return self.take(1)[0]

    def u32(self):
        return struct.unpack(">I", self.take(4))[0]

    def i32(self):
        return struct.unpack(">i", self.take(4))[0]

    def qstring(self):
        n = self.u32()
        if n == 0xFFFFFFFF:
            return None
        return self.take(n).decode("utf-16-be")

    def variant(self):
        t = self.u32()  # Qt_4_0 stream: no is-null byte
        if t == 3:
            return self.u32()
        if t == 9:
            return [self.variant() for _ in range(self.u32())]
        if t == 10:
            return self.qstring()
        if t == 1:
            return bool(self.u8())
        if t == 2:
            return self.i32()
        if t == 127:
            name = self.take(self.u32()).rstrip(b"\0").decode()
            if name == "ShortcutTarget":
                return self.shortcut_target()
            raise ValueError("user type " + name)
        raise ValueError("type %d" % t)

    def shortcut_target(self):
        # Mumble 1.3 layout (no "v2" prefix)
        st = {"users": bool(self.u8()), "forceCenter": bool(self.u8())}
        if st["users"]:
            st["list"] = [self.qstring() for _ in range(self.u32())]
        else:
            st["channel"] = self.i32()
            st["group"] = self.qstring()
            st["links"] = bool(self.u8())
            st["children"] = bool(self.u8())
        return st


def main():
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY)
    size = winreg.QueryValueEx(k, "size")[0]
    for i in range(1, size + 1):
        try:
            sk = winreg.OpenKey(k, str(i))
        except OSError:
            continue
        vals = {}
        for name in ("index", "keys", "data", "suppress"):
            try:
                vals[name] = winreg.QueryValueEx(sk, name)[0]
            except OSError:
                vals[name] = None
        out = {"index": vals["index"], "suppress": vals["suppress"]}
        for name in ("keys", "data"):
            b = variant_bytes(vals[name]) if isinstance(vals[name], (bytes, str)) else None
            if b is None:
                out[name] = vals[name]
                continue
            r = Reader(b)
            out[name] = r.variant()
            if r.o != len(b):
                out[name + "_rest"] = b[r.o:].hex()
        print(i, out)


if __name__ == "__main__":
    sys.exit(main())
