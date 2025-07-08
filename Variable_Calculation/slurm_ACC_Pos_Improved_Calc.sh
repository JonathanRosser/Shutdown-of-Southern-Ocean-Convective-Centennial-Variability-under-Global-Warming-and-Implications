#!/bin/bash -l
#SBATCH --partition=high-mem
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jonros74@bas.ac.uk



source /home/users/jonros74/anaconda3/etc/profile.d/conda.sh

source activate Coding1

echo "$1 $2 $3 $4 $5"
python3 ACC_Pos_Improved_Calc.py $1 $2 $3 $4 $5


