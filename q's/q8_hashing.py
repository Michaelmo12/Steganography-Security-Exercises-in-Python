import hashlib

def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()
