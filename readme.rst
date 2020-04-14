Purpose
-------
The tools extract the necessary information for the X-ray data of the solar analogs

How to Use
----------
There are a few sequences that must be obeyed to properly use the tools.

X-ray data preparation
  | To extract X-ray source properties, use:
  |
  |   p35 extract_photons.py
  |
  | which uses the the positions in the provided extraction file (``extract_prop_fn`` 
  | or ``measured_cen_extr_fn``) and the SAS generated files (by ``run_extract.sh``).
  |
  | To generate the required files (e.g. `pn_spec.fits`), do:
  |
  |   p35 make_extract_table.py
  |            (which gathers the source and background information into one file) 
  |   p35 measured_centroids.py 
  |            (updates the table constructed by `make_extract_table.py` with the measured OM 
  |             centroid and generates a new table)
  |   p35 make_expressions.py
  |            (Note: ONLY uses the backgrounds defined in ``bgs_ecsv_fn``, when make_extract_table
  |             has been run (for make_expressions.py) or when make_extract_table.py AND make_expressions.py 
  |             were run (for measured_centroids.py))
  |
  |   . run_extract.sh 
  |            (which must be manually updated to the specific filename of the extraction script)
  |   . soft_linking.sh
  |            (might need some modification depending on filenames)
  |
  |   . run_ds9.sh (loops throught the observations to check the source and background regions)
  |   . run_update.sh (loops throught the observations and re-runs odfingest/cifgen, needed when changing between PCs)
  
X-ray properties
  | There are two options to extract the source properties, pTools and pyxspec. Both are implemented
  |
  | They are called by:
  |    p35 extract_photons.py
  | and
  |    cd ../data/specs/ ; p27 xspec_fluxes.py
  | They store their results in: `extracted_photons_fn` and `xspec_fluxes_fn`, resp.
  | 
  | The script
  |   p35 merge_source_prop_tables.py
  | merges the results of both options.
  
OM source properties
  | To extract the fluxes and count rates from the OM data, use::
  |
  |  p35 get_OM_fluxes.py
  |
  | which stores the data in ``OM_fluxes_fn``.


Description of data
-------------------

I use ecsv for storing the relevant information in various tables. Specifically, the following 
files exist, their exact pathes are defined in ``parameters.py``:

Some tables contain a *use* column, which is currently not considered. Its idea is to de-select sources for the analysis. TBI

Observed Sources
  | Contains: name, obsID, observatory
  | Constructed by: Manually
  | Path: ``observed_sources_fn``
  
Sources
  | Contains: name,obsID,RA,Dec,src_x,src_y
  | Constructed by: make_sources_ecsv.py
  | Path: ``sources_ecsv_fn``
  | 
  | The source positions are obtained from Simbad and corrected for the 
  | epoch of the observation, and then transfered to detector coordinates
  
Backgrounds
  | Contains: source, obsID, detector, ID, bg_x, bg_y, bg_r, use
  | Constructed by hand, ie, the background locations are obtained by eye
  | Path: ``bgs_ecsv_fn``
 
Centroids
  | Contains: obsID,expID, RA, Dec
  | Constructed manually by inspection of the OM SIMAGEs, one entry for each SIMAGE
  | Path: ``om_centroids_fn``
  
Extraction properties from Simbad positions
  | Contains: source,obsID,fn,src_x,src_y,src_r,bkg_x,bkg_y,bkg_r
  | Contructed by: make_extract_table.py
  | Path: ``extract_prop_fn``
  |
  | Reads the source positions from ``sources_ecsv_fn``, the backgrounds from
  | ``bgs_ecsv_fn``, and the observation information from ``Xobs_ecsv_fn`` to
  | to generate a file that includes all necessary information to generate the
  | SAS extraction script.
  
Extraction properties from measured OM centroids
  | Contains: source,obsID,fn,src_x,src_y,src_r,bkg_x,bkg_y,bkg_r
  | Constructed by: measured_centroid.py
  | Path: measured_cen_extr_fn
  |
  | Takes the measured centroids from ``om_centroids_fn``, averages them
  | and updates the source positions in ``extract_prop_fn`` with the measured 
  | centroids.
  
Xobs
  | Contains: obsID; observatory; data_origin; directory; use
  | Constructed manually
  | Path: ``Xobs_ecsv_fn``
  
OM data
  | Contains: target,obsID,OM_mag,OM_rate
  | Constructed by: get_OM_fluxes.py
  | Path: ``OM_fluxes_fn``

Xspec fluxes
  | Contains: target, obsID, flux_lo, flux, flux_hi, rate, rate_err
  | Constructed by: xspec_fluxes.py (Note: must be run ../data/specs/)
  | Path: ``xspec_fluxes_fn``
  
Extracted Photons
  | Contains: source,obsID,src_cts,bkg_cts,area_scale,ontime,net_rate
  | Contructed by: extract_photons.py
  | Path: ``extracted_photons_fn``
  
Primary Source Properties
  | Contains: source,obsID_1,flux_lo,flux,flux_hi,rate,rate_err,obsID_2,src_cts,bkg_cts,area_scale,ontime,net_rate
  | Constructed by: merge_source_prop_tables.py
  | Path: ``primary_source_props_fn``
 
The extracted data are 