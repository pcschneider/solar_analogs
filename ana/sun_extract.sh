#!bin/bash

pd=$(pwd -P)

dirs=$(ls ../data/*/0*/odata/*extract_bin1.sh)
# echo $dirs
for dr in $dirs
do
  echo $dr
  cdd=${dr:0: -18}
  bdd=${dr:0: -24}
  echo "cdd=$cdd"
  echo "bdd=$bdd"
  sasi=$(ls ${bdd}sas*.sh)
  echo "sasi=$sasi"
  
#   cd $bdd
  source $sasi
  
  cd $cdd
#   source pn_extract_bin1.sh

  cd $pd
done  

