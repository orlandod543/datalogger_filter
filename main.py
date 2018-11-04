##Software that log the data sent by a filter through serial port
#the software is split as follows:
#each time there is a new string arriving to the serial port, it
#it time stamp it, load to a txt file with the name of the current date
#and it will upload the file to dropbox
#The example string is as follows:
#-> RAtio = $i          Concentration = 0
#import section. Define here all clases to use
import filter

import sys, traceback
import pendrive
import yaml
import Datalogger
import os
import exceptions
from dropbox.files import WriteMode
import dropbox.exceptions as DropboxErrors
import requests.exceptions as HTTPRequestsErrors
import DataloggerFunctions


"""Read the yaml configuration file"""
try:
     with open("Conf.yaml",'r') as ConfFile:
        try:
            Configuration= yaml.safe_load(ConfFile)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
except IOError as Err:
    print(Err)
    print "Please check your configuration file"
    sys.exit(1)
    """Load the configuration variables"""

#Configuration section. Define here global variables or settings"""
DropboxEnable = True

DLinfo = Configuration["DataloggerInfo"]    #Datalogger to create
         #Sensors to load
try:
    SensorList = Configuration["Sensors"]
except KeyError:
    print "There are not sensors available"
    sys.exit(1)
else:
    if not SensorList:
        print "There are not sensors available"
        sys.exit(1)
    else:
        print "Found %d sensors" % len(SensorList)
 #Dropbox configuration to load
 #Dropbox configuration
    #Dropbox to configure
try:
    DBUserList = Configuration["DBUserList"]    #dropbox users to attend
except KeyError:
    DropboxEnable = False
    print "Key not found, Dropbox upload Disabled"
else:
    if not DBUserList:
        DropboxEnable = False
        print "No Dropbox users found, upload disabled"
    else:
        print "Found %d Dropbox users, upload Enabled" % len(DBUserList)

"""Sensor Creation"""
for Sensor in SensorList:
    SnsobjList = filter.air_filter(port = SensorList[Sensor]["Port"],
                                    baudrate = SensorList[Sensor]["Baudrate"],
                                    timeout=SensorList[Sensor]["Timeout"],
                                    datanumber = SensorList[Sensor]["DatasetSize"],
                                    datanamestr = SensorList[Sensor]["Dataname"])
    SnsobjList.air_filter_start()

"""Datalogger creation"""
for Dataloggerobj  in DLinfo:
    DatalogPath =  DLinfo[Dataloggerobj]["DatalogPath"]
    Averagefilter = DLinfo[Dataloggerobj]["AverageFilter"]
    AverageTimewindow = DLinfo[Dataloggerobj]["AverageTimeWindow"]
    Datalogger = Datalogger.datalogger(Alias=Dataloggerobj ,
                                        SensorList = SnsobjList,
                                        FolderPath=DatalogPath,
                                        AverageFilter = Averagefilter,
                                        AverageTimewindow =AverageTimewindow)

"""Dropbox Initialization"""
#Create a dictionary with a list of users to pass to InitializeDropboxUsers"""
DBAccessTokendict = {}
for DBuser in DBUserList:
    DBAccessTokendict[DBuser] = DBUserList[DBuser]["AccessToken"]
dbfilepath = DBUserList[DBuser]["Folder"]
#Initialize all the dropbox sessions and return a dictionary
print "Attempting to connect to Dropbox server"
DBSessionObjects = DataloggerFunctions.InitializeDropboxUsers(DBAccessTokendict)
#Dropboxsection
PD_db_folder = "/Filterdata/"
dropbox_user_agent = "Filter"


"""From this point the program start"""
print "Starting logging data:"

#The filter waits until a line of data arrives to the serial port and timestamp it
try:
    while True:
        #get and timestamp the data
        data = Datalogger.CollectData()
        print data
        filename = data[0][:8]+'.txt' #set the name of the file by the data

        #For new files, the file header is writen at the beginning.
        #then the data is appended onto the file
        if not p.file_exists(filename):
            print "Creating file " + str(filename)
            p.create_file_header(filename,file_header)
        p.write_append(filename,' '.join(map(str,data))+"\n")

        #Upload data onto dropbox
        filepath = datalog_path+filename
#        DataloggerFunctions.UploadFileToDropboxUsers(filepath, dbfilepath, DBSessionObjects)
        print data

except KeyboardInterrupt: #Clean the code if the program is keyboard interrupted
    #print f.filter_close()
    sys.exit(0)
