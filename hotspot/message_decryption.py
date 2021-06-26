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

if __name__ == "__main__":
    decrypt('f7c3ddc5431ec7b7a5eaf03a8659e6e19c0d1cc5d09d5136c52f0a3b897881dea776e5a94d69e12e1da18fc51d6054e7', '6615d80df9d8732350d9716b2becef6c')