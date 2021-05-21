import xspec as xs
import glob
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits as pyfits
#from astropy.table import Table
from parameters import *
import os

def fluxes(fn):
    xs.AllData(fn)
    xs.Plot.xAxis = "keV"   
    xs.AllData.ignore("**-0.2")
    xs.AllData.ignore("1.-**")
    xs.AllData.ignore("bad") 
    m = xs.Model("cflux*apec")
    m.setPars({1:0.2, 2:10, 3:-14, 4:0.2})
    xs.Xset.abund = "angr"
    m(7).frozen = True
    m(4).frozen = True
    xs.Fit.statMethod = "cstat"
    xs.Fit.show()
    xs.Fit.nIterations = 10000
    xs.Fit.query = "yes"
    xs.Fit.perform()
    xs.Fit.show()
    ra =  xs.AllData(1).rate
    try:
        xs.Fit.error("3")
        print(m(3).values, m(3).error)
        print("rate",ra)
        a,b =  m(3).error[0], m(3).error[1]
    except:
        a, b = -1, -1
        
    ff = pyfits.open(fn)
    targ = ff[0].header["OBJECT"]
    oi = ff[0].header["OBS_ID"]

    xs.Fit.show()
    xs.Plot.device="/xs"
    xs.Plot("data")
    return list([targ, oi, a, m(3).values[0], b, ra[0], ra[1]])
    #m.error[1]
    
    
cwd = os.getcwd()
print("cwd: ",cwd)
res = []    
files = glob.glob("../data/*/*/odata/*final*.12ch")
for fn in files:
    dr = os.path.dirname(fn)
    spec_fn = os.path.basename(fn)
    print(fn, dr, " -> ",spec_fn)
    os.chdir(dr)
    print(os.getcwd())
    r = fluxes(spec_fn)
    print(spec_fn)
    print("     ", r)
    targ = dr.split("/")[-3]
    targ = targ[0:2]+" "+targ[2:]
    print("targ: ",targ)
    r[0] = targ
    res.append(r)
    #print()
    print(80*"=")
    print()
    os.chdir(cwd)    
#exit()    
    
res = np.array(res)
fn = xspec_fluxes_fn
#fn = fn.replace("../data/","../") # because it is run from data/specs and not from ana

np.savetxt(fn, res,delimiter=", ", fmt="%s", header="target, obsID, flux_lo, flux, flux_hi, rate, rate_err")    
#tt = Table(rows=res, names=("target", "obsID", "lo", "fit", "hi"))
#tt.write(xspec_fluxes_fn, format='ascii.ecsv', delimiter=',')
