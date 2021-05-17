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
for star in stars:
    #for obsid in xobs["obsID"]:
    gi = np.where(xobs["target"] == star)[0]
    if len(gi)==0: 
        print(" No obs data found")
        print(80*"=")
        continue
    obsid = xobs["obsID"][gi[0]]
    observatory = xobs["observatory"][gi[0]]
    print(star, obsid, observatory)
    if observatory != "XMM": 
        print(" Not XMM data")
        print(80*"=")
        continue
    
    direct = "../data/*/"+str(obsid)+"/odata/omf"
    print("Checking: ",direct)
    directory = glob.glob(direct)
    print(directory)
    if len(directory)==0:
        direct = "../data/*/"+str(obsid)+"/omf"        
        print("Checking: ",direct)
        directory = glob.glob(direct)
    if len(directory)==0:
        direct = "../data/*/"+str(obsid)+"/omi"
        print("Checking: ",direct)
        directory = glob.glob(direct)
    if len(directory)==0:
        print("No OM data for ",obsid)
        print(80*"=")
        continue
    
    print("Using ",directory[0])
    oo = om.OM(directory[0])
    for fn in oo.images:
        print("Reading ",fn)
        ff = pyfits.open(fn)
        print("image: ",fn, " -> ", ff[0].header["FILTER"] ," ", ff[0].header["EXPOSURE"])
    cens = oo.source_positions()
    if cens is None: 
        print("No centroid positions found.")
        print(80*"=")
        continue
    
    for oi in cens:
        print("Adding centroids for ",star, " obsID: ",oi)
        for exp in cens[oi]:
            print(exp, cens[oi][exp])
            xx = cens[oi][exp][0].split()
            tab.append([oi, exp, xx[0], xx[1], star])
    #print(tab)
    
    print(80*"=")
    print()

tt = Table(rows=tab, names=("obsID","expID", "RA", "Dec", "target"))
fn = om_centroids_fn
#fn = "test2.ecsv"
tt.write(fn, format='ascii.ecsv', delimiter=',',overwrite=True)

print("Centroids for ",len(np.unique(tt["target"])), " stars.")
