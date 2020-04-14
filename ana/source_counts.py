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

stars = ["HD 114174","HD 135101","HD 2071","HD 210918","HD 25874", "HD 45289"]
ages = {"HD 114174":6.4,"HD 135101":9.6,"HD 2071":4.7,"HD 210918":9.2,"HD 25874":7.3, "HD 45289":9.5}
   
        
    
    
outdata = {}

for st in stars:
    dr = "../data/"+st.replace(" ","")
    oi = glob.glob(dr+"/0*")[0][-10:]
    o = XMMobservation(oi)
    o.baseDir = dr
    o.initializeFilenames()
    
    s = AstroObject(st)
    s.populateFromSimbad()
    s.age = ages[st]
    print(s)
    ep = o.obsDate(which="pn")
    print(ep)
    print("coords at obs: ",s.coordinates(epoch=ep).to_string(style='hmsdms'))
    co = PNpixCoords(s, o)
    co.run()
    print("pix coords",co)
    #evselect table=mos1.fits withimageset=yes imageset=image.fits  xcolumn=X ycolumn=Y imagebinning=imageSize ximagesize=600 yimagesize=600


    nc = PNflux(s, o)
    nc.run(eLo=200, eHi=1000, cfc = 5.0e-12)
    print (st)
    print(oi, o.obsDate("pn"))
    print(nc, s.age)
    outdata[st] = {"flux":float(nc.value), "error":float(nc.value.error), "age":s.age}
    #ds9 = ds9call(s, o)
    #ds9.run(filePostfix="[PI=300:1000]", extraParams="-bin factor 16 -zoom 4")
    #print(ds9)
    
    
    print("=====================================================")
print()
with open(data_fn, 'wb') as output:
  pickle.dump(outdata, output)

for st in stars:
    print(outdata[st])
    