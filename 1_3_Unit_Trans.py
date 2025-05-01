# This script is used to transform (Al+Fe)ox from mmol/m2 to mmol/kg soil mass:
# (Al+Fe)ox [mmol/kg] = (Al+Fe)ox [mmol/m2] * 0.001 / (bulk_density [kg/dm-3] * 0.4 topsoil_depth [m])

import os
import numpy as np
import xarray as xr

input_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw'
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil'
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_P_Cycling'


f_Al_Fe = os.path.join(process_dir, f"Al_Fe_Ox_top40cm_05d.nc")
f_bd = os.path.join(input_dir, f"Soil/hwsd_soil_data_on_cropland.nc")

ds_AlFe = xr.open_dataset(f_Al_Fe)
ds_bd = xr.open_dataset(f_bd)

AlFe = ds_AlFe["Al_Fe_Ox_total"] # Unit: mmol/m2
bd = ds_bd["bulk_density"] # Unit: kg/dm3

Al_Fe_ox = AlFe * 0.001/ (bd * 0.4) # Unit: mmol/kg soil mass

# Create a new dataset with all the calculated values
ds_Al_Fe_ox = xr.Dataset(
    {
        "Al_Fe_ox": Al_Fe_ox
    },
    coords=ds_bd.coords
)

# Add attributes
ds_Al_Fe_ox["Al_Fe_ox"].attrs["long_name"] = "Oxalate extractable Al and Fe content"
ds_Al_Fe_ox["Al_Fe_ox"].attrs["units"] = "mmol/kg soil mass"

# Save to netCDF file
output_file = os.path.join(output_dir, f"Al_Fe_ox_05d.nc")
ds_Al_Fe_ox.to_netcdf(output_file)

print(f"(Al+Fe)ox [mmol/kg] has been calculated and saved to: {output_file}")