#!bin/bash

pd=$(pwd -P)

dirs=$(ls ../data/*/0*/odata/*extract_bin1.sh)
# echo $dirs
for dr in $dirs
do
  echo $dr
  cdd=${dr:0: -18}
#   bdd=${dr:0: -24}
  echo "cdd=$cdd"
  cd $cdd
  ds9 pn.fits -region load pn_regions_bin1.reg
  echo
  cd $pd
done  

cd $pd

