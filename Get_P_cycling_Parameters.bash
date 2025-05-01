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

# -----------------   Paramter 1: (Al+Fe)ox calculation --------------------------------

# 1_1: Sum up the Al_oxalate and Fe_oxalate for top 40 cm at 1 km degree, transform from .tif to .nc
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/P_cycling_Paramters/1_1_Cal_Al_Fe_Ox.py

# 1_2 Upscale the data from 1 km to 0.5 degree, and get the total (Al+Fe)ox [mmol/m2]
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/P_cycling_Paramters/1_2_Res_Trans_Upscale_05d.py

# 1_3 Transform the data unit from kg/m2 to mmol/kg soil mass by dividing the output of 1_2 with bulk density
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/P_cycling_Paramters/1_3_Unit_Trans.py

# -----------------   Paramter 2: PC ratio calculation --------------------------------
# python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/P_cycling_Paramters/2_Cal_PC_Ratio.py

# -----------------   Paramter 3: P Olsen calculation --------------------------------
python /lustre/nobackup/WUR/ESG/zhou111/Code/Data_Processing/P_cycling_Paramters/3_Cal_P_Olsen.py