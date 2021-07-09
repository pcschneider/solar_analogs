from astropy.io import ascii
from astropy.table import Table
import io

ifn = "../tables/xspec_fluxes.ecsv"
ofn = "xspec.tex"

dd = ascii.read(ifn)
print(dd)
dd["rate"]*=1000
dd["rate_err"]*=1000
dd.remove_columns(['flux_lo','flux_hi'])
#print(ascii.latex.latexdicts['AA'])

f = io.StringIO()

ascii.write(dd, f, Writer = ascii.Latex, latexdict = {'tabletype': 'table*','preamble':'\centering','header_start': '\\hline \\hline', 'header_end': '\\hline', 'data_end': '\\hline','units': {'flux':'erg s$^{-1}$ cm$^{-2}$', 'rate': 'ks$^{-1}$','rate_err': 'ks$^{-1}$'}}, formats={"flux_lo":"%5.2f", "flux":"%5.2f", "flux_hi":"%5.2f","rate":"%5.2f", "rate_err":"%5.2f" }, overwrite=True)

fc = f.getvalue()
#f.write(ofn)
#f.close()

fc = fc.replace("target","Target")
fc = fc.replace("rate_err","$\sigma_{Rate}$")
fc = fc.replace("rate","Count rate")
fc = fc.replace("flux","log Flux")


oo = open(ofn, "w")
oo.write(fc)
oo.close()
