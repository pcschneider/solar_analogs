#!bin/bash

out_dir=../data/specs/

pd=$(pwd -P)

cd $out_dir

dirs=$(ls ../../data/*/0*/odata/*extract_bin1.sh)
# echo $dirs
for dr in $dirs
do
  echo $dr
  cdd=${dr:0: -18}
#   bdd=${dr:0: -24}
  echo "cdd=$cdd"
#   echo "bdd=$bdd"
  
  files=$(ls ${cdd}/*_pn200_spec.*)
  echo "Found ${files}"
  for f in $files
  do
    echo "ln -s $f"
    ln -s $f
  done
  bg_spec=$(ls ${cdd}/*_pn200_spec_bg.*)
  ln -s $bg_spec
  
  echo
done  

cd $pd

