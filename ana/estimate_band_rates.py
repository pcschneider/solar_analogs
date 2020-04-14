from __future__ import print_function
import xspec as xs
import glob
import matplotlib.pyplot as plt
import numpy as np
import pyfits
#from astropy.table import Table
from parameters import *

def fluxes(fn):
    xs.AllData(fn)
    xs.Plot.xAxis = "keV"   
    xs.AllData.ignore("**-0.2")
    xs.AllData.ignore("2.-**")
    xs.AllData.ignore("bad") 
    m = xs.Model("apec")
    xs.Xset.abund = "angr"
    m(4).frozen = True
    
    res = {}
    
    for t in temps:
       res[t] = []
       m.setPars({1:t/12.6})
       
       for band in bands:
        xs.AllData.notice("0.2-2.0")
        
        xs.AllData.ignore("**-"+str(band[0]))
        xs.AllData.ignore(str(band[1])+"-**")
        ra =  xs.AllData(1).rate        
        res[t].append([band, str("%5.2f" % ra[3])])
    ff = pyfits.open(fn)
    targ = ff[0].header["OBJECT"]
    oi = ff[0].header["OBS_ID"]
    xs.Fit.show()

    for r in res:
        print(res[r])
    return targ, oi, res
    #m.error[1]
    
    
temps = [1.0, 2.0]    
bands = [(0.2,0.4), (0.5,0.6), (0.47,0.65),(0.47,0.7),  (0.2,1.0), (0.2,2.0)]
res = []    
files = glob.glob("*.12ch")
#files = glob.glob("*.1grp")
print("files: ",files)
for f in files:
    r = fluxes(f)
    print(f, r)
    res.append(r)
    print()
    
mns = {}
for t in temps:
  mns[t] = {}
  for b in bands:
    mns[t][b] = []

for r in res:
    print(r[0], r[1])    
    dct = r[2]
    print(dct)
    for d in dct:
        print(d, dct[d])
        for r in dct[d]:
            #print(r)
            mns[d][r[0]].append(r[1])
        
    print()    

for t in temps:
    for b in bands:
        arr = np.array(mns[t][b]).astype(float)
        print(t, b, np.mean(arr), np.std(arr))
    print()
#res = np.array(res)
#fn = xspec_fluxes_fn
#fn = fn.replace("../data/","../") # because it is run from data/specs and not from ana

#np.savetxt(fn, res,delimiter=", ", fmt="%s", header="target, obsID, flux_lo, flux, flux_hi, rate, rate_err")    
##tt = Table(rows=res, names=("target", "obsID", "lo", "fit", "hi"))
##tt.write(xspec_fluxes_fn, format='ascii.ecsv', delimiter=',')
