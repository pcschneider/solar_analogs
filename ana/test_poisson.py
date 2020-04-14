from __future__ import print_function
from scipy.stats import poisson
import matplotlib.pyplot as plt

for x in range(1, 30):
  plt.scatter([x], [poisson.cdf(x, 10, loc=0)])

plt.show()