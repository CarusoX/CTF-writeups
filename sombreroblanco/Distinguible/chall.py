#!/usr/bin/env python3

from Crypto.Cipher import AES

admin = b'username=superadministrator&password=$3cReT_p45S'

with open('iv.txt', 'rb') as f:
    IV = f.read()

with open('key.txt', 'rb') as f:
    KEY = f.read()

with open('flag.txt', 'r') as f:
    FLAG = f.read()


def chall(cmd, data):
    aes = AES.new(KEY, AES.MODE_CBC, IV)

    if cmd == 'Enc':
        if admin in data:
            return b'Mal hacker, no hay cerveza para ti'

        else:
            C = aes.encrypt(data)
            return C

    elif cmd == 'Login':
        P = aes.decrypt(data)
        if P == admin:
            return FLAG.encode()

        else:
            return b'Credenciales incorrectas'

    else:
        return b'???'

