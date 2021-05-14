from __future__ import print_function

from astropy.io import fits as pyfits
#import wcs
import collections
import astropy.coordinates as coords
import astropy.units as u
from astropy import wcs
import numpy as np

class WCS:
    def __init__(self, fn):
       self.filename = fn  
       self.read(self.filename)
    def read(self, fn, ext=1):   
       self.ff = pyfits.open(fn)
       self.header = self.ff[ext].header
       
       
class XMMwcs(WCS):
    def __init__(self, fn):
       WCS.__init__(self, fn)
       
       ref_ra  = self.header["TCRPX6"]
       ref_dec = self.header["TCRPX7"]
       val_ra  = self.header["TCRVL6"]
       val_dec = self.header["TCRVL7"]
       dlt_ra  = self.header["TCDLT6"]
       dlt_dec = self.header["TCDLT7"]
       typ_ra = self.header["TCTYP6"]
       typ_dec = self.header["TCTYP7"]
       self.wcs = wcs.WCS(naxis=2)
       self.wcs.wcs.crpix = np.array([ref_ra, ref_dec])
       self.wcs.wcs.cdelt = np.array([dlt_ra, dlt_dec])
       self.wcs.wcs.ctype = [typ_ra, typ_dec]
       self.wcs.wcs.crval = np.array([val_ra, val_dec])

       #self.wcs.wcs.print_contents()
       
    def pix2sky(self, arr, verbose=2):
        lst = True
        if not isinstance(arr[0], collections.Iterable):
            arr = [arr]
            lst = False
        ret = self.wcs.wcs_pix2world(arr, 1)
        if verbose>1:
            print("ret: ",ret)
        if not lst:
            return ret[0]
        return ret
    def sky2pix(self, arr):
        lst = True
        if not isinstance(arr, collections.Iterable):
            arr = [arr]
            lst = False
        ret = []  
        arr = [arr]
        ret = self.wcs.wcs_world2pix(arr, 1)
        if not lst:
            return ret[0]
        return ret
    

if __name__ == "__main__":        
    xmm = XMMwcs("../../data/HD114174/0784240301/odata/3042_0784240301_EPN_S003_ImagingEvt_filt.fits")

    #pixcrd = np.array([[0, 0], [24, 38], [45, 98]], np.float_)
    #print(xmm.wcs.wcs_pix2world(pixcrd, 1))
    #exit()
    x = xmm.pix2sky(np.array([24000,28000]))
    print(x)
    #print(x.to_string('decimal'))
    #x, y = "8:00:01", "6:00:01"
    #c = coords.SkyCoord(x+" "+y, frame="fk5", unit=(u.hour, u.deg))
    #x, y = "197.30215278","5.23226389"
    #c = coords.SkyCoord(x+" "+y, frame="fk5", unit=(u.deg, u.deg))
    print(xmm.sky2pix(x))
