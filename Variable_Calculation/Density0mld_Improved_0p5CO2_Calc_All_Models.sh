#!/bin/bash
slurm_path="/home/users/jonros74/Coding/Slurm/"




InstitutionArray=("NASA-GISS" "MOHC" "IPSL" "MIROC" "CNRM-CERFACS" "MRI" "NCAR")

SourceArray=("GISS-E2-1-G" "HadGEM3-GC31-LL" "IPSL-CM6A-LR" "MIROC6" "CNRM-CM6-1" "MRI-ESM2-0" "CESM2")

ExptArray=("abrupt-0p5xCO2" "abrupt-0p5xCO2" "abrupt-0p5xCO2" "abrupt-0p5xCO2" "abrupt-0p5xCO2" "abrupt-0p5xCO2" "abrupt-0p5xCO2")

VariantArray=("r1i1p1f1" "r1i1p1f3" "r1i1p1f1" "r1i1p1f1" "r1i1p1f2" "r1i1p1f1" "r1i1p1f1")







GridArray=("gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn" "gn")










script_name="slurm_Density0mld_Improved_Calc.sh"
memory_allocation=10000
time_allocation=20
file_table_id="Omon"
file_var="thetao"

len=${#InstitutionArray[@]}

for ((i=4; i<${len}; i++));
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
                let model_memory_allocation=memory_allocation*2
                let model_time_allocation=time_allocation*2
        else
                let model_memory_allocation=memory_allocation
                let model_time_allocation=time_allocation
        fi
        echo "${model_memory_allocation}"


        overall_start_year=200000
        overall_end_year=0
        for file in /badc/cmip6/data/CMIP6/CFMIP/${InstitutionArray[$i]}/${SourceArray[$i]}/${ExptArray[$i]}/${VariantArray[$i]}/${file_table_id}/${file_var}/${GridArray[$i]}/latest/*.nc
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
        num_iterations=$total_years
        echo "$num_iterations"
        for ((j=0; j<${num_iterations}; j++));
        do
                echo "$j"
                echo "${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]} $j"
                #sbatch slurm_Density2_Improved_Calc.sh ${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]} $j
                sbatch  --mem=${model_memory_allocation} --time=${model_time_allocation}  --job-name="${script_name}_${SourceArray[$i]}_${j}_run" --output="${slurm_path}${script_name}_${SourceArray[$i]}_${j}.out"   --err="${slurm_path}${script_name}_${SourceArray[$i]}_${j}.err"  ${script_name} ${InstitutionArray[$i]} ${SourceArray[$i]} ${ExptArray[$i]} ${VariantArray[$i]} $j
        done
done

