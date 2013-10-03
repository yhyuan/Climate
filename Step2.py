# This script read the list.txt and a series of weather files
# and create a file geodatabase with weather station feature class. 
import sys, string, os
import arcpy
reload(sys)
sys.setdefaultencoding("latin-1")
import zipfile
INPUT_PATH = "input"
OUTPUT_PATH = "output"
os.system("ls " + INPUT_PATH + "//*.txt > " + INPUT_PATH + "//list.txt")
if arcpy.Exists(OUTPUT_PATH + "\\Climate.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\Climate.gdb /s /q")
arcpy.CreateFileGDB_management(OUTPUT_PATH, "Climate", "9.3")
OUTPUT_GDB = OUTPUT_PATH + "\\Climate.gdb"
arcpy.CreateFeatureclass_management(OUTPUT_GDB, "WeatherStations", "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
WeatherStations = OUTPUT_GDB + "\\WeatherStations"
# Process: Define Projection
arcpy.DefineProjection_management(WeatherStations, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
# Process: Add Fields	
arcpy.AddField_management(WeatherStations, "STATIONNAME", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
arcpy.AddField_management(WeatherStations, "ID", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
arcpy.AddField_management(WeatherStations, "Latitude", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(WeatherStations, "Longitude", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(WeatherStations, "Elevation", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(WeatherStations, "Climate_ID", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
arcpy.AddField_management(WeatherStations, "WMO_ID", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
arcpy.AddField_management(WeatherStations, "TC_ID", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
arcpy.AddField_management(WeatherStations, "COMMENTS", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
f = open (INPUT_PATH + "\\list.txt","r")
stations = f.read().split("\n")
f.close()
stations = map(lambda station: station[7:-4], stations)
#print stations
arcpy.env.workspace = OUTPUT_GDB
try:
	with arcpy.da.InsertCursor("WeatherStations", ("SHAPE@XY", "STATIONNAME", "ID", "Latitude", "Longitude", "Elevation", "Climate_ID", "WMO_ID", "TC_ID", "COMMENTS")) as cur:
		cntr = 1
		#print stations
		for StationID in stations:
			#print StationID
			f = open (INPUT_PATH + "\\" + StationID + ".txt","r")
			data = f.read()
			f.close()
			#print StationID
			items = data.split("\n")
			StationName = items[0].split("\",\"")[1][:-1]
			Latitude = float(items[2].split("\",\"")[1][:-1])
			Longitude = float(items[3].split("\",\"")[1][:-1])
			Elevation = items[4].split("\",\"")[1][:-1]
			if(len(Elevation) > 0):
				Elevation = float(Elevation)
			else:
				Elevation = float('nan')
			ClimateIdentifier = items[5].split("\",\"")[1][:-1]
			WMOIdentifier = items[6].split("\",\"")[1][:-1]
			TCIdentifier = items[7].split("\",\"")[1][:-1]
			Comments = ""
			if StationID == "4490":
				Latitude = 45.348
				Longitude = -80.035
				Comments = "Lat&Lng are calculated using Parry Sound."
			rowValue = [(Longitude, Latitude), StationName, StationID, Latitude, Longitude, Elevation, ClimateIdentifier, WMOIdentifier, TCIdentifier, Comments]
			cur.insertRow(rowValue)			
			#print StationID + "\t" + StationName + "\t" + Latitude + "\t" + Longitude + "\t" + Elevation + "\t" + ClimateIdentifier + "\t" + WMOIdentifier + "\t" + TCIdentifier
except Exception as e:
	print e.message

