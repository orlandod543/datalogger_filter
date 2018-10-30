import serial
import serial.tools.list_ports
import dropbox
from time import localtime, strftime, time
from dropbox.files import WriteMode
import dropbox.exceptions as DropboxErrors
import requests.exceptions as HTTPRequestsErrors

def CollectSensorData(f):
    """
    Function that collects a single data from the sensor and adds the timestamp
    Input: filter.air_filter object
    Output: list data (str time, float data1, float data2)
    """
    #get and timestamp the data
    data =  f.get_data() #get the filter data
    strtime = strftime("%y-%m-%d-%H:%M:%S", localtime()) #get the local time
    data.insert(0,strtime) #append the time to the data
    return data

def RetrieveARduinoCOMport():
    """
    Function that query the ports available on the system and picks the one
    where the Arduino is connected.
    If there is more than one Arduino, return the first one,
    If there is no arduino return empty string.
    Input: None
    Output: str COM port.
    """
    comports =  serial.tools.list_ports.comports()
    port_to_use = [comport.device for comport in comports
		if comport.manufacturer and
		"Arduino" in comport.manufacturer]
    if not port_to_use: #If there
        return ""
    else:
        return port_to_use[0]

def InitializeDropboxUsers(DBAccessTokenList):
    '''
    Initialize a set of dropbox sessions
    input: dict DBSessionObjects{"UserAlias" : "Access Token"}
    output: dict {"UserAlias" : Dropboxuser}
    '''
    DBSessionObjects = dict()
    for DropboxUser in DBAccessTokenList:
        DBSessionObjects[DropboxUser] = dropbox.Dropbox(DBAccessTokenList[DropboxUser],
                                    max_retries_on_error = 4,
                                    max_retries_on_rate_limit = 4,
                                    user_agent = DropboxUser,
                                    session = None,
                                    headers = None,
                                    timeout = 30)

    '''Try to establish a connection with the dropbox accounts'''
    for DropboxUser in DBSessionObjects:
        try:
            DBSessionObjects[DropboxUser].users_get_current_account()
        except DropboxErrors.AuthError:
            print DropboxUser+" Authentication access token is wrong"
            pass
        except HTTPRequestsErrors.ConnectionError:
            print "HTTP error"
            pass
        else:
            print "Connection with "+DropboxUser+" successful"
    return DBSessionObjects

def UploadFileToDropboxUsers(filepath,dbfilepath, DBSessionObjects):
    '''
    Upload a file to all the dropbox users on DBSessionObjects
    Input: str file path to upload, str file path to store on dropbox, dict {"UserAlias" : Dropboxuser}
    Output: None
    '''
    file = open(filepath,"r")#open file to upload
    contents = file.read()
    for DropboxUser in DBSessionObjects:
        try:
            DBSessionObjects[DropboxUser].files_upload(contents,
                                            dbfilepath,
                                            mode = WriteMode('overwrite'))
        except HTTPRequestsErrors.ConnectionError:
            print "HTTP error. No data uploaded"
            pass                       #so it is catched here.
        except HTTPRequestsErrors.ReadTimeout:
            print "HTTP read timeout reached. No data uploaded"
            pass
    file.close()
    return None

def CollectFilteredData(f,
                        TimeWindow = 1): #Timewindow in seconds
    """
    Function that accumulates a dataset within a timewindow and outputs the average
    and adds the timestamp. If nothing was retrieved, returns a list of 0 with len(f.datanumber)
    Input:
            filter.air_filter object
            TimeWindow:defined time window to wait for new data
    Output: list data (str time, float Averdata1, float Averdata2)
    """
    FltData = [0]*f.datanumber #create an unitialized list with the size of the number of data to expect
    Samplenr = 0 #number of sampled data received in the window
    StartTime = time() #get the starting point of the timewindow
    #start gathering the data
    while((time()- StartTime)<TimeWindow): #while time elapsed is below the timewindow
        accdata = f.get_data() #get the sensor data. Expected to return a list of size f.datanumber
        #Check whether the list exists and has the correct lenght
        if accdata and len(accdata) == f.datanumber:
            print accdata
            for i in range(len(accdata)):
                FltData[i] = FltData[i] + accdata[i]
            Samplenr += 1
    if Samplenr>0: #if there is at least one value sampled
        FltData[:]= [ round(data/Samplenr,2) for data in FltData] #divide all values by the number of data samples
        # Timestamping the collected data
    strtime = strftime("%y-%m-%d-%H:%M:%S", localtime()) #get the local time
    FltData.insert(0,strtime) #append the time to the data
    return FltData
