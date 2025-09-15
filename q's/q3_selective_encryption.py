import re, base64

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))

def encrypt_sensitive(text, patterns, key):
    def repl(m):
        enc = xor_bytes(m.group(0).encode(), key.encode())
        return f"ENC({base64.b64encode(enc).decode()})"
    return re.sub("|".join(patterns), repl, text)

def decrypt_sensitive(text, key):
    def repl(m):
        raw = base64.b64decode(m.group(1))
        return xor_bytes(raw, key.encode()).decode(errors="replace")
    return re.sub(r"ENC\(([^)]+)\)", repl, text)
