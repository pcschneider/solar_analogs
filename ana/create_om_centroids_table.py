import numpy as np
from astropy.table import Table
from astropy.io import fits as pyfits
from parameters import *
import glob
import sys
sys.path.append("tools")
from tools import om

xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';') 

tab = []
for obsid in xobs["obsID"]:
    print(obsid)
    try:
        directory = glob.glob("../data/*/"+str(obsid)+"/odata/omf")[0]
    except     IndexError:
        print("No OM data for ",obsid)
        continue
    
    print(directory)
    oo = om.OM(directory)
    for fn in oo.images:
        ff = pyfits.open(fn)
        print("image: ",fn, " -> ", ff[0].header["FILTER"] ," ", ff[0].header["EXPOSURE"])
    cens = oo.source_positions()
    for oi in cens:
        for exp in cens[oi]:
            xx = cens[oi][exp][0].split()
            tab.append([oi, exp, xx[0], xx[1]])
    #print(tab)
    
    print(80*"=")
    print()

tt = Table(rows=tab, names=("obsID","expID", "RA", "Dec"))
fn = om_centroids_fn
fn = "test2.ecsv"
tt.write(fn, format='ascii.ecsv', delimiter=',',overwrite=True)
