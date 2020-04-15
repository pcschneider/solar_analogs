import parameters as pm
from astropy.table import Table
import glob 
import numpy as np

ofn = "props.tex"
oo = open(ofn,"w")

fn = pm.observed_sources_fn
dd = Table.read(fn, format='ascii.ecsv', delimiter=',')
print(dd["name"].data)

fn = pm.stellar_props_fn
#fn = "test.ecsv"
props = Table.read(fn, format='ascii.ecsv', delimiter=',')
prop_names = np.array([star[0] for star in props])

header = """
\\begin{table*}
  \centering
  \\begin{tabular}{rccccccccl}
    \hline
    \hline
    Target & Mass      & \multicolumn{3}{c}{Age} & $\log R'_{\mathrm{HK}}$ & Vmag & Gmag &  Distance & Refs\\\\
           & $M_\odot$ & min & nominal & max     &                       &      &      & (pc) & \\\\ 
    \hline       
"""


footer = """
    \hline
  \end{tabular}
  
   \\tablebib{
(1)~\citet{Ramirez_2014}; (2) \citet{Gaia_2016}; \citet{Gaia_2018};
}
\end{table*}
"""
oo.write(header)

#dirs = glob.glob("../data/HD*")
#for f in dirs:
    #star = f.split("/")[2].replace("HD", "HD ")
si = np.argsort(props["R_HK"])    
for star in prop_names[si]:    
    
    ol=""
    print("\"%s\"" % star)
    print(star[-2:])
    if star[-2:] == "_2": continue

    idx = np.where(star == prop_names)[0]
    print(idx)
    if len(idx)==0: 
        ol= str("%s \\\\ \n" % star)
    else:
        pp = props[idx]
        ol+=str("%s & %4.2f$\pm$%4.2f & %4.2f & %4.2f & %4.2f & %4.2f & %4.2f & %4.2f & %4.2f & 1, 2 \\\\ \n" % (pp["name"][0], pp["Mass"], pp["Mass_err"], pp["age_min"],  pp["age"],pp["age_max"], pp["R_HK"], pp["Vmag"], pp["Gmag"], pp["distance"] ))
    print(ol)
    #columns = ["Target", "Vmag", "Gmag", "Mass","]
    
    
    print()
    oo.write(ol)
oo.write(footer)    
oo.close()    
