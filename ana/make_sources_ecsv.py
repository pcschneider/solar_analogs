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

sources_dd = Table.read(observed_sources_fn, format='ascii.ecsv', delimiter=',')
print(sources_dd["name"])


xx, yy, = [], []
ois = []
ras, decs = [], []

for star in sources_dd:
    st = star["name"]
    dr = "../data/"+st.replace(" ","")
    oi = glob.glob(dr+"/0*")[0][-10:]
    ois.append(oi)
    o = XMMobservation(oi)
    o.baseDir = dr
    o.initializeFilenames()
    print(o, o.filename["pn"])
    
    s = AstroObject(st)
    s.populateFromSimbad()
    ra, dec = s.coordinates().ra.degree, s.coordinates().dec.degree
    ras.append(ra)
    decs.append(dec)
    
    print(ra, dec)
    co = PNpixCoords(s, o)
    co.run()
    print(co.value)
    xx.append(co.value[0][0])
    yy.append(co.value[0][1])
    print()
    


oo = Table([sources_dd["name"], ois, ras, decs, xx, yy], names=['name', 'obsID','RA', 'Dec', 'src_x', 'src_y'])
oo.write(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')