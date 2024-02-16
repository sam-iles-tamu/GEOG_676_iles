## 02-15-2024 
## Lab 04

#Tasks: 
#1. Read in garage location X/Y coords from the provided .csv
#2. Create a geodatabase and add in the input layers
#3. Buffer the garage points
#4. Intersect the buildings layer with the buffered garage points
#5. Output the resulting table to a .csv

import arcpy
arcpy.env.workspace = "P:/676/ArcGISpython/Lab_04" 
arcpy.env.scratchWorkspace = "P:/676/ArcGISpython/scratch"

# (1)
garages_table = r"P:/676/ArcGISpython/mod_17/garages.csv"
garages = arcpy.MakeXYEventLayer_management(garages_table, "X", "Y", "garages")

# (2)
arcpy.CreateFileGDB_management(arcpy.env.workspace, 'garages.gdb')

campus = r"P:/676/ArcGISpython/mod_17/Campus.gdb"
structures = campus + "/Structures"
inputlayers = [garages, structures]
arcpy.FeatureClassToGeodatabase_conversion(inputlayers, "P:/676/ArcGISpython/Lab_04/garages.gdb")

# (3) 
#arcpy.analysis.Buffer(in_features, out_feature_class, buffer_distance_or_field, {line_side}, {line_end_type}, {dissolve_option}, {dissolve_field}, {method})
garages_gdb = r"P:/676/ArcGISpython/Lab_04/garages.gdb"
buffer_input = input('Buffer distance in meters: ')
arcpy.Buffer_analysis(garages_gdb + '/garages', garages_gdb + '/garages_buff', buffer_input)

# (4)
#arcpy.analysis.Intersect(in_features, out_feature_class, {join_attributes}, {cluster_tolerance}, {output_type})
arcpy.Intersect_analysis([garages_gdb + '/garages_buff', structures], garages_gdb + '/garage_str_intersect')
# (5)
arcpy.ExportTable_conversion(garages_gdb + "/garage_str_intersect.dbf", arcpy.env.workspace + "/created_intersection.csv") 
