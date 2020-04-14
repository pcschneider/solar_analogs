from astropy.table import Table
import glob
import os
from os.path import expanduser

def create_directory(row, prefix="~/hdd/Xdata/Analogs/data/"):
    """
      create the home-relative directory based on target name
    """
    nn = row["name"].replace(" ", "")
    home = expanduser("~")
    prefix = prefix.replace("~", home)
    
    rr = prefix+nn+"/"+row["obsID"]    
    if os.path.isdir(rr):
      dd = os.listdir(rr)
      if "odata" not in dd:
          print("odata not found!", rr)
    else:
      print(rr," does not exist!")
    return rr

fn = "observed_targets.ecsv"
dd = Table.read(fn, format='ascii.ecsv', delimiter=',')

for d in dd:
    #print(d)
    cc = create_directory(d)
    
#print(dd, len(dd))
dd.write("t.tex", format='latex')