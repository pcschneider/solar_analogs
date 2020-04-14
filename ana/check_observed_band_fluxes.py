from astropy.table import Table, vstack, hstack, join
import numpy as np
from parameters import *
import matplotlib.pyplot as plt
from PyAstronomy.pyasl import ps_pdf_lams
from PyAstronomy import pyaC

extracted_photons_fn
extracted_photons_02_04_fn
extracted_photons_O7_fn
t0 = Table.read(extracted_photons_fn, format='ascii.ecsv', delimiter=',')
t1 = Table.read(extracted_photons_02_04_fn, format='ascii.ecsv', delimiter=',')  
t2 = Table.read(extracted_photons_O7_fn, format='ascii.ecsv', delimiter=',')  

s0 = Table.read(extracted_photons_200_fn, format='ascii.ecsv', delimiter=',')
s1 = Table.read(extracted_photons_200_02_04_fn, format='ascii.ecsv', delimiter=',')  
s2 = Table.read(extracted_photons_200_O7_fn, format='ascii.ecsv', delimiter=',')  

l = np.linspace(0., 30., 200)

res = []

for targ in t0["source"]:
  print(targ)
  if targ == "HD 120690": continue
  
  
  
  gi0, gi1, gi2 = np.where(targ == t0["source"])[0], np.where(targ == t1["source"])[0], np.where(targ == t2["source"])[0]
  for t, s, b in zip([t0, t1, t2], [s0, s1, s2], ["02-10","02-04","O7"]):
      row = [targ]
      row.append(b)
      
      gi = np.where(targ == t["source"])[0]
      si = np.where(targ == s["source"])[0]
      
      p0, p1, p2 = t["src_cts"][gi].data, t["bkg_cts"][gi].data, t["area_scale"][gi].data
      p0, p1, p2 = p0[0], p1[0], p2[0]
      a = ps_pdf_lams(l, p0, p1, p2)
      csa = np.cumsum(a)/np.sum(a)
      lla, ula = pyaC.zerocross1d(l, csa-0.05, getIndices=False), pyaC.zerocross1d(l, csa-0.95, getIndices=False)
      neta = (t["src_cts"][gi].data - t["bkg_cts"][gi].data * t["area_scale"][gi].data) / t["ontime"][gi].data
      if len(lla)<1:
          lla = [0]
          ula = pyaC.zerocross1d(l, csa-0.9, getIndices=False)
      if len(ula)==0:
          ula = [-1]          
      row.append(t["src_cts"][gi].data[0])
      row.append(t["bkg_cts"][gi].data[0])
      row.append(t["area_scale"][gi].data[0])
      row.append(neta[0])
      row.append(lla[0])
      row.append(ula[0])
      
      p0, p1, p2 = s["src_cts"][gi].data, s["bkg_cts"][gi].data, s["area_scale"][gi].data
      p0, p1, p2 = p0[0], p1[0], p2[0]
      b = ps_pdf_lams(l, p0, p1, p2)
      csb = np.cumsum(b)/np.sum(b)
      llb, ulb = pyaC.zerocross1d(l, csb-0.05, getIndices=False), pyaC.zerocross1d(l, csb-0.95, getIndices=False)
      netb = (s["src_cts"][gi].data - s["bkg_cts"][gi].data * s["area_scale"][gi].data) / s["ontime"][gi].data
      if len(llb)<1:
          llb = [0]
          ulb = pyaC.zerocross1d(l, csb-0.9, getIndices=False)      
      row.append(s["src_cts"][gi].data[0])
      row.append(s["bkg_cts"][gi].data[0])
      row.append(s["area_scale"][gi].data[0])
      row.append(netb[0])
      row.append(llb[0])
      try:
          row.append(ulb[0])
      except:
          row.append(-1)
      row.append(s["ontime"][gi].data[0])
      
      
      #print(lla, ula, llb, ulb)
      if len(ulb)==0:
          #print("p", p0, p1, p2)
          #plt.plot(l, b, ls='--',color='r')
          #plt.plot(l, csb, color='r')
          #plt.plot(l, a, ls='--',color='b')
          #plt.plot(l, csa, color='b')
          #plt.show()
          ulb = [-1]
      
      a0, b0, c0, d0, e0 = t["src_cts"][gi].data, t["bkg_cts"][gi].data * t["area_scale"][gi].data, float(lla[0]), float(ula[0]), neta
      a1, b1, c1, d1, e1 = s["src_cts"][si].data, s["bkg_cts"][si].data * s["area_scale"][si].data, float(llb[0]), float(ulb[0]), netb
      #print(a0, b0, c0, d0, e0, a1, b1, c1, d1, e1)
      
      print("%3i - %5.2f limits: %5.2f - %5.2f rate: %5.2e      ====     %3i - %5.2f limits: %5.2f - %5.2f rate: %5.2e (%5.2e) " % (a0, b0, c0, d0, e0, a1, b1, c1, d1, e1, e1*1.25))
          #"           ",\
           #s["src_cts"][si].data, s["bkg_cts"][si].data * s["area_scale"][si].data, " limits: ",llb, ulb, "rate",netb)
          #src_cts,bkg_cts,area_scale
      res.append(row)    
      #print("row",row)
  print()
  
tt = Table(rows=res, names=("target", "band", "src_300", "bkg_300", "area_scale_300", "net_300","lo_300","hi_300", "src_200", "bkg_200", "area_scale_200", "net_200", "lo_200","hi_200", "ontime"))
tt.write(count_rates_fn, format='ascii.ecsv', delimiter=',')
