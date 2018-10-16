__author__ = "Orlando"
#Class defining the air filter as a black box with serial communication.
#the input is the serial com where the filter is connectedself.

import serial #Pyserial module to control the serial port

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
        """Start the air filter serial port. Returns true if its open"""
        self.open()
        return self.is_open

    def get_data(self):
        return self.is_open

    def get_serial_params(self):
        #Return serial parameters of the air filter
        return self.baudrate

    def get_name(self):
        return self.name
