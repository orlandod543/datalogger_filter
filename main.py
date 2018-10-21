##Software that log the data sent by a filter through serial port
#the software is split as follows:
#each time there is a new string arriving to the serial port, it
#it time stamp it, load to a txt file with the name of the current date
#and it will upload the file to dropbox
#The example string is as follows:
#-> RAtio = $i          Concentration = 0
#import section. Define here all clases to use
import filter
from time import localtime, strftime
import sys, traceback
import pendrive
import dropbox
import os
import exceptions
from dropbox.files import WriteMode
import dropbox.exceptions as DropboxErrors
import requests.exceptions as HTTPRequestsErrors
import serial.tools.list_ports

"""function section"""
def collect_filter_data(f):
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


"""Configuration section. Define here global variables or settings"""
#Check if there is an arduino connected. If there is no, it stops
#the software
print "-----Dust Sensor Datalogger-----"
print "Attempting connection with the arduino"
"""port = RetrieveARduinoCOMport()"""
port =  "/dev/ttyACM0"
if not port:
    print "There is no Arduino available"
    sys.exit(1)
else:
    print "Found Arduino on port"+ str(port)


baudrate = 9600
datalog_path = "data/"
DBAccessTokenList = {'DBOrlando' : 'QL-hU5_KShUAAAAAAAALMCIFlNcHRN-GQQOA3PvGtaShc_EPlakjUhyJD026tmLT',
                     'DBPulseDynamics' :'oEgHuggfnPAAAAAAAAACOOkjlzybdPgSd8ZPWHkxqUA9d-bnthhTaY_BSJiZoX5D'}
PD_db_folder = "/Filterdata/"
dropbox_user_agent = "Filter"
file_header = "YY-MM-DD-HH:MM:SS Ratio[%] Concentration[pcs/L]\n"



"""Setup section. Define here all the objects to use and configure them."""
#create and initialize the filter object
#Note: Set the timeout to be bigger than sample time. for now is 60 seconds.
f = filter.air_filter(port,
                    baudrate,
                    timeout=60) #Set the timeout to a bigger time than the sample
f.air_filter_start()

p = pendrive.pendrive(datalog_path)
print "Attempting to connect to Dropbox server"
'''Initialize all the dropbox sessions and return a dictionary'''
DBSessionObjects = dict()
for DropboxUser in DBAccessTokenList:
    DBSessionObjects[DropboxUser] = dropbox.Dropbox(DBAccessTokenList[DropboxUser],
                                max_retries_on_error = 4,
                                max_retries_on_rate_limit = 4,
                                user_agent = dropbox_user_agent,
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

"""From this point the program start"""
print "Starting logging data:"

#The filter waits until a line of data arrives to the serial port and timestamp it
try:
    while True:
        #get and timestamp the data
        data = collect_filter_data(f) #collect data logger data
        filename = data[0][:8]+'.txt' #set the name of the file by the data

        #For new files, the file header is writen at the beginning.
        #then the data is appended onto the file
        if not p.file_exists(filename):
            print "Creating file " + str(filename)
            p.create_file_header(filename,file_header)
        p.write_append(filename,' '.join(map(str,data))+"\n")

        #Upload data onto dropbox
        file = open(datalog_path+filename,"r")#open file to upload
        contents = file.read()
        for DropboxUser in DBSessionObjects:
            try:
                DBSessionObjects[DropboxUser].files_upload(contents,
                                                PD_db_folder+filename,
                                                mode = WriteMode('overwrite'))
            except HTTPRequestsErrors.ConnectionError:
                print "HTTP error. No data uploaded"
                pass                       #so it is catched here.
        file.close()
        print data

except KeyboardInterrupt: #Clean the code if the program is keyboard interrupted
    print f.filter_close()
    sys.exit(0)
