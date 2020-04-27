from __future__ import print_function
from astroquery.simbad import Simbad
import astropy.coordinates as coords
import astropy.units as u
import astropy.time as time
import collections
import numpy as np

def coordinate4epoch(co, time, pm, verbose=1):
    """
      Return coordinate for a specific epoch
      
      Parameters
      ----------
        co - Coordinate, astropy.SkyCoord instance
        time - Delta time in years, float 
        pm - array of pm_ra, pm_dec, unit should be astropy.unit.marcsec (milli-arcsec)
        
      Returns
      -------
        new_coord - Coordinate advanced by time, astropy.SkyCoord instance
    """
    
    lst = True
    
    try:
        for x in co:
            pass
        lst = True
    except:
        lst = False
    
    if not lst: #not isinstance(co, collections.Iterable):
        lst = False
        co = [co]
        time = [time]
        pm = [pm]
    ret = []
    
    
    if verbose>3:
        print("properMotion.py -> coordinate4epoch - Info: co, time, pm",co, time, pm)
    
    # Some checks:
    if len(co) != len(time):
        print("properMotion.py -> coordinate4epoch - ERROR: len(co) != len(time). Returning None")
        return None
    if len(co) != len(pm):
        print("properMotion.py -> coordinate4epoch - ERROR: len(co) != len(pm). Returning None")
        return None
    
    for c, t, p in zip(co, time, pm):
      if verbose>3: print("properMotion.py -> coordinate4epoch - Info: c.ra",c.ra)
      x = c.ra + t * p[0] * u.marcsec / np.cos(c.dec)
      y = c.dec + t* p[1] * u.marcsec 
      if verbose>3: print("properMotion.py -> coordinate4epoch - Info: x, y:",x, y)
      tmp = coords.SkyCoord(x, y, frame='fk5')
      if verbose>3: print("properMotion.py -> coordinate4epoch - Info: tmp",tmp.to_string("hmsdms"))
      ret.append(tmp)
      if verbose>3: print("properMotion.py -> coordinate4epoch - Info: ret: ",ret)  
    if not lst:
        return ret[0]
    return ret

if __name__=="__main__":
    x, y = "8:00:00", "6:00:00"
    c = coords.SkyCoord(x+" "+y, frame="irc", unit=(u.hour, u.deg))
    c = coordinate4epoch([c, c], [10.0, 20], 2*[[1000,1000]])
    #c = coordinate4epoch(c, 20, [1000,1000])
    print(c)
