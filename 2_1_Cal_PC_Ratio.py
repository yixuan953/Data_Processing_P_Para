# This code is used to calculate the PC ratio for P deomposition calculation
# The calculation function is from Tipping et al. (2016) https://link.springer.com/article/10.1007/s10533-016-0247-z#Sec5

import os
import numpy as np
import xarray as xr

soil_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Soil/hwsd_soil_data_on_cropland.nc"
ds_soil = xr.open_dataset(soil_file)
soc = ds_soil["oc"] # Unit: %

import xarray as xr
import numpy as np

# Open the soil data file
soil_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Soil/hwsd_soil_data_on_cropland.nc"
ds_soil = xr.open_dataset(soil_file)
soc = ds_soil["oc"]  # Unit: %

# Define constants for PC ratio calculation
PC_npSOM = 0.0011
PC_nrSOM = 0.016  

# Create new DataArrays for Fnpsom and Fnrsom with the same dimensions as soc
Fnpsom = xr.zeros_like(soc)
Fnrsom = xr.ones_like(soc)

# Apply the conditions using where
# Condition 1: soc < 0.1 -> Fnpsom = 0, Fnrsom = 1 (already initialized this way)
# Condition 2: soc > 50 -> Fnpsom = 1, Fnrsom = 0
Fnpsom = Fnpsom.where(soc <= 50, 1)
Fnrsom = Fnrsom.where(soc <= 50, 0)
# Condition 3: 0.1 <= soc <= 50
mask_middle = (soc >= 0.1) & (soc <= 50)
log_calculation = np.log10(soc/0.1) / np.log10(50/0.1)
Fnpsom = Fnpsom.where(~mask_middle, log_calculation)
Fnrsom = Fnrsom.where(~mask_middle, 1 - log_calculation)

# Calculate the final PC ratio
PC_ratio = PC_npSOM * Fnpsom + PC_nrSOM * Fnrsom

# Create a new dataset with all the calculated values
ds_pc_ratio = xr.Dataset(
    {
        "PC_ratio": PC_ratio
    },
    coords=ds_soil.coords
)

# Add attributes
ds_pc_ratio["PC_ratio"].attrs["long_name"] = "PC ratio calculated from SOC"
ds_pc_ratio["PC_ratio"].attrs["units"] = "-"
ds_pc_ratio["PC_ratio"].attrs["description"] = f"PC_ratio = PC_npSOM * Fnpsom + PC_nrSOM * Fnrsom"

# Save to netCDF file
output_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Para_P_Cycling/PCratio_05d.nc"
ds_pc_ratio.to_netcdf(output_file)

print(f"PC ratio calculations saved to: {output_file}")