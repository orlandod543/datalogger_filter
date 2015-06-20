#!/usr/bin/env python
import minimalmodbus
import serial

ser = serial.Serial('/dev/ttyUSB1',9600,stopbits=2)

print ser


instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1) # port name, slave address (in decimal)
instrument.serial.stopbits = 2
instrument.serial.baudrate = 9600
print instrument.serial.baudrate
print instrument.serial.port
print instrument.address
print instrument.mode
print instrument.serial.stopbits
## Read temperature (PV = ProcessValue) ##
while True:
    for i in range(1, 30):
        temperature = instrument.read_register(i, 0) # Registernumber, number of decimals
        print temperature
## Change temperature setpoint (SP) ##
#NEW_TEMPERATURE = 95
#instrument.write_register(24, NEW_TEMPERATURE, 1) # Registernumber, value, number of decimals for storage
