Purpose
-------
The tools extract the necessary information for the X-ray data of the solar analogs

Article
-------

*Table 1* (Targets)

The data are mostly from Ramirez+ 2014 and the relevant tables are stored locally (``tables/tab2.dat`` and ``tables/tab4.dat``).
The script ``ana/read_ramirez.py`` takes those data, adds Gaia information (for Gmag and distance) to produce ``tables/stars.ecsv``.
This file can now be used to automatically create a **stab** for Table 1 using ``ana/targets_tex_table.py``, which is then manually adjusted to include all relevant data that are not present in Ramirez+ 2014. Therefore, this script currently produces a *local* file named ``props.tex`` that one would need to copy into the ``TEX`` folder, i.e., run (in ``ana/``)::
  
  p37 read_ramirez.py
  p37 targets_tex_table.py
  cp props.tex ../TEX/

*Table 2* (Observations)  

The observations are read from ``tables/Xobs.ecsv``. The obs-date and exposure times are from the pn-files (``pn.fits``). Run (in ``ana/``)::

  p37 obs_table.py
  cp obs.tex ../TEX/

  
Target positions
----------------

**OM**

For most XMM observations, the OM provides strictly simultaneous UV measurements. These can be used to determine accurate source positions. This is done using::

  p37 create_om_centroids_table.py
  
This can write a table (*om_centroids_fn* from ``parameters.py``). Currently only a test-file is written, which must be changed to overwrite *om_centroids_fn*.

**Nominal source positions**

This can be done for XMM using::

    make_sources_ecsv.py
    
which writes a new *sources_ecsv_fn*-file (value specified in ``parameters.py``). It depends on the info in *observed_sources_fn* (specified in ``parameters.py``).


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


Re-run everything
-----------------

Do::
  
  p37 make_sources_ecsv.py
  # Create file containing the nominal source positions in detector coordinates
          # -> sources_ecsv_fn
  p37 check_bkgs.py
          # Checks if background regions are defined for all sources
  p37 make_extract_table.py 
          # Takes the information for the src and bkg regions and generates an "extraction" table
          # -> extract_prop_fn          
          
Update with OM positions::

  p37 create_om_centroids_table2.py 
          # Reads OM information and stores it in 
          # -> om_centroids_fn  
    p37 measured_centroids.py 
          # Reads OM centroids and averages them 
          # -> measured_cen_extr_fn
  
Update SAS config (in 'ana'; loops through the 'pn300_extract_bin1.sh'-files)::

  . run_update.sh
  
Create extract scripts::

  p37 make_expressions.py # Takes the extractions listed in `fn` given at the beginning of the script
  # Update the 'ls'-statement to return the desired extract scripts (line 5 of the script)
  . run_extract.sh 
  
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
