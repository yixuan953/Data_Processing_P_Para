The scripts in this folder is used to calculate the parameters that are related to P cycling

To calculate the following factors, we need the original inputs as follows:

1. (Al+Fe)ox: Oxalate extractable AL and Fe contents (mmol/kg)
   The data is from Ren et al.(2024) (https://doi.org/10.1111/gcb.17576) and is available on: https://zenodo.org/records/13995030
2. Soil total P 
   The data is from He et al.(2021) (https://essd.copernicus.org/articles/13/5831/2021/) and is available on: https://figshare.com/articles/figure/Global_patterns_and_drivers_of_soil_total_phosphorus_concentration/14583375
3. P Olsen
   The data is from (2023 ) (https://doi.org/10.1038/s41597-023-02022-4) and is available on: https://figshare.com/articles/dataset/Global_Available_Soil_Phosphorus_Database/14241854


--------------- Maximum labile and stable pool -------------
1. Maximum labile P pool [mmol/kg] = 1/6 * (Al+Fe)ox
2. Maximum stable P pool [mmol/kg] = 1/3 * (Al+Fe)ox

--------------- P transfer constant -------------
1. KF: Freudlich constant of the stable pool = 0.5 * ((Al+Fe)ox - Lmax)/90
2. miu_DisS = 0.0014
3. miu_SDis* = 
    - Sand: 2 * 10-6
    - Clay: 44 * 10-6
    - Loam?

---------------------- Other Factors -----------------------
1. Humification coefficient (hc, unit: -): 
   (1-hc) = how much organic input (manure + residue) will be available for crop uptake in inorganic format
   The coefficent could be found from: https://edepot.wur.nl/541822  
