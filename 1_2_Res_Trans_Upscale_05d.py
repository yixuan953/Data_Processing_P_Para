import os
import numpy as np
import xarray as xr

dir = '/lustre/nobackup/WUR/ESG/zhou111/Data/Processed/Soil'

f_Al = os.path.join(dir, f"Alo_top40cm_1km.nc")
f_Fe = os.path.join(dir, f"Feo_top40cm_1km.nc")

ds_Al = xr.open_dataset(f_Al)
ds_Fe = xr.open_dataset(f_Fe)

# Define the target grid resolution (0.5 degrees)
resolution = 0.5

# Create the target grid coordinates (centers of the cells)
lat_centers = np.linspace(89.75, -89.75, 360)  # Exactly 360 elements
lon_centers = np.linspace(-179.75, 179.75, 720)  # Exactly 720 elements

# Create a combined dataset with the variables we want to regrid
ds_combined = xr.Dataset({
    'Al_ox': (['lat', 'lon'], ds_Al['total_oxlate'].values),
    'Fe_ox': (['lat', 'lon'], ds_Fe['total_oxlate'].values)
}, coords={
    'lat': ds_Al.lat,
    'lon': ds_Al.lon
})

# Create the target grid
target_grid = xr.Dataset(coords={
    'lat': lat_centers,
    'lon': lon_centers
})

# Function to perform the regridding
def regrid_dataset(ds, target_grid):
    """
    Regrid a dataset to a target grid using binning approach that works for regular lat/lon grids
    """
    # Create a new dataset for the regridded data
    regridded = xr.Dataset(
        data_vars={
            var_name: (['lat', 'lon'], np.full((len(target_grid.lat), len(target_grid.lon)), np.nan))
            for var_name in ds.data_vars
        },
        coords={
            'lat': target_grid.lat,
            'lon': target_grid.lon
        }
    )
    
    # Calculate bin edges for the target grid
    lat_edges = np.linspace(-90, 90, 361)  # Include both edges for 360 bins
    lon_edges = np.linspace(-180, 180, 721)  # Include both edges for 720 bins
    
    # Bin the data using histogram2d approach for each variable
    for var_name in ds.data_vars:
        # Get the variable data and coordinates
        var_data = ds[var_name].values
        lats = ds.lat.values
        lons = ds.lon.values
        lon_grid, lat_grid = np.meshgrid(lons, lats)

        # Create masks for valid data points
        valid_mask = ~np.isnan(var_data)
        valid_lats = lat_grid[valid_mask]
        valid_lons = lon_grid[valid_mask]
        valid_data = var_data[valid_mask]
        
        if len(valid_data) > 0:
            # Use numpy's histogram2d to bin the data
            sum_hist, _, _ = np.histogram2d(
                valid_lats, valid_lons, bins=[lat_edges, lon_edges],
                weights=valid_data
            )
            
            count_hist, _, _ = np.histogram2d(
                valid_lats, valid_lons, bins=[lat_edges, lon_edges]
            )
            
            # Calculate the mean (avoiding division by zero)
            with np.errstate(divide='ignore', invalid='ignore'):
                mean_data = np.divide(sum_hist, count_hist)
            
            # Assign the regridded data
            regridded[var_name].values = mean_data[::-1, :]
               
    return regridded


# Perform the regridding
regridded = regrid_dataset(ds_combined, target_grid)

# Calculate the total in mmol/m2
regridded['Al_Fe_Ox_total'] = regridded['Al_ox'] * 37073.4 + regridded['Fe_ox'] * 17858.0

# Add attributes
regridded['Al_ox'].attrs['units'] = 'kg/m2'
regridded['Al_ox'].attrs['long_name'] = 'Al oxalate extractable content at 0-40 cm depth'

regridded['Fe_ox'].attrs['units'] = 'kg/m2'
regridded['Fe_ox'].attrs['long_name'] = 'Fe oxalate extractable content at 0-40 cm depth'

regridded['Al_Fe_Ox_total'].attrs['units'] = 'mmol/m2'
regridded['Al_Fe_Ox_total'].attrs['long_name'] = 'Total Al-Fe oxalate extractable content at 0-40 cm depth'

# Save the result
output_path = os.path.join(dir, 'Al_Fe_Ox_top40cm_05d.nc')
regridded.to_netcdf(output_path)

print(f"Regridded .nc file has been saved successfully at: {output_path}")