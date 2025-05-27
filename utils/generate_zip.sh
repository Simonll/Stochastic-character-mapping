#!/bin/bash
rep=forward-simulation-$(date +"%D"-"%T"| sed "s/\//-/g"| sed "s/:/-/g")
cd /tmp/
git clone --recursive git@github.com:Simonll/forward-simulations.git $rep
zip -r $rep.zip $rep -x '*.git*'  $rep/exp/\* $rep/notes/\* $rep/bioinfo/\* $rep/sections/\* $rep/notebooks/\* $rep/refs/\*
zip -u $rep.zip $rep/notebooks/workflow.ipynb
