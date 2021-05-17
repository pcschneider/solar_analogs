import numpy as np
from astropy.table import Table
from parameters import *
import glob
import astropy.coordinates as coords
from astropy.coordinates import FK5
from astropy.coordinates import SkyCoord
import astropy.units as u
import sys
sys.path.append("tools")
from tools.Tasks import *
from tools.Observation import *

xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';') 
cens = Table.read(om_centroids_fn, format='ascii.ecsv', delimiter=',')
srcs = Table.read(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')
extr = Table.read(extract_prop_fn, format='ascii.ecsv', delimiter=',')

extr.add_column("nominal", name='pos_origin')

print("Number of observations: ",len(xobs["obsID"]))
nothing = []

cnt = 0

for targ,  oi, dr in zip(xobs["target"], xobs["obsID"], xobs["directory"]):
    ci = np.where(cens["obsID"] == oi)[0]
    print(targ, "obsID: ",oi, " (in ",dr,") number of OM centroids: ",len(ci))
    if len(ci)>0:
        ras, decs = [], []
        for i in ci:
            ra, dec = cens["RA"][i], cens["Dec"][i]
            #print(ra, dec)
            c = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))#, FK5, unit=(u.deg, u.hourangle))
            print(c.ra, c.dec)
            ras.append(c.ra.degree)
            decs.append(c.dec.degree)
        ra, dec = np.mean(ras), np.mean(decs)
        print("Mean RA, Dec: ",ra, dec, "std: ",np.std(ras), "DEC: ",np.std(decs)*3600,"arcsec")
        xi = np.where(oi == xobs["obsID"])[0]
        pn_fn = "../"+xobs["directory"][xi][0]+"/pn.fits"
        c = SkyCoord(ra, dec, unit=(u.deg, u.deg))

        #ti = np.where(srcs["obsID"] == oi)[0]
        #targ = srcs["name"][ti]
        #print(targ, "ti", ti)
        #if len(ti)==0: continue
        #dr = "../data/"+targ[0].replace(" ","")
        dr = "../data/"+targ.replace(" ","")
        print("Directory", dr)
        o = XMMobservation(oi)
        o.baseDir = dr
        o.initializeFilenames()
        
        nominal_pos = o.coord4target(targ)
        print("Nominal pos: ", nominal_pos, " dist to mean OM: ",c.separation(nominal_pos).arcsec, "arcsec")
        if c.separation(nominal_pos).arcsec > 5:
            print(" Separation between nominal and OM position too large!")
            print(80*"=")
            nothing.append(targ)
            continue
        
        pix = o.sky2pix(np.array(c.to_string("decimal", precision=10 ).split()).astype(float))[0]
        print("pix",pix)
        
        ei = np.where(targ == extr["target"])[0]
        print("ei",ei)
        if len(ei)==0:
            print(" No extraction info found in ",extract_prop_fn, " (='extract_prop_fn')")
            print(80*"=")
            nothing.append(targ)
            continue
        src_x, src_y = extr["src_x"][ei][0], extr["src_y"][ei][0]
        print(src_x, src_y, "d = ",((pix[0]-src_x)**2 + (pix[1]-src_y)**2)**0.5 / 20," arcsec")
        
        extr["src_x"][ei] = pix[0]
        extr["src_y"][ei] = pix[1]
        extr["pos_origin"][ei] = "OM"
        cnt+=1
    else:
        print("No centroid information: ",targ)
        nothing.append(targ)
    print(80*"=")

print("Centroids for ",cnt, " stars.")    
print(extr["src_x"][-1])
extr.write(measured_cen_extr_fn, format='ascii.ecsv', delimiter=',', overwrite=True)
print("Writing data to ",measured_cen_extr_fn)
print("Nothing for ",nothing)
