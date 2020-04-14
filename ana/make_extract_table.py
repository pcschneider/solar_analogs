from parameters import *
from astropy.table import Table
import numpy as np
import glob
import os
#import astropy.io.ascii
#from astropy.io import ascii

src = Table.read(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')
bkg = Table.read(bgs_ecsv_fn, format='ascii.ecsv', delimiter=',')
xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';')

def gather_info(source, source_file="pn.fits", src_radius=300):
    si = np.where(src["name"] == source)[0]    
    gi = np.where(np.logical_and(bkg["source"] == d["name"], bkg["obsID"] == d['obsID']))[0]
    if len(gi)!=1:
        if len(gi) == 0:
            print("No info for ",d["name"])
            return False
        print("No unique info ",d["name"])
        return False
    xi = np.where(xobs["obsID"] == d["obsID"])[0]
    print(d["name"], d["obsID"], gi)
    directory = xobs["directory"][xi].data
    #print(directory[0])
    fn = "../"+directory[0]+"/"+source_file
    #print(fn)
    gl = glob.glob(fn)
    #print(gl)
    src_x, src_y,src_r = src["src_x"][si].data[0], src["src_y"][si].data[0], src_radius
    bkg_x, bkg_y, bkg_r = bkg["bg_x"][gi].data[0], bkg["bg_y"][gi].data[0], bkg["bg_r"][gi].data[0]
    #print(src_x, src_y, src_r)
    #print(bkg_x, bkg_y, bkg_r)
    #print()
    
    return source, d["obsID"], fn, src_x, src_y, src_r, bkg_x, bkg_y, bkg_r

rows = []    
for d in src:
    row = gather_info(d["name"])
    if row != False:
      rows.append(row)    
tt = Table(rows=rows, names=("source", "obsID", "fn", "src_x", "src_y", "src_r", "bkg_x", "bkg_y", "bkg_r"))
tt.write(extract_prop_fn, format='ascii.ecsv', delimiter=',')
