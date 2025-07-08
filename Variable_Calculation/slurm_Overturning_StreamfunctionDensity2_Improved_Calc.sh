#!/bin/bash -l
#SBATCH --partition=high-mem
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jonros74@bas.ac.uk



source /home/users/jonros74/anaconda3/etc/profile.d/conda.sh

source activate Coding1

echo "$1 $2 $3 $4 $5"
python3 Overturning_StreamfunctionDensity2_Improved_Calc.py $1 $2 $3 $4 $5


