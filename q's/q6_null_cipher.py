def null_cipher_hide(cover_text, secret, every_m_words=3, take_char_index=1):
    words = cover_text.split()
    s_idx = 0
    for i in range(every_m_words - 1, len(words), every_m_words):
        if s_idx >= len(secret):
            break
        w = words[i]
        if len(w) <= take_char_index:
            w += "." * (take_char_index + 1 - len(w))
        w = w[:take_char_index] + secret[s_idx] + w[take_char_index + 1:]
        words[i] = w
        s_idx += 1
    return " ".join(words)

def null_cipher_reveal(cover_text, every_m_words=3, take_char_index=1):
    words = cover_text.split()
    return "".join(w[take_char_index] for i, w in enumerate(words) if (i+1) % every_m_words == 0 and len(w) > take_char_index)
