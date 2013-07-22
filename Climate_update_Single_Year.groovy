/**
 * 
 */



/**
 * @author Administrator
 *
 */
public class Climate_update_Single_Year{
	public static String [] typeList = ["hly","dly","mly","alm"]

	/**
	 * @param args
	 */
	public static void main(def args){
		try{
		//String stationId = '26891';
		println args[0];
		String stationId = args[0];
		String year = '2009';
		GroovyHTTP h2 = new GroovyHTTP('http://climate.weatheroffice.gc.ca/climateData/bulkdata_e.html')
		h2.setMethod('GET') 
		h2.setParam('timeframe', '2')
		h2.setParam('Prov', 'XX')
		h2.setParam('StationID', stationId)
		h2.setParam('Year', year)
		h2.setParam('Month', '01')
		h2.setParam('Day', '01')
		h2.setParam('type', 'dly')
		h2.open()
		h2.write()
		h2.read() 				 
		String output2 =  h2.getContent()
		File dataFile = new File("C:\\working\\climate\\dly_" + stationId + "_" + year + ".csv")
		dataFile.append(output2)
		h2.close()
		    		
		println(dataFile.getName())
		Thread.sleep(2000)
	}catch(Exception e){
		System.out.println("Error")
	}
	}	
}
