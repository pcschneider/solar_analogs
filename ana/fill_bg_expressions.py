from parameters import *
from astropy.table import Table
#import astropy.io.ascii
#from astropy.io import ascii

dd = Table.read(bgs_ecsv_fn, format='ascii.ecsv', delimiter=',')

for d in dd:
    print(d)
    expr = 
    print()

