from __future__ import print_function
import pyfits
from astroquery.simbad import Simbad
import astropy.coordinates as coords
import astropy.units as u
from properMotion import coordinate4epoch
import astropy.time as time
from XMMobservation import XMMwcs
import numpy as np

# add fields to the simbad querry, which we need lateron
customSimbad = Simbad()
customSimbad.get_votable_fields()
customSimbad.add_votable_fields('parallax','pm')


class AstroObject():
  def __init__(self, idf, verbose=1):
        self.identifier = idf
        self.coord2000 = None
        self.pm = None
        self.properties = None
        self.initialized = False
        self.observations = []
        self.verbose = verbose
  def populateFromSimbad(self, verbose=1):
        result_table = customSimbad.query_object(self.identifier)
        if verbose>2:
            print("AstroObject.py -> AstroObject::populateFromSimbad - Info: Data returned from Simbad:")
            print(result_table)
        if len(result_table) != 1:
            print("More than one object found!")
            self.initialized = False
        else:
            x, y = result_table.field("RA")[0], result_table.field("DEC")[0]
            pm_ra, pm_dec = result_table.field("PMRA")[0], result_table.field("PMDEC")[0]
            co = coords.SkyCoord(x, y, frame='fk5', unit=(u.hour, u.deg))
            self.coord2000 = co
            self.pm = [pm_ra, pm_dec]
            self.initialized = True
  def coordinates(self, epoch=2000., epochFormat="decimalyear", verbose=1):
        if not isinstance(epoch, time.Time):
            epoch = time.Time(epoch, format=epochFormat)
        deltaTime = epoch.decimalyear - 2000.
        newCoord = coordinate4epoch(self.coord2000, deltaTime, self.pm, verbose=verbose)
        print(self.identifier, self.coord2000.to_string('hmsdms'), newCoord.to_string('hmsdms'))
        return newCoord
  def __str__(self):      
      if self.initialized:
        return self.identifier+":\n Coordinates (2000): "+self.coord2000.to_string('hmsdms') +"\n Proper Motion: " + str(self.pm) + "\n"
      else:
        return "AstroObject instance not initialized"
      
if __name__ == "__main__":
    #o = AstroObject("HD 25874")
    o = AstroObject("HD 210918")
    o.populateFromSimbad()
    print(o)
    co = o.coordinates(epoch=2016.8)
    xmmFn = "../../data/HD210918/0784240901/orig_data/3007_0784240901_EPN_S003_ImagingEvt_filt.fits"
    #o.pixPosXMM(xmmFn, )
    print(o.skyPosXMM(xmmFn, np.array([24000,28000])))