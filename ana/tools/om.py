from astropy.io import fits as pyfits
import numpy as np
import matplotlib.pyplot as plt
import astropy.coordinates as C
import glob
from astropy import wcs

class OM():
    glob_strings = {"images":"*SIMA*.FIT", "srclists":"*SWSRLI*"}
    def __init__(self, dr):
        """
          Parameters
          ----------
          dr : str, directory
        """
        self.directory = dr
        self.images = []
        self.srclists = []
        self.populate()
        
    def populate(self, dr=None):
        """
          Use glob strings to populate the filename arrays
        """
        if dr is not None: self.directory = dr
        
        for k in OM.glob_strings:
            string =self.directory+"/"+OM.glob_strings[k]
            print("OM::populate -- Checking ",k," (",string,")", end="")
            fnames = glob.glob(string)
            print("... found",len(fnames), "files")
            setattr(self, k, fnames)
            #print(k, lst)
            
    #def source_positions(self, dist_cutoff=2.):
        #"""
          #Sky coordinates of all sources
          
          #Parameters
          #----------
            #dist_cutoff : float (in arcsec)
                #Sources within this distance are considered to be the same
          #Returns
          #-------
          #SkyCoords instance
        #"""
        
        #crds = []
        #for fn in self.srclists:
            #print("OM::source_positions -- checking:  ",fn) 
            #ff = pyfits.open(fn)
            #ra, dec = ff[1].data["RA"], ff[1].data["DEC"]
            #rate = ff[1].data["CORR_RATE"]
            #coords = C.SkyCoord(ra, dec, unit=("deg", "deg"), frame='icrs')
            #if len(crds)==0: 
                #crds=coords
                #continue
            #for c in crds:
                #dist = c.separation(coords).arcsec
                #gi = np.where(dist>2)[0]
                #for i in gi:
                    #crds.append(c)
        #return crds
    
    def source_positions(self, dist_cutoff=None):
        """
          Sky coordinates of all sources
          
          Parameters
          ----------
            dist_cutoff : float (in arcsec)
                Sources within this distance are considered to be the same
          Returns
          -------
          SkyCoords instance
        """
        
        crds = {}
        for fn in self.srclists:
            
            print("OM::source_positions -- checking:  ",fn) 
            ff = pyfits.open(fn)
            idf = fn[-20:-14]
            obsid = ff[0].header["OBS_ID"]
            print(obsid, idf)
            try:
                ra, dec = ff[1].data["RA"], ff[1].data["DEC"]
            except:
                print(fn," does not contain RA, Dec coordinates.")
                continue
            rate = ff[1].data["CORR_RATE"]
            coords = C.SkyCoord(ra, dec, unit=("deg", "deg"), frame='icrs')
            tc = []
            ci = []
            for i, c in enumerate(coords):
                #print(c)
                if len(tc) == 0: 
                    tc.append(c.to_string("hmsdms",sep=':', precision=2, pad=True))
                    ci.append(i)
                    continue
                #print(c, tc, sc)
                dist = c.separation(coords[ci]).arcsec
                #print("dist: ",dist)
                gi = np.where(dist>2)[0]
                for j in gi:
                    tc.append(c.to_string("hmsdms",sep=':', precision=2, pad=True))
                    #ci.append(j)
            if len(tc)>0:
                crds[idf] = tc
            #else:
        if len(crds) == 0:
            return None
        return {obsid:crds}
    
    
    
    
    def ds9_line(self, center_coordinates, width=20 ):
        """
          Image array for specified position
          
          Parameters
          ----------
          width : integer, in pixels
        """
        for fn in self.images:
            print(fn)
            ff = pyfits.open(fn)
            w = wcs.WCS(ff[0].header)
            co = center_coordinates
            print(co.ra.deg, co.dec.deg )
            #pix = w.wcs_world2pix([co.ra], [co.dec], 0)
            #for a, b, in zip(pix[0], pix[1]):
                #print(a,b)
                #a0, a1 = a-width/2, a+width/2
                #b0, b1 = b-width/2, b+width/2
                #a0, a1, b0, b1 = int(a0[0]), int(a1[0]), int(b0[0]), int(b1[0])
                #print(a0, a1, b0, b1)
                #im = ff[0].data[b0:b1,a0:a1 ]
                #plt.imshow(im, origin="lower", extent=(b0,b1,a0,a1))
                #plt.scatter(b, a, marker='x', color='r', s=30)
                ##plt.scatter(a, b, marker='o', color='r', s=30)
                #plt.show()
            ds9string = str("ds9 %s -pan to %f %f wcs -zoom 16-cmap b -colorbar no -cmap invert yes "% (fn, co.ra.deg, co.dec.deg))
            print(ds9string)
                
            #print(pix)
            print()
            
if __name__ == "__main__":
    om = OM("../../data/HD2071/0784240101/odata/omf")
    c = om.source_positions()
    print(c)
    #im = om.ds9_line(c)
    
    
        
