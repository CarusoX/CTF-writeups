# Write up

In this challenge we were given a ciphertext which was encrypted from 1 to 20 times
using either base64 or hex encodings picked randomly

Also the problem is that the flag of length 22 was cut in half, and we computed the xor of the two parts. Luckily for us, as we know that `b00t2root{` has length 10 and `}` is at the end, we can recover the remaining letters if we know the first ciphertext.

To recover it, we just compute all possibilities, but we drop the ones that are not possible

```

def recover(msg):

    msg = msg.decode('hex')

    if(len(msg) != 11): return

    dec = ['b','0','0','t','2','r','o','o','t','{','*','*','*','*','*','*','*','*','*','*','*','}']
    dec[10] = chr(ord('}') ^ ord(msg[10]))
    for i in range(11, 21):
        dec[i] = chr(ord(msg[i-11]) ^ ord(dec[i-11]))
    print ''.join(dec)

def doit(lvl, msg):
    if(lvl == 0):
        recover(msg)
        return

    try: doit(lvl - 1, msg.decode('hex'))
    except: pass

    try: doit(lvl - 1, msg.decode('base64'))
    except: pass

f = open('chall.txt', 'r').read()

for i in range(1, 21): doit(i, f)
```

```
b00t2root{fantasticcc}
```