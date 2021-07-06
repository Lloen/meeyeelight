from Crypto.Cipher import AES
from binascii import unhexlify, hexlify
from hashlib import md5

def decrypt(cipher, token):
    key = get_md5(unhexlify(token))
    pre_iv = str(key) + str(token)
    iv = get_md5(unhexlify(pre_iv))
    aes = AES.new(unhexlify(key), AES.MODE_CBC, unhexlify(iv))
    message = aes.decrypt(unhexlify(cipher))
    padding_bytes = message[-1]
    return message[:-padding_bytes]

def encrypt(message, token):
    def pad(m):
        return m+chr(16-len(m)%16)*(16-len(m)%16)
    key = get_md5(unhexlify(token))
    pre_iv = str(key) + str(token)
    iv = get_md5(unhexlify(pre_iv))
    aes = AES.new(unhexlify(key), AES.MODE_CBC, unhexlify(iv))
    return aes.encrypt(pad(message))

def get_md5(message):
    return md5(message).hexdigest()
