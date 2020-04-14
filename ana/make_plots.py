from __future__ import print_function
import sys
sys.path.append("tools")
#import tools
from tools.Observation import *
from tools.Object import *
from tools.Tasks import *
import glob
import pickle
from scipy.stats import poisson
from parameters import *
import aplpy
import os
import pyfits
from astropy.coordinates import SkyCoord
from astropy import units as u
    
image_fn = "pn_image_300-1000.fits"
    
for st in stars:
    dr = "../data/"+st.replace(" ","")
    oi = glob.glob(dr+"/0*")[0][-10:]
    o = XMMobservation(oi)
    o.baseDir = dr
    o.initializeFilenames()
    s = AstroObject(st)
    s.populateFromSimbad()

    ep = o.obsDate(which="pn")
    print(ep)
    print("coords at obs: ",s.coordinates(epoch=ep).to_string(style='hmsdms'))
    co = PNpixCoords(s, o)
    co.run()
    print("pix coords",co)
    
    pn_fn = o.filename["pn"]
    print("pn: ",pn_fn)
    
    with pyfits.open(pn_fn) as ff:
      roll = (ff[1].header["PA_PNT"]- 90)*np.pi/180 
    
    dr = "../data/"+st.replace(" ","")
    oi = glob.glob(dr+"/0*")[0][-10:]
    fn = dr+"/"+oi+"/odata/"+image_fn
    print("fn   ",fn)
    fig = aplpy.FITSFigure(fn)
    pos = s.coordinates(epoch=ep) #.to_string(style='decimal')
    print("center degree", pos)
    x, y = pos.ra.degree, pos.dec.degree
    fig.show_colorscale()
    fig.recenter(x, y, width=5/60., height=5/60.)  # degrees
    fig.show_circles(x, y, 15/3600) # 300 = 15
    fig.show_circles(x, y, 25/3600) # 500 = 25
    fig.show_circles(x, y, 35/3600) # 700 = 35
    
    length = 6.5*15/3600.#*abs(np.cos(y))
    dx, dy = length*np.sin(roll), length*np.cos(roll)
    bgx, bgy = x+dx, y+dy
    bg_co = SkyCoord(bgx*u.degree, bgy*u.degree)
    print(bg_co)
    
    inp = np.array(bg_co.to_string("decimal", precision=10 ).split()).astype(float)
    pix = o.sky2pix(inp)
    
    print("pix", pix)
    #bkg_co = PNpixCoords()
    
    fig.show_circles(bgx, bgy, 35/3600) # 700 = 35
    
    #fig.show_anulus
    fig.add_colorbar()
    fig.colorbar.set_location('right')
    fig.add_label(x, y, st)
    fig.colorbar.set_axis_label_text('Counts')
    #fig.scalebar.show(15/3600)  # length in degrees
    #fig.scalebar.set_label('5 pc')
    
    ofn = st.replace(" ","_")+".pdf"
    print("ofn",ofn)
    
    fig.save(ofn)
    fig.close()