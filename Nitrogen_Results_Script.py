##install package
import arcpy
import os
import sys

#Overwrite the output feature class if it already exists
arcpy.env.overwriteOutput = True
#
Directory = r"D:\PWELL\LocalDirectory_PWELL_GIS\PWELL_Python"
#
# # Set a new workspace
arcpy.env.workspace = os.path.join((Directory, "Nitrogen_Scripting"))
arcpy.env.scratchWorkspace = (Directory + "\Nitrogen_Scripting")

print arcpy.env.workspace

in_Table = Directory + r"\NitrateResults.csv"
x_coords = "X"
y_coords = "Y"
z_coords = ""
out_Layer = "Tested_well_locations"
saved_Layer = r"Step_1_Tested_well_locations_Output.shp"

#Set Spatial Reference
spRef = arcpy.SpatialReference(2249)
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, "")

#Save to layer file
arcpy.CopyFeatures_management(lyr, saved_Layer)
if arcpy.Exists(saved_Layer):
    print "SHP file creation successful"


#Extract extent

desc = arcpy.Describe(saved_Layer)
XMin = desc.extent.XMin
XMax = desc.extent.XMax
YMin = desc.extent.YMin
YMax = desc.extent.YMax

# Spatial reference: NAD_1983_StatePlane_Massachusetts_Mainland_FIPS_2001Lambert_Conformal_Conic

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2249)



##################################################################################################################
####SOURCE CODE ####https://github.com/deelesh/batch-geocoding-python/blob/master/BatchGeocoding.py########
#############################################################################################################

#Set Input
csvfile = os.path.join((Directory, "Up_To_Date_PWELL_Volunteer_list"))




#Create a file geodatabase to store the output feature class

output_gdb_name = "OutputPythonGeocode.gdb"

output_gdb = os.path.join(arcpy.env.workspace, output_gdb_name)

if not os.path.exists(output_gdb):

    arcpy.management.CreateFileGDB(arcpy.env.workspace, output_gdb_name)

output_feature_class = os.path.join(output_gdb, "WellLocations")

print "GDB Created"



#Create the ArcGIS Server connection file

server_url = r"https://geocode.arcgis.com/arcgis/services"

conn_file_name = r"arcgis_online_batch_geocoding.ags"

conn_file = os.path.join(Directory, conn_file_name)

username = "URI.NRS.awengefelda"

password = "KaylaMae26!"

arcpy.mapping.CreateGISServerConnectionFile("USE_GIS_SERVICES", Directory, conn_file_name, server_url,

                                            "ARCGIS_SERVER", username=username, password=password)

print "Log on to ARCGIS Server Successful"

#Build field mappings from the input table

input_mappings = {"Address": "well_address",

                  "City": "well_city",

                  "Region": "well_state",

                  "Postal": "zip"}

field_mappings = arcpy.FieldInfo()

for field in input_mappings:

    field_mappings.addField(field, input_mappings[field], "VISIBLE", "NONE")

print "field mapping built"

#Perform batch geocoding

address_locator = os.path.join(conn_file, "World.GeocodeServer")

arcpy.GeocodeAddresses_geocoding(input_table, address_locator, field_mappings, output_feature_class)

print arcpy.GetMessages()


