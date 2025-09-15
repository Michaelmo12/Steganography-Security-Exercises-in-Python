import base64

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(d ^ key[i % len(key)] for i, d in enumerate(data))

def encrypt_metadata(record, key):
    meta = str(record.get("metadata", {})).encode()
    enc = xor_bytes(meta, key.encode())
    record["metadata"] = {"enc_b64": base64.b64encode(enc).decode()}
    return record

def decrypt_metadata(record, key):
    meta = record.get("metadata", {})
    if "enc_b64" not in meta:
        return record
    enc = base64.b64decode(meta["enc_b64"])
    dec = xor_bytes(enc, key.encode()).decode(errors="replace")
    record["metadata"] = dec
    return record
