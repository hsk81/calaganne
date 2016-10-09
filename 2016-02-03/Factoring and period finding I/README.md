# Factoring and period finding I

Once you understand Shor's period-finding then it is an easy piece of cake to also grasp how you can do factoring of for example a number with two large prime factors $N=pq$ with $p$, $q$ in $\mathbb{P}$.

Today, we won't go into the details how that is done, but look at a preliminary number theoretic relation, which enables us (in combination with *Shor's period finding*) to do factoring. It's a little difficult to understand the details, but the general picture is quite clear:

The probability is at least $1/2$ that if $a$ is a random member of $G_{pq}$ for prime $p$ and $q$, then the order $r$ of $a$ in $G_{pq}$ satisfies both 

$$\begin{equation}r\text{ is even}\label{i}\end{equation}$$

and 

$$\begin{equation}a^{r/2}\not\equiv−1 \pmod{pq}\label{ii}\end{equation}$$

where $a$ to the power of it's order $r$ is equal to $1 \pmod{pq}$. Let's compress this already mathematical statement a little more. For $a\in G_{pq}$ and $p, q\in\mathbb{P}$ it holds that:

$$\begin{equation}\Pr\{a^{r/2}\not\equiv−1\pmod{pq}\}⩾1/2\end{equation}$$

with $ar\equiv1\pmod{pq}$, where I've omitted the $r$ is even part, since the condition $\eqref{ii}$ can be subsumed in $\eqref{i}$. Alright, let's do some plotting:

![$\Pr\{a^{r/2}\not\equiv−1\pmod{pq}\}⩾1/2$][1]

The plot may be displayed rather small, so I'd suggest you click on it: What you'll see is that all probabilities are larger or equal than $1/2$ for some chosen prime pairs $p$ and $q$. Apparently, the larger $p$ and $q$ the higher the probability that $ar/2\not\equiv−1\pmod{pq}$, which makes sense since there are then a lot more numbers *not* congruent to $−1$ in $G_{pq}$. Above the prime pairs $(p,q)$ are in the range $(3,3)$…$(19,19)$. When we extend the range then the probabilities get very close to $1$:

![$\Pr\{a^{r/2}\not\equiv−1\pmod{pq}\}⩾1/2$][2]

This looks fantastic! Given this relation we can now factor a larger number with prime factors $N=pq$ into it's components, the details of which will follow in my next post.

```python
01 #!/usr/bin/env python
02 ########################################################################
03 
04 import itertools as it
05 import numpy as np
06 import random
07 import math
08 import gmpy2 as gmp
09 
10 from matplotlib import pyplot as pp
11 
12 ########################################################################
13 
14 def POWERs(a, p, q):
15 	fn = lambda k: a**k % (p*q)
16 	return map(fn, range(p*q))
17 def ORDERs(a, p, q, rem=1):
18 	f1 = lambda t: t[1] == rem
19 	f2 = lambda t: t[0]
20 	return map(f2, filter(f1, enumerate(POWERs(a, p, q))))
21 def ORDER(a, p, q):
22 	return list(it.islice(ORDERs(a, p, q), 1, 2))[0] \
23 		if a % p != 0 and a % q else None
24 def OSAMPLE(p, q, sz):
25 	f1 = lambda _: random.randint(0, p*q - 1)
26 	f2 = lambda a: (a, ORDER(a, p, q))
27 	f3 = lambda t: t[1] is not None
28 	return filter(f3, map(f2, map(f1, range(sz))))
29 def M1(p, q, sz):
30 	fn = lambda t: t[1] % 2 == 0
31 	return sum(map(fn, OSAMPLE(p, q, sz))) / sz
32 def M2(p, q, sz):
33 	fn = lambda t: gmp.powmod(t[0], int(t[1]/2), p*q) != -1
34 	return sum(map(fn, OSAMPLE(p, q, sz))) / sz
35 
36 def PRIMEs(n):
37 	sieve = [True] * n
38 	for i in range(3,int(n**0.5)+1,2):
39 		if sieve[i]: sieve[i*i::2*i]=[False]*int((n-i*i-1)/(2*i)+1)
40 	return [i for i in range(3,n,2) if sieve[i]]
41 
42 def PSAMPLE(sz):
43 	return [(p1, p2) for p1 in PRIMEs(n=sz) for p2 in PRIMEs(n=sz)]
44 
45 ps = PSAMPLE(sz=25)
46 m2 = list(map(lambda p: M2(p[0], p[1], sz=250), ps))
47 
48 for i, p in enumerate(ps):
49 	pass ## pp.text(i, m2[i], '(%s,%s)' % p)
50 
51 pp.title('M2: Pr{a^{order(a)/2} != -1 (mod pq)} for random a in G{pq}')
52 pp.plot(m2, 'b*')
53 pp.grid()
54 pp.show()
55 
56 ########################################################################
```

[1]: https://4.bp.blogspot.com/-JZG-tGcZzFM/VtFCxXZww1I/AAAAAAAAARY/hvlsYNAam6w/s640/m2-a.png

[2]: https://1.bp.blogspot.com/-WOePAeljKWc/VtFCxyIIGsI/AAAAAAAAARo/FO_nV5cWoW8/s640/m2-d.png