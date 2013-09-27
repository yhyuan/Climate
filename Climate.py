import httplib, time
def processOnePage(data1):
	results = []
	items = data1.split('<div class="span-2 row-end row-start margin-bottom-none station  wordWrap">')
	for i in range(1, len(items) - 1):
		StationName = items[i].split('</div> 				<div class="span-1 row-end row-start margin-bottom-none wordWrap">')[0].strip()
		StationID = items[i].split('<input type="hidden" name="StationID" value="')[1].split('" />  	<input type="hidden" name="Prov" value="ONT" />')[0]
		hlyRange = items[i].split('<input type="hidden" name="hlyRange" value="')[1].split('" /> 		<input type="hidden" name="dlyRange" value="')[0]
		dlyRange = items[i].split('<input type="hidden" name="dlyRange" value="')[1].split('" />   	<input type="hidden" name="mlyRange" value="')[0]
		mlyRange = items[i].split('<input type="hidden" name="mlyRange" value="')[1].split('" />  	<input type="hidden" name="StationID" value="')[0]
		# http://climate.weather.gc.ca/climateData/dailydata_e.html?timeframe=2&Prov=ONT&StationID=4612&dlyRange=1931-01-01|1966-11-30&Year=1966&Month=11&Day=01
		#conn = httplib.HTTPConnection("lrcdrrvsdvap002")
		#conn.request("GET", "/web/page2.htm")
		YMD = dlyRange.split("|")[1].split("-")
		conn = httplib.HTTPConnection("climate.weather.gc.ca")
		conn.request("GET", "/climateData/dailydata_e.html?timeframe=2&Prov=ONT&StationID=" + StationID + "&dlyRange=" + dlyRange + "&Year=" + YMD[0] + "&Month=" + YMD[1] + "&Day=" + YMD[2])		
		data1 = conn.getresponse().read()
		latitude = data1.split('<a href="/glossary_e.html#latitude">Latitude</a>:')[1].split('<a href="/glossary_e.html#longitude">Longitude</a>:')[0]
		latitude = latitude.split('<td>')[1].split('</td>')[0]
		degree = float(latitude.split('<abbr title="degrees">&deg;</abbr>')[0])
		minute = float(latitude.split('<abbr title="degrees">&deg;</abbr>')[1].split('<abbr title="minute">\'</abbr>')[0])
		second = float(latitude.split('<abbr title="minute">\'</abbr>')[1].split('<abbr title="second">&quot;</abbr>')[0])
		latitude = str(degree + minute/60.0 + second/3600.0)
		longitude = data1.split('<a href="/glossary_e.html#longitude">Longitude</a>:')[1].split('<a href="/glossary_e.html#elevation">Elevation</a>:')[0]
		longitude = longitude.split('<td>')[1].split('</td>')[0]	
		degree = float(longitude.split('<abbr title="degrees">&deg;</abbr>')[0])
		minute = float(longitude.split('<abbr title="degrees">&deg;</abbr>')[1].split('<abbr title="minute">\'</abbr>')[0])
		second = float(longitude.split('<abbr title="minute">\'</abbr>')[1].split('<abbr title="second">&quot;</abbr>')[0])
		longitude = str(-(degree + minute/60.0 + second/3600.0))
		elevation = data1.split('<a href="/glossary_e.html#elevation">Elevation</a>:')[1].split('<a href="/glossary_e.html#climate_ID">Climate ID</a>:')[0]
		elevation = elevation.split('<td>')[1].split('<abbr title="meter">m</abbr></td>')[0]
		climateID = data1.split('<a href="/glossary_e.html#climate_ID">Climate ID</a>:')[1].split('<a href="/glossary_e.html#wmo_id"><abbr title="World Meteorological Organization">WMO</abbr> ID</a>:')[0]
		climateID = climateID.split('<td>')[1].split('</td>')[0]
		WMOID = data1.split('<a href="/glossary_e.html#wmo_id"><abbr title="World Meteorological Organization">WMO</abbr> ID</a>:')[1].split('<a href="/glossary_e.html#tc_ID"><abbr title="Transport Canada">TC</abbr> ID</a>:')[0]
		WMOID = WMOID.split('<td>')[1].split('</td>')[0]
		TCID = data1.split('<a href="/glossary_e.html#tc_ID"><abbr title="Transport Canada">TC</abbr> ID</a>:')[1].split('</tbody>')[0]
		TCID = TCID.split('<td>')[1].split('</td>')[0]
		results.append([StationName, StationID, hlyRange, dlyRange, mlyRange, latitude, longitude, elevation,  climateID, WMOID, TCID])
		#print StationName + "\t" + StationID + "\t" + hlyRange + "\t" + dlyRange + "\t" + mlyRange + "\t" + latitude + "\t" + longitude + "\t" + elevation  + "\t" + climateID + "\t" + WMOID + "\t" + TCID
		time.sleep(5)
	return results

# http://climate.weather.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ONT&optLimit=yearRange&StartYear=1840&EndYear=2013&Year=2013&Month=9&Day=25&selRowPerPage=100&cmdProvSubmit=Search
# http://climate.weather.gc.ca/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ONT&optLimit=yearRange&StartYear=1840&EndYear=2013&Year=2013&Month=9&Day=27&selRowPerPage=100&cmdProvSubmit=Search&startRow=201
#conn = httplib.HTTPConnection("lrcdrrvsdvap002")
#conn.request("GET", "/web/page1.htm")
conn = httplib.HTTPConnection("climate.weather.gc.ca")
conn.request("GET", "/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ONT&optLimit=yearRange&StartYear=1840&EndYear=2013&Year=2013&Month=9&Day=25&selRowPerPage=100&cmdProvSubmit=Search")
r1 = conn.getresponse()
data1 = r1.read()
recordNumber = int(data1.split('locations match your customized search. Confirm the')[0].split('to share your comments and suggestions.</p>                </div></div><p>')[1])
time.sleep(5)
results = processOnePage(data1)
startRow = 101
while (startRow < recordNumber):
	conn = httplib.HTTPConnection("climate.weather.gc.ca")
	conn.request("GET", "/advanceSearch/searchHistoricDataStations_e.html?searchType=stnProv&timeframe=1&lstProvince=ONT&optLimit=yearRange&StartYear=1840&EndYear=2013&Year=2013&Month=9&Day=25&selRowPerPage=100&cmdProvSubmit=Search&startRow=" + str(startRow))
	results =  results + processOnePage(conn.getresponse().read())
	time.sleep(5)
	startRow = startRow + 100
f = open ("rows_contaion_enter.txt","w")
f.write("\t".join(["StationName", "StationID", "hlyRange", "dlyRange", "mlyRange", "latitude", "longitude", "elevation", "climateID", "WMOID", "TCID"]) + "\n")
for result in results:
	#print "\t".join(result)
	f.write("\t".join(result) + "\n")
f.close()
#print len(items)