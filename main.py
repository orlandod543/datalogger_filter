##Software that log the data sent by a filter through serial port
#the software is split as follows:
#each time there is a new string arriving to the serial port, it
#it time stamp it, load to a txt file with the name of the current date
#and it will upload the file to dropbox
#The example string is as follows:
#-> radio = $i          Concentration = 0
#import section. Define here all clases to use
import filter
from time import localtime, strftime
import sys, traceback
import pendrive
import dropbox
import os
from dropbox.files import WriteMode

"""function section"""
def collect_filter_data(f):
    """
    Function that collects data from the file and add the timestamp
    Input: None
    Output: list data (str time, float data1, float data2)
    """
    #get and timestamp the data
    data =  f.get_data() #get the filter data
    strtime = strftime("%y-%m-%d-%H:%M:%S", localtime()) #get the local time
    data.insert(0,strtime) #append the time to the data
    return data

"""Configuration section. Define here global variables or settings"""
#Define filter serial port parameters
port = "/dev/ttyACM0"
baudrate = 9600
datalog_path = "data/"
PD_db_access_token = 'QL-hU5_KShUAAAAAAAALMCIFlNcHRN-GQQOA3PvGtaShc_EPlakjUhyJD026tmLT'
PD_db_folder = "/mnt/sda1/"



"""Setup section. Define here all the objects to use and configure them."""
#create and initialize the filter object
f = filter.air_filter(port, baudrate, timeout=10)
f.air_filter_start()
f.reset_input_buffer()
f.flushInput()
#create an object pendrive. ToDo. Refactorize and fix this class.
p = pendrive.pendrive(datalog_path)
PD_dropbox = dropbox.Dropbox(PD_db_access_token)
print PD_dropbox.users_get_current_account()

"""From this point the program start"""

#The filter waits until a line of data arrives to the serial port and timestamp it
try:
    while True:
        #get and timestamp the data
        data = collect_filter_data(f) #collect data logger data
        filename = data[0][:8]+'.txt' #set the name of the file by the data

        if not p.file_exists(filename):
            print "Creating file " + str(filename)
        #map function applies str() to convert strings from float to the list
        #of data.
        p.write_append(filename,' '.join(map(str,data))+"\n")
        #Upload data onto dropbox
        file = open(datalog_path+filename,"r")#open file to upload
        contents = file.read()
        PD_dropbox.files_upload(contents,
        PD_db_folder+filename,
        mode = WriteMode('overwrite'))
        file.close()

        print data
except KeyboardInterrupt: #Clean the code if the program is keyboard interrupted
    print f.filter_close()
    sys.exit()
