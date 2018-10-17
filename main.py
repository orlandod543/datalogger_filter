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

#Configuration section. Define here global variables or settings
#Define filter serial port parameters
port = "/dev/ttyACM0"
baudrate = 9600
datalog_path = "data/"
#Setup section. Define here all the objects to use and configure them.
#create and initialize the filter object
f = filter.air_filter(port, baudrate, timeout=10)
f.air_filter_start()
f.reset_input_buffer()
f.flushInput()
#create an object pendrive. ToDo. Refactorize and fix this class.
p = pendrive.pendrive(datalog_path)

#From this point the program start

#The filter waits until a line of data arrives to the serial port and timestamp it
try:
    while True:
        #get and timestamp the data
        data =  f.get_data() #get the filter data
        strtime = strftime("%y-%m-%d-%H:%M:%S", localtime()) #get the local time
        data.insert(0,strtime) #append the time to the data

        #define the filename and attempt to write the data
        filename = strtime[:8]+'.txt'
        if not p.file_exists(filename):
            print "Creating file " + str(filename)
        #map function applies str() to convert strings from float to the list
        #of data.
        p.write_append(filename,' '.join(map(str,data))+"\n")

        print data
except KeyboardInterrupt: #Clean the code if the program is keyboard interrupted
    print f.filter_close()
    sys.exit()
