from q1_obfuscation import sum_of_squares_readable, _O0O0
from q3_selective_encryption import encrypt_sensitive, decrypt_sensitive
from q4_access_control import User, Resource, can_access
from q5_data_obfuscation import obfuscate_phone, deobfuscate_phone
from q6_null_cipher import null_cipher_hide, null_cipher_reveal
from q7_filtering_input import validate_username, validate_password
from q8_hashing import sha256_hex
from q9_chaffing_winnowing import chaff_message, winnow
from q10_metadata_encryption import encrypt_metadata, decrypt_metadata

def demo():
    print("Q1:", sum_of_squares_readable([1,2,3]), _O0O0([1,2,3]))

    text = "Card 4580-1234-5678-9999, ID 123456789"
    enc = encrypt_sensitive(text, [r"\d{4}-\d{4}-\d{4}-\d{4}", r"\d{9}"], "k")
    print("Q3:", enc, "->", decrypt_sensitive(enc, "k"))

    admin = User("alice", ["admin"])
    res = Resource("panel", ["admin"])
    print("Q4:", can_access(admin, res))

    obf = obfuscate_phone("0541234567")
    print("Q5:", obf, "->", deobfuscate_phone(obf, 10))

    cover = "זה טקסט כיסוי עם הרבה מילים להדגמה פשוטה מאוד"
    hidden = null_cipher_hide(cover, "סוד")
    print("Q6:", hidden, "->", null_cipher_reveal(hidden))

    print("Q7:", validate_username("Arad_1"), validate_password("GoodPass123!"))

    print("Q8:", sha256_hex("hello"))

    pkts = chaff_message("secret", "k")
    print("Q9:", winnow(pkts, "k"))

    doc = {"data": "public", "metadata": {"author": "Arad"}}
    enc_doc = encrypt_metadata(doc, "k")
    print("Q10:", decrypt_metadata(enc_doc, "k"))

if __name__ == "__main__":
    demo()
