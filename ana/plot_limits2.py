from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pickle
import matplotlib
from parameters import *
from astropy.table import Table

matplotlib.rcParams['font.size'] = 16




#plt.plot(sun[0], sun[1])
#plt.plot(age, r)
#plt.show()


fig = plt.figure()
fig.subplots_adjust(bottom=0.12, right = 0.95, top=0.97)

im = plt.imread("X_age2.png")

with open(data_fn, 'rb') as inpt:
    data = pickle.load(inpt)

plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.imshow(im, extent=(1e6, 1.2e10, 6e25,6e31), aspect='auto')

for k in data.keys():    
    x = data[k]["age"] * 1e9
    y = data[k]["error"]
    f = data[k]["flux"] 
    print(k, float(x/1e9), f, y)
    if f > 1.5*y:
      plt.scatter([x], [f], marker='o', s=200, zorder=10, alpha=0.1)  
    else:    
      plt.scatter([x], [y], marker='v', s=200, zorder=10, alpha=0.1)

ddf = Table.read("../data/tables/fluxes.csv", format='ascii.csv', delimiter=',',names=("target", "lo", "value", "hi"))
for d in ddf:
    try:
        age = ages[d["target"]]
    except:
        age = 4.0
    print(d, age)
    y = d["value"]
    print(type(age), type(y))
    age = np.array([age]) * 1e9
    y = np.array([y])
    print(age, y)
    plt.scatter(age, y, marker='d',s=50)
    y0 = d["lo"]
    if y0 == 0:
        y0 = 1e24
    plt.plot([age[0],age[0]], [y0, d["hi"]], color='b', lw=3)

#HIP 97420
#plt.scatter([5.4*1e9],[1.5e27], color='b', marker='o', s=200, alpha=1.0, zorder=1)
#plt.annotate(r"HIP 97420", xy=(7e8, 7e26), color='b', fontsize=16, alpha=0.8) # : $10^4$ erg/s/cm$^2$

#HIP 43726
#plt.scatter([3.7*1e9],[1.3e28], color='b', marker='o', s=200, alpha=1.0, zorder=20)

age = np.logspace(8.8, 10.1, 100)
age = age / 1e9
plt.plot(age*1e9, 0.8* 2.9/5.0 *  3e28 * age**(-1.5), color='b')

# 18 Sco
plt.scatter([4.47*1e9],[3e26], color='k', marker='D', s=300, alpha=0.8, zorder=1)
plt.annotate(r"18 Sco", xy=(2e9, 3e26), color='k', fontsize=16, alpha=0.8) # : $10^4$ erg/s/cm$^2$

## HIP 29432
#plt.scatter([2.6*1e9],[7e26], color='k', marker='D', s=300, alpha=0.8, zorder=1)
#plt.annotate(r"HIP 29432", xy=(7e8, 7e26), color='k', fontsize=16, alpha=0.8) # : $10^4$ erg/s/cm$^2$



plt.annotate(r"Sun", xy=(2.4e9, 4e27), color='r', fontsize=20, alpha=0.5)
plt.annotate(r"$\alpha$ Cen A", xy=(2.0e9, 8e25), color='r', alpha=0.5)

sun = np.loadtxt("sun_radius.dat", unpack=True)
pol = np.polyfit(sun[0], sun[1], 2)
r= np.polyval(pol, age)
surf = 0.8*2.9/5.0 * 6.e22 * 1e4 * r**2
#print(surf)
plt.plot(age *1e9, surf,  color='g')
plt.annotate(r"Min. X-ray Surface Flux", xy=(4e7, 1e26), color='g', fontsize=20) # : $10^4$ erg/s/cm$^2$

plt.xlim(1e6, 1.2e10)
plt.xlim(2e7, 1.2e10)
plt.ylim(6.5e25, 6e31)
plt.annotate(r"$L_X \sim age^{-1.5}$", xy=(4e8, 1e28), color='b', rotation=-33, fontsize=20)# : $10^4$ erg/s/cm$^2$

#print(data)

plt.annotate(r"log $L_X / L_{bol} = -3$", xy=(4e8, 1e30), color='r',fontsize=20)
#plt.annotate(r"$L_X \sim age^{-1.5}$", xy=(4e8, 1e28), color='r',fontsize=20)

plt.annotate(r"Field stars", xy=(8e8, 2.5e31), color='k',fontsize=20)
plt.annotate(r"Clusters", xy=(8e8, 1.02e31), color='k',fontsize=20)

plt.annotate("Old\nTwins", xy=(7e9,1e27), xytext=(3e9,2e28), color='b', fontsize=20, rotation=0,bbox=dict(boxstyle="round4", fc="w", ec='b'),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.25",
                                  relpos=(0.5, 0.),
                                  fc="b", ec='b', lw=2))

plt.ylabel(r"$L_X$ (erg s$^{-1}$)")
plt.xlabel("Age (yr)")
#plt.savefig("X_evolution.pdf")
plt.show()
