from __future__ import print_function
import glob
from Object import *
from properMotion import coordinate4epoch
from evtWcs import XMMwcs
import astropy.time as time
import pToolsRegion
import pToolsUtils
import Tasks

odata = "orig_data/"
odata = "odata/"

class Value():
    """
      Class that holds value and error, but behaves like normal floats otherwise
    """
    def __init__(self, v, e=None):
        self.value = v 
        self.error = e
    def __float__(self):
        return float(self.value)
    def __int__(self):
        return int(self.value)
    def __add__(self, x):
        return float(self) + x
    def __radd__(self, x):
        return float(self) + x
    def __sub__(self, x):
        return float(self) - x 
    def __rsub__(self, x):
        return float(self) - x 
    def __str__(self):
        if self.error is not None:
            return str(self.value) +"+-"+str(self.error)
        return str(self.value)

class Observation():
  """
      Base class to derive specific incarnations
  """
  def __init__(self):
      self.filename = {}
      self.filenamesInitialized = False
  #def addAnalyzer(self, an):
      ## check if a similarly names analyzer already exists
      #if an.name in self.analyzers.keys():
          #print("Observation.py -> Observations::addAnalyzer - Error Cannot add analyzer named ",an.name)
      #else:
        #self.analyzers[an.name] = an
        #self.analyzers[an.name].observation = self
  #def runAnalyzer(self, name, **kwargs):
      #"""
        #Run the analyzer given and return (value, error)
      #"""
      #if name in self.analyzers.keys():
          #self.analyzers[name].run()
  #def __getitem__(self, name):
      #"""
        #Shortcut to run the analyzer
      #"""
      #self.runAnalyzer(name)
      #return self.analyzers[name].value

class XMMobservation(Observation):
    """
      Contains the routines needed to deal with XMM data
    """
    knownFiletypes = ["pn","pn_filt"]
    def __init__(self, idf):
        self.obsID = idf
        self.baseDir = None
        self.obsDates = {}
        self.expTimes = {}
        self.wcs = {}
        Observation.__init__(self)
    def expTime(self, which="pn", method="glob", verbose=10):
        """
        Get the exposure time for specific instrument
        
        Parameters
        ----------
        which : string
              must be in ["pn"]
        method : string
              passed to self.filename to construct the filename
              
        Returns
        -------
        float - Exposure time
        """
        try:
            return self.expTimes[which]
        except:
            if self.filenamesInitialized:
                fn = self.filename[which]
                if verbose>10: print("fn",fn)
                ff = pyfits.open(fn)
                tmp = ff[1].header["ONTIME"]
                self.expTimes[which] = tmp
                return tmp
            else:
                print("Observation.py -> XMMobservation::obsDate - ERROR: filenames not initialized!")
                return False
    def obsDate(self, which="pn", method="glob", verbose=4):
        """
        Get observation date.
        
        Parameters
        ----------
        which : string
              must be in ["pn"]
        method : string
              passed to self.filename to construct the filename
              
        Returns
        -------
        astropy.time instance
        """
        try:
            return self.obsDates[which]
        except:
            if self.filenamesInitialized:
                fn = self.filename[which]
                if verbose>10: print("fn",fn)
                ff = pyfits.open(fn)
                dd = ff[0].header["DATE-OBS"]
                tmp = time.Time(dd, format="fits")
                self.obsDates[which] = tmp
                return tmp
            else:
                print("Observation.py -> XMMobservation::obsDate - ERROR: filenames not initialized!")
                return False
    def download(self, which="pps"):
        """
          Download data from XMM archive
          
          Not implemented yet
        """
        return False
    def initializeFilenames(self, method="glob", verbose=1):
        """
          Initialize Filename with the given method. The mehtod
          is passed to ``createFilename``.
          
          Prameters
          ---------
            method - string, must be in ["glob"]
        """
        if self.baseDir != None:
            for idf in XMMobservation.knownFiletypes:
                self.filename[idf] = self.createFilename(idf, method=method, verbose=verbose)
            self.filenamesInitialized = True    
        else:
            self.filenamesInitialized = False
            if verbose>0:
                print("Observation.py -> XMMobservation::initializeFilenames - ERROR: baseDir not set")
    def createFilename(self, idf, method='glob', verbose=1):
        """
        Get real filename for specific filetypes like pn_filt.fits
          
        Parameters
        ----------
        idf : string
              identifies the filetype (must be in \'knownFiletypes\')
        method : string, default: "glob"
                 Determines how the filename is generated.

        Returns
        -------
        path : string, relative path
        """
        if idf not in XMMobservation.knownFiletypes:
            if verbose>0:
                print("Observation.py -> XMMobservation::filename - ERROR: Don't know anything of ",idf)
                return False
        if idf == "pn_filt":
            if method == "glob":
                fnames = glob.glob(self.baseDir+"/"+self.obsID+"/"+odata+"*EPN*ImagingEvt_filt.fits")
                if len(fnames) == 1:
                  return fnames[0]
                else:
                   print("Observation.py -> XMMobservation::filename - ERROR: More than file matches glob string (",idf," -> ",st,")")
                   return False
        if idf == "pn":
            if method == "glob":
                st = self.baseDir+"/"+self.obsID+"/"+odata+"*EPN*ImagingEvts.ds"
                fnames = glob.glob(st)
                if len(fnames) == 1:
                  return fnames[0]
                else:
                   print("Observation.py -> XMMobservation::filename - ERROR: More than file matches glob string (",idf," -> ",st,")")
                   return False
            return False
    def sky2pix(self, coords, which="pn"):
        """
          Get pixel coordinates
          
          Parameters
          ----------
          coords : astropy.coord instance  
          which : string, must be in ["pn"]
          
          Returns
          -------
            Pixelcoordinates : 
        """
        if which not in XMMobservation.knownFiletypes:
            print("Observation.py -> XMMobservation::sky2pix - ERROR: which (",which,") not known!")
            return False
        try:
          self.wcs[which]
        except:
            if self.filenamesInitialized:
                self.wcs[which] = XMMwcs(self.filename[which])
            else:
                print("Observation.py -> XMMobservation::sky2pix - ERROR: Filenames not initialized!")
                return False
        pix = self.wcs[which].sky2pix(coords)
        return pix
        
    def __str__(self):
        return "XMMobservation - ObsID: "+str(self.obsID)
        
        
if __name__ == "__main__":

    s = AstroObject("HD 2071")
    s.populateFromSimbad()
    #s.setCoords(coords.SkyCoord("6.1777285 -53.983998", frame="fk5", unit=(u.deg, u.deg)))
    
    o = XMMobservation("0784240101")
    o.baseDir = "../../data/HD2071"
    o.initializeFilenames()
    o.obsDate("pn")
    
    #pnPix = PNpixCoords(s, o)
    #pnPix.run()
    #print(pnPix)
    
    #netCts = Tasks.PNrate(s, o)
    #netCts.run(eLo=300, eHi=1000)
    #print(netCts)
    
    netCts = Tasks.PNflux(s, o)
    netCts.run(eLo=300, eHi=1000, cfc = 3.185e-12) 
    print(netCts)
    
    
    ll = Tasks.ds9call(s, o)
    ll.run()
    print(ll.value)
    #exit()
    
    #srcCts = PNcounts(s, o)
    ##reg = pToolsRegion.circle((0, 0, 300))
    #srcCts.run()#region = reg)
    #print(srcCts)
    #exit()
    
    #call = ds9call(s, o)
    #call.run(filePostfix="[PI=300:1000]", extraParams="-bin factor 16 -zoom 4")
    #print(call)
    
    #pnc = PNcounts(s)
    #o.addAnalyzer(pnc)
    #print(o["PNcounts"])
