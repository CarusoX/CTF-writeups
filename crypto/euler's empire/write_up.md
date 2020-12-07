# Write up


In this challenge we are given an encrypted message `C = L ^ Z ^ M`, where `L` and `Z` are some constants and `M` is the original message.

`Z` is given, but `L` is calculated as:
```
L = pow(2, pow(2, T), N)
```
where T and N are also some constants.

The problem is that pow(2, T) is too big, and therefore we can't have the value `L`. But we have to remember that when dealing with an equation modulo `N`, the exponent is only needed module `ϕ(N)` (https://en.wikipedia.org/wiki/Euler%27s_theorem)

To calculate `ϕ(N)` we just need to factorize `N`:
```
>>> import sympy as sp
>>> N = 126176329335043454027341235009057683290541781096785538088437185779950106283534462102786883
>>> factors = sp.factorint(N)
{940957051: 1, 648863389: 1, 611738359: 1, 806952673: 1, 973139887: 1, 856368371: 1, 914351299: 1, 848994661: 1, 834612803: 1, 775357619: 1}
>>> phin = 1
>>> for f in factors.keys(): phin *= f - 1
...
>>> phin
126176327766347868670445253548423866264423599446222116653637264931304799576112524861440000
```

And with this we can calculate `L = pow(2, pow(2, T, phin), N)`.

Finally, `M = C ^ L ^ Z`

```
b00t2root{Eul3r_w4s_4_G3niu5}
```