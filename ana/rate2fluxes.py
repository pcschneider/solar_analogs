from astropy.table import Table, vstack, hstack, join
import numpy as np
from parameters import *
import sys
sys.path.append("tools")
#import tools
#from tools.Observation import *
from tools.Object import *

tt = Table.read(count_rates_fn, format='ascii.ecsv', delimiter=',')

rate2flux = {"02-10":{1.0: 3.69666666667e-11, 1.5: 8.67777777778e-12, 2.0: 4.94666666667e-12},\
             "02-04":{1.0: 8.13555555556e-11, 1.5:  3.20111111111e-11, 2.0:  2.49666666667e-11},\
             "O7": {1.0: 1.38e-10, 1.5: 2.00888888889e-11, 2.0: 1.01177777778e-11}}

last = ""
for row in tt:
    if row["target"] != last:
        print()
    s = AstroObject(row["target"])
    s.populateFromSimbad()
    dist_scaling = 4.*np.pi * (3.1e18 * s.distance)**2
    dist_scaling = 1.0
    print("%10s %10s %7.5f %7.5f %7.5f" % (row["target"], row["band"], row["net_300"]*1000, row["net_200"]*1000, row["hi_200"]/row["ontime"]*1000))
    for t in [1.0, 1.5, 2.0]:
        print("           %5.2e  %5.2e  " % (row["net_300"] * dist_scaling * rate2flux[row["band"]][t],  row["net_200"] * dist_scaling * rate2flux[row["band"]][t])) 
    last = row["target"]
    
