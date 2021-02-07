import socket
blocks = [
    'username=superad',  # P1
    'ministrator&pass',  # P2
    'word=$3cReT_p45S',  # P3
]

cipher = [
    b'\xdc\xc4`G\xe0\xf7\xb1|\x82VK\x89-\xed\x02\xf1',  # C1
    b'\xae\t\x01\xd6)`\n\xe6\xcf\xf7\x0c+N_3c',  # C2
]


def connect(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    return s


def xor(s, t):
    assert(len(s) == len(t))
    return b''.join([bytes([x ^ y]) for x, y in zip(s, t)])


s = connect('144.202.8.144', 5768)


plaintext = blocks[0].encode() + blocks[1].encode() + \
    xor(cipher[0], xor(cipher[1], blocks[1].encode())) + \
    blocks[2].encode()

print(plaintext)

msg = b'Enc ' + plaintext + b'\n'


# s.send(msg) # send it to the server to obtain ciphertext

# Aca ya obtuve el resultado
la_posta = b'Login \xdc\xc4`G\xe0\xf7\xb1|\x82VK\x89-\xed\x02\xf1\xae\t\x01\xd6)`\n\xe6\xcf\xf7\x0c+N_3c\xf8\xc5\xc63\x1aq\x03Q.\x94Pi\x8ao\xa6O\n'

s.send(la_posta)

print(s.recv(1024))
