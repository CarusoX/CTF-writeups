# Write up

For this challenge, we need to understand block encryption ciphering. You can read more about it here https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation

It's important to notice that the KEY is also the IV

We mainly need to understand one thing, to decrypt a string, we basically do:
```
P[i] = DECRYPT(C[i]) ^ C[i-1]
C[0] = IV
```

Where `P[i]` is the i-th block of the plaintext, the `C[i]` is the i-th block of the ciphertext, and `IV` is the initializacion vector. (We are using 1-based index for the plaintext).

So let's see what happens if we send to the server 2 blocks of 32 0s (32 0s are 16 bytes which is the block size) and ask it to decrypt it.

```
1. Enter key and get flag
2. Encrypt plaintext
3. Decrypt ciphertext

Enter option: 3
Enter hex ciphertext: 0000000000000000000000000000000000000000000000000000000000000000
Plaintext:  1d8dec46a622bc7f2dd8d3236262a4866de29c23df47c81748abb24a0e0dd6f4
```

Lets write the formulas:
```
P[2] = DECRYPT(C[2]) ^ C[1]
P[1] = DECRYPT(C[1]) ^ C[0] = DECRYPT(C[1]) ^ IV
```

But we know that `C[1]` = 0x00000000000000000000000000000000 = 0, and also `C[1] = C[2] = 0`
```
P[2] = DECRYPT(0)
P[1] = DECRYPT(0) ^ IV
```

What happens if we use the `xor` between the 2 blocks of the plaintext?

```P[2] ^ P[1] = DECRYPT(0) ^ DECRYPT(0) ^ IV = IV = KEY```


The script:
```
# I sent 0000000000000000000000000000000000000000000000000000000000000000 for decryption

# 2 blocks

C = '1d8dec46a622bc7f2dd8d3236262a4866de29c23df47c81748abb24a0e0dd6f4'

a, b = C[:32], C[32:]
print(a,b)

# A = DECRYPTION(0) ^ IV
# B = DECRYPTION(0) ^ 0

# A ^ B = IV

flag = ""
for i in range(0, 32, 2): flag += hex(int(a[i:i+2],16)^int(b[i:i+2],16))[2:]
print(flag) # send this to the server
```

```
b00t2root{th3y_4r3_g0ing_t0_k1ll_u5}
```


