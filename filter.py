__author__ = "Orlando"
#Class defining the air filter as a black box with serial communication.
#the input is the serial com where the filter is connectedself.

import serial #Pyserial module to control the serial port
import re
class air_filter(serial.Serial):
    def __init__(self, port, baudrate = 9600, stopbits = serial.STOPBITS_ONE,
    timeout = 2, bytesize = serial.EIGHTBITS):
        """
        Air filter inherits the serial class
        sets all the serial parameters and any nother important configuration on
        the filter
        """
        serial.Serial.__init__(self)
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.timeout = timeout
        self.bytesize = bytesize

    def air_filter_start(self):
        """
        Start the air filter serial port. Returns true if its open
        Input: None
        Outuput bool
        """
        self.open()
        self.reset_input_buffer()
        return self.is_open

    def get_data(self):
        """
        reads a line of data, then extract the two variables and return a list
        with the two variables
        returns 0.0 0.0 if there is an error.
        Input: None
        Output:[Value1, Value2]
        """
        line = self.readline() #read one line of data
        m = re.match(r'(.*)          (.*)', line) #extract data according to the pattern
        try:
            ratio = float(m.group(1))
            concentration = float(m.group(2))
        except(AttributeError,ValueError):
            ratio = 0.0
            concentration = 0.0

        return [ratio, concentration]


    def get_timeout(self):
        """
        Returns the timeout parameter of the filter
        """
        #Return serial parameters of the air filter
        return self.timeout


    def get_name(self):
        """
        Returns the port name used
        """
        return self.name

    def filter_close(self):
        """
        Close the filter port
        """
        self.close()
        return not self.is_open
