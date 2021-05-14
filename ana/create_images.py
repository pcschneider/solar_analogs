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
#import aplpy
import os

        
    
    
outdata = {}

for st in stars:
    dr = "../data/"+st.replace(" ","")
    print("dr: ",dr)
    gg = glob.glob(dr+"/0*")
    print("gg gg: ", gg)
    if len(gg)<1: continue
    oi = gg[0][-10:]
    print("directory: %s, obsID: %s" % (dr, oi))
    o = XMMobservation(oi)
    
    o.baseDir = dr
    o.initializeFilenames()
    
    s = AstroObject(st)
    s.populateFromSimbad()
    
    s.age = ages[st]
    print(s)
    ep = o.obsDate(which="pn")
    print(ep)
    
    print("coords at obs: ",s.coordinates(epoch=ep, epochFormat='fits').to_string(style='hmsdms'))
    co = PNpixCoords(s, o)
    co.run()

    ofile = os.path.dirname(o.filename["pn"])+"/pn_image_300-1000.fits"
    print("ofile",ofile)
    print("pix coords",co)

    #ofile="image.fits"
    
    call = makeImageCall(s, o)
    #print("-----------------")

    call.run(ofile=ofile,expression="PI in [300:1000]")
    print(call.value)
    outdata[st] = call.value
    print("=====================================================")
print()
    
    
for k in outdata.keys():
    print(outdata[k])
    
