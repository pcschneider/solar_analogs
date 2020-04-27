from __future__ import print_function
import glob
from Object import *
from properMotion import coordinate4epoch
from evtWcs import XMMwcs
import astropy.time as time
import pToolsRegion
import pToolsUtils
from scipy.stats import poisson

odata = "orig_data/"


def lim(x, tol=0.95):
    cdf = 0.
    print("   xxxx    ",x)
    y = int(x)
    while cdf < tol:
        y+=1
        cdf = poisson.cdf(y, x)
    return y 

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
        
class Task():
    """
    Perform tasks on Observations
    """
    def __init__(self, obj, obs):
        self.object = obj
        self.observation = obs
        self.value = None
        self.name = "unknown"
    def run(self):
        pass
    def __str__(self):
        return "Task: "+self.name + " value="+str(self.value)
            
    #def __str__(self):
        #return "Task - "+self.name

class PNcounts(Task):
    name = "PNcounts"    
    def __init__(self, obj, obs):
        self.usedRegion = None
        Task.__init__(self, obj, obs)    
    def run(self, verbose=1, region=pToolsRegion.circle((0, 0, 300)), eLo=200, eHi=10000, centerOnSource=True):
        """
          Parameters
          ----------
            region : pToolsRegion instace
                     The coordinates will be set to the center
        """
        fn = self.observation.filename["pn_filt"]
        co = self.object.coordinates(epoch=self.observation.obsDate(which="pn"))
        inp = np.array(co.to_string("decimal", precision=10 ).split()).astype(float)
        pix = self.observation.sky2pix(inp)[0]
        if centerOnSource:
          region.x = float(pix[0])
          region.y = float(pix[1])
        cts = pToolsUtils.eventsInRegion(fn, region, verbose=verbose, eLo = eLo, eHi=eHi)
        self.usedRegion = region
        
        if verbose>3:
            print("PNcounts - analyzing", self.observation)
            print(self.object)
            print(fn, " obsDate: ",self.observation.obsDate())
            print(" Coordinates for observing date: ",co.to_string('hmsdms'))
            print(" pix: ",pix)
            print(" region: ",region)
            print(" cts: ",cts)

        self.value = cts
        return True

#class 

class PNnetCounts(Task):
    name = "PNnetCounts"
    def __init__(self, obj, obs):
        self.ctsTask = PNcounts(obj, obs)
        Task.__init__(self, obj, obs)
    def run(self, verbose=10, eLo=200, eHi=12000):
        self.ctsTask.run(eLo=eLo, eHi=eHi)
        srcCts = self.ctsTask.value
        srcArea = self.ctsTask.usedRegion.area()
        bkg = pToolsRegion.annulus((0,0, 500, 700))
        self.ctsTask.run(region=bkg, eLo=eLo, eHi=eHi)
        bkgArea = self.ctsTask.usedRegion.area()
        bkgCts = self.ctsTask.value
        print("srcCts, bkgCts: ",srcCts, bkgCts)
        lm = lim(bkgCts[0])*srcArea/bkgArea
        print(" upper lim:", lm)
        
        net = srcCts[0] - bkgCts[0]*srcArea/bkgArea
        error = (srcCts[0] + bkgCts[0] * srcArea/bkgArea)**0.5
        error = (lm - bkgCts[0]*srcArea/bkgArea)
        self.value = Value(net, e=error)
        return True

class PNrate(Task):
    def __init__(self, obj, obs):
       self.netTask = PNnetCounts(obj, obs)
       Task.__init__(self, obj, obs) 
    def run(self, eLo=200, eHi=12000, verbose=10):   
        self.netTask.run()
        net = self.netTask.value
        expTime = self.observation.expTime(which="pn")
        self.value = Value(net.value / expTime, e = net.error/expTime)
        return True

class PNflux(Task):
    def __init__(self, obj, obs):
       self.rateTask = PNrate(obj, obs)
       Task.__init__(self, obj, obs) 
    def run(self, eLo=200, eHi=12000, verbose=10, cfc = 1.0):   
        self.rateTask.run()
        rate = self.rateTask.value
        dist = self.object.distance
        print("dist",dist)
        scaling = 4.0 * np.pi * (3.1e18 * dist)**2  * cfc / 0.71 # The latter is the encircled energy correction factor from: http://xmm-tools.cosmos.esa.int/external/sas/current/doc/eupper/node4.html
        self.value = Value(rate.value*scaling , e = rate.error * scaling)
        return True

class PNpixCoords(Task):
    def __init__(self, obj, obs):
        Task.__init__(self, obj, obs)        
        self.name = "PNpixCoords"
    def run(self, verbose=10):
        fn = self.observation.filename["pn_filt"]
        co = self.object.coordinates(epoch=self.observation.obsDate(which="pn", format='decimalyear'))
        inp = np.array(co.to_string("decimal", precision=10 ).split()).astype(float)
        pix = self.observation.sky2pix(inp)
        self.value = pix    
        return True

class makeImageCall(Task):
    """
      Creates the command line call to create a fits image using the SAS tool evselect. 
      
      Details are provided at
      https://heasarc.gsfc.nasa.gov/docs/xmm/abc/node8.html#SECTION00820000000000000000
    """
    name = "makeImageCall"
    def run(self, which="pn", ofile="image.fits", ximagesize=600, yimagesize=600, expression=None):
        """
          Generates the calling sequence.
        """
        fn = self.observation.filename[which]
        epoch = self.observation.obsDate("pn")
        co = self.object.coordinates(epoch=epoch)
        inp = np.array(co.to_string("decimal", precision=10 ).split()).astype(float)
        pix = self.observation.sky2pix(inp)[0]
        x, y = pix[0], pix[1]
        print("fn, epoch, pix", fn, epoch, (x, y))
        out = "evselect table="+fn+" withimageset=yes imageset="+ofile+" xcolumn=X ycolumn=Y imagebinning=imageSize ximagesize=" + str(ximagesize)+ " yimagesize="+str(yimagesize)
        if expression is not None:
            out+=" expression=\""+expression+"\""
        self.value = out
        return True

class ds9call(Task):
    """
      Generate command line call to display the region around the source.
    """
    name = "ds9call"
    def run(self, which="pn", filePostfix = "", extraParams = "", standardParams = "-scale log -scale limits 0 10", regionTextPostfix="", verbose=1):
        """
          Generate the call. Stores the result in ``self.value``.
          
          Parameters
          ----------
          which : string, must be within []
          
          Returns
          -------
            bool : True if successful, False if not
        """
        fn = self.observation.filename[which]
        epoch = self.observation.obsDate("pn")
        co = self.object.coordinates(epoch=epoch)
        inp = np.array(co.to_string("decimal", precision=10 ).split()).astype(float)
        pix = self.observation.sky2pix(inp)[0]
        x, y = pix[0], pix[1]
        print("fn, epoch, pix", fn, epoch, (x, y))
        sourceReg = ' -regions command "circle ' + str(x) + " " + str(y) +  ' 300 # color=red  text='+str(self.object.identifier).replace(" ","")+regionTextPostfix+'"'
        #pix = self.observations
        print(" co: ",co.to_string("hmsdms"))
        pan2 = co.to_string("hmsdms", sep=':') #co.ra.to_string(sep=':') + " " + co.dec.to_string(sep=':', precision=2, pad=True)
        self.value = "ds9 "+fn+filePostfix+" -pan to "+ pan2 + " wcs fk5 " + " " + standardParams + " " + extraParams + sourceReg
        return True
    #def __str__(self):
        #return "Task: " = self.name + " value=" + str(self.value)

        
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
    
    netCts = PNnetCounts(s, o)
    netCts.run(eLo=300, eHi=1000)
    print(netCts)
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
