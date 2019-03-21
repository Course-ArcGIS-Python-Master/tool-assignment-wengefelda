
#install packages

import arcpy
import sys
import os

# Set a new workspace

arcpy.env.workspace = r"C:\LocalDirectory_PWELL_GIS\PWELL_Python\Nitrogen_Scripting"

arcpy.env.scratchWorkspace = r"C:\LocalDirectory_PWELL_GIS\PWELL_Python\Nitrogen_Scripting"


# Set the geoprocessing environment extent


# Top - 993361.415
# Bottom - 979906.554
# Left - 2701885.213
# Right -  2763306.328

# Spatial reference: NAD_1983_StatePlane_Massachusetts_Mainland_FIPS_2001Lambert_Conformal_Conic


arcpy.env.extent = arcpy.Extent(2701885.213, 979906.554, 2763306.328, 993361.415)

in_Table = r"C:\LocalDirectory_PWELL_GIS\nresults\NitrateResults_script.xlsx"

x_coords = "X"

y_coords = "Y"

z_coords = ""

out_Layer = "Tested_well_locations"

saved_Layer = r"Step_1_Tested_well_locations_Output.shp"



# Set the spatial reference

spRef = arcpy.SpatialReference(2249)  # 2249 == NAD_1983


###################################################################################################################

cwd = sys.path[0]

#Set Input and Output
input_table = os.path.join(cwd, "Up_To_Date_PWELL_Volunteer_list.xlsx")

#Create a file geodatabase to store the output feature class
output_gdb_name = "OutputsPythonGeocode.gdb"
output_gdb = os.path.join(cwd, output_gdb_name)
if not os.path.exists(output_gdb):
    arcpy.management.CreateFileGDB(cwd, output_gdb_name)
output_feature_class = os.path.join(output_gdb,"WellLocations")

#Overwrite the output feature class if it already exists
arcpy.env.overwriteOutput = True

#Create the ArcGIS Server connection file
server_url = r"https://geocode.arcgis.com/arcgis/services"
conn_file_name = r"arcgis_online_batch_geocoding.ags"
conn_file = os.path.join(cwd, conn_file_name)
username = "URI.NRS.awengefelda"
password = "KaylaMae26!"
arcpy.mapping.CreateGISServerConnectionFile("USE_GIS_SERVICES", cwd, conn_file_name, server_url,
                                            "ARCGIS_SERVER", username=username, password=password)

#Build field mappings from the input table
input_mappings = {"Address": "well_address",
                  "City":"well_city",
                  "Region": "well_state",
                  "Postal": "zip"
                  }
field_mappings = arcpy.FieldInfo()
for field in input_mappings:
    field_mappings.addField(field, input_mappings[field], "VISIBLE", "NONE")

#Perform batch geocoding
address_locator = os.path.join(conn_file, "World.GeocodeServer")
arcpy.geocoding.GeocodeAddresses(input_table, address_locator, field_mappings,
                                 output_feature_class)
print arcpy.GetMessages()




