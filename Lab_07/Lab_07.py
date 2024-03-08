## Lab 07 raster analysis
## Sam Iles 03-08-2024

import arcpy
# Step 1: assign bands
source = r"P:/676/ArcGISpython/Lab_07/"
band1 = arcpy.Raster(source + r"Band1.tif")
band2 = arcpy.Raster(source + r"Band2.tif")
band3 = arcpy.Raster(source + r"Band3.tif")
band4 = arcpy.Raster(source + r"Band4.tif")
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"output_combined.tif")

# Step 2: hillshade
dem_file = arcpy.Raster(source + r"n44_w123_1arc_v3.tif") #note this step is not in tutorial
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.HillShade_3d(dem_file, source + r"output_hill.tif", azimuth, altitude, shadows, z_factor)

# Step 3: slope
output_meas = "DEGREE"
arcpy.Slope_3d(dem_file, source + r"output_slope.tif",output_meas, z_factor)