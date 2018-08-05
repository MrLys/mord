from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha512
import secrets
import string
import base64

# Derived from:
# https://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python
# To make this openssl compatible, this function tries to mimic:
# https://www.openssl.org/docs/manmaster/man3/generate_key_and_iv.html
def generate_key_and_iv(pwd, salt, key_len, iv_len):
    '''
    Derive the key and the IV from the given pwd and salt.
    '''
    pwd = pwd.encode('ascii','ignore')
    pwd_dgs = sha512(pwd + salt).digest()
    tmp_dgs = [ pwd_dgs ]
    while len(pwd_dgs)<(iv_len+key_len):
        tmp_dgs.append( sha512(d[-1] + pwd + salt).digest() )
        pwd_dgs += tmp_dgs[-1]
    return pwd_dgs[:key_len], pwd_dgs[key_len:key_len+iv_len]
# Decrypt by openssl standard.
# The first 8 bytes should be 'Salted__' followed by the 8 byte salt.
def decrypt(data,pwd):
    raw = base64.b64decode(data)
    assert(raw[:8] == b'Salted__')
    salt = raw[8:16]
    key, iv = generate_key_and_iv(pwd, salt, 32,16)
    ct = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_p = cipher.decrypt(ct)
    # The pt is padded with the value of padding*padding at the
    # end, and is therefor not part of the actual plaintext(pt)
    padding = pt_p[-1]
    pt = pt_p[:-padding]
    return pt

def generate_salt():
    # Secure per https://docs.python.org/3/library/secrets.html
    # Needs some research
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(8))

# Encrypt by openssl standard.
# openssl pwdmanager openssl enc  -aes-256-cbc -md sha512 -a -in <input file> \
# -out <output file>
def encrypt(data, pwd):
    salt =  generate_salt().encode('ascii')
    key, iv = generate_key_and_iv(pwd, salt, 32, 16)
    encrypt_suite = AES.new(key, AES.MODE_CBC, iv)

    # PKCS#7 padding
    data = str(data).encode('ascii')
    padding =  16 - (len(data) % 16)
    ct = encrypt_suite.encrypt(pad(data, AES.block_size))
    salted_ct = 'Salted__'.encode('ascii') + salt + ct
    encoded_cipher = base64.b64encode(salted_ct)
    return encoded_cipher

if __name__ == '__main__':
    print('This is only a library, import and call the wanted functions!')
