# This code is used to calculate the (Al+Fe)ox at 0.5 degree using the data from Ren et al.(2024): https://zenodo.org/records/13995030

import rasterio
import numpy as np
import glob
import os
import xarray as xr

# Path for required data
Polsen_file = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/P_pool/OlsenP/OlsenP_kgha1_World_Aug2022_ver_COG.tif'
soil_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Soil/hwsd_soil_data_on_cropland.nc"
ds_soil = xr.open_dataset(soil_file)
soc = ds_soil["oc"] # Unit: %

# Other directories
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil' 
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_P_Cycling'

with rasterio.open(Polsen_file) as src_Polsen:
    Polsen = src_Polsen.read(1).astype(float) # Unit: mg/kg
    lon = np.linspace(src_Polsen.bounds.left, src_Polsen.bounds.right, src_Polsen.width)
    lat = np.linspace(src_Polsen.bounds.top, src_Polsen.bounds.bottom, src_Polsen.height)