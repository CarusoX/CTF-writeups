# Distinguible

Codigo del challenge
```
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


```

La idea del challenge es proveer un texto encriptado,
tal que, una vez decriptado sea exactamente igual a `username=superadministrator&password=$3cReT_p45S`.

Las cosas que sabemos gracias al codigo son:

- Usamos AES en modo CBC
- IV y KEY podrian ser distintos
- Tenemos la posibilidad de encriptar casi cualquier plaintext que queramos

La complicacion surge justamente de que no podemos mandar el string `username=superadministrator&password=$3cReT_p45S` tal cual.

Vayamos resolviendo de a partes entonces. Primero tenemos que entender bien como funciona CBC (se puede leer algo [aqui](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)))

Lo importante es entender que se va encriptando bloque por bloque la informacion, pero justamente la encriptacion del bloque actual, depende de la del anterior (en el caso del primer bloque, depende del IV). En formulas seria algo como
```
C1 = E(P1 ^ IV) // E es la funcion que hace la magia en AES (depende de la KEY)
C2 = E(P2 ^ C1)
C3 = E(P3 ^ C2)
...
```

Otra cosa importante, es saber que los bloques en este caso son de 16 bytes, asi que podriamos dividir nuestro "objetivo" en tres partes justamente (cada una de 16 letras).

```
P1 = username=superad
P2 = ministrator&pass
P3 = word=$3cReT_p45S
```

Como primera instancia, podemos enviarle al servicio de encriptacion, solo los dos primeros bloques. Es decir mandamos

```
Enc username=superadministrator&pass
```

Y recibiremos el texto encriptado de esa parte

```
\xdc\xc4`G\xe0\xf7\xb1|\x82VK\x89-\xed\x02\xf1\xae\t\x01\xd6)`\n\xe6\xcf\xf7\x0c+N_3c

// Por bloques
C1 = \xdc\xc4`G\xe0\xf7\xb1|\x82VK\x89-\xed\x02\xf1
C2 = \xae\t\x01\xd6)`\n\xe6\xcf\xf7\x0c+N_3c
```

Ahora bien, no podemos mandar el ultimo bloque `word=$3cReT_p45S` por separado (pues la encriptacion de ese bloque debe depender del bloque anterior `ministrator&pass`). Y tampoco podemos mandar los 3 juntos, porque justamente no nos dejan hacer eso.

Entonces estaria bueno crear un bloque nuevo en el medio "milagroso", que mantenga el estado del cipher, y recien ahi podamos poner el bloque `word=$3cReT_p45S`.

Es decir, estamos intentando crear un plaintext con la siguiente forma
```
P1 | P2 | Paux | P3
```

Nosotros queremos que el cifrado sea de la siguiente forma (notese que C2 se repite para no modificar el estado)
```
C1 | C2 | C2 | C3
```
Entonces, tenemos que el cifrado del plaintext auxiliar debe ser igual a C2
```
Caux = C2
```

Pero, Caux como esta tercero, depende de C2
```
Caux = E(Paux ^ C2) 
```

Ademas sabemos que
```
C2 = E(P2 ^ C1)
```

Luego, podemos igualar las ecuaciones
```
Caux = E(Paux ^ C2) = E(P2 ^ C1) = C2
```

Y ahora igualamos los inputs de la funcion E, y despejamos Paux
```
Paux ^ C2 = P2 ^ C1
Paux = P2 ^ C1 ^ C2
```

Entonces, poniendo Paux en tercer lugar, nos garantiza no cambiar el estado del cipher, y entonces al mandarlos al server y quedarnos con los bloques 1, 2 y 4 (el 3 no interesa porque es Caux), obtenemos el ciphertext deseado.

Dejo tambien el codigo que fui usando (medio desprolijo pero en fin) en el archivo crack.py