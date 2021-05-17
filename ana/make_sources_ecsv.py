from __future__ import print_function
import sys
sys.path.append("tools")
from parameters import *
from astropy.table import Table
import glob
from tools.Object import *
from tools.Tasks import *
from tools.Observation import *

radius = 300

#sources_dd = Table.read(observed_sources_fn, format='ascii.ecsv', delimiter=',')
xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';')
print(" Creating source positions for ",len(xobs["target"]), " targets.")
print()
nothing = []
xx, yy, = [], []
ois, stars = [], []
ras, decs = [], []
odates = []
raobs, decobs = [], []
fnames = []

gi = np.where(xobs["observatory"] == "XMM")

for st, dr in zip(xobs["target"][gi], xobs['directory'][gi]):

    dr = "../data/"+st.replace(" ","")
    print(dr)
    
    oi = glob.glob(dr+"/0*")[0][-10:]
    o = XMMobservation(oi)
    o.baseDir = dr
    try:
        o.initializeFilenames()
    except Exception as ee:
        print(ee)
        print(80*"=")
        print()
        nothing.append((st, dr))

        continue
    
    ois.append(oi)
    stars.append(st)
    print(o, o.filename["pn"])
    
    s = AstroObject(st)
    s.populateFromSimbad()
    co = s.coordinates()
    #print(co)
    ra, dec = co.ra.degree, co.dec.degree
    #print(ra, dec)
    
    ras.append(ra)
    decs.append(dec)
    odate = o.obsDate(which="pn", format='decimalyear')
    co_obs = s.coordinates(epoch=odate)
    #print(co_obs)
    odates.append(odate)
    raobs.append(co_obs.ra.degree)
    decobs.append(co_obs.dec.degree)
    fnames.append(o.filename["pn"])
    print(raobs[-1], decobs[-1])
    print(ra, dec)
    co = PNpixCoords(s, o)
    co.run()
    print(co.value)
    xx.append(co.value[0][0])
    yy.append(co.value[0][1])
    print(80*"=")
    print()
    
print("Nothing for: ", nothing)    
    
#print(stars, ois, ras, decs, odates, raobs, decobs, xx, yy)

oo = Table([stars, ois, ras, decs, odates, raobs, decobs, xx, yy, fnames], names=['name', 'obsID','RA', 'Dec', 'obs_epoch', 'RA_obs', 'Dec_obs', 'src_x', 'src_y', "pn_filename"])
oo.write(sources_ecsv_fn, format='ascii.ecsv', delimiter=',', overwrite=True)
