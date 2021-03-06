from __future__ import print_function
from astropy.io import fits as pyfits
from astroquery.simbad import Simbad
import astropy.coordinates as coords
import astropy.units as u
from properMotion import coordinate4epoch
import astropy.time as time
from XMMobservation import XMMwcs
import numpy as np
from astropy.table import Table

# add fields to the simbad querry, which we need lateron
customSimbad = Simbad()
customSimbad.get_votable_fields()
customSimbad.add_votable_fields('parallax','pm')


class AstroObject():
  """
      Contains information needed for an astronomical object
  """
  def __init__(self, idf, verbose=1):
        self.identifier = idf
        self.coord2000 = None
        self.pm = None
        self.distance = None
        self.properties = None
        self.initialized = False
        self.observations = []
        self.verbose = verbose
  def setCoords(self, co, verbose=1, keepPM=False):
      """
        Set Coordinates of the Object
        
        Parameters
        ----------
        co : Coordinates
             astropy.coordinates.SkyCoord instance
        keepPM : boolean
             keep any possibly existing proper motion information, set to (0, 0) otherwise
      """
      self.coord2000 = co
      if not keepPM:
        self.pm = [0, 0]
        self.initialized = True
  def populateFromSimbad(self, verbose=1):
        """
          Read information from Simbad using ``astroquerry``.
        """
        result_table = customSimbad.query_object(self.identifier)
        if verbose>2:
            print("AstroObject.py -> AstroObject::populateFromSimbad - Info: Data returned from Simbad:")
            print(result_table)
            #print(dir(result_table), result_table.colnames)
        if len(result_table) != 1:
            print("More than one object found!")
            self.initialized = False
        else:
            x, y = result_table.field("RA")[0], result_table.field("DEC")[0]
            pm_ra, pm_dec = result_table.field("PMRA")[0], result_table.field("PMDEC")[0]
            plx = result_table.field("PLX_VALUE")[0]
            self.distance = 1000./float(plx)
            #print("plx: ",plx)
            co = coords.SkyCoord(x, y, frame='fk5', unit=(u.hour, u.deg))
            self.coord2000 = co
            self.pm = [pm_ra, pm_dec]
            self.initialized = True
  def coordinates(self, epoch=2000., epochFormat="decimalyear", verbose=1):
        #print("xxxxxxxxxxxxxxxxX", epoch, type(epoch))
        if not isinstance(epoch, time.Time):
            epoch = time.Time(epoch, format=epochFormat)
        deltaTime = epoch.decimalyear - 2000.
        newCoord = coordinate4epoch(self.coord2000, deltaTime, self.pm, verbose=verbose)
        if verbose>2:
            print(self.identifier, self.coord2000.to_string('hmsdms'), newCoord.to_string('hmsdms'))
        return newCoord
  def __str__(self):      
      if self.initialized:
        return self.identifier+":\n Coordinates (2000): "+self.coord2000.to_string('hmsdms') +"\n Proper Motion: " + str(self.pm) + "\n"
      else:
        return "AstroObject instance not initialized"


def get_filename(fn, parameter):
    parameters = __import__(fn[0:-3])
    pm = getattr(parameters, parameter)
    return pm

class ObservedObject(AstroObject):
    def __init__(self, idf, parameters_fn=None, verbose=1):
        AstroObject.__init__(self, idf, verbose=verbose)
        self.gatherObservations(parameters_fn)
        
    def gatherObservations(self, parameters_fn):    
        #exec(open(parameters_fn).read())
        ##parameters = __import__(parameters_fn[0:-3])
        Xobs_ecsv_fn = get_filename(parameters_fn, 'Xobs_ecsv_fn')
        xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';') 
        gi = np.where(xobs["target"] == self.identifier)[0]
        if len(gi)>0:
            print(self.identifier, xobs["obsID"][gi].data, xobs["observatory"][gi].data,  xobs["directory"][gi].data)
    def getOMcenroid(self):
        parameters = __import__(parameters_fn[0:-3])
        Xobs_ecsv_fn = getattr(parameters, 'Xobs_ecsv_fn')
        
if __name__ == "__main__":
    #o = AstroObject("HD 25874")
    o = AstroObject("HD 210918")
    #o.populateFromSimbad()
    print(o)
    o.setCoords(coords.SkyCoord("6.1777285 -53.983998", frame="fk5", unit=(u.deg, u.deg)))
    co = o.coordinates(epoch=2016.8)
    xmmFn = "../../data/HD210918/0784240901/orig_data/3007_0784240901_EPN_S003_ImagingEvt_filt.fits"
    #o.pixPosXMM(xmmFn, )
    #print(o.skyPosXMM(xmmFn, np.array([24000,28000])))
