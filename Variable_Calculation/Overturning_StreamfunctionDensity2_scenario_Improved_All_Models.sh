#!/bin/bash
slurm_path="/home/users/jonros74/Coding/Slurm/"

InstitutionArray=("CCCma" "CCCma" "CCCma" "CCCma"   "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma"   "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "NOAA-GFDL" "NOAA-GFDL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO-ARCCSS" "CSIRO" "CSIRO" "CSIRO" "CSIRO" "CSIRO" "CSIRO" "MRI" "MRI" "MRI" "MRI" "MRI" "NOAA-GFDL" "NOAA-GFDL" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "NASA-GISS")


SourceArray=( "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "GFDL-CM4" "GFDL-CM4" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-CM2" "ACCESS-ESM1-5" "ACCESS-ESM1-5" "ACCESS-ESM1-5" "ACCESS-ESM1-5" "ACCESS-ESM1-5" "ACCESS-ESM1-5" "MRI-ESM2-0" "MRI-ESM2-0" "MRI-ESM2-0" "MRI-ESM2-0" "MRI-ESM2-0" "GFDL-CM4" "GFDL-CM4" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "GISS-E2-1-G")

ExptArray=( "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp119" "ssp119" "ssp119" "ssp119" "ssp119" "ssp585" "ssp245" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585"  "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp585" "ssp585" "ssp585" "ssp585" "ssp585" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp585" "ssp585" "ssp585" "ssp245" "ssp245" "ssp245" "ssp126" "ssp126" "ssp126" "ssp245" "ssp245" "ssp245" "ssp126" "ssp126" "ssp126" "ssp585" "ssp245" "ssp245" "ssp245" "ssp126" "ssp585" "ssp245" "ssp585" "ssp585" "ssp585" "ssp585" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp126" "ssp245" "ssp245" "ssp245" "ssp245" "ssp245" "ssp126" "ssp126" "ssp126" "ssp126" "ssp126" "ssp585")


VariantArray=("r1i1p1f1" "r1i1p2f1" "r2i1p1f1" "r2i1p2f1" "r3i1p1f1" "r3i1p2f1" "r4i1p1f1" "r4i1p2f1"  "r5i1p1f1" "r5i1p2f1" "r6i1p1f1" "r6i1p2f1" "r7i1p1f1" "r7i1p2f1" "r8i1p1f1" "r8i1p2f1" "r9i1p1f1/" "r9i1p2f1" "r10i1p1f1" "r10i1p2f1" "r1i1p1f1" "r1i1p2f1" "r2i1p1f1" "r2i1p2f1" "r3i1p1f1" "r3i1p2f1" "r4i1p1f1" "r4i1p2f1"  "r5i1p1f1" "r5i1p2f1" "r6i1p1f1" "r6i1p2f1" "r7i1p1f1" "r7i1p2f1" "r8i1p1f1" "r8i1p2f1" "r9i1p1f1/" "r9i1p2f1" "r10i1p1f1" "r10i1p2f1" "r1i1p1f1" "r1i1p2f1" "r2i1p1f1" "r2i1p2f1" "r3i1p1f1" "r3i1p2f1" "r4i1p1f1" "r4i1p2f1"  "r5i1p1f1" "r5i1p2f1" "r6i1p1f1" "r6i1p2f1" "r7i1p1f1" "r7i1p2f1" "r8i1p1f1" "r8i1p2f1" "r9i1p1f1/" "r9i1p2f1" "r10i1p1f1" "r10i1p2f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r6i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r6i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r6i1p1f1" "r1i1p1f1" "r3i1p1f1" "r4i1p1f1" "r6i1p1f1" "r9i1p1f1" "r1i1p1f1" "r2i1p1f1" "r4i1p1f1" "r5i1p1f1" "r6i1p1f1" "r1i1p1f1" "r4i1p1f1" "r6i1p1f1" "r9i1p1f1" "r11i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r5i1p1f2" "r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r5i1p1f2" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f1" "r1i1p1f3" "r2i1p1f3" "r3i1p1f3" "r4i1p1f3" "r1i1p1f3" "r2i1p1f3" "r3i1p1f3" "r4i1p1f3" "r5i1p1f3" "r1i1p1f1" "r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r5i1p1f2" "r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r5i1p1f2" "r1i1p1f2")



script_name="slurm_Overturning_StreamfunctionDensity2_Improved_Calc.sh"
memory_allocation=64000
time_allocation=60
file_table_id="Omon"
file_var="thetao"

len=${#InstitutionArray[@]}

for ((i=150; i<${len}; i++));
do echo "${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]}"
        if [ ${SourceArray[$i]} = "GFDL-CM4" ]	
        then
                let model_memory_allocation=memory_allocation*4
                let model_time_allocation=time_allocation*4
        elif [ ${SourceArray[$i]} =  "MPI-ESM1-2-HR" ]
        then
                let model_memory_allocation=memory_allocation*2
                let model_time_allocation=time_allocation*2
        elif [ ${SourceArray[$i]} =  "MIROC-ES2L" ]
        then
                let model_memory_allocation=memory_allocation*2
                let model_time_allocation=time_allocation*2
        elif [ ${SourceArray[$i]} =  "MRI-ESM2-0" ]
        then
                let model_memory_allocation=memory_allocation*5
                let model_time_allocation=time_allocation*5
        else
                let model_memory_allocation=memory_allocation
                let model_time_allocation=time_allocation
        fi
        echo "${model_memory_allocation}"
        overall_start_year=200000
        overall_end_year=0
        for file in /badc/cmip6/data/CMIP6/ScenarioMIP/${InstitutionArray[$i]}/${SourceArray[$i]}/${ExptArray[$i]}/${VariantArray[$i]}/${file_table_id}/${file_var}/gn/latest/*.nc
        do
                echo "$file"
                start_year=${file: -16 : 4}
                end_year=${file: -9 : 4}
                echo "$start_year"
                echo "$end_year"
                if [ $overall_start_year -gt $start_year ]
                then
                       overall_start_year=$start_year
                fi
                if [ $overall_end_year -lt $end_year ]
                then
                       overall_end_year=$end_year
                fi

        done
        echo "$overall_start_year"
        echo "$overall_end_year"
        total_years=$(( 10#$overall_end_year - 10#$overall_start_year + 1 ))
        echo "$total_years"
        #num_iterations=$(( ( $total_years + 9 )  / 10 ))
        num_iterations=${total_years}
        echo "$num_iterations"
        for ((j=0; j<${num_iterations}; j++));
        do
                echo "$j"
                echo "${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]} $j"
                sbatch  --mem=${model_memory_allocation} --time=${model_time_allocation}  --job-name="${script_name}_${SourceArray[$i]}_${j}_run" --output="${slurm_path}${script_name}_${SourceArray[$i]}_${j}.out"   --err="${slurm_path}${script_name}_${SourceArray[$i]}_${j}.err"  ${script_name} ${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]} $j
        done
done

