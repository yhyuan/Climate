# This script downloads the weather station information from Canada National Climate Archives and save it in a text file named weather.txt. 
# This script need to send the http request to outside network. Firewall may restrict the access. 
import httplib, time
import urllib2
				  
def parseLatlng(input):
	items = input.split('<abbr title="degrees">&deg;</abbr>')
	degree = int(items[0][items[0].rfind('<td>') + len('<td>'):])
	items = items[1].split('<abbr title="minute">\'</abbr>')
	minute = int(items[0])
	second = float(items[1][:items[1].find('<abbr title="second">')])
	return str(degree + minute/60.0 + second/3600.0)
def processOnePage(data1):
	results = []
	items = data1.split('<div class="span-2 row-end row-start margin-bottom-none station  wordWrap">')
	for i in range(1, len(items) - 1):
		StationID = items[i].split('<input type="hidden" name="StationID" value="')[1].split('" />      <input type="hidden" name="Prov" value="ON" />')[0]
		dlyRange = items[i].split('<input type="hidden" name="dlyRange" value="')[1].split('" />      <input type="hidden" name="mlyRange" value="')[0]
		hlyRange = items[i].split('<input type="hidden" name="hlyRange" value="')[1].split('" />              <input type="hidden" name="dlyRange" value="')[0]
		mlyRange = items[i].split('<input type="hidden" name="mlyRange" value="')[1].split('" />      <input type="hidden" name="StationID" value="')[0]
		print StationID + "\t" + hlyRange + "\t" + dlyRange + "\t" + mlyRange
		if (hlyRange != "|"):
			end = hlyRange.split('|')[1].split('-')
			url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=ON&StationID=' + StationID + '&hlyRange=' + hlyRange + '&Year=' + end[0] + '&Month=' + str(int(end[1])) + '&Day=' + str(int(end[2]))
		elif (dlyRange != "|"):
			end = dlyRange.split('|')[1].split('-')
			url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=2&Prov=ON&StationID=' + StationID + '&dlyRange=' + dlyRange + '&Year=' + end[0] + '&Month=' + str(int(end[1])) + '&Day=01'
		elif (mlyRange != "|"):
			end = mlyRange.split('|')[1].split('-')
			url = 'http://climate.weather.gc.ca/climateData/hourlydata_e.html?timeframe=3&Prov=ON&StationID=' + StationID + '&mlyRange=' + mlyRange + '&Year=' + end[0] + '&Month=01&Day=01'
			#f = open('output//' + StationID + "_mly.html", 'w+')
			#f.write(urllib2.urlopen(url).read())
			#f.close()
		else:
			print "hlyRange, dlyRange, mlyRange are all missing."
			return []
		data = urllib2.urlopen(url).read()
		stationNameTag = '<th colspan="6" class="boxColor margin-bottom-none"><b>'
		temp = data[data.find(stationNameTag) + len(stationNameTag):]
		StationName = temp[:temp.find('<br />')].strip();
		tag = '<a href="http://climate.weather.gc.ca/glossary_e.html#latitude">Latitude</a>:'
		temp = data[data.find(tag) + len(tag):]
		temp = temp[temp.find('<td>'):temp.find('</td>')].strip()
		if len(temp) > 5:
			Latitude = parseLatlng(temp);
		else:
			Latitude = '0.0'
		tag = '<a href="http://climate.weather.gc.ca/glossary_e.html#longitude">Longitude</a>:'
		temp = data[data.find(tag) + len(tag):]
		temp = temp[temp.find('<td>'):temp.find('</td>')].strip()
		if len(temp) > 5:
			Longitude = str(-1*float(parseLatlng(temp)));
		else:
			Longitude = '0.0'
		tag = '<a href="http://climate.weather.gc.ca/glossary_e.html#elevation">Elevation</a>:'
		temp = data[data.find(tag) + len(tag):]
		Elevation = temp[temp.find('<td>') + len('<td>'):temp.find('</td>')].strip();
		if (Elevation.find('<abbr') > 0):
			Elevation = Elevation[:Elevation.find('<abbr')].strip();
		tag = '<a href="http://climate.weather.gc.ca/glossary_e.html#climate_ID">Climate ID</a>:'
		temp = data[data.find(tag) + len(tag):]
		ClimateID = temp[temp.find('<td>') + len('<td>'):temp.find('</td>')].strip();
		tag = '<a href="http://climate.weather.gc.ca/glossary_e.html#wmo_id"><abbr title="World Meteorological Organization">WMO</abbr> ID</a>:'
		temp = data[data.find(tag) + len(tag):]
		WMO_ID = temp[temp.find('<td>') + len('<td>'):temp.find('</td>')].strip();
		tag = '<a href="http://climate.weather.gc.ca/glossary_e.html#tc_ID"><abbr title="Transport Canada">TC</abbr> ID</a>:'
		temp = data[data.find(tag) + len(tag):]
		TC_ID = temp[temp.find('<td>') + len('<td>'):temp.find('</td>')].strip();
		
		time.sleep(2)
		results.append([StationName, StationID, Latitude, Longitude, Elevation, TC_ID, "", ClimateID, WMO_ID])
	return results

conn = httplib.HTTPConnection("climate.weather.gc.ca")
conn.request("GET", "/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=1840&EndYear=2015&Year=2015&Month=7&Day=29&selRowPerPage=100&cmdProvSubmit=Search")
r1 = conn.getresponse()
data1 = r1.read()
temp = data1[:data1.find('locations match your customized search. Confirm the')]
recordNumber = int(temp[temp.rfind('>') + 1:])
time.sleep(5)
results = processOnePage(data1)
startRow = 101
while (startRow < recordNumber):
	conn = httplib.HTTPConnection("climate.weather.gc.ca")
	conn.request("GET", "/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ON&optLimit=yearRange&StartYear=1840&EndYear=2015&Year=2015&Month=7&Day=29&selRowPerPage=100&cmdProvSubmit=Search&startRow=" + str(startRow))
	results =  results + processOnePage(conn.getresponse().read())
	time.sleep(2)
	startRow = startRow + 100

#print results
f = open ("weather.txt","w")
f.write("\n".join(map(lambda row: "\t".join(row), results)))
f.close()
