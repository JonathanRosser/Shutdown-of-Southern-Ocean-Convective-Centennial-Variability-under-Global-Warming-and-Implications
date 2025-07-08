#!/bin/bash
slurm_path="/home/users/jonros74/Coding/Slurm/"

InstitutionArray=("CCCma" "CCCma" "CCCma" "CCCma"   "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "CCCma" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "NOAA-GFDL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "IPSL" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "EC-Earth-Consortium" "CCCma" "MIROC" "MIROC" "MIROC" "MIROC" "MIROC" "BCC" "BCC" "BCC" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CNRM-CERFACS" "CSIRO" "CSIRO-ARCCSS" "MIROC" "MPI-M" "MRI" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC" "MOHC")


SourceArray=( "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "CanESM5" "HadGEM3-GC31-LL"  "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "HadGEM3-GC31-LL" "GFDL-CM4" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "IPSL-CM6A-LR" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "EC-Earth3" "CanESM5" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "MIROC6" "BCC-ESM1" "BCC-ESM1" "BCC-ESM1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "CNRM-ESM2-1" "ACCESS-ESM1-5" "ACCESS-CM2" "MIROC-ES2L" "MPI-ESM1-2-HR" "MRI-ESM2-0" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL" "UKESM1-0-LL")

ExptArray=( "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical"  "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical"  "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "piControl" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical" "historical")


VariantArray=("r1i1p1f1" "r1i1p2f1" "r2i1p1f1" "r2i1p2f1" "r3i1p1f1" "r3i1p2f1" "r4i1p1f1" "r4i1p2f1"  "r5i1p1f1" "r5i1p2f1" "r6i1p1f1" "r6i1p2f1" "r7i1p1f1" "r7i1p2f1" "r8i1p1f1" "r8i1p2f1" "r9i1p1f1/" "r9i1p2f1" "r10i1p1f1" "r10i1p2f1" "r1i1p1f3" "r2i1p1f3" "r3i1p1f3" "r4i1p1f3" "r5i1p1f3" "r11i1p1f3" "r12i1p1f3" "r13i1p1f3" "r14i1p1f3" "r15i1p1f3" "r16i1p1f3" "r17i1p1f3" "r18i1p1f3" "r19i1p1f3" "r20i1p1f3" "r21i1p1f3" "r22i1p1f3" "r23i1p1f3" "r24i1p1f3" "r25i1p1f3" "r1i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r6i1p1f1" "r7i1p1f1" "r8i1p1f1" "r9i1p1f1" "r10i1p1f1" "r11i1p1f1" "r12i1p1f1" "r13i1p1f1" "r14i1p1f1" "r15i1p1f1" "r16i1p1f1" "r17i1p1f1" "r18i1p1f1" "r19i1p1f1" "r20i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r6i1p1f1" "r7i1p1f1" "r8i1p1f1" "r9i1p1f1" "r10i1p1f1" "r11i1p1f1" "r12i1p1f1" "r13i1p1f1" "r14i1p1f1" "r15i1p1f1" "r16i1p1f1" "r17i1p1f1" "r18i1p1f1" "r19i1p1f1" "r20i1p1f1" "r1i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r4i1p1f1" "r5i1p1f1" "r1i1p1f1" "r2i1p1f1" "r3i1p1f1" "r1i1p1f2" "r2i1p1f2" "r3i1p1f2" "r4i1p1f2" "r5i1p1f2" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r2i1p1f2" " r3i1p1f2" "r4i1p1f2" "r5i1p1f3" "r6i1p1f3" "r7i1p1f3" "r8i1p1f2" "r9i1p1f2" "r10i1p1f2" "r11i1p1f2" "r12i1p1f2" "r16i1p1f2" "r17i1p1f2" "r18i1p1f2" "r19i1p1f2")

script_name="slurm_Overturning_StreamfunctionDensity2_Improved_Calc.sh"
memory_allocation=64000
time_allocation=60
file_table_id="Omon"
file_var="thetao"

len=${#InstitutionArray[@]}

for ((i=81; i<82; i++));
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
        for file in /badc/cmip6/data/CMIP6/CMIP/${InstitutionArray[$i]}/${SourceArray[$i]}/${ExptArray[$i]}/${VariantArray[$i]}/${file_table_id}/${file_var}/gn/latest/*.nc
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

