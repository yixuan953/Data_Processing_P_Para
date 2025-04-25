# This code is used to calculate the (Al+Fe)ox at 0.5 degree using the data from Ren et al.(2024): https://zenodo.org/records/13995030

import rasterio
import numpy as np
import glob
import os
import xarray as xr

# Path for required data
input_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/P_pool/Al_Fe_Oxalate'
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil' 
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_P_Cycling'

elements = ["Al", "Fe"]

# Calculate the Fe_ox and Al_ox content for each layer at 1 km resolution 
for ele in elements:
    
    ly1_oxalate_file = os.path.join(input_dir, f"{ele}o_0_20.tif")
    ly2_oxalate_file = os.path.join(input_dir, f"{ele}o_0_20.tif") 
    
    with rasterio.open(ly1_oxalate_file) as src_ly1_oxalate:
        ly1_oxalate = src_ly1_oxalate.read(1).astype(float) # Unit: kg/m2
        ly1_oxalate[ly1_oxalate <= 0] = np.nan
        lon = np.linspace(src_ly1_oxalate.bounds.left, src_ly1_oxalate.bounds.right, src_ly1_oxalate.width)
        lat = np.linspace(src_ly1_oxalate.bounds.top, src_ly1_oxalate.bounds.bottom, src_ly1_oxalate.height)

    with rasterio.open(ly2_oxalate_file) as src_ly2_oxalate:
        ly2_oxalate = src_ly2_oxalate.read(1).astype(float) # Unit: kg/m2
        ly2_oxalate[ly2_oxalate <= 0] = np.nan
        lon = np.linspace(src_ly2_oxalate.bounds.left, src_ly2_oxalate.bounds.right, src_ly2_oxalate.width)
        lat = np.linspace(src_ly2_oxalate.bounds.top, src_ly2_oxalate.bounds.bottom, src_ly2_oxalate.height)

    total_oxlate = ly1_oxalate +  ly2_oxalate # Unit: kg/m2

    data_total_oxlate = np.full((len(lat), len(lon)), np.nan, dtype=np.float32)  
    data_total_oxlate[:] = total_oxlate
    total_oxlate[total_oxlate <= 0] = np.nan

    ds = xr.Dataset(
            {"total_oxlate": (["lat", "lon"], data_total_oxlate)},
            coords={"lat": lat, "lon": lon},
            attrs={"units": "kg/m2"}
        )
    output = os.path.join(process_dir, f"{ele}o_top40cm_1km.nc")
    ds.to_netcdf(output)

    print(f"{ele}ox for top 40cm has been calculated and saved to {output}")