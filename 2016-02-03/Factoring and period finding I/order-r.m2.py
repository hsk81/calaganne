#!/usr/bin/env python
###############################################################################

import itertools as it
import numpy as np
import random
import math
import gmpy2 as gmp

from matplotlib import pyplot as pp

###############################################################################

def POWERs(a, p, q):
	fn = lambda k: a**k % (p*q)
	return map(fn, range(p*q))
def ORDERs(a, p, q, rem=1):
	f1 = lambda t: t[1] == rem
	f2 = lambda t: t[0]
	return map(f2, filter(f1, enumerate(POWERs(a, p, q))))
def ORDER(a, p, q):
	return list(it.islice(ORDERs(a, p, q), 1, 2))[0] \
		if a % p != 0 and a % q else None
def OSAMPLE(p, q, sz):
	f1 = lambda _: random.randint(0, p*q - 1)
	f2 = lambda a: (a, ORDER(a, p, q))
	f3 = lambda t: t[1] is not None
	return filter(f3, map(f2, map(f1, range(sz))))
def M1(p, q, sz):
	fn = lambda t: t[1] % 2 == 0
	return sum(map(fn, OSAMPLE(p, q, sz))) / sz
def M2(p, q, sz):
	fn = lambda t: gmp.powmod(t[0], int(t[1]/2), p*q) != -1
	return sum(map(fn, OSAMPLE(p, q, sz))) / sz

def PRIMEs(n):
	sieve = [True] * n
	for i in range(3,int(n**0.5)+1,2):
		if sieve[i]: sieve[i*i::2*i]=[False]*int((n-i*i-1)/(2*i)+1)
	return [i for i in range(3,n,2) if sieve[i]]

def PSAMPLE(sz):
	return [(p1, p2) for p1 in PRIMEs(n=sz) for p2 in PRIMEs(n=sz)]

ps = PSAMPLE(sz=25)
m2 = list(map(lambda p: M2(p[0], p[1], sz=250), ps))

for i, p in enumerate(ps):
	pass ## pp.text(i, m2[i], '(%s,%s)' % p)

pp.title('M2: Pr{a^{order(a)/2} != -1 (mod pq)} for random a in G{pq}')
pp.plot(m2, 'b*')
pp.grid()
pp.show()

###############################################################################
