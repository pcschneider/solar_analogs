from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pickle
import matplotlib
from parameters import *
from astropy.table import Table

matplotlib.rcParams['font.size'] = 16

vsini = {"HD 2071":1.79,\
    "HD 42618":1.83,\
    "HD 114174":1.98,\
    "HD 25874":1.62,\
    "HD 120690":2.77,\
    "HD 210918":0.82,\
    "HD 45289":1.43,\
    "HD 135101":1.66,\
    "HD 39881":1.32}



#plt.plot(sun[0], sun[1])
#plt.plot(age, r)
#plt.show()


fig = plt.figure()
fig.subplots_adjust(bottom=0.12, right = 0.95, top=0.97)

im = plt.imread("Wood_1994_cut.png")


plt.gca().set_xscale("log")
#plt.gca().set_yscale("log")
plt.imshow(im, extent=(0.1, 10., 26,30), aspect='auto')


ddf = Table.read("../data/tables/fluxes.csv", format='ascii.csv', delimiter=',',names=("target", "lo", "value", "hi"))
for d in ddf:
    age = ages[d["target"]]
    print(d, age)
    y = d["value"]
    print(type(age), type(y))
    age = np.array([age]) * 1e9
    y = np.array([y])
    HK = vsini[d["target"]]
    print(age, y)
    y0 = d["lo"]
    if y0 == 0:
        y0 = 1e24
        plt.scatter(HK, [np.log10(d["hi"]) ], marker='v', color='b', s=70)
        plt.scatter( HK, np.log10(y),marker='d', color='b',s=50, alpha=0.3)
    else:
        plt.scatter(HK,np.log10(y),  marker='d', color='b'       ,s=100)
    plt.plot(2*[HK], np.log10(np.array([y0, d["hi"]])),color='b', lw=3, alpha=0.3)



plt.annotate("Solar\nAnalogs", xy=(2.5,26.7), xytext=(4, 27.2), color='b', fontsize=20, rotation=0,bbox=dict(boxstyle="round4", fc="w", ec='b'),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.25",
                                  relpos=(0.5, 0.),
                                  fc="b", ec='b', lw=2))


plt.ylim(26,29.9)
plt.xlim(0.1, 10)
plt.xlabel("v sin i (km/s)")
plt.ylabel("log $L_X$ (erg/s)" )
plt.savefig("vsini.pdf")
plt.show()
exit()







#for k in data.keys():    
    #x = data[k]["age"] * 1e9
    #y = data[k]["error"]
    #f = data[k]["flux"] 
    #print(k, float(x/1e9), f, y)
    #if f > 1.5*y:
      #plt.scatter([x], [f], marker='o', s=200, zorder=10, alpha=0.1)  
    #else:    
      #plt.scatter([x], [y], marker='v', s=200, zorder=10, alpha=0.1)

ddf = Table.read("../data/tables/fluxes.csv", format='ascii.csv', delimiter=',',names=("target", "lo", "value", "hi"))
for d in ddf:
    age = ages[d["target"]]
    print(d, age)
    y = d["value"]
    print(type(age), type(y))
    age = np.array([age]) * 1e9
    y = np.array([y])
    print(age, y)
    y0 = d["lo"]
    if y0 == 0:
        y0 = 1e24
        plt.scatter([age[0]], [d["hi"]], marker='v', color='b', s=70)
        plt.scatter(age, y, marker='d', color='b',s=50, alpha=0.3)
    else:
        plt.scatter(age, y, marker='d', color='b'       ,s=100)
    plt.plot([age[0],age[0]], [y0, d["hi"]], color='b', lw=3, alpha=0.3)

#HIP 97420
#plt.scatter([5.4*1e9],[1.5e27], color='b', marker='o', s=200, alpha=1.0, zorder=1)
#plt.annotate(r"HIP 97420", xy=(7e8, 7e26), color='b', fontsize=16, alpha=0.8) # : $10^4$ erg/s/cm$^2$

#HIP 43726
#plt.scatter([3.7*1e9],[1.3e28], color='b', marker='o', s=200, alpha=1.0, zorder=20)

age = np.logspace(8.8, 10.1, 100)
age = age / 1e9

# 18 Sco
plt.scatter([4.47*1e9],[3e26], color='y', marker='D', s=200, alpha=0.8, zorder=1)
plt.annotate(r"18 Sco", xy=(1.8e9, 2.3e26), color='y', fontsize=16, alpha=0.8) # : $10^4$ erg/s/cm$^2$

## HIP 29432
#plt.scatter([2.6*1e9],[7e26], color='k', marker='D', s=300, alpha=0.8, zorder=1)
#plt.annotate(r"HIP 29432", xy=(7e8, 7e26), color='k', fontsize=16, alpha=0.8) # : $10^4$ erg/s/cm$^2$



#plt.annotate(r"Sun", xy=(2.ls4e9, 4e27), color='r', fontsize=20, alpha=0.5)
plt.annotate(r"$\alpha$ Cen A", xy=(2.0e9, 8e25), color='r', alpha=0.5)

sun = np.loadtxt("radius/Sun_evo.dat", unpack=True)
r = sun[1]
t = sun[0]
surf = 1e4 * 6.09e22 * r**2
#print(surf)
plt.plot(t *1e9, surf,  color='g', lw=2)
plt.annotate(r"Min. X-ray Surface Flux", xy=(4e7, 5e26), color='g', fontsize=20) # : $10^4$ erg/s/cm$^2$

a2 = np.logspace(7.8, 8.5, 100)/1e9
plt.plot(a2*1e9,  20e28 * a2**(-0.8), color='0.5', ls='--')
#plt.annotate(r"$L_X \sim age^{-1.5}$", xy=(4e8, 4.5e28), color='.5', rotation=-33, fontsize=20)# : $10^4$ erg/s/cm$^2$
plt.plot(age*1e9,  8e28 * age**(-2.5), color='0.5', ls='--')
plt.annotate(r"$L_X \sim age^{-2.5}$", xy=(4e8, 7e28), color='0.5', rotation=-45, fontsize=20)# : $10^4$ erg/s/cm$^2$



plt.xlim(1e6, 1.2e10)
plt.xlim(2e7, 1.2e10)
plt.ylim(6.5e25, 6e31)
plt.ylim(1e26, 6e31)

#print(data)

plt.plot(t * 1e9, sun[2] * 1e-3 * 3.8e33, color='r', lw=2)
plt.annotate(r"log $L_X / L_{bol} = -3$", xy=(4e8, 1e30), color='r',fontsize=20)
#plt.annotate(r"$L_X \sim age^{-1.5}$", xy=(4e8, 1e28), color='r',fontsize=20)

#plt.annotate(r"Field stars", xy=(8e8, 2.5e31), color='k',fontsize=20)
#plt.annotate(r"Clusters", xy=(8e8, 1.02e31), color='k',fontsize=20)

plt.ylabel(r"$L_X$ (erg s$^{-1}$)")
plt.xlabel("Age (yr)")
plt.savefig("X_evolution.pdf")
plt.show()
