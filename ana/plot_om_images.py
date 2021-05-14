import numpy as np
from astropy.table import Table
from astropy.io import fits as pyfits
from parameters import *
import glob
import sys
sys.path.append("tools")
from tools import om, evtWcs
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import astropy.units as u
from astropy.visualization.wcsaxes import SphericalCircle
plt.rcParams.update({'font.size': 13})

xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';') 
#bkg = Table.read(bgs_ecsv_fn, format='ascii.ecsv', delimiter=',')
extr = Table.read(measured_cen_extr_fn, format='ascii.ecsv', delimiter=';')

tab = []
for obsid in xobs["obsID"]:
    ei = np.where(obsid == extr["obsID"])[0]
    #bi = np.where(obsid == bkg["obsID"])[0]
    print("obsID: ",obsid," exposureID: ",ei," pn_fn:", extr["fn"])
    pn_fn = extr["fn"][ei].data[0]
    src_x, src_y = extr["src_x"][ei].data[0], extr["src_y"][ei].data[0]
    print(obsid, " ",ei, " filename: ",pn_fn)
    w = evtWcs.XMMwcs(pn_fn)
    sky = w.pix2sky([src_x, src_y])
    print("sky: ",sky, type(sky))
    #print(bkg["bg_x"][bi].data)
    
    #src_x,src_y,src_r,bkg_x,bkg_y,bkg_r
    
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
        
        hdu=ff[0]
        wcs = WCS(hdu.header)

        
        plt.subplot(projection=wcs)
        plt.subplots_adjust(right=0.96)
        ax = plt.gca()
        mn, mx = np.nanmin(hdu.data), np.nanmax(hdu.data)
        #c = Circle(sky, 0.001, edgecolor='yellow', facecolor='none', linewidth=3,  transform=ax.get_transform('fk5'))
        #ax.add_patch(c)
        c2 = SphericalCircle((sky[0], sky[1])*u.degree, 1*u.arcsec, edgecolor='red', facecolor='none', linewidth=3,  transform=ax.get_transform('fk5'))
        ax.add_patch(c2)
        #plt.scatter([15],[15], color='r')
        sc = plt.scatter([sky[0]], [sky[1]], transform=ax.get_transform("fk5"), color='m', marker='x')
        #print(dir(sc), sc.get_offsets(), sc.get_offset_position())
        tt = plt.gca().get_transform('world')
        #print(tt, dir(tt))
        im = plt.imshow(hdu.data, vmin=mn, vmax=mx, origin='lower')
        plt.colorbar(im)
        plt.xlabel("RA")
        plt.ylabel("Dec")
        plt.annotate(str("%s: %ss" % (ff[0].header["FILTER"] , ff[0].header["EXPOSURE"])), xy=(0.05,0.92), xycoords="axes fraction",bbox=dict(facecolor='w', edgecolor='none'))
        plt.title(str("%s, EXP_ID=%s" % (ff[0].header["OBJECT"], ff[0].header["EXP_ID"])))
        plt.show()
        
    cens = oo.source_positions()
    for oi in cens:
        for exp in cens[oi]:
            xx = cens[oi][exp][0].split()
            tab.append([oi, exp, xx[0], xx[1]])
    #print(tab)
    
    print(80*"=")
    print()
