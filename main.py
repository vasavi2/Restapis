from flask import Flask,request
from flask_cors import CORS
from Alert import InputFile
from Plant import InputFile2
from Asset import InputFile3
from Sensors import InputFile4
from UploadCsvFiles import InputFile5
from Threshold import  InputFile6
from Model_config import InputFile7
from  Worldcities import  InputFile9
from  Static import InputFile8
from dashboard import  InputFile10
from Workspace import InputFile12
from image_gallery import InputFile20
from date import  InputFile100
from Specific_Dates import InputFile15


app = Flask(__name__)
CORS(app)

x = InputFile()
x2=InputFile2()
x3=InputFile3()
x4=InputFile4()
x5=InputFile5()
x6=InputFile6()
x7=InputFile7()
x9=InputFile9()
x8=InputFile8()
x10=InputFile10()
x12=InputFile12()
x20=InputFile20()
#specified 30 days
x15=InputFile15()

x100=InputFile100()


@app.route("/", methods=['GET'])
def home():
    return "RUN SUCCESSFULL"


#Regrading Alert Table Apis
@app.route("/getalert", methods=['GET'])
def Get_Alert():
    return "RUN SUCCESSFULL"

@app.route("/getalert/<string:asset_id>", methods=['GET'])
def Get_Alert_with_Asset(asset_id):
    return "RUN SUCCESSFULL"



@app.route("/getAlertList/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def Get_Alert_with_Sensor(asset_id,sensor_group):
    return x.GetAlert_with_Sensor(asset_id,sensor_group)

# GetAlert_with_Sensorwithalert

@app.route("/getAlertListAlert/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def Get_Alert_with_Sensoralert(asset_id,sensor_group):
    return x.GetAlert_with_Sensorwithalert(asset_id,sensor_group)


# sample
@app.route("/getAlertLists/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def Get_Alert_with_Sensors(asset_id,sensor_group):
    return x.GetAlert_with_Sensors(asset_id,sensor_group)

@app.route("/getAlertLists_powerbi/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def GetAlert_with_Sensors_powerbi(asset_id,sensor_group):
    return  x.GetAlert_witth_Sensors_powerbi(asset_id,sensor_group)

@app.route("/updateAlert", methods=['POST'])
def Update_Alert():
    return x.Update_Alert_Status()


@app.route("/insertAlert", methods=['POST'])
def Insert_AlertConsolidate():
    return x.Create_AddButton_AlertConsolidate()


@app.route("/deleteAlert", methods=['POST'])
def Delete_AlertConsolidate():
    return x.DeleteAlertConsolidate()


@app.route("/api/getLatestOpenedRow", methods=['GET'])
def getLatestOpenedRow():
    return x.getLatestOpenedRow()


@app.route("/api/updateNotificationAlerts", methods=['POST'])
def UpdateAlertStatus():
    return  x.UpdateAlertStatus()

@app.route("/getassetcard/<string:asset_name>/<string:sensor_name>", methods=['GET'])
def GetAssetCard_with_asset_sensor(asset_name,sensor_name):
    return x.GetAssetCard_with_asset_sensor(asset_name,sensor_name)

@app.route("/getassetcard_data/", methods=['GET'])
def GetAssetCard():
    return x.GetAssetCard()



#Regrading Plant Table Apis

@app.route("/getplants", methods=['GET'])
def GetPlant():
    return x2.GetPlant()





# sample GetPlantId.

@app.route("/getplantids", methods=['GET'])
def GetPlantId():
    return x2.GetPlantId()

@app.route("/insertPlantData",methods=['POST'])
def Insert_PlantData():
    return x2.insert_Plant_Data()


@app.route("/insertPlantId",methods=['POST'])
def insert_Plant_ID():
    return  x2.insert_Plant_ID()



# note:-Based upon plant_id it will automatically delete data in asset and sensor which related to selected plant_name and their assets and sensors
@app.route("/deletePlantData", methods=['POST'])
def Delete_EntirePlantData():
    return x2.DeleteEntirePlantData()

@app.route("/deletePlantData2", methods=['POST'])
def Delete_EntirePlantData2():
    return x2.DeleteEntirePlantData2()


@app.route("/getlimitplants", methods=['GET'])
def Get_PlantData_Limit():
    return x2.GetPlant_limit()


@app.route("/updatePlantData",methods=['Post'])
def Update_PlantData():
    return x2.Update_PlantData()


# note:-Here delete only plant data
@app.route("/deletePlant",methods=["Post"])
def Delete_Plant():
    return x2.DeletePlant()

@app.route('/api/countries', methods=['GET'])
def Get_countries():
    return x9.get_countries()

@app.route('/api/regions', methods=['GET'])
def Get_regions():
    return x9.get_regions()

@app.route('/api/coordinates', methods=['GET'])
def Get_coordinate():
    return x9.get_coordinates()



@app.route("/get_plantName",methods=['POST'])
def getPlantName():
    return x2.getPlantName()









#<-------Regrading Asset Table Apis------>

@app.route("/getAssets", methods=['GET'])
def Get_Asset():
    return x3.GetAsset()

@app.route("/insertAssetData",methods=['POST'])
def insert_Asset():
    return x3.insert_asset_data()




@app.route("/getassetList/<string:plant_id>", methods=['GET'])
def GetAsset_with_plant(plant_id):
    return x3.GetAsset_with_plant(plant_id)


@app.route("/getassetListIds/<string:plant_id>", methods=['GET'])
def GetAsset_with_plantIds(plant_id):
    return x3.GetAsset_with_plantIds(plant_id)




@app.route("/updateAsset",methods=['POST'])
def Update_AssetData():
    return x3.Update_AssetData()

@app.route("/deleteAsset",methods=["Post"])
def DeleteAsset():
    return x3.DeleteAsset()




#Regrading Sensor Table Apis
@app.route("/getsensor", methods=['GET'])
def Get_Sensor():
    return "RUN SUCCESSFULL"
@app.route("/getSensor",methods=["GET"])
def Get_SensorList():
    return x4.GetSensor()
@app.route("/getsensorList/<string:asset_id>", methods=['GET'])
def Get_Sensor_with_asset(asset_id):
    return x4.GetSensor_with_asset(asset_id)

@app.route("/insertsensorData",methods=['POST'])
def Insert_SensorData():
    return x4.insert_sensorgroup_data()

@app.route("/insertsensorData2",methods=['POST'])
def Insert_SensorData2():
    return x4.insert_sensorgroup_data2()

@app.route("/updatesensorData",methods=["POST"])
def Update_SensorData():
    return x4.Update_SensorData()
@app.route("/deleteSensor",methods=["POST"])
def DeleteSensor():
    return x4.DeleteSensor()




#Upload csv files
@app.route('/upload_Files', methods=['POST'])
def upload_CsvFiles():
    return x5.Upload_CsvFiles()





#Regrading Threshold Table

@app.route("/insertAlgorithm",methods=['POST'])
def insertAlgorithm_data():
    return x6.insertAlgorithm_data()

@app.route("/insertThresholdData",methods=['POST'])
def insertThreshold_data():
    return x6.insertThreshold_data()


@app.route("/getThresholdList/<string:asset_id>", methods=['GET'])
def GetThreshold_with_AssetID(asset_id):
    return x6.GetThreshold_with_AssetID(asset_id)

@app.route("/getThreshold",methods=["GET"])
def GetThreshold():
    return x6.GetThreshold()

@app.route("/getThresholdTable",methods=["GET"])
def getThreshold_Table():
    return x6.GetThreshold_Table()

@app.route("/insertThresholdTable",methods=["POST"])
def insert_Threshold_Data():
    return x6.insert_Threshold_Data()


@app.route("/getlimitthreshold", methods=['GET'])
def Get_Threshold_Limit():
    return x6.GetThreshold_limit()

@app.route("/updateThreshold",methods=["POST"])
def updateThreshold():
    return  x6.updateThreshold()












#Regrading Model Config Table
@app.route("/getModelConfig",methods=['GET'])
def GetModelConfig_Data():
    return x7.GetModelConfig_Table()
@app.route("/insertModelConfig",methods=['POST'])
def insert_ModelConfig_Data():
    return x7.insert_ModelConfig_Data()

@app.route("/updateModelConfig",methods=['POST'])
def Update_ModelConfigData():
    return x7.Update_ModelConfigData()


@app.route("/getModelLimit",methods=['GET'])
def GetModel_limit():
    return x7.GetModel_limit()




@app.route("/getstatic", methods=['GET'])
def GetStatic():
    return x8.GetStatic()


@app.route("/_2k1701_cps1_raw", methods=['GET'])
def GetCpsi():
    return x8.GetCpsi()


# dashboard
@app.route("/getdashboard", methods=['GET'])
def GetDashboard():
    return x10.GetDashboard()

@app.route("/insertDashboardData",methods=['POST'])
def insert_dashboard_data():
    return x10.insert_dashboard_data()

#workspace
@app.route("/getWorkspace", methods=['GET'])
def GetWorkspace():
    return x12.GetWorkspace()

@app.route("/insertWorkspace",methods=['POST'])
def insert_workspace_data():
    return x12.insert_workspace_data()

# @app.route("/_2k1701_cps1_raw2", methods=['GET'])
# def GetCpsi2(self):
#         page = int(request.args.get('page', 1))
#
#         per_page = int(request.args.get('per_page', 10))
#
#         data = Get_data2(page, per_page)
#
#         return jsonify(data)


# x20=InputFile20()

#sample -image_gallery

@app.route("/api/list", methods=['GET'])
def getImage():
    return x20.GetImages()

@app.route("/api/getLatestRow", methods=['GET'])
def getLatestRow():
    return x20.getLatestRow()


@app.route("/api/upload", methods=['POST'])
def PostImages():
    return x20.PostImages()

@app.route("/api/updateNotification", methods=['POST'])
def UpdateImages():
    return  x20.UpdateImages()



#dates

@app.route("/date",methods=['POST'])
def Insert_date():
    return x100.insert_date()


# specific dates
#30 days for alerts
@app.route("/getAlertList30/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def Get_Alert_with_Sensor_thirtydays(asset_id,sensor_group):
    return x15.GetAlert_with_Sensor_thirtydays(asset_id,sensor_group)

#6 months for alerts
@app.route("/getAlertList6months/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def Get_Alert_with_Sensor_six_months(asset_id,sensor_group):
    return x15.GetAlert_with_Sensor_sixmonth(asset_id,sensor_group)


# GetAlert_with_Sensor_lastyear


@app.route("/getAlertListlastyear/<string:asset_id>/<string:sensor_group>", methods=['GET'])
def GetAlert_with_Sensor_lastyear(asset_id,sensor_group):
    return x15.GetAlert_with_Sensor_lastyear(asset_id,sensor_group)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
