import serial
import serial.tools.list_ports
import dropbox
from time import localtime, strftime
from dropbox.files import WriteMode
import dropbox.exceptions as DropboxErrors
import requests.exceptions as HTTPRequestsErrors

def CollectSensorData(f):
    """
    Function that collects data from the file and add the timestamp
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
    port_to_use = [comport.device for comport in comports if
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
