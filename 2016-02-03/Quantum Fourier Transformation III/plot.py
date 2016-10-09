#!/usr/bin/env python

from matplotlib import pyplot as pp
from numpy import *

N = 8
R = 17

def s(y, k, r, n, i=complex(0,1)):
    return exp(2*pi*i*k*r*y/2**n)

def m(r, n):
    return int(2**n / r)

def p(y, r=R, n=N):
    return 1.0/(m(r,n)*2**n) * abs(sum([s(y, k, r, n) for k in range(m(r,n))]))**2.0

fig, ax_1 = pp.subplots()
ax_2 = ax_1.twinx()

ax_1.set_ylabel('Pr{Y=y}')
ax_2.set_ylabel('∑Pr{Y=y}, Pr{Y=y}×R')

ys = list(range(2**N))
ps = list(map(p, ys))
rs = list(map(lambda p: p*R, ps))
cs = list(cumsum(ps))


ax_1.plot(ys, ps, 'r-.')
ax_2.bar(ys, rs, 0.2, color='g', edgecolor='g')
ax_2.plot(ys, cs, 'b.-')

ax_1.legend(['Pr{Y=y}'], loc='upper right')
ax_2.legend(['∑Pr{Y=y}', 'Pr{Y=y}×R'], loc='lower right')

pp.title('Measurement Pr{Y=y} with N=%d, R=%d and M=%d' % (N, R, m(R, N)))
pp.grid()
pp.show()
