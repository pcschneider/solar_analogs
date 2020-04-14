from astropy.table import Table, vstack, hstack, join
import numpy as np
from parameters import *
import sys
sys.path.append("tools")
#import tools
#from tools.Observation import *
from tools.Object import *

tt = Table.read("../data/tables/rates.csv", format='ascii.csv', delimiter=',',names=("target", "rate", "ul", "lf", "uf"))

rate2flux = {"02-10":{1.0: 3.69666666667e-11, 1.2:1.78e-11, 1.3: 1.34e-11, 1.4:1.06e-11, 1.5: 8.67777777778e-12, 2.0: 4.94666666667e-12},\
             "02-04":{1.0: 8.13555555556e-11, 1.5:  3.20111111111e-11, 2.0:  2.49666666667e-11},\
             "O7": {1.0: 1.38e-10, 1.5: 2.00888888889e-11, 2.0: 1.01177777778e-11}}

def T4LX(lx):
    return (lx/1.61e26)**(1/4.05)

res = []
for row in tt:
    tmp = []
    s = AstroObject(row["target"])
    s.populateFromSimbad()
    dist_scaling = 4.*np.pi * (3.1e18 * s.distance)**2
    #dist_scaling = 1.0
    print(row["target"],":")
    tmp.append(row["target"])
    for t in [1.0, 1.3, 1.4, 1.5, 2.0]:
      scaling = rate2flux["02-10"][t]
      if row["ul"]:
          a = scaling * dist_scaling * row["rate"]
          b = a*row["uf"]    
          print("T=%4.1f              %5.2e < %5.2e -> T= %5.2f" % (t, a, b, T4LX(b)))
      else:
          b = scaling * dist_scaling * row["rate"]
          a = b/row["lf"]
          c = b*row["uf"]
          print("T=%4.1f  %5.2e < %5.2e < %5.2e -> T= %5.2f" % (t, a, b, c, T4LX(b)))
          
    print()      
    
