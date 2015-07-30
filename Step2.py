# This script read the weather.txt and create a file geodatabase with weather station feature class. 

import sys, string, os, time
import arcpy
reload(sys)
sys.setdefaultencoding("latin-1")
import zipfile
start_time = time.time()
INPUT_PATH = "input"
OUTPUT_PATH = "output"
#os.system("ls " + INPUT_PATH + "//*.txt > " + INPUT_PATH + "//list.txt")
if arcpy.Exists(OUTPUT_PATH + "\\Climate.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\Climate.gdb /s /q")
arcpy.CreateFileGDB_management(OUTPUT_PATH, "Climate", "9.3")
OUTPUT_GDB = OUTPUT_PATH + "\\Climate.gdb"
arcpy.env.workspace = OUTPUT_PATH + "\\Climate.gdb"

def createFeatureClass(featureName, featureData, featureFieldList, featureInsertCursorFields):
	print "Create " + featureName + " feature class"
	featureNameNAD83 = featureName + "_NAD83"
	featureNameNAD83Path = arcpy.env.workspace + "\\"  + featureNameNAD83
	arcpy.CreateFeatureclass_management(arcpy.env.workspace, featureNameNAD83, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	# Process: Define Projection
	arcpy.DefineProjection_management(featureNameNAD83Path, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	# Process: Add Fields	
	for featrueField in featureFieldList:
		arcpy.AddField_management(featureNameNAD83Path, featrueField[0], featrueField[1], featrueField[2], featrueField[3], featrueField[4], featrueField[5], featrueField[6], featrueField[7], featrueField[8])
	# Process: Append the records
	cntr = 1
	try:
		with arcpy.da.InsertCursor(featureNameNAD83, featureInsertCursorFields) as cur:
			for rowValue in featureData:
				cur.insertRow(rowValue)
				cntr = cntr + 1
	except Exception as e:
		print "\tError: " + featureName + ": " + e.message
	# Change the projection to web mercator
	#arcpy.Project_management(featureNameNAD83Path, arcpy.env.workspace + "\\" + featureName, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	#arcpy.FeatureClassToShapefile_conversion([featureNameNAD83Path], OUTPUT_PATH + "\\Shapefile")
	#arcpy.Delete_management(featureNameNAD83Path, "FeatureClass")
	print "Finish " + featureName + " feature class."

featureName = "EC_Weather_Stations"
featureFieldList = [["STATIONNAME", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["ID", "LONG", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["Latitude", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["Longitude", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["ALTITUDE", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["TC_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["COMMENTS", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["Climate_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["WMO_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""]]
featureInsertCursorFields = tuple(["SHAPE@XY"] + map(lambda list: list[0],featureFieldList))

f = open (INPUT_PATH + "\\weather.txt","r")
stations = f.read().split("\n")
f.close()
def getRow(line):
	items = line.split('\t')
	items = map(lambda item: item.replace("&nbsp;", ""), items)
	#print items
	stationName = items[0]
	stationID = int(items[1])
	latitude = float(items[2])
	longitude = float(items[3])
	elevation = None if len(items[4]) == 0 else float(items[4])
	TC_ID = items[5]
	COMMENTS = items[6]
	Climate_ID = items[7]
	WMO_ID = items[8]
	if stationID == 4490:
		latitude = 45.348
		longitude = -80.035
		COMMENTS = "Lat&Lng are calculated using Parry Sound."	
	return [(longitude, latitude), stationName, stationID, latitude, longitude, elevation, TC_ID, COMMENTS, Climate_ID, WMO_ID]
rows = map(getRow, stations);
createFeatureClass(featureName, rows, featureFieldList, featureInsertCursorFields)

elapsed_time = time.time() - start_time
print elapsed_time


