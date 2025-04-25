#!/bin/bash
#-----------------------------Mail address-----------------------------

#-----------------------------Output files-----------------------------
#SBATCH --output=HPCReport/output_%j.txt
#SBATCH --error=HPCReport/error_output_%j.txt

#-----------------------------Required resources-----------------------
#SBATCH --time=600
#SBATCH --mem=250000

#--------------------Environment, Operations and Job steps-------------
# Python scripts
module load python/3.12.0
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/P_cycling_Paramters/2_1_Cal_PC_Ratio.py