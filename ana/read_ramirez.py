import numpy as np
import parameters as pm
from astroquery.simbad import Simbad
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import time
from requests.exceptions import HTTPError


ofn = pm.stellar_props_fn
#ofn = "test.ecsv"
print("Writing to \"%s\"..." % ofn)
print()

tab2 = np.genfromtxt("../tables/tab2.dat", unpack=False, skip_header=6, delimiter='\t')
HDs2 = np.genfromtxt("../tables/tab2.dat", unpack=True, skip_header=6, delimiter='\t', dtype=str)[1]
HDs2 = np.array([HD[0:-1] for HD in HDs2])

tab4 = np.genfromtxt("../tables/tab4.dat", unpack=False, skip_header=6, delimiter='\t')
HDs4 = np.genfromtxt("../tables/tab4.dat", unpack=True, skip_header=6, delimiter='\t', dtype=str)[1]
HDs4 = np.array([HD[0:-1] for HD in HDs4])

header = """
# %ECSV 0.9
# ---
# datatype:
# - {name: name, datatype: string}
# - {name: Teff, datatype: float, description: effective temperature}
# - {name: Teff_err, datatype: float, description: error on effective temperature}
# - {name: Teff_ref, datatype: str, description: reference for effective temperature}
# - {name: Mass, datatype: float, description: stellar mass in solar units}
# - {name: Mass_err, datatype: float, description: error on mass}
# - {name: Mass_ref, datatype: string, description: reference for mass}
# - {name: age, datatype: float, description: Age in Gyrs}
# - {name: age_min, datatype: float, description: Age in Gyrs}
# - {name: age_max, datatype: float, description: Age in Gyrs}
# - {name: age_ref, datatype: str, description: reference for age}
# - {name: Vmag, datatype: float, description: optical brightness}
# - {name: R_HK, datatype: float, description: log activity index}
# - {name: R_HK_ref, datatype: str, description: activity index reference}
# - {name: Gmag, datatype: float, description: Gaia magnitude}
# - {name: distance, datatype: float, description: distance in pc}
name, Teff, Teff_err, Teff_ref, Mass, Mass_err, Mass_ref, age, age_min, age_max, age_ref,Vmag,  R_HK, R_HK_ref, Gmag, distance
"""

oo = open(ofn, "w")
oo.write(header)

for s in sorted(pm.stars):
    #print(s)
    hdn = str(s[3:])
    idx2 = np.where(HDs2==hdn)[0]
    idx4 = np.where(HDs4==hdn)[0]
    print(s, idx2, idx4)
    
    ol=""
    try:
        # Teff
        
         # Teff
        dd = tab4
        idx = idx4
        
        val = dd[idx][0][2]
        err = dd[idx][0][3]
        
        print("Name,        Teff, Teff err, ref,          Mass, Mass err, ref,                Age, min, max,    ref,   Vmag,     R'_HK,      ref")
        #print("\"HD %s\", " % hdn, end="")
        #print(val,", ",err,", \"Ramirez 2014\", ", end ="")
        ol+=str("\"HD %s\", " % hdn)
        ol+=str("%f, %f, \"Ramirez 2014\", " % (val, err))
        
        
        # mass
        val = dd[idx][0][10]
        err = dd[idx][0][11]
        ol+=str("%f, %f, \"Ramirez 2014\", " % (val, err))

        # age
        val = dd[idx][0][12]
        val0 = dd[idx][0][13]
        val1 = dd[idx][0][14]
        #print(val,", ",val0, ", ",val1,", \"Ramirez 2014\",",end="") 
        ol+=str("%f, %f, %f, \"Ramirez 2014\", " % (val, val0, val1))
        
        dd = tab2
        idx = idx2
        
        Vmag = dd[idx][0][2]
        R_HK = dd[idx][0][6]
        #print("Name,        Vmag     R'_HK         ref")
        #print("\"HD %s\", " % hdn, end="")
        ol+=str("%s, %s, \"Ramirez 2014\", " % (Vmag, R_HK))
        #print(Vmag,", ",R_HK,", \"Ramirez 2014\"")        
        print(ol)        
    except IndexError:
        ol+=str("\"HD %s\",  " % hdn)
        ol+=13*", "
    except Exception as ee:
        print(ee)
    
    
    result_table = Simbad.query_object(s)
    ra, dec = result_table["RA"].data[0], result_table["DEC"].data[0]
    
    print(ra, dec)
    coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg), frame='icrs')
    print(coord)
    try:
        j = Gaia.cone_search_async(coord, 0.3*u.arcmin)
        r = j.get_results()
        #print(r.columns)
        r.sort("phot_g_mean_mag")  
        print(r["phot_g_mean_mag"].data)
        ol+=str("%f, %f" % (r["phot_g_mean_mag"].data[0], 1000/r["parallax"].data[0]))
        #r.pprint_all()
    except HTTPError:     
        print("FAILED")
    except Exception as ee:
        print(ee)
        pass
    
    print(ol)
    oo.write(ol+"\n")
    print()
    
oo.close()
