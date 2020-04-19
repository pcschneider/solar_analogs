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

for oi in xobs["obsID"]:
    ci = np.where(cens["obsID"] == oi)[0]
    print(oi, ci)
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
        print(ra, dec)
        xi = np.where(oi == xobs["obsID"])[0]
        pn_fn = "../"+xobs["directory"][xi][0]+"/pn.fits"
        c = SkyCoord(ra, dec, unit=(u.deg, u.deg))

        ti = np.where(srcs["obsID"] == oi)[0]
        targ = srcs["name"][ti]
        print(targ)
        dr = "../data/"+targ[0].replace(" ","")
        
        o = XMMobservation(oi)
        o.baseDir = dr
        o.initializeFilenames()
        
        pix = o.sky2pix(np.array(c.to_string("decimal", precision=10 ).split()).astype(float))[0]
        print("pix",pix)
        
        ei = np.where(targ == extr["source"])[0]
        print("ei",ei)
        src_x, src_y = extr["src_x"][ei][0], extr["src_y"][ei][0]
        print(src_x, src_y, "d = ",((pix[0]-src_x)**2 + (pix[1]-src_y)**2)**0.5 / 20," arcsec")
        
        extr["src_x"][ei] = pix[0]
        extr["src_y"][ei] = pix[1]
        
        
    print(80*"=")
    
#extr.write(measured_cen_extr_fn, format='ascii.ecsv', delimiter=',')
