import matplotlib.pyplot as plt
import numpy as np
from parameters import *
from astropy.table import Table
import matplotlib
matplotlib.rcParams['font.size'] = 16

fig = plt.figure()
fig.subplots_adjust(bottom=0.12, right = 0.95, top=0.97)


im = plt.imread("Mamajek_X_vs_Ca_cut.png")

plt.imshow(im, extent=(-2.8, -7.4, -3.7, -5.2), aspect='auto')

R_HKs = {"HD 2071":-4.93,\
    "HD 42618":-4.95,\
    "HD 114174":-4.99,\
    "HD 25874":-5.00,\
    "HD 120690":-4.80,\
    "HD 210918":-5.00,\
    "HD 45289":-5.01,\
    "HD 135101":-5.04,\
    "HD 39881":-5.00}


ddf = Table.read("../data/tables/fluxes.csv", format='ascii.csv', delimiter=',',names=("target", "lo", "value", "hi"))
for d in ddf:
    age = ages[d["target"]]
    print(d, age)
    y = d["value"]
    print(type(age), type(y))
    age = np.array([age]) * 1e9
    y = np.array([y])
    HK = R_HKs[d["target"]]
    print(age, y)
    y0 = d["lo"]
    if y0 == 0:
        y0 = 1e24
        plt.scatter([np.log10(d["hi"]) - 33.6], HK, marker='>', color='b', s=70)
        plt.scatter(np.log10(y) - 33.6, HK, marker='d', color='b',s=50, alpha=0.3)
    else:
        plt.scatter(np.log10(y) - 33.6, HK, marker='d', color='b'       ,s=100)
    plt.plot(np.log10(np.array([y0, d["hi"]])) - 33.6, 2*[HK], color='b', lw=3, alpha=0.3)

plt.annotate("Solar\nAnalogs", xy=(-6.87, -4.85), xytext=(-6.2,-4.6), color='b', fontsize=20, rotation=0,bbox=dict(boxstyle="round4", fc="w", ec='b'),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=0.25",
                                  relpos=(0.5, 0.),
                                  fc="b", ec='b', lw=2))


plt.xlim(-4,-7.2)
plt.ylim(-4.3, -5.2)
plt.xlabel("log $L_X / L_{bol}$")
plt.ylabel("log $R'_{HK}$")
plt.savefig("R_HK.pdf")
plt.show()