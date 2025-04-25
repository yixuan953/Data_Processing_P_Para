# This code is used to sum up the (Al+Fe)ox of the top 0-40 layers by ta
import os
import numpy as np
import xarray as xr

dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil'

f_Al = os.path.join(dir, f"Alo_top40cm_1km.nc")
f_Fe = os.path.join(dir, f"Feo_top40cm_1km.nc")

ds_Al = xr.open_dataset(f_Al)
ds_Fe = xr.open_dataset(f_Fe)

# Create the latitude and longitude bins
lat_bins = np.arange(90, -90, -0.5)
lon_bins = np.arange(-180, 180, 0.5)

# Assign bins to both datasets
ds_Al['lat_bin'] = xr.DataArray(np.digitize(ds_Al['lat'], lat_bins) - 1, dims="lat")
ds_Al['lon_bin'] = xr.DataArray(np.digitize(ds_Al['lon'], lon_bins) - 1, dims="lon")

ds_Fe['lat_bin'] = xr.DataArray(np.digitize(ds_Fe['lat'], lat_bins) - 1, dims="lat")
ds_Fe['lon_bin'] = xr.DataArray(np.digitize(ds_Fe['lon'], lon_bins) - 1, dims="lon")

# First, combine the two datasets before binning to ensure consistent bins
ds_combined = xr.Dataset({
    'Al_ox': ds_Al['total_oxlate'],
    'Fe_ox': ds_Fe['total_oxlate']
})

# Transfer the bin indices
ds_combined['lat_bin'] = ds_Al['lat_bin']
ds_combined['lon_bin'] = ds_Al['lon_bin']

# Group and average by bins using mean (proper spatial averaging)
regridded = ds_combined.groupby(['lat_bin', 'lon_bin']).mean(skipna=True)

# Calculate the bin centers for real lat/lon values
lat_centers = lat_bins[:-1] + 0.25
lon_centers = lon_bins[:-1] + 0.25

# Assign the real lat/lon coordinates
regridded = regridded.assign_coords({
    "lat": ("lat_bin", lat_centers[regridded.lat_bin.values]),
    "lon": ("lon_bin", lon_centers[regridded.lon_bin.values])
})

# Calculate the total in mmol/m2
regridded['Al_Fe_Ox_total'] = regridded['Al_ox'] * 37073.4 + regridded['Fe_ox'] * 17858.0

# Rename dimensions to standard lat/lon
regridded = regridded.rename({"lat_bin": "lat", "lon_bin": "lon"})

# Add attributes
regridded['Al_ox'].attrs['units'] = 'kg/m2'
regridded['Al_ox'].attrs['long_name'] = 'Al oxalate extractable content at 0-40 cm depth'

regridded['Fe_ox'].attrs['units'] = 'kg/m2'
regridded['Fe_ox'].attrs['long_name'] = 'Fe oxalate extractable content at 0-40 cm depth'

regridded['Al_Fe_Ox_total'].attrs['units'] = 'mmol/m2'
regridded['Al_Fe_Ox_total'].attrs['long_name'] = 'Total Al-Fe oxalate extractable content at 0-40 cm depth'

output_path = os.path.join(dir, 'Al_Fe_Ox_top40cm_05d.nc')
regridded.to_netcdf(output_path)

print(f"Regridded .nc file has been saved successfully at: {output_path}")