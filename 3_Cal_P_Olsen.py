import rasterio
import numpy as np
import os
import xarray as xr
from scipy.ndimage import zoom
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Path for required and output data
Polsen_file = '/lustre/nobackup/WUR/ESG/zhou111/Data/Raw/Nutri/P_pool/OlsenP/OlsenP_kgha1_World_Aug2022_ver_COG.tif'
process_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil' 
output_dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Para_P_Cycling'

# Open the original .tiff file
with rasterio.open(Polsen_file) as src_Polsen:
    # Read the data as float
    Polsen = src_Polsen.read(1).astype(float)  # Unit: mg/kg
    crs = src_Polsen.crs
    transform = src_Polsen.transform
    
    # Replace values greater than 1e5 with NaN (missing values)
    Polsen[Polsen > 1e5] = np.nan
    
    # Define target CRS (WGS84)
    dst_crs = 'EPSG:4326'
    
    # Calculate the transform for the reprojected data
    transform_reproj, width_reproj, height_reproj = calculate_default_transform(
        crs, dst_crs, src_Polsen.width, src_Polsen.height, *src_Polsen.bounds
    )
    
    # Create an empty array for the reprojected data
    reprojected_data = np.empty((height_reproj, width_reproj), dtype=np.float32)
    
    # Reproject the data
    reproject(
        source=Polsen,
        destination=reprojected_data,
        src_transform=src_Polsen.transform,
        src_crs=crs,
        dst_transform=transform_reproj,
        dst_crs=dst_crs,
        resampling=Resampling.bilinear  # Using bilinear for better quality
    )

# Create target latitude and longitude grid with 0.5 degree resolution
target_lat = np.arange(89.75, -90, -0.5)   # From 89.75 to -89.75
target_lon = np.arange(-179.75, 180, 0.5)  # From -179.75 to 179.75

# Calculate the resolution of the reprojected data
res_lat = abs(transform_reproj[4])  # y resolution
res_lon = transform_reproj[0]       # x resolution

# Calculate the number of pixels needed for 0.5 degree
new_height = int(transform_reproj[5] + height_reproj * transform_reproj[4] - transform_reproj[5]) / 0.5
new_width = int(transform_reproj[2] + width_reproj * transform_reproj[0] - transform_reproj[2]) / 0.5

# Calculate zoom factors for resampling
zoom_y = len(target_lat) / reprojected_data.shape[0]
zoom_x = len(target_lon) / reprojected_data.shape[1]

# Convert P Olsen from mg/kg to mmol/kg (if needed)
Polsen_mol = reprojected_data / 30.97  # Conversion from mg P to mmol P

# Perform bilinear resampling (zooming)
data_resampled = zoom(Polsen_mol, (zoom_y, zoom_x), order=1)  # order=1 for bilinear interpolation

# Create xarray Dataset
ds = xr.Dataset(
    {
        "P_Olsen": (("lat", "lon"), data_resampled)
    },
    coords={
        "lat": target_lat,
        "lon": target_lon
    }
)
ds["P_Olsen"].attrs["long_name"] = "P Olsen upscaled from 1 km"
ds["P_Olsen"].attrs["units"] = "mmol/kg"
ds["P_Olsen"].attrs["description"] = f"P Olsen [mmol/kg] = P Olsen [mg/kg] / 30.97"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the resulting dataset as a NetCDF file
output_nc = os.path.join(output_dir, "POlsen_05d.nc")
ds.to_netcdf(output_nc)

# Output message
print(f"P Olsen data has been successfully saved to: {output_nc}")