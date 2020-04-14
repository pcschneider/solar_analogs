from parameters import *
from astropy.table import Table
import numpy as np
import glob
import os
import pyfits
import matplotlib.pyplot as plt

src = Table.read(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')

a, b, c, d = [],[],[],[]


for s in src:

    targ = s["name"]
    print(targ)
    
    dr = "../data/"+targ.replace(" ","")+"/"+s["obsID"]+"/odata/omf"
    print(dr)
    fns = glob.glob(dr+"/*TIMESR*.FIT")
    print(fns)
    mn_crs = []
    mags = []
    for fn in fns:
      ff = pyfits.open(fn)
      print("Filter: ",ff[1].header["FILTER"], ff[1].header["MAGNITUD"], np.median(ff[1].data["RATE"] - ff[1].data["BACKV"]))
      plt.plot(ff[1].data["TIME"], ff[1].data["RATE"] - ff[1].data["BACKV"], label=fn)
      mags.append(ff[1].header["MAGNITUD"])
      mn_crs.append(np.median(ff[1].data["RATE"] - ff[1].data["BACKV"]))
    if len(fns)>0:
        a.append(targ)
        b.append(s["obsID"])
        c.append(np.log10(np.mean(10**np.array(mags))))
        d.append(np.mean(mn_crs))
        print(c[-1], d[-1])    
    plt.title(targ)  
    plt.legend()
    plt.show()  
    
t = Table([a, b, c, d], names=('target', 'obsID', 'OM_mag', 'OM_rate'))
t.write(OM_fluxes_fn, format='ascii.ecsv', delimiter=',')