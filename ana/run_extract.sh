#!bin/bash

pd=$(pwd -P)

scripts=$(ls ../data/*/0*/odata/pn_final*extract_bin1.sh)
# echo $dirs
for dr in $scripts
do
  echo $dr
#   cdd=${dr:0: -18}
  cdd=${dr%/*}
  bdd=${cdd%/*}
  bn=${dr##*/}
  echo "cdd=$cdd"
  echo "bdd=$bdd"
  sasi=$(ls ${bdd}/sas*.sh)
  echo "sasi=$sasi"
  echo "script name: ${bn}"
#   
# #   cd $bdd
  source $sasi
# #   
#   
  cd $cdd
  source $bn
  pdir=$(pwd -P) 
  echo " should have run ${pdir}/${bn} now..."
  cd $pd
  echo
done  

