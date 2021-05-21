from parameters import *
from astropy.table import Table
import numpy as np
import glob
import os
from astropy.io import fits as pyfits
import pToolsRegion
import pToolsUtils

src = Table.read(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')
bkg = Table.read(bgs_ecsv_fn, format='ascii.ecsv', delimiter=',')
xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';')
#extr = Table.read(extract_prop_fn, format='ascii.ecsv', delimiter=';')
#extr = Table.read(measured_cen_extr_200_fn, format='ascii.ecsv', delimiter=';')
extr = Table.read(measured_cen_extr_fn, format='ascii.ecsv', delimiter=';')

prefix="pn_final"

res = []

for source in src:
    xi = np.where(source["obsID"] == xobs["obsID"])[0]
    ei = np.where(source["obsID"] == extr["obsID"])[0]
    oi = source["obsID"]
    sfn = xobs["directory"][xi].data[0]+"/odata/"+oi+"_"+prefix+"_spec.fits"
    bfn = xobs["directory"][xi].data[0]+"/odata/"+oi+"_"+prefix+"_spec_bg.fits"
    print(source["name"], xobs["obsID"][xi].data, sfn, bfn)
    try:
        ff_src = pyfits.open(sfn)
        ff_bkg = pyfits.open(bfn)
        src_cts = np.sum(ff_src[1].data["COUNTS"])
        bkg_cts = np.sum(ff_bkg[1].data["COUNTS"])
        src_area, bkg_area = ff_src[1].header["BACKSCAL"], ff_bkg[1].header["BACKSCAL"]
        print(src_cts, bkg_cts* src_area/bkg_area, bkg_cts, src_area/bkg_area)
        
        fn = extr["fn"][ei].data[0]
        fn = fn.replace("pn.fits","pn_filt.fits")
        print("fn",fn)
        sx, sy, sr = extr["src_x"][ei].data[0], extr["src_y"][ei].data[0],  extr["src_r"][ei].data[0]
        bx, by, br = extr["bkg_x"][ei].data[0], extr["bkg_y"][ei].data[0],  extr["bkg_r"][ei].data[0]
        print(fn, sx, sy, sr)
        print("                 ",bx, by, br)
        src_reg = pToolsRegion.circle((sx, sy, sr))
        bkg_reg = pToolsRegion.circle((bx, by, br))
        
        src_cts = pToolsUtils.eventsInRegion(fn, src_reg, eLo=200, eHi=1000)
        bkg_cts = pToolsUtils.eventsInRegion(fn, bkg_reg, eLo=200, eHi=1000)
        
        #src_cts = pToolsUtils.eventsInRegion(fn, src_reg, eLo=200, eHi=400)
        #bkg_cts = pToolsUtils.eventsInRegion(fn, bkg_reg, eLo=200, eHi=400)
        
        #src_cts = pToolsUtils.eventsInRegion(fn, src_reg, eLo=470, eHi=700)
        #bkg_cts = pToolsUtils.eventsInRegion(fn, bkg_reg, eLo=470, eHi=700)
        
        print(src_cts, bkg_cts)
        area_scale = src_area/bkg_area
        print(bkg_cts[0]*area_scale)
        
        ontime = pyfits.open(fn)[1].header["LIVETIME"]
        rate = (src_cts[0] - bkg_cts[0] * area_scale)/ontime
        print("rate: ",rate)
        res.append([source["name"], source["obsID"], src_cts[0], bkg_cts[0], area_scale, ontime, rate])
        
    except Exception as e:
        print(e)
        pass
    print()

for r in res:
    print(r)
    
tt = Table(rows=res, names=("source", "obsID", "src_cts", "bkg_cts", "area_scale", "ontime", "net_rate"))
#tt.write(extracted_photons_fn, format='ascii.ecsv', delimiter=',')
#tt.write(extracted_photons_02_04_fn, format='ascii.ecsv', delimiter=',')
#tt.write(extracted_photons_O7_fn, format='ascii.ecsv', delimiter=',')
    
#tt.write(extracted_photons_200_fn, format='ascii.ecsv', delimiter=',')
#tt.write(extracted_photons_200_02_04_fn, format='ascii.ecsv', delimiter=',')
#tt.write(extracted_photons_200_O7_fn, format='ascii.ecsv', delimiter=',')
    
    
