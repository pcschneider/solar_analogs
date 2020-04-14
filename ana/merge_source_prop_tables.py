from astropy.table import Table, vstack, hstack, join
import numpy as np
from parameters import *

t0 = Table.read(xspec_fluxes_fn, format='ascii.csv', delimiter=',', comment='#', names=("source", "obsID", "flux_lo", "flux", "flux_hi", "rate", "rate_err"))
t1 = Table.read(extracted_photons_fn, format='ascii.ecsv', delimiter=',')  

rows = []       
for targ in t1["source"]:
  print(targ)
  si = np.where(t0["source"] == targ)[0]
  print(t0[si])
  
  print()
  
t0["obsID"] = t0["obsID"].astype(str)
t1["obsID"] = t1["obsID"].astype(str)
  
merged = hstack([t0, t1])
merged = join(t0, t1, keys='source', join_type='outer')
print()
print(merged)
  
merged.write(primary_source_props_fn, format='ascii.ecsv', delimiter=',')  
  
#primary_source_props_fn = "../data/tabels/primary_source_props.ecsv"