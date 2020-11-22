from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import bcrypt
import os

def encrypt_flag(flag, key):
    kdf_salt = os.urandom(16)
    aad = os.urandom(16)
    key = PBKDF2(key, kdf_salt)
    
    hflag = bcrypt.hashpw(flag.encode(), bcrypt.gensalt())

    cipher = AES.new(key, AES.MODE_GCM)
    cipher.update(aad)
    ciphertext, tag = cipher.encrypt_and_digest(hflag)
    nonce = cipher.nonce

    return f"{kdf_salt.hex()},{aad.hex()},{nonce.hex()},{ciphertext.hex()},{tag.hex()}"

def decrypt_flag(enc_flag, key):
    kdf_salt, aad, nonce, ciphertext, tag = enc_flag.split(",")

    kdf_salt = bytes.fromhex(kdf_salt)
    aad = bytes.fromhex(aad)
    nonce = bytes.fromhex(nonce)
    ciphertext = bytes.fromhex(ciphertext)
    tag = bytes.fromhex(tag)

    key = PBKDF2(key, kdf_salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    cipher.update(aad)

    try:
        return cipher.decrypt_and_verify(ciphertext, tag).decode()
    except ValueError:
        return None

if __name__ == '__main__':
    key = "test"
    flag = "flag{hello_ja}"
    enc_flag = encrypt_flag(flag, key)
    print(f"Enc Flag: {enc_flag}")
    hflag = decrypt_flag(enc_flag, key)
    print(f"Hashed Flag: {hflag}")

    assert bcrypt.checkpw(flag.encode(), hflag.encode()), "Fail"
