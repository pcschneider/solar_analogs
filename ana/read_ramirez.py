import numpy as np
import parameters as pm

ofn = pm.stellar_props_fn
ofn = "test.ecsv"
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
# - {name: Mass_ref, datatype: float, description: reference for mass}
# - {name: age, datatype: float, description: Age in Gyrs}
# - {name: age_min, datatype: float, description: Age in Gyrs}
# - {name: age_max, datatype: float, description: Age in Gyrs}
# - {name: age_ref, datatype: str, description: reference for age}
# - {name: distance, datatype: float, description: distance in pc}
# - {name: R_HK, datatype: float, description: log activity index}
# - {name: R_HK_ref, datatype: str, description: activity index reference}
# - {name: Vmag, datatype: float, description: optical brightness}
name, Teff, Teff_err, Teff_ref, Mass, Mass_err, Mass_ref, age, age_min, age_max, age_ref,Vmag,  R_HK, R_HK_ref, distance
"""

oo = open(ofn, "w")
oo.write(header)

for s in pm.stars:
    #print(s)
    hdn = str(s[3:])
    idx2 = np.where(HDs2==hdn)[0]
    idx4 = np.where(HDs4==hdn)[0]
    print(s, idx2, idx4)
    
    
    try:
        # Teff
        
         # Teff
        dd = tab4
        idx = idx4
        
        val = dd[idx][0][2]
        err = dd[idx][0][3]
        ol=""
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
        
        oo.write(ol+"\n")
    except IndexError:
        pass
    except Exception as ee:
        print(ee)
    
    print()
    
oo.close()
