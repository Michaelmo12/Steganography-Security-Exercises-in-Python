import os, random, hashlib, hmac

def chaff_message(message, key, chaff_ratio=1.0):
    packets = []
    k = key.encode()
    for i, ch in enumerate(message):
        tag = hmac.new(k, f"{i}:{ch}".encode(), hashlib.sha256).hexdigest()
        packets.append((i, ch, tag))

    n_chaff = int(len(message) * chaff_ratio)
    for _ in range(n_chaff):
        i = random.randint(0, len(message))
        ch = random.choice("abcdefghijklmnopqrstuvwxyz ")
        bad_tag = hashlib.sha256(os.urandom(16)).hexdigest()
        packets.append((i, ch, bad_tag))

    random.shuffle(packets)
    return packets

def winnow(packets, key):
    k = key.encode()
    valid = []
    for i, ch, tag in packets:
        good = hmac.new(k, f"{i}:{ch}".encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(good, tag):
            valid.append((i, ch))
    valid.sort(key=lambda t: t[0])
    return "".join(ch for _, ch in valid)
