# Write up

The encryption works as follow:

First we rotate the **lowercase** letters `X` number of times, by a random ammount each time. But overall result is rotating the whole thing by a constant `C`.

After that, we encode the thing en base64, and then we set `cipher[i] = cipher[i] ^ cipher[(i+1)%len(cipher)]`

To reverse this operation, one needs to notice that the base64 cipher after the first encryption (the rotations) contains the `\n` character at the end. So basically we know the last byte of the cipher before the `xor` encryption.

Therefore we can recover the cipher before the `xor` operations, doing some `xor` operations.

After that, we only need to rotate the string with all possible offsets, and recover the flag.

```
import base64
from z3 import *

cipher = "MRU2FDcePBQlPwAdVXo5ElN3MDwMNURVDCc9PgwPORJTdzATN2wAN28="
cipher = base64.b64decode(cipher)

last = 10

pong = [0] * len(cipher)
pong[-1] = ord('\n')

for i in range(len(cipher) - 2, -1, -1):
    pong[i] = pong[i+1] ^ cipher[i]

pong = ''.join(map(chr, pong))

string = "y00q2ollq{Blka. Jxjbp Blka.}"

def rot(s, num):
	l=""
	for i in s:
		if(ord(i) in range(97,97+26)):
			l+=chr((ord(i)-97+num)%26+97)
		else:
			l+=i
	return l

for i in range(27):
    print(rot(string, i))
```

```
b00t2root{Bond. James Bond.}
```