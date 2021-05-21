import numpy as np
from astropy.table import Table
from astropy.io import fits as pyfits
from parameters import *
import glob
import sys, os
sys.path.append("tools")
from tools import om, evtWcs, AstroObject
from astropy.wcs import WCS
import astropy.units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import astropy.units as u
from astropy.visualization.wcsaxes import SphericalCircle
plt.rcParams.update({'font.size': 13})

xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';') 
#bkg = Table.read(bgs_ecsv_fn, format='ascii.ecsv', delimiter=',')
extr = Table.read(measured_cen_extr_fn, format='ascii.ecsv', delimiter=';')
extr = Table.read(extract_prop_fn, format='ascii.ecsv', delimiter=';')
#extr = Table.read("test2.ecsv", format='ascii.ecsv', delimiter=';')
image_fn = "pn_image_300-1000.fits"

nothing = {}

tab = []
for tt, obsid in zip(xobs["target"], xobs["obsID"]):
    
    try:
        ei = np.where(obsid == extr["obsID"])[0]
        pn_fn = extr["fn"][ei].data[0]
    except:
        print("No extraction information found in ",measured_cen_extr_fn)
        print(80*"=")
        print()
        if tt not in nothing: nothing[tt] = [obsid] 
        else:  nothing[tt].append(obsid)
        continue

    print("obsID: ",obsid," exposureID: ",ei," pn_fn:", pn_fn)
    
    
    fn = os.path.dirname(os.path.abspath(pn_fn))+"/"+image_fn
    src_x, src_y, src_r = extr["src_x"][ei].data[0], extr["src_y"][ei].data[0], extr["src_r"][ei].data[0]
    bkg_x, bkg_y, bkg_r = extr["bkg_x"][ei].data[0], extr["bkg_y"][ei].data[0], extr["bkg_r"][ei].data[0]
    w = evtWcs.XMMwcs(pn_fn)
    
    sky = w.pix2sky([src_x, src_y])
    bkg = w.pix2sky([bkg_x, bkg_y])
    print("sky: ",sky, type(sky), "(", src_x, src_y, src_r,")")

    try:
        ff = pyfits.open(fn)
    except:
        print("Cannot open image file ",fn)
        print(80*"=")
        print()
        #nothing.append()
        if tt not in nothing: nothing[tt] = [obsid] 
        else:  nothing[tt].append(obsid)
        continue
    print("image: ",fn, " -> ", ff[0].header["FILTER"] ," ", ff[0].header["EXPOSURE"])
    target = ff[0].header["OBJECT"]
    date_obs = ff[0].header["DATE-OBS"]
    oo = AstroObject(target)
    oo.populateFromSimbad()
    print("target: ",target, " date-Obs: ",date_obs)
    cc = oo.coordinates(date_obs, epochFormat='fits')
    print(cc)
    hdu=ff[0]
    wcs = WCS(hdu.header)
    
        
    plt.subplot(projection=wcs)
    plt.subplots_adjust(right=0.96)
    im = plt.imshow(hdu.data, vmin=0, vmax=6, origin='lower', aspect='auto')

    ax = plt.gca()
    
    
    
    mn, mx = np.nanmin(hdu.data), np.nanmax(hdu.data)
    #c = Circle(sky, 0.001, edgecolor='yellow', facecolor='none', linewidth=3,  transform=ax.get_transform('fk5'))
    #ax.add_patch(c)
    c2 = SphericalCircle((sky[0], sky[1])*u.degree, src_r/20*u.arcsec, edgecolor='red', facecolor='none', linewidth=3,  transform=ax.get_transform('fk5'))
    ax.add_patch(c2)
    
    c2 = SphericalCircle((bkg[0], bkg[1])*u.degree, bkg_r/20*u.arcsec, edgecolor='green', facecolor='none', linewidth=3,  transform=ax.get_transform('fk5'))
    ax.add_patch(c2)
    
    #plt.scatter([15],[15], color='r')
    sc = plt.scatter([sky[0]], [sky[1]], transform=ax.get_transform("fk5"), color='m', marker='x')
    sc2 = plt.scatter([cc.ra.degree],[cc.dec.degree], transform=ax.get_transform("fk5"), color='c', marker='+', s=50)
    #sc.set_offset_position("data")
    #print(dir(sc), sc.get_offsets(), sc.get_offset_position())
    tt = ax.get_transform('fk5')
    #print(tt, dir(tt))
    plt.colorbar(im)
    
    #print("ax",dir(ax), ax.coords)
    
    rac = ax.coords['RA']
    decc = ax.coords['Dec']
    #pritn
    print(rac,decc)
    rac.set_major_formatter('d.ddd')
    decc.set_major_formatter('d.ddd')

    #s = SkyCoord(ra=sky[0], dec=sky[1], unit=(u.degree, u.degree))
    #x1, x0 = s.directional_offset_by(90.*u.degree, 200*u.arcsec).ra.to_value(),s.directional_offset_by(270.*u.degree, 200*u.arcmin).ra.to_value()
    #y0, y1 = s.directional_offset_by(0.*u.degree, 200*u.arcsec).dec.to_value(),s.directional_offset_by(180.*u.degree, 200*u.arcmin).dec.to_value()
    #print(x0, x1, y0, y1)
    ##print(ax.get_xlim(transform=ax.get_transform("fk5")))
    #print("XXX",dir(rac))
    ##print(rac.transform.transform(np.array([3,2])))
    ##ax.set_xlim(x0, x1)
    ##ax.set_ylim(y0, y1)
    
    ##tmp = ax.transLimits.inverted().transform([(x0, x1), (y0, y1)])
    #tmp = ax.transData.inverted().transform([(x0,x1), (y0, y1)])
    
    #tmp0 = ax.transData.transform([0,0])
    #tmp0 = tt.inverted().transform(tmp0)
    #print("tmp0a: ",tmp0)
    ##tmp0 = tt.transform([sky[0],sky[1]])
    #tmp0 = tt.transform(tmp0)
    #print("tmpX",tmp0)
    #tmp0 = ax.transData.inverted().transform(tmp0)
    #print("tmp0b: ",tmp0)
    
    #tmp0 = tt.inverted().transform([599,599])
    #print("tmp0c: ",tmp0)
    ##tmp0 = tt.transform([sky[0],sky[1]])
    #tmp0 = tt.transform([tmp0[0],tmp0[1]])
    #print("tmp0d: ",tmp0)
    
    ##tmp[1] = 600-tmp[1]
    #tmp1 = ax.transData.inverted().transform(tmp0)
    #print("tmp1: ",tmp1)
    ##tmp0 = tmp1
    
    
    #print(cc)
    cc = tt.transform([sky[0],sky[1]])
    cc = ax.transData.inverted().transform(cc)
    print(cc)
    ax.set_xlim(cc[0]-23, cc[0]+23)
    ax.set_ylim(cc[1]-23, cc[1]+23)
    
    #ax.set_xlim(tmp1[1]-50, tmp1[1]+50)
    #ax.set_ylim(tmp1[0]-50, tmp1[0]+50)
    ##tmp = wcs.wcs_world2pix(x0, y0, 1)
    
    
    
    sc2 = plt.scatter([0],[0], color='c', marker='x', s=200)
    sc2 = plt.scatter([599],[599], color='c', marker='x', s=200)

    
    
    #ax.coords[1].set_format_unit(u.degree)
    plt.xlabel("RA")
    plt.ylabel("Dec")
    plt.annotate(str("%s: %5.1fs" % (ff[0].header["FILTER"] , ff[0].header["EXPOSURE"])), xy=(0.05,0.92), xycoords="axes fraction",bbox=dict(facecolor='w', edgecolor='none'))
    plt.title(str("%s, EXP_ID=%s" % (ff[0].header["OBJECT"], ff[0].header["EXP_ID"])))
    plt.show()
        
    
    print(80*"=")
    print()
    continue

print("Nothing for")
for k in nothing:
    print("  ",k)
    for oi in nothing[k]:
        gi = np.where(oi == xobs["obsID"])[0]
        print("    ",oi, xobs["directory"][gi].data[0])
    
