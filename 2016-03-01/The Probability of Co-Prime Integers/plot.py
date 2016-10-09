#!/usr/bin/env python
###############################################################################

import numpy as np
from math import gcd
from matplotlib import pyplot as pp

###############################################################################

def NEXT(n):
	return np.random.random_integers(2**n)
def CO_PRIME_PCT(m, n):
	return sum([1 if gcd(NEXT(n), NEXT(n))==1 else 0 for i in range(m)]) / m
def SAMPLE(size, m=1000,n=48):
	return np.fromiter(map(lambda _: CO_PRIME_PCT(m,n), range(size)), dtype=np.float)

s0 = SAMPLE(size=256)
s1 = SAMPLE(size=256)
s2 = SAMPLE(size=256)

mm = 0.0; std = 0.0
m0 = s0.mean(); mm += m0 / 3.0; std += s0.std() / 3.0
m1 = s1.mean(); mm += m1 / 3.0; std += s1.std() / 3.0
m2 = s2.mean(); mm += m2 / 3.0; std += s2.std() / 3.0

pp.plot(s0, s1, 'r.')
pp.plot(s1, s2, 'g.')
pp.plot(s2, s0, 'b.')

mm = float(100.0*mm)
std = float(100.0*std)

pp.title('Pr{co-prime(X=x,Y=y)} = ca. %0.2f%% ± %0.2f%%' % (mm, std))
pp.legend(['Sample #1 vs #2','Sample #2 vs #3','Sample #3 vs #1'])
pp.grid()
pp.show()

###############################################################################
