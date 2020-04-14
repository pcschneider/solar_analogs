from __future__ import print_function
import sys
import matplotlib.pylab as plt
#sys.path.append("tools")
##import tools
#from tools.probability import *
import numpy as np
from PyAstronomy.pyasl import ps_pdf_lams
from PyAstronomy import pyaC

l = np.linspace(0., 30., 200)


#for i in range(5):
  #print(i, ps_pdf_lams(i, 5, 10, 5))

ls = ps_pdf_lams(l, 5, 10, 0.2)
plt.plot(l, ls, label='5')

ls = ps_pdf_lams(l, 6, 10, 0.2)
#print(ls)
plt.plot(l, ls, label='15')

plt.legend()
plt.show()

gi = np.isfinite(ls)
cs = np.cumsum(ls[gi])/np.nansum(ls)

print(pyaC.zerocross1d(l, cs-0.9, getIndices=False))
print(pyaC.zerocross1d(l, cs-0.05, getIndices=False), pyaC.zerocross1d(l, cs-0.95, getIndices=False))
plt.plot(l[gi], np.cumsum(ls[gi])/np.nansum(ls))
plt.grid()
plt.show()