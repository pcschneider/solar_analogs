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
\caption{Log of X-ray observations\label{tab:obs}}

  \centering
  \\begin{tabular}{rcccr}
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


hdn = [int(a[3:]) for a in xobs["target"]]
hdi = np.argsort(hdn)

for si in hdi:
    src  = xobs["target"][si]
    print(src, end=" ")
    
    dr = xobs["directory"][si]
    fn = dr+"/pn.fits"
    obsid = xobs["obsID"][si]
    
    
    obse = xobs["observatory"][si]
    print(obse)

    
    i = np.where(srcs["obsID"] == xobs["obsID"][si])[0]
    
    print(i, si, end=" ")
    #if len(i)==0:
        #oo.write("%s \\\\ \n" % src)
        #print()
        #print()
        #continue

    
    #print(type(dr))
    print(obsid, dr, fn)
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
    

