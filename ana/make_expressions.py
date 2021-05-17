from parameters import *
from astropy.table import Table
import numpy as np
import glob
import os
import pyfits
#import astropy.io.ascii
#from astropy.io import ascii

prefix="pn300"
binning=1
fn = extract_prop_fn
fn = measured_cen_extr_fn #_200_fn



#src = Table.read(sources_ecsv_fn, format='ascii.ecsv', delimiter=',')
#bkg = Table.read(bgs_ecsv_fn, format='ascii.ecsv', delimiter=',')
#xobs = Table.read(Xobs_ecsv_fn, format='ascii.ecsv', delimiter=';')

## Template
#evselect table=pn_filt.fits withspectrumset=yes spectrumset=pn_spec.fits energycolumn=PI withspecranges=yes specchannelmin=0 specchannelmax=20479 spectralbinsize=5 expression="(FLAG==0) && (PATTERN<=4) && ((X,Y) in circle(${srcc},400))"
#evselect table=pn_filt.fits withspectrumset=yes spectrumset=pn_spec_bg.fits energycolumn=PI withspecranges=yes specchannelmin=0 specchannelmax=20479 spectralbinsize=5 expression="(FLAG==0) && (PATTERN<=4) && ((X,Y) IN circle(${bgpn},900))"
#backscale spectrumset=pn_spec.fits badpixlocation=pn_filt.fits
#backscale spectrumset=pn_spec_bg.fits badpixlocation=pn_filt.fits
#rmfgen spectrumset=pn_spec.fits rmfset=pn_spec.rmf
#arfgen spectrumset=pn_spec.fits arfset=pn_spec.arf withrmfset=yes rmfset=pn_spec.rmf badpixlocation=pn_filt.fits detmaptype=psf
#grppha pn_spec.fits pn_spec.${spec_bin}grp comm="chkey respfile pn_spec.rmf & chkey backfile pn_spec_bg.fits & chkey ancrfile pn_spec.arf & group min ${spec_bin} & exit"


def generate_script(fn, src_x, src_y, src_r, bkg_x, bkg_y, bkg_r,prefix, binning=1, ):
    ff = pyfits.open(fn)
    oi = str(ff[0].header["OBS_ID"])
    tt = ""
    fn_basename = os.path.basename(fn)
    tt+="evselect table="+fn_basename
    tt+=" withspectrumset=yes "
    tt+="spectrumset="+oi+"_"+prefix+"_spec.fits"
    tt+=" energycolumn=PI withspecranges=yes specchannelmin=0 specchannelmax=20479 spectralbinsize=5 "
    tt+="expression=\"(FLAG==0) && (PATTERN<=4) && "
    tt+="((X,Y) IN circle("+str(src_x)+","+str(src_y)+","+str(src_r)+"))\""    
    t0 = tt
    
    tt = ""
    tt+="evselect table="+fn_basename
    tt+=" withspectrumset=yes "
    tt+="spectrumset="+oi+"_"+prefix+"_spec_bg.fits"
    tt+=" energycolumn=PI withspecranges=yes specchannelmin=0 specchannelmax=20479 spectralbinsize=5 "
    tt+="expression=\"(FLAG==0) && (PATTERN<=4) && "
    tt+="((X,Y) IN circle("+str(bkg_x)+","+str(bkg_y)+","+str(bkg_r)+"))\""    
    t1 = tt
    
    tt = ""
    tt+="backscale spectrumset="+oi+"_"+prefix+"_spec.fits badpixlocation="+fn_basename
    t2 = tt
    
    tt = ""
    tt+="backscale spectrumset="+oi+"_"+prefix+"_spec_bg.fits badpixlocation="+fn_basename
    t3 = tt
    
    tt=""
    tt+="rmfgen spectrumset="+oi+"_"+prefix+"_spec.fits rmfset="+oi+"_"+prefix+"_spec.rmf"
    t4 = tt
    
    tt=""
    tt+="arfgen spectrumset="+oi+"_"+prefix+"_spec.fits arfset="+oi+"_"+prefix+"_spec.arf withrmfset=yes"
    tt+=" rmfset="+oi+"_"+prefix+"_spec.rmf badpixlocation="+prefix+"_filt.fits detmaptype=psf"
    t5 = tt
    
    tt=""
    #tt+="grppha "+oi+"_"+prefix+"_spec.fits "+oi+"_"+prefix+"_spec."+str(binning)+"grp comm=\"chkey "
    tt+="grppha "+oi+"_"+prefix+"_spec.fits "+oi+"_"+prefix+"_spec.12ch comm=\"chkey "
    tt+="respfile "+oi+"_"+prefix+"_spec.rmf & chkey backfile "+oi+"_"+prefix+"_spec_bg.fits & chkey ancrfile "+oi+"_"+prefix+"_spec.arf & "
    #tt+="group min "+str(binning)+" & exit\""
    tt+="group 1 4096 12 & exit\""    
    t6 = tt
    
    print(t0)
    print(t1)
    print(t2)
    print(t3)
    print(t4)
    print(t5)
    print(t6)
    return t0+"\n\n"+t1+"\n\n"+t2+"\n"+t3+"\n\n"+t4+"\n"+t5+"\n\n"+t6

print("Reading ",fn)    
tt = Table().read(fn, format='ascii.ecsv', delimiter=',')
print("Generating scripts for ",len(tt["fn"]), " files.")
for t in tt:
    print(t)
    #continue
    #generate_script(fn, src_x, src_y, src_r, bkg_x, bkg_y, bgk_r,prefix, binning=1, ):
    oo = generate_script(t["fn"], t["src_x"],t["src_y"], t["src_r"], t["bkg_x"], t["bkg_y"], t["bkg_r"], prefix=prefix)
    print(oo)
    out_fn=os.path.dirname(t["fn"])+"/"+prefix+"_extract_bin"+str(binning)+".sh"
    print(out_fn)
    with open(out_fn, "w") as out:
        out.write(oo)
    out_fn=os.path.dirname(t["fn"])+"/"+prefix+"_regions_bin"+str(binning)+".reg"
    print(out_fn)
    with open(out_fn, "w") as out:
        out.write("# Region file format: DS9 version 4.1\n")
        out.write("# Filename: pn.fits[EVENTS]\n")
        out.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
        out.write("physical\n")
        out.write("circle("+str(t["src_x"])+","+str(t["src_y"])+","+str(t["src_r"])+")\n")
        out.write("circle("+str(t["bkg_x"])+","+str(t["bkg_y"])+","+str(t["bkg_r"])+")\n")
        #out.write(oo)
    
