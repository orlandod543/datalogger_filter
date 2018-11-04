import serial
import serial.tools.list_ports
import dropbox
from time import localtime, strftime, time
from dropbox.files import WriteMode
import dropbox.exceptions as DropboxErrors
import requests.exceptions as HTTPRequestsErrors
import pendrive
class datalogger:
    def __init__(self,
                 Alias,
                 SensorList, #list of sensors to measure
                 FolderPath = "filter/",
                 AverageFilter = False,
                 AverageTimewindow = 60):
        self.Alias = Alias
        self.FolderPath = FolderPath
        self.AverageFilter = AverageFilter
        self.AverageTimeWindow = AverageTimewindow
        self.SensorList = SensorList #list of sensors to check. What if there is empty?
        self.FileHandler = pendrive.pendrive(self.FolderPath)

    def CollectSensorData(self):
        """
        Function that collects a single data from the sensor and adds the timestamp
        Input: filter.air_filter object
        Output: list data (str time, float data1, float data2)
        """
        #get and timestamp the data
        data =  self.SensorList.get_data() #get the filter data
        strtime = strftime("%y-%m-%d-%H:%M:%S", localtime()) #get the local time
        data.insert(0,strtime) #append the time to the data
        return data

    def CollectFilteredData(self): #Timewindow in seconds
        """
        Function that accumulates a dataset within a timewindow and outputs the average
        and adds the timestamp. If nothing was retrieved, returns a list of 0 with len(f.datanumber)
        Input:
                filter.air_filter object
                TimeWindow:defined time window to wait for new data
        Output: list data (str time, float Averdata1, float Averdata2)
        """
        FltData = [0]*self.SensorList.datanumber #create an unitialized list with the size of the number of data to expect
        Samplenr = 0 #number of sampled data received in the window
        StartTime = time() #get the starting point of the timewindow
        #start gathering the data
        while((time()- StartTime)<self.AverageTimeWindow): #while time elapsed is below the timewindow
            accdata = self.SensorList.get_data() #get the sensor data. Expected to return a list of size f.datanumber
            #Check whether the list exists and has the correct lenght
            if accdata and len(accdata) == self.SensorList.datanumber:
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

    def CollectData(self):
        """
        Method that collects data from sensors and save them into a file_exists
        Input : None
        Output: [str file saved, str time, float data1, float data2]
        """
        if self.AverageFilter:
            print "Collecting filtered data"
            data =  self.CollectFilteredData()
        else:
            print "Collecting normal data"
            data = self.CollectSensorData()
        print data
        filename = data[0][:8]+'.txt' #set the name of the file by the data
        self.AppendData2File(data, filename,self.SensorList.datanamestr)
        data.insert(0,filename)
        return data

    def CloseDatalogger(self):
        """
        Closes the file opened by the datalogger
        input: None
        Output: None
        """

    def AppendData2File(self,data, filename, file_header):
        """
        Writes the data collected to the file
        Input: list data (str time, float data1, float data2)
                str filename. Name of the file to write
                str file_header header to add on the top
        Output: None
        """
        if not self.FileHandler.file_exists(filename):
            print "Creating file " + str(filename)
            self.FileHandler.create_file_header(filename,file_header+"\n")
        self.FileHandler.write_append(filename,' '.join(map(str,data))+"\n")

    def SensorClose(self):
        """
        Closes the COM port
        """
        return self.SensorList.filter_close()
