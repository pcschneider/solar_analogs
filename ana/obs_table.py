import sys
sys.path.append("tools")
from parameters import *
from astropy.table import Table
import glob
import numpy as np
from astropy.io import fits as pyfits
from astropy.time import Time

print("Reading ",Xobs_ecsv_fn)  
xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';') 
print("Reading ",sources_ecsv_fn)  
srcs = Table.read(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')

oo = open("obs.tex","w")

header = """
\\begin{table}
  \centering
  \\begin{tabular}{ccccc}
    \hline
    \hline
    Target & Observatory & Obs ID & Date & Exp Time \\\\
           &              &       &      & (ks) \\\\ 
    \hline       
"""

footer = """
    \hline
  \end{tabular}
\end{table}
"""
oo.write(header)


for i, src in enumerate(sorted(srcs["name"])):
    print(src, end=" ")
    si = np.where(srcs["obsID"] == xobs["obsID"][i])[0]
    
    print(si, end=" ")
    if len(si)==0: continue

    obse = xobs["observatory"][si].data[0]
    print(obse)

    dr = xobs["directory"][si].data[0]
    fn = dr+"/pn.fits"
    obsid = xobs["obsID"][si].data[0]
    #print(type(dr))
    print(xobs["obsID"][si].data, dr, fn)
    try:
        ff = pyfits.open(fn)
    except FileNotFoundError:
        pass
    tt = ff[0].header["DATE-OBS"]
    print(tt)
    t = Time(tt, format='isot').to_value("decimalyear")
    du = ff[0].header["DURATION"]/1e3
    
    oo.write("%s & %s & %s & %7.3f & %5.1f \\\\ \n" % (src, obse, obsid, t, du))
    
    print(t)
    print()
    
oo.write(footer)
oo.close()
    

