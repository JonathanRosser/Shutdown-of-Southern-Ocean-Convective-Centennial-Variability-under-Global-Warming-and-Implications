#!/bin/bash



InstitutionArray=("BCC" "CCCma" "CNRM-CERFACS" "CSIRO" "CSIRO-ARCCSS" "EC-Earth-Consortium" "IPSL" "MIROC" "MIROC" "MPI-M" "MRI" "NASA-GISS" "NCC" "NOAA-GFDL" "MOHC" "MOHC")

SourceArray=("BCC-ESM1" "CanESM5" "CNRM-ESM2-1" "ACCESS-ESM1-5" "ACCESS-CM2" "EC-Earth3" "IPSL-CM6A-LR" "MIROC6" "MIROC-ES2L" "MPI-ESM1-2-HR" "MRI-ESM2-0" "GISS-E2-1-G" "NorESM2-MM" "GFDL-CM4" "UKESM1-0-LL" "HadGEM3-GC31-LL")

ExptArray=("piControl" "esm-piControl" "esm-piControl" "esm-piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl" "piControl")

VariantArray=("r1i1p1f1" "r1i1p1f1" "r1i1p1f2"  "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1")





len=${#InstitutionArray[@]}

for ((i=0; i<${len}; i++));
do echo "${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]}"
	sbatch slurm_SI_calc.sh ${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]}  
done



