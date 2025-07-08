#!/bin/bash -l
#SBATCH --partition=high-mem
#SBATCH -o /home/users/jonros74/Coding/Slurm/%x-%j.out
#SBATCH -e /home/users/jonros74/Coding/Slurm/%x-%j.err
#SBATCH --time=120
#SBATCH --mem=96000
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jonros74@bas.ac.uk



source /home/users/jonros74/anaconda3/etc/profile.d/conda.sh

source activate Coding1


python3 SI_Calc.py $1 $2 $3 $4


