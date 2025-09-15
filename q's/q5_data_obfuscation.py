import random

def obfuscate_phone(phone, seed=1337):
    rnd = random.Random(seed + sum(ord(c) for c in phone))
    noisy = []
    for ch in phone:
        noisy.append(ch)
        for _ in range(rnd.randint(0, 2)):
            noisy.append(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ"))
    return "".join(noisy)

def deobfuscate_phone(obf, original_length):
    digits = [c for c in obf if c.isdigit()]
    return "".join(digits)[:original_length]
