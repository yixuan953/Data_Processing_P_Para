# This code is used to calculate the P Olsen at 0.5 degree using the data from McDowell et al.(2023): https://doi.org/10.1038/s41597-023-02022-4

import rasterio
import numpy as np
import os
import xarray as xr
from scipy.ndimage import zoom

# Path for required data
Polsen_file = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/P_pool/OlsenP/OlsenP_kgha1_World_Aug2022_ver_COG.tif'
# soil_file = "/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Soil/hwsd_soil_data_on_cropland.nc"
# ds_soil = xr.open_dataset(soil_file)
# bd = ds_soil["bulk_density"] # Unit: kg/dm3

# Other directories
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil' 
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_P_Cycling'

with rasterio.open(Polsen_file) as src_Polsen:
    Polsen = src_Polsen.read(1).astype(float) # Unit: mg/kg
    transform = src_Polsen.transform
    original_lon= np.linspace(src_Polsen.bounds.left, src_Polsen.bounds.right, src_Polsen.width)
    original_lat = np.linspace(src_Polsen.bounds.top, src_Polsen.bounds.bottom, src_Polsen.height)

# Desired resolution
target_lat = np.arange(89.75, -90, -0.5)   # From 89.75 to -89.75
target_lon = np.arange(-179.75, 180, 0.5)  # From -179.75 to 179.75

zoom_y = len(target_lat) / Polsen.shape[0]
zoom_x = len(target_lon) / Polsen.shape[1]

data_resampled = zoom(Polsen, (zoom_y, zoom_x), order=1)  # order=1: bilinear interpolation

# Create xarray Dataset
ds = xr.Dataset(
    {
        "P Olsen": (("lat", "lon"), data_resampled)
    },
    coords={
        "lat": target_lat,
        "lon": target_lon
    }
)

# Save to NetCDF
output_nc = os.path.join(output_dir, f"POlsen_05d.nc")
ds.to_netcdf(output_nc)
print(f"P Olsen [mmol/kg] has been saved to: {output_nc}")