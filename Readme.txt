The scripts in this folder is used to calculate the parameters that are related to P cycling

1. (Al+Fe)ox: Oxalate extractable AL and Fe contents (mmol/kg)
   The data is from Ren et al.(2024) (https://doi.org/10.1111/gcb.17576) and is available on: https://zenodo.org/records/13995030
   Here we: 
      1-1 Sum up the Al-oxalate and Fe-oxalate for top 40cm at 1km (unit = kg/m2)
      1-2 Upscale to 0.5 degree, and transform to (Al+Fe)ox (unit = mmol/m2)
      1-3 Transform the unit to the mmol/kg by dividing soil bulk density from HWSD:
          (Al+Fe)ox [mmol/kg] = (Al+Fe)ox [mmol/m2] * area_of_each_pixel [m2] / (bulk_density [kg/dm-1] * topsoil_depth [4dm])
   
2. PC ratio of soil organic matter: [-]
   The calculation method is from Tipping et al. (2016) based on global soil organic matter analysis: https://link.springer.com/article/10.1007/s10533-016-0247-z#Sec5
   PC_ratio = PC_npSOM * Fnpsom + PC_nrSOM * Fnrsom 
   Here:
      - PC_npSOM = 0.0011
      - PC_nrSOM = 0.016
      if soc < 0.1: Fnpsom = 0, Fnrsom = 1; 
      if soc > 50.: Fnpsom = 1, Fnrsom = 0; 
      if 0.1<= soc <= 50.: 
         Fnpsom = log10(soc/0.1) / log10(50/0.1)
         Fnrsom = 1 - Fnpsom
   The soc data is from HWSD at https://www.hydroshare.org/resource/1361509511e44adfba814f6950c6e742/

3. P Olsen [mmol/kg]
   The data is from McDowell et al. (2023) (https://doi.org/10.1038/s41597-023-02022-4) and is available on: https://figshare.com/articles/dataset/Global_Available_Soil_Phosphorus_Database/14241854
   The original P Olsen is mg/kg at 1 km. Here we:
   1) Firstly upscale to 0.5 degree;
   2) Transform the unit to mmol/kg by dividing 30.97


The above mentioned parameters will be used for following calculations:

--------------- Maximum labile and stable pool -------------
1. Maximum labile P pool (Lmax) [mmol/kg] = 1/6 * (Al+Fe)ox
2. Maximum stable P pool [mmol/kg] = 1/3 * (Al+Fe)ox

--------------- P transfer constant -------------
KF: Freudlich constant of the stable pool = 0.5 * ((Al+Fe)ox - Lmax)/90**nP

---------------------- Other Factors -----------------------
1. Humification coefficient (hc, unit: -): 
   (1-hc) = how much organic input (manure + residue) will be available for crop uptake in inorganic format
   The coefficent could be found from: https://edepot.wur.nl/541822 

2. miu_DisS = 0.0014

3. miu_SDis* = 
    - Sand: 2 * 10-6
    - Clay: 44 * 10-6
    - Loam: Take the average 
