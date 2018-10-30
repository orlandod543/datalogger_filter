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

import os
import exceptions
from dropbox.files import WriteMode
import dropbox.exceptions as DropboxErrors
import requests.exceptions as HTTPRequestsErrors
import DataloggerFunctions

"""function section"""
#Write all functions to DataloggerFunctions


"""Configuration section. Define here global variables or settings"""
#sensor section
Sensortimeout = 60 #time window in seconds to wait for new data
Sensordatasesize = 2#size of the dataset data the sensor delivers
Sensorbaudrate = 9600
#File section
datalog_path = "data/"
file_header = "YY-MM-DD-HH:MM:SS Ratio[%] Concentration[pcs/L]\n"


#Dropboxsection
DBAccessTokenList = {'DBOrlando' : 'QL-hU5_KShUAAAAAAAALMCIFlNcHRN-GQQOA3PvGtaShc_EPlakjUhyJD026tmLT'
                    ,'DBPulseDynamics' :'oEgHuggfnPAAAAAAAAACOOkjlzybdPgSd8ZPWHkxqUA9d-bnthhTaY_BSJiZoX5D'
                     }
PD_db_folder = "/Filterdata/"
dropbox_user_agent = "Filter"

#Datalogger section
TimeWindow = 60#the time window to filter the data in seconds

"""Setup section. Define here all the objects to use and configure them."""
#Check if there is an arduino connected. If there is no, it stops
#the software
print "-----Dust Sensor Datalogger-----"
print "Attempting connection with the arduino"
SensorPort = DataloggerFunctions.RetrieveARduinoCOMport()
if not SensorPort:
    print "There is no Arduino available"
    sys.exit(1)
else:
    print "Found Arduino on port"+ str(SensorPort)

#create and initialize the filter object
#Note: Set the timeout to be bigger than sample time. for now is 60 seconds.
f = filter.air_filter(SensorPort,
                    Sensorbaudrate,
                    timeout=Sensortimeout,#Set the timeout to a bigger time than the sample
                    datanumber = Sensordatasesize)
f.air_filter_start()

#initialize the pendrive
p = pendrive.pendrive(datalog_path)

print "Attempting to connect to Dropbox server"
'''Initialize all the dropbox sessions and return a dictionary'''
DBSessionObjects = DataloggerFunctions.InitializeDropboxUsers(DBAccessTokenList)

"""From this point the program start"""
print "Starting logging data:"

#The filter waits until a line of data arrives to the serial port and timestamp it
try:
    while True:
        #get and timestamp the data
        data = DataloggerFunctions.CollectFilteredData(f,TimeWindow) #collect filtered datalogger data
        filename = data[0][:8]+'.txt' #set the name of the file by the data

        #For new files, the file header is writen at the beginning.
        #then the data is appended onto the file
        if not p.file_exists(filename):
            print "Creating file " + str(filename)
            p.create_file_header(filename,file_header)
        p.write_append(filename,' '.join(map(str,data))+"\n")

        #Upload data onto dropbox
        filepath = datalog_path+filename
        dbfilepath = PD_db_folder+filename
        DataloggerFunctions.UploadFileToDropboxUsers(filepath, dbfilepath, DBSessionObjects)
        print data

except KeyboardInterrupt: #Clean the code if the program is keyboard interrupted
    print f.filter_close()
    sys.exit(0)
