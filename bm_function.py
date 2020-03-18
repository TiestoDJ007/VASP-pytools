#!/home/universe/local_env/anaconda3/envs/abinit/bin/python
import math

import numpy as np

a, E = np.loadtxt('data', usecols=(0, 1), delimiter=' ', unpack=True)
x = (a * 1) ** (-2)
p = np.polyfit(x, E, 3)
c0 = p[3]
c1 = p[2]
c2 = p[1]
c3 = p[0]
x1 = (math.sqrt(4 * c2 ** 2 - 12 * c1 * c3) - 2 * c2) / (6 * c3)
para = 1 / math.sqrt(x1)
print('The final lattice is: %s  ' % (para))
