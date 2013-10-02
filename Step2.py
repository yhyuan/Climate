# This script read the list.txt and a series of weather files
# and create a file geodatabase with weather station feature class. 
import sys, string, os
import arcpy
reload(sys)
sys.setdefaultencoding("latin-1")
import zipfile
INPUT_PATH = "input"
OUTPUT_PATH = "output"
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
stations = map(lambda station: station[:-4], stations)
#print stations
arcpy.env.workspace = OUTPUT_GDB
try:
	with arcpy.da.InsertCursor("WeatherStations", ("SHAPE@XY", "STATIONNAME", "ID", "Latitude", "Longitude", "Elevation", "Climate_ID", "WMO_ID", "TC_ID", "COMMENTS")) as cur:
		cntr = 1
		# = ["10084", "10087", "10088", "10197", "10220", "10244", "10664", "10685", "10726", "10753", "10787", "10804", "10899", "10900", "10903", "10910", "10911", "10918", "10950", "10955", "10973", "10999", "11000", "11008", "26770", "26771", "26773", "26775", "26799", "26859", "26860", "26861", "26862", "26891", "26912", "26953", "27001", "27002", "27003", "27004", "27082", "27083", "27084", "27087", "27197", "27206", "27207", "27227", "27291", "27322", "27323", "27335", "27337", "27447", "27448", "27485", "27488", "27528", "27529", "27530", "27531", "27533", "27534", "27535", "27545", "27603", "27604", "27605", "27612", "27613", "27614", "27615", "27616", "27618", "27647", "27674", "27865", "27866", "28037", "28071", "29368", "29391", "29516", "29846", "29906", "30186", "30240", "30242", "30246", "30247", "30266", "30435", "30455", "30578", "30667", "30682", "30723", "31008", "31009", "31010", "31011", "31028", "31047", "31048", "31049", "31127", "31147", "31367", "31688", "32008", "32128", "32393", "32473", "3913", "3914", "3915", "3916", "3917", "3918", "3919", "3920", "3921", "3922", "3923", "3924", "3925", "3926", "3927", "3928", "3929", "3930", "3931", "3932", "3933", "3934", "3935", "3936", "3937", "3938", "3939", "3940", "3941", "3942", "3943", "3944", "3945", "3946", "3947", "3948", "3949", "3950", "3951", "3952", "3953", "3954", "3955", "3956", "3957", "3958", "3959", "3960", "3961", "3962", "3963", "3964", "3965", "3966", "3967", "3968", "3969", "3970", "3971", "3972", "3973", "3974", "3975", "3976", "3977", "3978", "3979", "3980", "3982", "3983", "3984", "3985", "3986", "3987", "3988", "3989", "3990", "3991", "3992", "3993", "3994", "3995", "3996", "3997", "3998", "3999", "4000", "4001", "4002", "4003", "4004", "4005", "4006", "4007", "4008", "4009", "4010", "4011", "4012", "4013", "4014", "4015", "4016", "4017", "4018", "4019", "4020", "4021", "4022", "4023", "4024", "4025", "4026", "4027", "4028", "4029", "4030", "4031", "4032", "4033", "4034", "4035", "4036", "4037", "4038", "4039", "4040", "4041", "4042", "4043", "4044", "4045", "4046", "4047", "4048", "4049", "4050", "4051", "4052", "4053", "4054", "4055", "4056", "4057", "4058", "4059", "4060", "4061", "4062", "4063", "4064", "4065", "4066", "4067", "4068", "4069", "4070", "4071", "4072", "4073", "4074", "4075", "4076", "4077", "4078", "4079", "4080", "4081", "4082", "4083", "4084", "4085", "4086", "4087", "4088", "4089", "4090", "4091", "4092", "4093", "4094", "4095", "4096", "4097", "4098", "4099", "4100", "4101", "4102", "4103", "4104", "4105", "4106", "4107", "4108", "4109", "4110", "4111", "4112", "4113", "4114", "4115", "4116", "4117", "4118", "4119", "4120", "4121", "4122", "4123", "4124", "4125", "4126", "4127", "4128", "4129", "4130", "4131", "4132", "4133", "4134", "4135", "4136", "4137", "4138", "4139", "4140", "4141", "4142", "4143", "4144", "4145", "4146", "4147", "4148", "4149", "4150", "4151", "4152", "4153", "4154", "4155", "4156", "4157", "4158", "4159", "41595", "4160", "4161", "4162", "4163", "4164", "4165", "4166", "4167", "4168", "4169", "4170", "4171", "4172", "4173", "41738", "4174", "4175", "4176", "4177", "4178", "4179", "4180", "41803", "4181", "4182", "4183", "4184", "4185", "4186", "4187", "4188", "4189", "4190", "4191", "4192", "4193", "4194", "4195", "4196", "4197", "4198", "41983", "4199", "4200", "42003", "42004", "42005", "42006", "4201", "4202", "4203", "4204", "4205", "4206", "4207", "4208", "4209", "4210", "4211", "4212", "42123", "4213", "4214", "4215", "4216", "4217", "4218", "42183", "4219", "4220", "4221", "4222", "4223", "4224", "4225", "4226", "4227", "4228", "4229", "4230", "4231", "4232", "4233", "4234", "4235", "4236", "4237", "4238", "4239", "4240", "4241", "4242", "42424", "4243", "4244", "4245", "4246", "4247", "4248", "4249", "4250", "4251", "4252", "42523", "4253", "4254", "4255", "4256", "4257", "4258", "4259", "4260", "4261", "4262", "42623", "4263", "4264", "4265", "4266", "4267", "4268", "4269", "4270", "4271", "4272", "4273", "4274", "4275", "4276", "4277", "4278", "4279", "4280", "4281", "4282", "4283", "4284", "4285", "4286", "4287", "4288", "4289", "4290", "4291", "4292", "4293", "4294", "4295", "4296", "42967", "4297", "4298", "4299", "4300", "4301", "4302", "4303", "4304", "43046", "4305", "4306", "4307", "4308", "4309", "4310", "43104", "4311", "4312", "4313", "4314", "4315", "4316", "4317", "4318", "4319", "4320", "43203", "4321", "4322", "4323", "4324", "4325", "4326", "4327", "4328", "4329", "4330", "4331", "4332", "4333", "4334", "4335", "4336", "4337", "4338", "4339", "4340", "4341", "4342", "4343", "4344", "4345", "4346", "4347", "4348", "4349", "4350", "4351", "4352", "43520", "4353", "4354", "43540", "4355", "4356", "4357", "4358", "4359", "4360", "43600", "4361", "4362", "4363", "4364", "4365", "4366", "4367", "4368", "4369", "4370", "4371", "4372", "4373", "4374", "4375", "4376", "43763", "4377", "4378", "4379", "4380", "4381", "4382", "43823", "4383", "4384", "4385", "4386", "4387", "4388", "4389", "4390", "4391", "43910", "4392", "43923", "4393", "4394", "4395", "4396", "4397", "4398", "4399", "4400", "44004", "4401", "4402", "4403", "4404", "4405", "4406", "44063", "4407", "4408", "4409", "4410", "4411", "4412", "44123", "4413", "4414", "4415", "4416", "44163", "4417", "4418", "44183", "4419", "4420", "44205", "4421", "4422", "4423", "4424", "4425", "4426", "44263", "4427", "4428", "44283", "4429", "4430", "44303", "4431", "4432", "44323", "44324", "4433", "4434", "44343", "4435", "4436", "4437", "4438", "4439", "4440", "4441", "4442", "4443", "4444", "4445", "4446", "4447", "4448", "44483", "4449", "4450", "4451", "4452", "4453", "4454", "4455", "4456", "4457", "4458", "4459", "4460", "4461", "4462", "4463", "4464", "4465", "4466", "4467", "4468", "4469", "4470", "4471", "4472", "4473", "4474", "4475", "4476", "4477", "4478", "44787", "4479", "4480", "44806", "4481", "4482", "44826", "4483", "4484", "44847", "4485", "4486", "4487", "4488", "4489", "4490", "4491", "4492", "4493", "4494", "44947", "4495", "4496", "44967", "4497", "4498", "44987", "4499", "4500", "4501", "4502", "4503", "4504", "4505", "4506", "4507", "4508", "45088", "4509", "4510", "4511", "4512", "4513", "4514", "4515", "4516", "4517", "4518", "4519", "4520", "4521", "4522", "4523", "4524", "4525", "4526", "4527", "4528", "4529", "4530", "4531", "4532", "4533", "4534", "45347", "45348", "45349", "4535", "4536", "4537", "4538", "4539", "4540", "45407", "4541", "4542", "4543", "4544", "45447", "4545", "4546", "4547", "4548", "4549", "4550", "4551", "4552", "4553", "4554", "45547", "4555", "4556", "4557", "4558", "4559", "4560", "45607", "4561", "4562", "4563", "4564", "4565", "4566", "45667", "4567", "4568", "4569", "4570", "4571", "4572", "4573", "4574", "4575", "4576", "4577", "4578", "4579", "4580", "4581", "4582", "4583", "4584", "4585", "4586", "4587", "4588", "4589", "4590", "4591", "4592", "4593", "4594", "4595", "4596", "45967", "4597", "4598", "4599", "4600", "4601", "4602", "4603", "4604", "4605", "4606", "4607", "4608", "4609", "4610", "4611", "4612", "4613", "4614", "4615", "4616", "4617", "4618", "4619", "4620", "4621", "4622", "4623", "4624", "4625", "4626", "4627", "4628", "4629", "4630", "4631", "4632", "4633", "4634", "4635", "4636", "4637", "4638", "46387", "4639", "4640", "4641", "4642", "46427", "4643", "4644", "4645", "4646", "4647", "4648", "4649", "4650", "46507", "4651", "4652", "46527", "4653", "4654", "4655", "4656", "4657", "4658", "4659", "4660", "4661", "4662", "4663", "4664", "4665", "4666", "4667", "4668", "4669", "4670", "4671", "4672", "4673", "4674", "4675", "4676", "4677", "4678", "4679", "4680", "4681", "4682", "4683", "4684", "4685", "4686", "4687", "4688", "4689", "4690", "4691", "4692", "4693", "4694", "4695", "4696", "4697", "4698", "4699", "4700", "4701", "4702", "4703", "4704", "4705", "4706", "4707", "4708", "4709", "4710", "4711", "4712", "4713", "4714", "4715", "4716", "4717", "4718", "4719", "4720", "4721", "4722", "4723", "4724", "4725", "4726", "47267", "4727", "4728", "4729", "4730", "47307", "4731", "4732", "4733", "4734", "4735", "4736", "4737", "4738", "4739", "4740", "4741", "4742", "4743", "4744", "4745", "4746", "4747", "4748", "4749", "4750", "4751", "4752", "47527", "4753", "4754", "47547", "4755", "4756", "47567", "4757", "4758", "4759", "4760", "4761", "4762", "4763", "4764", "4765", "4766", "4767", "4768", "47687", "4769", "4770", "4771", "4772", "4773", "4774", "4775", "4776", "4777", "4778", "4779", "4780", "4781", "4782", "4783", "4784", "4785", "4786", "4787", "4788", "4789", "4790", "4791", "4792", "4793", "4794", "4795", "4796", "4797", "4798", "4799", "4800", "4801", "4802", "4803", "4804", "4805", "4806", "4807", "4808", "4809", "4810", "4811", "4812", "4813", "4814", "4815", "4816", "4817", "4818", "4819", "4820", "4821", "4822", "4823", "4824", "4825", "4826", "4827", "4828", "4829", "4830", "4831", "4832", "4833", "4834", "4835", "4836", "48368", "4837", "48372", "48373", "4838", "4839", "4840", "4841", "4842", "4843", "4844", "4845", "4846", "4847", "4848", "4849", "4850", "4851", "4852", "4853", "4854", "48549", "4855", "4856", "48569", "4857", "4858", "4859", "4861", "4862", "4863", "4864", "48649", "4865", "4866", "4867", "4868", "4869", "4870", "4871", "4872", "4873", "4874", "48748", "4875", "4876", "4878", "48788", "4879", "4880", "4881", "4882", "4883", "4884", "4885", "4886", "48869", "4887", "4888", "4889", "4890", "48908", "4891", "4892", "4893", "4894", "4895", "48950", "48952", "4896", "4897", "4898", "4899", "4900", "4901", "4902", "4903", "4904", "4905", "4906", "49068", "4907", "4908", "4909", "4910", "4911", "4912", "4913", "4914", "4915", "4916", "4917", "4918", "4919", "4920", "4921", "4922", "4923", "4924", "4925", "4926", "4927", "4928", "4929", "4930", "4931", "4932", "4933", "4934", "4935", "4936", "4937", "4938", "49389", "4939", "4940", "4941", "4942", "4943", "4944", "4945", "4946", "4947", "4948", "49488", "49489", "4949", "4950", "49508", "4951", "4952", "4953", "4954", "4955", "4956", "49568", "4957", "4958", "4959", "4960", "4961", "4962", "4963", "4964", "4965", "4966", "4967", "4968", "4969", "4970", "4971", "4972", "4973", "4974", "4975", "4976", "4977", "4978", "4979", "4980", "4981", "4982", "4983", "4984", "49848", "4985", "4986", "4987", "4988", "4989", "4990", "49908", "4991", "4992", "4993", "4994", "4995", "4996", "4997", "4998", "4999", "5000", "5001", "5002", "5003", "5004", "50048", "5005", "5006", "5007", "5008", "50092", "50093", "5011", "5012", "5013", "50131", "50132", "5014", "5015", "5016", "5022", "5023", "5024", "50248", "5025", "5026", "5027", "5028", "5029", "5030", "5031", "5032", "5033", "5034", "5035", "5036", "5037", "5038", "5039", "5040", "5041", "5042", "50428", "5043", "5044", "5045", "5046", "50460", "5047", "50478", "5048", "5049", "5050", "5051", "5052", "5053", "5054", "5055", "5056", "5057", "5058", "5059", "5060", "5061", "5062", "5063", "50637", "5064", "5065", "5066", "5067", "5068", "5069", "5070", "5071", "5072", "50722", "50723", "5073", "5074", "5075", "5076", "5077", "5078", "5079", "5080", "5081", "5082", "5083", "50839", "5084", "50840", "5085", "50857", "5086", "5087", "5088", "5089", "5090", "5091", "5092", "5093", "5094", "5095", "5096", "5097", "5098", "5099", "5100", "51017", "5102", "5103", "5104", "5105", "5106", "5107", "5108", "5109", "5110", "5111", "5112", "5113", "51137", "51138", "5114", "5115", "5116", "5117", "5118", "5119", "5120", "5121", "51219", "5122", "5123", "51237", "5124", "5125", "5126", "5127", "5128", "5130", "5131", "5132", "5133", "5135", "5136", "5137", "5138", "5139", "5140", "5141", "5142", "5143", "5144", "5145", "51459", "5146", "5147", "5148", "5149", "5150", "5151", "5152", "5153", "5154", "5155", "5156", "5157", "5158", "5159", "5160", "5161", "5162", "5163", "5164", "5165", "5166", "5167", "5168", "5169", "5170", "5171", "5172", "5173", "5174", "5175", "5176", "5177", "5178", "5179", "5180", "5181", "5182", "5183", "5184", "5185", "5186", "5187", "5188", "5189", "5190", "5191", "5192", "5193", "5194", "5195", "5196", "5197", "5198", "6897", "6898", "6899", "6900", "6901", "6902", "6903", "6904", "6905", "6906", "6907", "6908", "6909", "6910", "6911", "6912", "6952", "6953", "6954", "6958", "7370", "7578", "7581", "7582", "7593", "7595", "7632", "7633", "7647", "7671", "7684", "7697", "7704", "7733", "7747", "7790", "7793", "7844", "7868", "7870", "7925", "7940", "7977", "7981", "8997", "9004", "9005", "9006", "9026", "9032"]
		#print stations
		for StationID in stations:
			print StationID
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
